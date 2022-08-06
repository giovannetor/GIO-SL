---
# HOT POTATO 
Sopel Module to play Hot Potato Game on IRC!.
## HOW TO PLAY 
At the start of the game, a player receives the Potato, and the Bot Timer starts.
The players have to pass the Potato to each other. When the timer expires, whoever holds
the Potato in hand loses and is eliminated.


### USER COMMANDS 
1) `.potato` = Opens the game to players, but does not start it.
2) `.join` = Join the game.
3) `.deal` = Start the game. New players will no longer be able to join.
4) `.quit` = Leave the game.
5) `.give <nick>` = Pass the Potato to <nick>. Example: ".give ciccio"
6) `.help potato` = Call the help page (might differ from the README file).
7) `.potatostats` = Get your STATS
8) `.who` = Shows who's in game and who's holding the potato.

### ADMIN COMMANDS 
1) `.potgames `= Shows which channels there is a game in progress.
2) `.adstop potato` = Forcibly stop the game in progress in the channel in which it is written.
3) `.adpotatostats` = Get another user's STATS.
--- 
### NOTES
- During the Configuration, a Log Chan shall be defined. This is the chan where the bot will
send his logs, and can only be one, stated with the "#chan_name" format.
- During the Configuration, a list of Game Chans shall be defined. These are the chans where the game
is allowed to run. State one per line with the "#chan_name" format.
- During the Configuration, you'll be able to choose a language for the game. The default one is Italian. _Available_:Italiano , English
- While you are in the Game Channel, you will NOT be able to change NICKs. 
- To allow a friendlier game environment, you cannot pass back the Potato to the one who passed you in the first place.
- After a TOT number of turns (N° players + 3) the game will start asking to pass the Potato to inactive players.
