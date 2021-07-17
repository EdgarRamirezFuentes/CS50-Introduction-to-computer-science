import { is_valid_share, is_empty } from "./validation.js";

document.addEventListener('DOMContentLoaded', (e) => {
    const data_container = document.getElementById("data-container");
    const symbol = document.getElementById("symbol");
    const name_container = document.getElementById("name-container");
    const price_container = document.getElementById("price-container");
    const symbol_container = document.getElementById("symbol-container");
    const add_button = document.getElementById("add-button");
    const subs_button = document.getElementById("subs-button");
    const stock_id = document.getElementById("stock_id");
    const shares = document.getElementById("shares");
    const total = document.getElementById("total");
    const shares_error = document.getElementById("shares-error");
    const buy_button = document.getElementById("buy-button");
    let current_price = 0.00;

    shares.addEventListener("keydown", (e)=> {

        /// Get the pressed key code
        /// 8 -> delete key
        /// 48-57 -> 0-9 keys
        /// 96-105 -> 0-9 numeric key
        const key = e.keyCode;

        /// Accepts delete key
        if (key == 8) {
            return;
        }

        /// stops the event if the pressed key is not a number from 0-9
        if(!( (key >= 48 && key <= 57) || (key >= 96 && key <= 105))) {
            e.preventDefault();
        }
    });

    shares.addEventListener("change", (e) => {
        const current_shares = shares.value;
        if (current_shares == "") {
            shares.value = "1";
        }

        let new_shares = (current_shares == "" || !is_valid_share(current_shares)) ? 1 : parseInt(current_shares);

        if(new_shares < 100 && new_shares >= 0) {
            shares_error.innerHTML = "";
        } else if (new_shares > 100) {
            shares_error.innerHTML = "The max shares that you can purchase are 100";
        }

        if (new_shares < 1) {
            shares.value = "1";
            new_shares = 1;
        } else if (new_shares > 100) {
            shares.value = "100";
            new_shares = 100;
        }

        total.innerHTML = `${calculate_total(new_shares).toFixed(2)}`;
    });

    add_button.addEventListener("click", (e) => {
        const current_shares = shares.value;

        let new_shares = (current_shares == "" || !is_valid_share(current_shares)) ? 1 : parseInt(current_shares) + 1;

        if(new_shares > 100) {
            shares_error.innerHTML = "The max shares that you can purchase are 100";
            shares.value = "100";
            new_shares = 100;
        } else {
            shares.value = `${new_shares}`;
        }
        total.innerHTML = `${calculate_total(new_shares).toFixed(2)}`;
    });

    subs_button.addEventListener("click", (e) => {
        const current_shares = shares.value;

        let new_shares = (current_shares == "" || !is_valid_share(current_shares)) ? 1 : parseInt(current_shares) - 1;

        if(new_shares < 100 && new_shares > 0) {
            shares_error.innerHTML = "";
        }

        if (new_shares < 1) {
            shares.value = "1";
            new_shares = 1;
        } else if (new_shares > 100) {
            shares.value = "100";
            new_shares = 100;
        } else {
            shares.value = new_shares;
        }

        total.innerHTML = `${calculate_total(new_shares).toFixed(2)}`;
    });

    buy_button.addEventListener("click", (e) => {
            if (!is_valid_purchase()) { e.preventDefault(); }
    });

    symbol.addEventListener("keyup", (e) => {
        // POST request using fetch()
        fetch("/stock-info", {

        	// Adding method type
        	method: "POST",

        	// Adding body or contents to send
        	body: JSON.stringify({
        		symbol: symbol.value,
        	}),

        	// Adding headers to the request
        	headers: {
        		"Content-type": "application/json; charset=UTF-8"
        	}
        })
        // Converting to JSON
        .then(response => response.json())
        // Displaying information to its container
        .then( (data ) => {
            if (data) {
                const { name, price, symbol } = data;
                shares_error.innerHTML = "";
                name_container.innerHTML = name ? name : "The name is not available";
                price_container.innerHTML = price ? `${price}` : "The price is not available";
                symbol_container.innerHTML = symbol ? symbol : "The symbol is not available";
                stock_id.value = symbol ? symbol : "";
                shares.value = "1";
                total.innerHTML = price ? `${price}` : "";
                current_price = parseFloat(price);
            } else {
                shares_error.innerHTML = "";
                name_container.innerHTML = "";
                price_container.innerHTML = "";
                symbol_container.innerHTML = "";
                shares.value = "1";
                total.innerHTML = "";
                stock_id.value = "";
                current_price = 0.00;
            }
        })
        .catch( console.warn );
    });



    function calculate_total(shares_value) {
        if (!is_valid_share(shares_value.toString())) {
            shares_value = 1;
        }
        return shares_value * current_price;
    }

    function is_valid_purchase() {
        const stock_id_value = stock_id.value.trim();
        const shares_value = shares.value;
        const valid_shares = is_valid_share(shares_value);
        let valid_stock_id = true;
        if (stock_id_value == "") {
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