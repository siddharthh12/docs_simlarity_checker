function checkSimilarity() {
    let file1 = document.getElementById("file1").files[0];
    let file2 = document.getElementById("file2").files[0];

    if (file1 && file2) {
        let formData = new FormData();
        formData.append("file1", file1);
        formData.append("file2", file2);

        fetch('/compare', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            updateResult(data.similarity_score, data.highlighted_text);
        })
        .catch(error => console.error("Error:", error));
    } else {
        let doc1 = document.getElementById("doc1").value;
        let doc2 = document.getElementById("doc2").value;

        if (doc1.trim() === "" || doc2.trim() === "") {
            return;
        }

        fetch('/compare', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ doc1, doc2 })
        })
        .then(response => response.json())
        .then(data => {
            updateResult(data.similarity_score, data.highlighted_text);
        })
        .catch(error => console.error("Error:", error));
    }
}

let similarityChart = null;

function updateResult(score, highlightedText) {
    let numericScore = parseFloat(score);
    document.getElementById("result").innerText = `Similarity Score: ${numericScore.toFixed(2)}%`;

    document.getElementById("highlightedText").innerHTML = `<p>${highlightedText}</p>`;

    let ctx = document.getElementById('similarityChart').getContext('2d');

    if (similarityChart) {
        similarityChart.destroy();
    }

    similarityChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Similarity'],
            datasets: [{
                label: 'Score (%)',
                data: [numericScore],
                backgroundColor: numericScore > 50 ? 'green' : 'red'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,  // Maintain proportional size
            aspectRatio: 2,             // Adjusts width-to-height ratio
            scales: {
                y: { beginAtZero: true, max: 100 }
            },
            plugins: { legend: { display: false } }
        }
    });
}
