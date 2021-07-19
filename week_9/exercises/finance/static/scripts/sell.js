import {
    is_valid_share,
    is_empty
} from "./validation.js";

document.addEventListener('DOMContentLoaded', (e) => {
    const symbol = document.getElementById("symbol");
    const owned_shares = document.getElementById("owned-shares");
    const name_container = document.getElementById("name-container");
    const price_container = document.getElementById("price-container");
    const add_button = document.getElementById("add-button");
    const subs_button = document.getElementById("subs-button");
    const shares_container = document.getElementById("shares");
    const total = document.getElementById("total");
    const shares_error = document.getElementById("shares-error");
    const sell_button = document.getElementById("sell-button");
    let current_price = 0.00;

    shares_container.addEventListener("keydown", (e) => {

        /// Get the pressed key code
        const key = e.key;
        /// Accepts Backspace key
        if (key == "Backspace") {
            return;
        }

        /// stops the event if the pressed key is not a number from 0-9
        if (key < "0" || key > "9") {
            e.preventDefault();
        }
    });

    shares_container.addEventListener("change", (e) => {
        const current_shares = shares_container.value;
        if (current_shares == "") {
            shares_container.value = "1";
        }

        let new_shares = (current_shares == "" || !is_valid_share(current_shares)) ? 1 : parseInt(current_shares);

        if (new_shares < 100 && new_shares >= 0) {
            shares_error.innerHTML = "";
        } else if (new_shares > 100) {
            shares_error.innerHTML = "The max shares that you can sell are 100";
        }

        if (new_shares < 1) {
            shares_container.value = "1";
            new_shares = 1;
        } else if (new_shares > 100) {
            shares_container.value = "100";
            new_shares = 100;
        }

        total.innerHTML = `${calculate_total(new_shares).toFixed(2)}`;
    });

    add_button.addEventListener("click", (e) => {
        const current_shares = shares_container.value;

        let new_shares = (current_shares == "" || !is_valid_share(current_shares)) ? 1 : parseInt(current_shares) + 1;

        if (new_shares > 100) {
            shares_error.innerHTML = "The max shares that you can sell are 100";
            shares_container.value = "100";
            new_shares = 100;
        } else {
            shares_container.value = `${new_shares}`;
        }
        total.innerHTML = `${calculate_total(new_shares).toFixed(2)}`;
    });

    subs_button.addEventListener("click", (e) => {
        const current_shares = shares_container.value;

        let new_shares = (current_shares == "" || !is_valid_share(current_shares)) ? 1 : parseInt(current_shares) - 1;

        if (new_shares < 100 && new_shares > 0) {
            shares_error.innerHTML = "";
        }

        if (new_shares < 1) {
            shares_container.value = "1";
            new_shares = 1;
        } else if (new_shares > 100) {
            shares_container.value = "100";
            new_shares = 100;
        } else {
            shares_container.value = new_shares;
        }

        total.innerHTML = `${calculate_total(new_shares).toFixed(2)}`;
    });

    sell_button.addEventListener("click", (e) => {
        if (!is_valid_purchase()) {
            e.preventDefault();
        }
    });

    symbol.addEventListener("change", (e) => {
        if (symbol.value == "") {
            shares_error.innerHTML = "";
            name_container.innerHTML = "-";
            price_container.innerHTML = "0.00";
            shares_container.value = "1";
            total.innerHTML = "0.00";
            owned_shares.innerHTML = "0";
            current_price = 0.00;
            return;
        }

        // POST request using fetch()
        fetch(`/stock-info?symbol=${symbol.value}`, {
                // Adding method type
                method: "GET",
            })
            // Converting to JSON
            .then(response => response.json())
            // Displaying information to its container
            .then((data) => {
                if (data) {
                    const {
                        name,
                        price,
                        shares
                    } = data;
                    shares_error.innerHTML = "";
                    name_container.innerHTML = name ? name : "-";
                    price_container.innerHTML = price ? `${price}` : "0.00";
                    shares_container.value = "1";
                    owned_shares.innerHTML = shares ? shares : "0";
                    total.innerHTML = price ? `${price}` : "0.00";
                    current_price = parseFloat(price);
                } else {
                    shares_error.innerHTML = "";
                    name_container.innerHTML = "-";
                    price_container.innerHTML = "0.00";
                    shares_container.value = "1";
                    total.innerHTML = "0.00";
                    owned_shares.innerHTML = "0";
                    current_price = 0.00;
                }
            })
            .catch(console.warn);
    });


    /**
     * Calculate the total value of the current sale
     * @param {int} shares_values is the number of values that the user is trying to sell
     * @return {float}
     */
    function calculate_total(shares_value) {
        if (!is_valid_share(shares_value.toString())) {
            shares_value = 1;
        }
        return shares_value * current_price;
    }

    /**
     * Evaluate that the sale form  has all the needed information. If that does not happen
     * a message will be shown and will return false;
     * @return {bool}
     */
    function is_valid_purchase() {
        const stock_id_value = symbol.value.trim();
        const shares_value = shares.value;
        const valid_shares = is_valid_share(shares_value);
        let valid_stock_id = true;
        if (is_empty(stock_id_value)) {
            Swal.fire({
                position: 'center',
                icon: 'error',
                title: 'Enter a valid stock symbol',
                showConfirmButton: true,
            })
            valid_stock_id = false;
        }
        return valid_shares && valid_stock_id;
    }
});