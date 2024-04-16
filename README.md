# A simple 2048 Clone

Made this as a practice tutorial for Javascript.

## Done
* Grid created in HTML CSS
* Add EventListener on arrow keys
* Generate new tile
* Board starts automatically with 2 random numbers.
* Score improvements needed when update is done.
* Refactor the move() function

## Challenges
* Create Game loop
    * **Win**
        * Show a text in the winner div if a tile has reached 2048
    * **Valid Moves**
        * Immplement a Game function
        * Check the board for valid moves
        * Only if a valid move has been executed, a tile should be added
    * **Death**
        * Implement a Game function 
        * If there are no valid moves and no empty tiles
        * Player loses
    * **Restart**
        * Add a restart button
        * Should reset board and start a new game.
* Extra
    * Add a 'Best' Scoreboard
    * Should show value of best game in a session.
    * Restart should reset 'score' but 'Best' score should be maximum reached score until a user reloads the browser.