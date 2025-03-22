document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("predict-btn").addEventListener("click", function () {
        console.log("Button clicked! Sending request...");

        // Get input values
        let features = [
            parseFloat(document.getElementById("age").value),
            parseInt(document.getElementById("gender").value),
            parseInt(document.getElementById("education").value),
            parseFloat(document.getElementById("annual-income").value),
            parseInt(document.getElementById("experience").value),
            parseInt(document.getElementById("home-ownership").value),
            parseFloat(document.getElementById("loan-amount").value),
            parseInt(document.getElementById("loan-intent").value),
            parseFloat(document.getElementById("interest-rate").value),
            parseFloat(document.getElementById("loan-percent-income").value),
            parseInt(document.getElementById("credit-history").value),
            parseInt(document.getElementById("credit-score").value),
            parseInt(document.getElementById("previous-defaults").value),
        ];

        console.log("Sending data:", features);

        // Send data to backend
        fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ features: features }),
        })
        .then(response => response.json())
        .then(data => {
            console.log("Response received:", data);
            if (data.loan_approved !== undefined) {
                alert("Loan Approval Status: " + (data.loan_approved ? "Approved ✅" : "Rejected ❌"));
            } else {
                alert("Error: " + data.error);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Something went wrong. Check the console for details.");
        });
    });
});
