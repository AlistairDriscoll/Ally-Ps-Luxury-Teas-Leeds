/* jshint esversion: 6 */
/* global $ */


const europeanCountries = ["AL",
    "AD",
    "AM",
    "AT",
    "AZ",
    "BY",
    "BE",
    "BA",
    "BG",
    "HR",
    "CY",
    "CZ",
    "DK",
    "EE",
    "FI",
    "FR",
    "GE",
    "DE",
    "GR",
    "HU",
    "IS",
    "IE",
    "IT",
    "KZ",
    "XK",
    "LV",
    "LI",
    "LT",
    "LU",
    "MT",
    "MD",
    "MC",
    "ME",
    "NL",
    "MK",
    "NO",
    "PL",
    "PT",
    "RO",
    "RU",
    "SM",
    "RS",
    "SK",
    "SI",
    "ES",
    "SE",
    "CH",
    "TR",
    "UA",
    "VA",];
let countrySelector = $('#id_country');
let orderTotal = $('#order-total').value;
let hiddenDeliveryCost = $('#id_delivery_cost');
let hiddenGrandTotal = $('#id_grand_total');
let displayDeliveryCost = $('#display-delivery');
let displayGrandTotal = $('#display-grand-total');

countrySelector.addEventListener('change', function () {
    if (countrySelector.value === "UK") {
        displayDeliveryCost.value = 3;
        hiddenDeliveryCost.value = 3;
    } else if (europeanCountries.includes(countrySelector.value)) {
        displayDeliveryCost.value = 7;
        hiddenDeliveryCost.value = 7;
    } else {
        displayDeliveryCost.value = 15;
        hiddenDeliveryCost.value = 15;
    }
    hiddenGrandTotal.value = hiddenDeliveryCost.value + orderTotal;
    displayGrandTotal.value = hiddenGrandTotal.value + orderTotal;
});