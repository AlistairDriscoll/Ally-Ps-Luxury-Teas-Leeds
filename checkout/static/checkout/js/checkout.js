/* jshint esversion: 6 */
/* global $ */


const europeanCountries = ["AL", // Albania
    "AD", // Andorra
    "AM", // Armenia
    "AT", // Austria
    "AX", // Aland Islands
    "AZ", // Azerbaijan
    "BY", // Belarus
    "BE", // Belgium
    "BA", // Bosnia and Herzegovina
    "BG", // Bulgaria
    "HR", // Croatia
    "CY", // Cyprus
    "CZ", // Czechia (Czech Republic)
    "DK", // Denmark
    "EE", // Estonia
    "FI", // Finland
    "FR", // France
    "GE", // Georgia
    "DE", // Germany
    "GR", // Greece
    "HU", // Hungary
    "IS", // Iceland
    "IE", // Ireland
    "IT", // Italy
    "KZ", // Kazakhstan
    "XK", // Kosovo
    "LV", // Latvia
    "LI", // Liechtenstein
    "LT", // Lithuania
    "LU", // Luxembourg
    "MT", // Malta
    "MD", // Moldova
    "MC", // Monaco
    "ME", // Montenegro
    "NL", // Netherlands
    "MK", // North Macedonia
    "NO", // Norway
    "PL", // Poland
    "PT", // Portugal
    "RO", // Romania
    "RU", // Russia
    "SM", // San Marino
    "RS", // Serbia
    "SK", // Slovakia
    "SI", // Slovenia
    "ES", // Spain
    "SE", // Sweden
    "CH", // Switzerland
    "TR", // Turkey
    "UA", // Ukraine
    "VA", // Vatican City
    ];
let countrySelector = $('#id_country');
let orderTotal = parseFloat($('#order-total').text());
let hiddenDeliveryCost = $('#id_delivery_cost');
let hiddenGrandTotal = $('#id_grand_total');
let displayDeliveryCost = $('#display-delivery');
let displayGrandTotal = $('#display-grand-total');

/**
 * Checks to see if country selector has been changed
 * Checks the country, if it isn't in the UK or Europe delivery is £15
 * Else if in europe £7 or UK £3
 * Calculates grand total based on this and displays it, along with
 * adding the values to the submit_order form
 */
countrySelector.on('change', function () {
    let country = countrySelector.val();
    let deliveryCost = 15;
    if (country === "UK") {
        deliveryCost = 3;
    } else if (europeanCountries.includes(country)) {
        deliveryCost = 7;
    }

    displayDeliveryCost.text("Delivery cost: " + deliveryCost);
    hiddenDeliveryCost.val(deliveryCost);
    let grandTotal = orderTotal + deliveryCost;
    displayGrandTotal.text("Grand total: " + grandTotal);
    hiddenGrandTotal.val(orderTotal + deliveryCost);
});