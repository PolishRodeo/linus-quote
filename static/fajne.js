function fetchData(endpoint, elementId) {
    fetch(endpoint)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Błąd HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            document.getElementById(elementId).innerText = data.next_update_in || data.quote;
        })
        .catch(error => {
            console.error(`Błąd podczas pobierania danych z ${endpoint}:`, error);
        });
}

function updateTime() {
    fetchData("/api/time", "time");
}

function updateQuote() {
    fetchData("/api/qotd", "quote");
}

setInterval(updateTime, 1000);
setInterval(updateQuote, 1000);
