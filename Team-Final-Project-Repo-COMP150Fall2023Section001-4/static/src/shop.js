function updateGlobalCurrencyDisplay() {
    fetch('/getGlobalCurrency')
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

function purchaseGame(gameId, gamePrice) {
    // Replace 'userId' with the actual user's identifier.
    const userId = 'user123';

    fetch('/purchaseGame', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            userId,
            gameId,
            gamePrice,
        }),
    })
    .then((response) => {
        if (response.status === 200) {
            // Purchase successful, update the currency display
            getGlobalCurrencyFromServer(userId);
        } else {
            console.error('Purchase failed');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

const userId = 'user123'; // Replace with the actual user's identifier.

// Initialize the currency display
getGlobalCurrencyFromServer(userId);


