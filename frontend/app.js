const API = "http://127.0.0.1:5000";


// ============================
// Add Transaction
// ============================
async function addTransaction() {

    const userId = document.getElementById("userId").value;
    const amount = document.getElementById("amount").value;
    const requestId = document.getElementById("requestId").value;

    try {

        const response = await fetch(`${API}/transaction`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                user_id: Number(userId),
                amount: Number(amount),
                request_id: requestId

            })

        });


        const data = await response.json();


        const message = document.getElementById("message");


        if (response.ok) {

            message.style.color = "green";
            message.innerText = data.message;

        }

        else {

            message.style.color = "red";

            message.innerText =
                data.error || data.message;

        }


        ranking();


    }


    catch (error) {


        document.getElementById("message").style.color = "red";

        document.getElementById("message").innerText =
            error.message;

    }


}




// ============================
// User Summary
// ============================
async function summary() {


    const id =
        document.getElementById("summaryId").value;



    try {


        const response = await fetch(

            `${API}/summary/${id}`

        );



        const data = await response.json();



        const result = document.getElementById(

            "summaryResult"

        );



        if (response.ok) {


            result.innerHTML = `


            <p>
            <strong>User ID:</strong>
            ${data.user_id}
            </p>



            <p>

            <strong>Total Amount:</strong>

            ₹${data.total_amount}

            </p>



            <p>

            <strong>Transactions:</strong>

            ${data.transactions}

            </p>


            `;


        }


        else {

            result.innerHTML = `


            <p style="color:red">

            ${data.error}

            </p>


            `;

        }


    }



    catch (error) {


        document.getElementById(

            "summaryResult"

        ).innerHTML = `


        <p style="color:red">

        ${error.message}

        </p>


        `;


    }


}





// ============================
// Ranking Table
// ============================
async function ranking() {


    try {


        const response = await fetch(

            `${API}/ranking`

        );


        const data = await response.json();



        const body = document.getElementById(

            "rankingBody"

        );


        body.innerHTML = "";



        data.forEach((user, index) => {


            let medal = "";


            if (index === 0)
                medal = "🥇";

            else if (index === 1)
                medal = "🥈";

            else if (index === 2)
                medal = "🥉";




            body.innerHTML += `


            <tr>


            <td>


            ${medal} ${index + 1}


            </td>



            <td>


            ${user.name}


            </td>



            <td>


            ₹${user.total_amount}


            </td>



            <td>


            ${user.transactions}


            </td>



            <td>


            ${user.score}


            </td>



            </tr>


            `;



        });



    }


    catch (error) {


        console.log(error);


    }


}



// Auto-load leaderboard
ranking();