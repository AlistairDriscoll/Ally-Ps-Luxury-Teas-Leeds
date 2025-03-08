/* jshint esversion: 6 */

// if no user information, let them know

let infoPElements = document.getElementsByClassName('display-info');
let infoDiv = document.getElementById('info-div');
let ordersDiv = document.getElementById('orders-div');
let orderPElements = document.getElementsByClassName('display-order');

if (infoPElements.length === 0) {
    infoDiv.textContent = "You currently have no information saved with us.";
}

if (orderPElements.length === 0) {
    ordersDiv.textContent = "You are yet to make any orders with us";
}
