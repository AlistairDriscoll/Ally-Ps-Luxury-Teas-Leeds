// if no user information, let them know

let infoPElements = document.getElementsByClassName('display-info');
let infoDiv = document.getElementById('info-div');

if (infoPElements.length === 0) {
    infoDiv.textContent = "You currently have no information saved with us."
}