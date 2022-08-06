![alt text](https://github.com/giovannetor/Trinacry/blob/main/perlogo_small.png)

# Elemental Adventure!
## What is it?
Sopel.dev8.0.0 module to play Elemental Adventure. 

[RULES](https://webchat.duckie.chat/uploads/2ab66fbf957ab02d/paste.txt)

## User Commands
1. `.elemental adventure | .elad | ` Opens the lobby. Doesn't start the game.
2. `.join      | .jo |` Joins the match.
3. `.quit      | .qu | `Leave the match. ATTENTION! The enemy will win.
4. `.deal      | .de |` Start the match.
5. `.play      | .pl |` Play a Hero.
6. `.cards     | .ca |` Shows the Heroes in your hand, and the Enhanced Element.
7. `.help elad |     |` How did you get here without knowing? XD
8. `.language  |.lan |` Change the game's language (available english and italian)
9. `.rank      |     |` Show your stats.

## Admin Commands
1. `.adrank    |    |` Shows another player's stats.
2. `.teams     |.tm |` Show each team's reputation.
3. `.eladmove  |    |` Moves a match in another chan.
4. `.adstop elad |  |` Forcefully stops a match.
5. `.eladgames |.eladgm |` Shows in what chans a match is ongoing.

## CARD EXAMPLE

        `[id] Element Hero |⚔ atk |✪ rep|`

_id: It's the Hero's unique ID. Use .play <id> to use it.
Element: The Hero's Element.
Hero: The Hero you're using.
atk: The stat that defines how powerful a Hero is on the Field.
rep: The stat that defines how much a Hero is worth._

### NOTES
- During the Configuration, a Log Chan shall be defined. This is the chan where the bot will
send his logs, and can only be one, stated with the "#chan_name" format.
- During the Configuration, a list of Game Chans shall be defined. These are the chans where the game
is allowed to run. State one per line with the "#chan_name" format.
- During the Configuration, you'll be able to choose a language for the game. The default one is Italian. _Available_:Italiano , English
