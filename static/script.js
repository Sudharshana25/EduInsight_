document.addEventListener("DOMContentLoaded", function () {
    const uploadForm = document.getElementById("upload-form");
    const fileInput = document.getElementById("file");
    const predictionTable = document.getElementById("prediction-table");
    const tableBody = predictionTable.querySelector("tbody");

    uploadForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const formData = new FormData();
        formData.append("file", fileInput.files[0]);

        try {
            const response = await fetch("http://127.0.0.1:8000/predict", {
                method: "POST",
                body: formData,
            });

          if (!response.ok) {
                const errorText = await response.text();
                alert("Prediction failed: " + errorText);
                return;
}

            const data = await response.json();

            if (data.error) {
                alert("Prediction failed: " + data.error);
                return;
            }

            displayResults(data.predictions);
            updateChart(data.predictions);

        } catch (error) {
            alert("Prediction failed: " + error);
        }
    });

    function displayResults(predictions) {
        tableBody.innerHTML = "";

        predictions.forEach((item) => {
            const row = tableBody.insertRow();
            ["avg_quiz_score", "attendance_pct", "performance_label", "prediction"].forEach((col) => {
                const cell = row.insertCell();
                cell.textContent = item[col];

                // Highlight row based on prediction
                if (col === "prediction") {
                    if (item[col] === 2) {
                        row.style.backgroundColor = "#d4edda"; // green
                    } else if (item[col] === 1) {
                        row.style.backgroundColor = "#fff3cd"; // yellow
                    } else if (item[col] === 0) {
                        row.style.backgroundColor = "#f8d7da"; // red
                    }
                }
            });
        });

        predictionTable.style.display = "table";
    }

    function updateChart(predictions) {
        const counts = [0, 0, 0]; // [fail, average, pass]

        predictions.forEach((p) => {
            if (p.prediction === 0) counts[0]++;
            else if (p.prediction === 1) counts[1]++;
            else if (p.prediction === 2) counts[2]++;
        });

        const ctx = document.getElementById("predictionChart").getContext("2d");

        if (window.predChart) window.predChart.destroy(); // reset chart

        window.predChart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: ["Fail", "Average", "Pass"],
                datasets: [{
                    label: "Number of Students",
                    data: counts,
                    backgroundColor: ["#f8d7da", "#fff3cd", "#d4edda"],
                    borderColor: ["#f5c6cb", "#ffeeba", "#c3e6cb"],
                    borderWidth: 1,
                }],
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        precision: 0,
                    },
                },
            },
        });
    }
});
