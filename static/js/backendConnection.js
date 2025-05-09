'use strict';

import {handleAnswer} from './gameState.js';

// Creates a call to backend python via Flask
export async function fetchCountryData(country) {
  const response = await fetch(
      `${SCRIPT_ROOT}/api/country?name=${encodeURIComponent(country)}`,
  );

  if (!response.ok) {
    console.error('Failed to fetch data from the backend.');
    document.getElementById(
        'country-data').innerHTML = '<p>Error loading data.</p>';
    return;
  }

  const data = await response.json();
  console.log('Backend response:', data);

  const box = document.getElementById('country-data');

  const answers = [data.correct, data.incorrect].sort(
      () => Math.random() - 0.5);

  // Creates a html element that contains the generated questions
  box.innerHTML = `
    <h2 class="white-text" id="country-name">${data.correct.country}</h2>
    <p id="country-question">${data.correct.question}</p>
    <ul id="answer-list">
      ${answers.map((ans, i) => `
        <li><button id="answer${i +
  1}" class="answer-button" type="button">${ans.result}</button></li>
      `).join('')}
    </ul>
    <h3 id="correct-answer-text" class="orange-text" style="display:none;">Correct answer!</h3>
    <h3 id="incorrect-answer-text" class="orange-text" style="display:none;">Wrong answer!<br>You lost 1 life</h3>
    <button id="close-btn" style="margin-top: 10px; display: none;">Continue</button>
    <a href="${SCRIPT_ROOT}/main-menu" id="gameOver-btn" class="game-button" style="margin-top: 10px; display: none;">
      Back to Main Menu
    </a>
  `;
  // Timer to calculate the earned points from a question
  let timeLeft = 30;
  const countdown = setInterval(() => {
    timeLeft--;
    if (timeLeft <= 0) {
      clearInterval(countdown);
    }
  }, 1000);

  document.getElementById('center-box').style.display = 'block'; //Displays the question box

  // Checks which answer was chosen
  answers.forEach((ans, i) => {
    document.getElementById(`answer${i + 1}`).addEventListener('click', () => {
      handleAnswer(ans.correct, i + 1, data.correct.country, timeLeft);
    });
  });
}




