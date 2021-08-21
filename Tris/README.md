![alt text](https://github.com/giovannetor/Trinacry/blob/main/perlogo_small.png)

# TicTacToe

Hi. This is a lil module to play TicTacToe on IRC with Trinacry. 
Called "Tris" in some countries, it's a popular 1v1 game.

## How to win
- Score 3 signs in a raw / column / diagonal
- Make the enemy leave.
<img src="https://github.com/giovannetor/Trinacry/blob/main/Tris/files/Jogo_da_velha_-_tic_tac_toe.png" alt="TTT" width="200" height="200">



## What it does 
Commands:
1. *cmd* `.ttt` : Starts the game.
2. *cmd* `.grid` : Shows the actual grid.
3. *cmd* `.play` : Put your sign on a slot. *ex: `.play A2`*
4. *cmd* `.join` : Joins the match.
5. *cmd* `.quit` : Quits the game.
6. *cmd* `.help ttt` : Provide a file with game help.
6. *cmd* `.adstop ttt` _(admin only)_ : Forcefully stops the game. 

Events:
1. *ev* `QUIT` : Triggered when the user quits. Executes `.quit`
2. *ev* `LEAVE` : Triggered when the user leaves. Executes `.quit`
