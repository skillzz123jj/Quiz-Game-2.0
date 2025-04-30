'use strict'

export function handleAnswer(selectedAnswer, button) {
  const btn1 = document.getElementById('answer1');
  const btn2 = document.getElementById('answer2');
  btn1.disabled = true;
  btn2.disabled = true;

  if (selectedAnswer && button === 1) {
    btn1.style.backgroundColor = 'green';
    btn2.style.backgroundColor = 'red';
  } else {
    btn1.style.backgroundColor = 'red';
    btn2.style.backgroundColor = 'green';
  }

}

document.getElementById('quit-btn').addEventListener('click', () => {
  window.location.href = 'start-menu.html';
});
