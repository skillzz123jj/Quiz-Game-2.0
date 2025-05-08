'use strict'

document.addEventListener('DOMContentLoaded', () => {
    const leaderboardList = document.getElementById('leaderboard-list');

    fetch(`${SCRIPT_ROOT}/getLeaderboard`)
        .then(res => res.json())
        .then(data => {
            leaderboardList.innerHTML = ''; 

            if (Array.isArray(data)) {
                data.forEach(entry => {
                    const li = document.createElement('li');
                    li.innerHTML = `<span class="white-text">${entry.username}</span> .............. <span class="white-text">${entry.score}</span>`;
                    leaderboardList.appendChild(li);
                });
            } else {
                leaderboardList.innerHTML = '<li>Error loading leaderboard</li>';
                console.error(data.error);
            }
        })
        .catch(err => {
            leaderboardList.innerHTML = '<li>Failed to load leaderboard</li>';
            console.error(err);
        });
});
