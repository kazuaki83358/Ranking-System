from flask import request, jsonify
from models import db, User, Transaction


def register_routes(app):

    ####################################################
    # POST /transaction
    ####################################################
    @app.route('/transaction', methods=['POST'])
    def add_transaction():

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No JSON data provided"
            }), 400

        required = ['user_id', 'amount', 'request_id']

        for field in required:
            if field not in data:
                return jsonify({
                    "error": f"{field} is required"
                }), 400

        user_id = data['user_id']
        amount = data['amount']
        request_id = data['request_id']

        # Validate amount
        if amount <= 0:
            return jsonify({
                "error": "Amount must be positive"
            }), 400

        # Prevent duplicate transactions
        duplicate = Transaction.query.filter_by(
            request_id=request_id
        ).first()

        if duplicate:
            return jsonify({
                "message": "Duplicate request"
            }), 409

        # Create user automatically
        user = db.session.get(User, user_id)

        if not user:
            user = User(
                id=user_id,
                name=f"User {user_id}"
            )

            db.session.add(user)

        # Add transaction
        transaction = Transaction(
            user_id=user_id,
            amount=amount,
            request_id=request_id
        )

        db.session.add(transaction)
        db.session.commit()

        return jsonify({
            "message": "Transaction Added"
        }), 201


    ####################################################
    # GET /summary/<user_id>
    ####################################################
    @app.route('/summary/<int:user_id>', methods=['GET'])
    def get_summary(user_id):

        user = db.session.get(User, user_id)

        if not user:
            return jsonify({
                "error": "User not found"
            }), 404


        transactions = Transaction.query.filter_by(
            user_id=user_id
        ).all()


        total_amount = sum(
            t.amount
            for t in transactions
        )


        history = []

        for t in transactions:

            history.append({

                "amount": t.amount,

                "request_id": t.request_id,

                "timestamp": t.timestamp.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

            })


        return jsonify({

            "user_id": user_id,

            "total_amount": total_amount,

            "transactions": len(transactions),

            "history": history

        })


    ####################################################
    # GET /ranking
    ####################################################
    @app.route('/ranking', methods=['GET'])
    def ranking():

        users = User.query.all()

        rankings = []


        for user in users:

            transactions = Transaction.query.filter_by(
                user_id=user.id
            ).all()


            total_amount = sum(
                t.amount
                for t in transactions
            )


            transaction_count = len(
                transactions
            )


            # Fair ranking formula
            score = (

                total_amount * 0.7

                +

                transaction_count * 100

            )


            rankings.append({

                "user_id": user.id,

                "name": user.name,

                "total_amount": total_amount,

                "transactions": transaction_count,

                "score": round(score, 2)

            })


        rankings.sort(

            key=lambda x: x['score'],

            reverse=True

        )


        return jsonify(

            rankings

        )