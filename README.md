# Licenses
We own no rights to the images used in this game.

# Running the app
- Install the python dependencies
  - requests
  - Flask
  - flask-cors
  - mysql-connector-python
- Create a database named "flight_game"
- Datadumped sql file is included in the project 
- Make sure that a user named "root" has access to the database with the password "root"
- Make sure that the database is running on port 3306
- Run `backend.py` to start the Flask server
- Open the address that the server prints (e.g. `127.0.0.1:5000`) to go to the app's start menu

# The game
In Quiz-Game player travels across the globe and visits countries. Player gets asked a question about their
chosen country and has to choose between two options. If player answers correctly they can receive up to 300 points
depending on how quickly they answer. However if the answer is incorrect player loses one life and once all three lives
have been lost the game ends. Players goal is to receive as high as possible score and they can and compare results with other players. 

# How to play
To start playing, first create a username. After that you can start a new game. In the world map you can move around with arrow keys, 
and then choose the country of your choice by pressing the Enter key. Once you've selected a country, you will be asked a question about that country.
From the two options, choose whichever option you think is correct. You can only answer one question per country, then you can move to the next country.

The game utilizes autosave feature which will allow you to continue where you left off. You can load your save from the main menus load game option.
