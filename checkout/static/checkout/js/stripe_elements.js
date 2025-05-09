/* jshint esversion: 6, globalstrict: true */
/* global $, Stripe */

/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here:
    https://stripe.com/docs/stripe-js
*/

/*
    Finds the public key and client secret, slices off the quotation marks.
    Sets up Stripe and its elements by passing through the public key.
    Creates a card element and gives it some styling.
    Mounts the card element onto the div with the id of 'card-element'.
*/

// Code taken and adapted from Code Institute Boutique Ado walkthrough

const zipRequiredCountries = ["US", "CA", "AU", "NZ"];
var stripePublicKey = $('#id_stripe_public_key').text().trim().slice(1, -1);
var clientSecret = $('#id_client_secret').text().trim().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();

/*
    Creates a new card configuration object with the correct ZIP/postcode setting.
*/
function createCard(hidePostalCode) {
    return elements.create('card', {
        style: {
            base: {
                color: '#000',
                fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
                fontSmoothing: 'antialiased',
                fontSize: '16px',
                '::placeholder': { color: '#aab7c4' }
            },
            invalid: { color: "#dc3545", iconColor: "#dc3545" }
        },
        hidePostalCode: hidePostalCode // Controls ZIP/postcode visibility
    });
}

// Creates the initial card element, defaulting to hiding ZIP/postcode
var card = createCard(true);
card.mount('#card-element');

// Stores the current ZIP visibility state to prevent unnecessary re-renders
var currentZipState = true;

/*
    Checks if the selected country's card payments require a ZIP code.
    Only updates the Stripe card element if a change is actually needed.
    Destroys the existing card element and recreates it with the correct ZIP/postcode setting.
*/
var countrySelector = document.getElementById("id_country");
countrySelector.addEventListener("change", function () {
    var selectedCountry = countrySelector.value.toUpperCase();
    var requireZip = zipRequiredCountries.includes(selectedCountry);

    console.log("Country Selected:", selectedCountry);
    console.log("Require ZIP Code:", requireZip);

    // Exit function if no update is needed
    if (currentZipState !== requireZip) {

        return;
    }

    card.destroy();
    card = createCard(!requireZip);
    card.mount("#card-element");
    currentZipState = !requireZip; // Store the new setting to prevent unnecessary re-renders
});

/*
    Handles and displays errors for invalid card details.
*/
card.addEventListener("change", function (event) {
    var errorDiv = document.getElementById("card-errors");
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        $(errorDiv).html("");
    }
});

/*
    Handles form submission by disabling inputs and confirming the payment.
*/
var form = document.getElementById("payment-form");

form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    $('#loading-overlay').fadeToggle(100);
    card.update({ disabled: true });
    $("#submit-button").attr("disabled", true);

    stripe.confirmCardPayment(clientSecret, {
        payment_method: { card: card }
    }).then(function (result) {
        if (result.error) {
            var errorDiv = document.getElementById("card-errors");
            var html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);
            card.update({ disabled: false });
            $("#submit-button").attr("disabled", false);
        } else {
            if (result.paymentIntent.status === "succeeded") {
                form.submit();
            }
        }
    });
});
