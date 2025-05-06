'use strict';

import { handleAnswer } from './gameState.js';

// Creates a call to backend python via Flask
export async function fetchCountryData(country) {
  const response = await fetch(
    `${SCRIPT_ROOT}/api/country?name=${encodeURIComponent(country)}`
  );

  if (!response.ok) {
    console.error("Failed to fetch data from the backend.");
    document.getElementById('country-data').innerHTML = "<p>Error loading data.</p>";
    return;
  }

  const data = await response.json();
  console.log("Backend response:", data);

  const box = document.getElementById('country-data');

  const answers = [data.correct, data.incorrect].sort(() => Math.random() - 0.5);

  box.innerHTML = `
  ${data.correct.country}<br>
  <p>What is the capital?</p>
  <ul>
    ${answers.map((ans, i) => `
      <li><button id="answer${i + 1}" type="button">${ans.result}</button></li>
    `).join('')}
  </ul>
  <p id="correctAnswer">Correct answer!</p>
  <p id="incorrectAnswer">Wrong answer!<br>You lost 1 life</p>
  <p id="incorrectAnswer">Wrong answer!<br>You lost 1 life</p>
 
  <button id="close-btn" style="margin-top: 10px; display: none;">Continue</button>
  <button id="gameOver-btn" style="margin-top: 10px; display: none;">Back to Main Menu</button>
`;

  document.getElementById('center-box').style.display = 'block';

  answers.forEach((ans, i) => {
    document.getElementById(`answer${i + 1}`).addEventListener('click', () => {
      handleAnswer(ans.correct, i + 1);
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const createButton = document.getElementById("authentication-form");
  const loginForm = document.getElementById("authentication-form"); // Get the form element

  createButton.addEventListener("submit", createUser);
  loginForm.addEventListener("submit", loginUser);
});

export async function createUser() {
  const input = document.getElementById("username-input");
  const username = input.value.trim();

  if (!username) {
    alert("Please enter a username.");
    return;
  }

  try {
    const response = await fetch(`{{ url_for('createUser') }}?name=${encodeURIComponent(username)}`);

    if (!response.ok) {
      console.error("Failed to fetch data from the backend.");
      return;
    }
    localStorage.setItem("username", username);
    console.log(localStorage.getItem("username"));
    window.location.href = "{{ url_for('main-menu') }}";
  } catch (error) {
    console.error("Error communicating with the backend:", error);
  }
}

export async function loginUser(event) {

  const input = document.getElementById("username-input");
  const username = input.value.trim();

  if (!username) {
    alert("Please enter a username.");
    return;
  }

  localStorage.setItem("username", username);
  console.log(localStorage.getItem("username"));

 // window.location.href = "{{ url_for('main-menu') }}";
}
