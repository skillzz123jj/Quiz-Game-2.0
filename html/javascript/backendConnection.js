'use strict';

import {handleAnswer} from './gameState.js';

//Creates a call to backend python via Flask
export async function fetchCountryData(country) {

  const response = await fetch(
      `http://localhost:5000/api/country?name=${encodeURIComponent(country)}`);

  if (!response.ok) {
    console.error("Failed to fetch data from the backend.");
    return;
  }
  const data = await response.json();
  console.log(data);

  const box = document.getElementById('country-data');

  box.innerHTML = `
    <strong>Country:</strong> ${data.country}<br>
    <ul>
      <li><button id="answer1" type="button">${data.result}</button></li>
      <li><button id="answer2" type="button">Placeholder</button></li>
    </ul>
  `;

  document.getElementById('center-box').style.display = 'block';

  document.getElementById('answer1').addEventListener('click', (e) => {
    handleAnswer(data.correct, 1);
  });

  document.getElementById('answer2').addEventListener('click', (e) => {
    handleAnswer(data.correct, 2);
  });

}


document.addEventListener("DOMContentLoaded", () => {
  const button = document.getElementById("create-user-btn");

  console.log("Button found?", button);
  if (button) {
    button.addEventListener("click", createUser);
  } else {
    console.error("Button not found in DOM");
  }
});



export async function createUser() {
  const input = document.getElementById("username-input");
  const username = input.value.trim();

  if (!username) {
    alert("Please enter a username.");
    return;
  }

  try {
    const response = await fetch(`http://localhost:5000/createUser?name=${encodeURIComponent(username)}`);

    if (!response.ok) {
      console.error("Failed to fetch data from the backend.");
      return;
    }

    console.log("Username:", username);

  } catch (error) {
    console.error("Error communicating with the backend:", error);
  }
}

