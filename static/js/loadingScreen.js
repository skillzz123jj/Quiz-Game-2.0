'use strict'

document.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    const map = document.getElementById("map");
    const quitBtn = document.getElementById("quit-btn");
    const loadingAnimation = document.querySelector(".loading-animation");
    map.classList.remove("hidden");
    quitBtn.classList.remove("hidden");
    loadingAnimation.classList.add("hidden");
  }, 1000);
});