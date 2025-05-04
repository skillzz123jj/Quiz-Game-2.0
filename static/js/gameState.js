'use strict'

export function handleAnswer(isCorrect, clickedButton) {
  const btn1 = document.getElementById('answer1');
  const btn2 = document.getElementById('answer2');
  btn1.disabled = true;
  btn2.disabled = true;

if (isCorrect) {
  document.getElementById(`answer${clickedButton}`).style.backgroundColor = 'rgba(0, 128, 0, 0.3)';
  document.getElementById(`answer${3 - clickedButton}`).style.backgroundColor = 'rgba(255, 0, 0, 0.3)';
} else {
  document.getElementById(`answer${clickedButton}`).style.backgroundColor = 'rgba(255, 0, 0, 0.3)';
  document.getElementById(`answer${3 - clickedButton}`).style.backgroundColor = 'rgba(0, 128, 0, 0.3)';
  checkLives(localStorage.getItem("username"));
}

  const closeBtn = document.getElementById('close-btn');
  closeBtn.style.display = 'inline-block';
  closeBtn.addEventListener('click', () => {
    document.getElementById('center-box').style.display = 'none';
  }, { once: true });
}

async function checkLives(userId) {

  console.log("username" + userId)
  const response = await fetch(
    `http://localhost:5000/databaseInteraction?username=${encodeURIComponent(userId)}`
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

  const lives = data.lives;

  if (lives === undefined) {
    console.error("No lives data found.");
    return;
  }

  console.log("Current lives:", lives);
  return lives;
}




