//Instructions popup
const showInstructions = document.getElementById("show-instructions");
const hideInstructions = document.getElementById("hide-instructions");
const instructionsDialog = document.getElementById("instructions-dialog");

showInstructions.addEventListener("click", event => {
  event.preventDefault();
  instructionsDialog.showModal();
});

hideInstructions.addEventListener("click", event => {
  event.preventDefault();
  instructionsDialog.close();
});

//Darkmode
function dark_mode() {
  var element = document.body;
  element.classList.toggle("dark-mode");
}


  const username = sessionStorage.getItem("username");
  if (username) {
  document.getElementById("usernameDisplay").textContent = username;
} else {
  window.location.href = "create-profile.html";
}

