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

  box.innerHTML = `
  <h2 class="white-text" id="country-name">${data.correct.country}</h2>
  <p id="country-question">${data.correct.question}</p>
  <ul id="answer-list">
    ${answers.map((ans, i) => `
      <li><button id="answer${i + 1}" class="answer-button" type="button">${ans.result}</button></li>
    `).join('')}
  </ul>
  <h3 id="correct-answer-text" class="orange-text">Correct answer!</h3>
  <h3 id="incorrect-answer-text" class="orange-text">Wrong answer!<br>You lost 1 life</h3>
 
  <button id="close-btn" style="margin-top: 10px; display: none;">Continue</button>
  <a href="${SCRIPT_ROOT}/main-menu" id="gameOver-btn" class="game-button" style="margin-top: 10px; display: none;">
    Back to Main Menu
  </a>
`;

  document.getElementById('center-box').style.display = 'block';

  answers.forEach((ans, i) => {
    document.getElementById(`answer${i + 1}`).addEventListener('click', () => {
      handleAnswer(ans.correct, i + 1, data.correct.country);
    });
  });
}

export async function createUser() {
  const input = document.getElementById('username-input');
  const username = input.value.trim();

  if (!username) {
    alert('Please enter a username.');
    return;
  }

  try {
    const response = await fetch(
        `{{ url_for('createUser') }}?name=${encodeURIComponent(username)}`);

    if (!response.ok) {
      console.error('Failed to fetch data from the backend.');
      return;
    }
    localStorage.setItem('username', username);
    console.log(localStorage.getItem('username'));
    window.location.href = '{{ url_for(\'main-menu\') }}';
  } catch (error) {
    console.error('Error communicating with the backend:', error);
  }
}

export async function loginUser(event) {

  const input = document.getElementById('username-input');
  const username = input.value.trim();

  if (!username) {
    alert('Please enter a username.');
    return;
  }

  localStorage.setItem('username', username);
  console.log(localStorage.getItem('username'));

}



