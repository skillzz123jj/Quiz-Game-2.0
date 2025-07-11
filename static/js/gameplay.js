'use strict';

import {dx, dy, handleKeyDown, handleKeyUp} from './inputs.js';
import {fetchCountryData} from './backendConnection.js';

window.addEventListener('keydown', handleKeyDown);
window.addEventListener('keyup', handleKeyUp);

const canvas = document.getElementById('gamecanvas');
const ctx = canvas.getContext('2d');

let foundCollidingDot = null;

//Initializes the plane canvases
const playerHorizontal = new Image();
const playerVerticalUp = new Image();
const playerVerticalDown = new Image();

playerHorizontal.src = `${SCRIPT_ROOT}/static/img/red-airplane-left.png`;

playerVerticalUp.src = `${SCRIPT_ROOT}/static/img/red-airplane-up.png`;

playerVerticalDown.src = `${SCRIPT_ROOT}/static/img/red-airplane-down.png`;

const spriteWidth = 54;
const spriteHeight = 54;

let playerX = canvas.width / 2 - spriteWidth / 2;
let playerY = canvas.height / 2 - spriteHeight / 2;

let flipHorizontal = true;
let currentSprite = playerHorizontal;

function drawPlayer() {
  ctx.save();

  if (flipHorizontal) {
    ctx.scale(-1, 1);
    ctx.drawImage(
        currentSprite,
        -playerX - spriteWidth,
        playerY,
        spriteWidth,
        spriteHeight,
    );
  } else {
    ctx.drawImage(currentSprite, playerX, playerY, spriteWidth, spriteHeight);
  }
  ctx.restore();
}

function updateDirection() {
  if (dy < 0) {
    currentSprite = playerVerticalUp;
    flipHorizontal = false;
  } else if (dy > 0) {
    currentSprite = playerVerticalDown;
    flipHorizontal = false;
  } else if (dx > 0) {
    currentSprite = playerHorizontal;
    flipHorizontal = true;
  } else if (dx < 0) {
    currentSprite = playerHorizontal;
    flipHorizontal = false;
  }
}

function getCanvasRelativePosition(dotElement, canvas) {
  const dotRect = dotElement.getBoundingClientRect();
  const canvasRect = canvas.getBoundingClientRect();

  return {
    x: dotRect.left - canvasRect.left + dotRect.width / 2,
    y: dotRect.top - canvasRect.top + dotRect.height / 2,
  };
}

//Checks if player is colliding with any of the dots
function isPlayerCollidingWithDot(
    dotElement, canvas, playerX, playerY, spriteWidth, spriteHeight) {
  const dotPos = getCanvasRelativePosition(dotElement, canvas);
  const playerCenterX = playerX + spriteWidth / 2;
  const playerCenterY = playerY + spriteHeight / 2;

  const dx = dotPos.x - playerCenterX;
  const dy = dotPos.y - playerCenterY;
  const distance = Math.sqrt(dx * dx + dy * dy);

  const collisionThreshold = spriteWidth / 2;

  return distance < collisionThreshold;
}

//Updates the game every frame so that sprites are updated and collisions checked
function updateGame() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  updateDirection();
  drawPlayer();
  const allDots = document.querySelectorAll('.country-dot');

  for (const dot of allDots) {
    if (dot.classList.contains('collected')) continue;
    if (isPlayerCollidingWithDot(dot, canvas, playerX, playerY, spriteWidth,
        spriteHeight)) {
      foundCollidingDot = dot;
      break;
    }
  }

  //Highlights the dot if player is on it
  for (const dot of allDots) {
    if (dot === foundCollidingDot) {
      dot.classList.add('highlighted');
    } else {
      dot.classList.remove('highlighted');
    }
  }

  requestAnimationFrame(updateGame);
}

//Checks if player has chosen a country
document.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' && foundCollidingDot) {
    fetchCountryData(foundCollidingDot.title);
    foundCollidingDot.style.backgroundColor = 'green';
    foundCollidingDot.classList.add('collected');
    foundCollidingDot = null;

  }
});

requestAnimationFrame(updateGame);


