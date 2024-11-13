function showResults() {
    const query = document.querySelector('.search-bar').value;

    fetch("http://127.0.0.1:8000/search/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Data received:", data);  // Confirm data is received
        document.querySelector('.container').classList.add('results-active');

        if (data.results && data.results.length > 0) {
            let resultsHTML = `
                <table>
                    <thead>
                        <tr>
                            <th>Producto</th>
                            <th>Precio</th>
                            <th>Tienda</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            data.results.forEach(result => {
                // Format the price with currency and thousand separators
                const formattedPrice = `$${Number(result.precio).toLocaleString('es-CO')}`;
                resultsHTML += `
                    <tr>
                        <td>${result.nom_product}</td>
                        <td>${formattedPrice}</td>
                        <td>${result.tienda}</td>
                    </tr>
                `;
            });

            resultsHTML += `</tbody></table>`;

            // Insert the results into the results div
            document.getElementById('results').innerHTML = resultsHTML;
            console.log("results HTML:", resultsHTML); // Log HTML for troubleshooting
        } else {
            document.getElementById('results').innerHTML = "<p>No se encontraron resultados.</p>";
        }
    })
    .catch(error => {
        console.error("Error fetching data:", error);
        document.getElementById('results').innerHTML = "<p>Error al obtener los resultados.</p>";
    });
}
