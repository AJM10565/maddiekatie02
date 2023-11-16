function incrementCount() {
    count++;
    document.getElementById("countDisplay").textContent = `Count: ${count}`;

    if (count % 10 === 0) {
        updateGlobalCurrencyOnServer(count / 10);
    }
}

function getGlobalCurrencyFromServer(userId) {
    fetch(`/getGlobalCurrency?userId=${userId}`, {
        method: 'GET',
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.globalCurrency) {
            document.getElementById("currencyValue").textContent = data.globalCurrency;
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

const userId = 'user123'; // Replace with the actual user's identifier.

// Initialize the currency display
getGlobalCurrencyFromServer(userId);






