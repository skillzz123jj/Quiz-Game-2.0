'use strict';

document.addEventListener("DOMContentLoaded", () => {
  if (typeof GAME_STATE !== "undefined") {
    updateScoreUI(GAME_STATE.score);
    updateHeartsDisplay(GAME_STATE.lives);
  }
});

function focusGameMap() {
  /* Focus the game map, so that it's possible to move on the map. */
  document.querySelector('.maplibregl-canvas').focus();
}

export function handleAnswer(isCorrect, clickedButton, country) {
  const btn1 = document.getElementById('answer1');
  const btn2 = document.getElementById('answer2');
  btn1.disabled = true;
  btn2.disabled = true;
  btn1.classList.add("disabled");
  btn2.classList.add("disabled");

  const selectedAnswer = document.getElementById(
      `answer${clickedButton}`
  );
  const otherAnswer = document.getElementById(
      `answer${3 - clickedButton}`
  );
  otherAnswer.style.opacity = '30%';
  if (isCorrect) {
    selectedAnswer.style.backgroundColor = 'var(--green)';
    otherAnswer.style.backgroundColor = 'var(--red)';
    document.getElementById('correct-answer-text').style.display = 'block';
    updateDatabase(100, country);
  } else {
    selectedAnswer.style.backgroundColor = 'var(--red)';
    otherAnswer.style.backgroundColor = 'var(--green)';
    checkLives();
    document.getElementById('incorrect-answer-text').style.display = 'block';
  }

  const closeBtn = document.getElementById('close-btn');
  closeBtn.style.display = 'inline-block';
  closeBtn.addEventListener('click', () => {
    document.getElementById('center-box').style.display = 'none';
    focusGameMap();
  }, {once: true});
}

async function checkLives() {
  const response = await fetch(`${SCRIPT_ROOT}/fetchLives`);

  if (!response.ok) {
    console.error('Failed to fetch data from the backend.');
    return;
  }

  const data = await response.json();

  if (data.error) {
    console.error(`Error from backend: ${data.error}`);
    return;
  }

  let lives = parseInt(data.lives);

  if (lives === undefined) {
    console.error('No lives data found.');
    return;
  }

  lives--;

  if (lives <= 0) {
    await updateLives(lives);
    updateHeartsDisplay(lives);
    endGame();
  } else {
    await updateLives(lives);
    updateHeartsDisplay(lives);
  }

}



function endGame() {
  const finalScoreText = document.getElementById('score-container').querySelector('p').textContent;
  const finalScore = parseInt(finalScoreText) || 0;

  fetch(`${SCRIPT_ROOT}/endGame`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ score: finalScore }),
  })
    .then((res) => res.json())
    .then((data) => {
      console.log('Game end response:', data);
    })
    .catch((err) => console.error('Failed to end game:', err));

  document.getElementById('incorrect-answer-text').textContent = 'Game over';
  document.getElementById('close-btn').style.display = 'none';
  document.getElementById('gameOver-btn').style.display = 'block';
}


async function updateLives(newLives) {
  const response = await fetch(`${SCRIPT_ROOT}/updateLives`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({lives: newLives}),
  });

  if (!response.ok) {
    console.error('Failed to update lives.');
    return;
  }

  const data = await response.json();
  console.log('Update response:', data);
}

function updateHeartsDisplay(lives) {
  const totalHearts = 3;
  console.log(lives);
  for (let i = 1; i <= totalHearts; i++) {
    const heart = document.getElementById(`life-${i}`);
    console.log(`life-${i}`);
    if (i <= lives) {
      heart.src = '{{ url_for(\'static\', filename=\'img/life.png\') }}';
      heart.src = `${SCRIPT_ROOT}/static/img/life.png`;
    } else {
      heart.src = `${SCRIPT_ROOT}/static/img/lost-life.png`;
    }
  }
}

function updateDatabase(addedScore, newCountry = null) {
  let scoreElement = document.getElementById('score-container').
      querySelector('p');
  let currentScore = parseInt(scoreElement.textContent) || 0;
  let newScore = currentScore + addedScore;

  scoreElement.textContent = `${newScore} points`;
  updateScoreAndCountryDatabase(newScore, newCountry);
}

function updateScoreUI(score) {
  const scoreEl = document.getElementById("score-container").querySelector("p");
  scoreEl.textContent = `${score} points`;
}

async function updateScoreAndCountryDatabase(newScore, newCountry = null) {
  const payload = {score: newScore};
  if (newCountry) {
    payload.new_country = newCountry;
  }

  try {
    const response = await fetch(`${SCRIPT_ROOT}/updateJSON`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok) {
      console.error('Failed to update score or country:', data.error);
    } else {
      console.log('Update successful:', data.message);
    }
  } catch (error) {
    console.error('Error communicating with the backend:', error);
  }
}


