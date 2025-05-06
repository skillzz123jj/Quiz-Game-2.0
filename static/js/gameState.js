'use strict'

export function handleAnswer(isCorrect, clickedButton, country) {
  const btn1 = document.getElementById('answer1');
  const btn2 = document.getElementById('answer2');
  btn1.disabled = true;
  btn2.disabled = true;

if (isCorrect) {
  document.getElementById(`answer${clickedButton}`).style.backgroundColor = 'var(--green)';
  document.getElementById(`answer${3 - clickedButton}`).style.backgroundColor = 'var(--red)';
  document.getElementById('correctAnswer').style.display = 'block';
  updateDatabase(100, country)
} else {
  document.getElementById(`answer${clickedButton}`).style.backgroundColor = 'var(--red)';
  document.getElementById(`answer${3 - clickedButton}`).style.backgroundColor = 'var(--green)';
  checkLives();
  document.getElementById('incorrectAnswer').style.display = 'block';
}

  const closeBtn = document.getElementById('close-btn');
  closeBtn.style.display = 'inline-block';
  closeBtn.addEventListener('click', () => {
    document.getElementById('center-box').style.display = 'none';
  }, { once: true });
}

async function checkLives() {
  const response = await fetch(
    `${SCRIPT_ROOT}/fetchLives`
  );

 if (!response.ok) {
    console.error("Failed to fetch data from the backend.");
    return;
  }

  const data = await response.json();

  if (data.error) {
    console.error(`Error from backend: ${data.error}`);
    return;
  }

  let lives = parseInt(data.lives);

  if (lives === undefined) {
    console.error("No lives data found.");
    return;
  }
  lives--;
  updateLives(lives)
  updateHeartsDisplay(lives)

  if (lives <= 0){
    endGame()
  document.getElementById('incorrectAnswer').textContent = 'Game over';
    document.getElementById('close-btn').style.display = 'none';
  document.getElementById('gameOver-btn').style.display = 'block';

  }

  console.log("Current lives:", lives);

}



function endGame(){

}
async function updateLives(newLives) {
  const response = await fetch(`${SCRIPT_ROOT}/updateLives`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ lives: newLives })
  });

  if (!response.ok) {
    console.error("Failed to update lives.");
    return;
  }

  const data = await response.json();
  console.log("Update response:", data);
}

function updateHeartsDisplay(lives) {
  const totalHearts = 3;
  console.log(lives)
  for (let i = 1; i <= totalHearts; i++) {
    const heart = document.getElementById(`life-${i}`);
    console.log(`life-${i}`)
    if (i <= lives) {
      heart.src = "{{ url_for('static', filename='img/life.png') }}";
    } else {
      heart.src = "{{ url_for('static', filename='img/lost-life.png') }}";
    }
  }
}

function updateDatabase(addedScore, newCountry = null) {
  let scoreElement = document.getElementById('score-container').querySelector('p');
  let currentScore = parseInt(scoreElement.textContent) || 0;
  let newScore = currentScore + addedScore;

  scoreElement.textContent = `${newScore} points`;
  updateScoreAndCountryDatabase(newScore, newCountry);
}


async function updateScoreAndCountryDatabase(newScore, newCountry = null) {
  const payload = { score: newScore };
  if (newCountry) {
    payload.new_country = newCountry;
  }

  try {
    const response = await fetch(`${SCRIPT_ROOT}/updateJSON`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (!response.ok) {
      console.error("Failed to update score or country:", data.error);
    } else {
      console.log("Update successful:", data.message);
    }
  } catch (error) {
    console.error("Error communicating with the backend:", error);
  }
}


