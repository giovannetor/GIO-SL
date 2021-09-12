"""
Woggle - bot framework

  Copyright (C) 2021 Giovanni Coci <giovanni.coci1@yahoo.com>

This file is part of Woggle. Woggle is free software: you can redistribute
it and/or modify it under the terms of the GNU General Public License as
published by the Free Software Foundation, version 3.

Woggle is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import threading

import sopel.plugin as plugin
from sopel import config
from sopel.formatting import colors, CONTROL_BOLD, CONTROL_COLOR, CONTROL_NORMAL

settings = config.Config('/Users/giova/.sopel/default.cfg')  # replace with the config path

from sopel.config.types import StaticSection, ListAttribute, ValidatedAttribute

game_chan = None


# Called when the module gets loaded
def setup(bot):
    bot.config.define_section("TicTacToe", TicTacToeConfigSection)

    # Set the allowed game channels
    global game_chan
    global log_chan
    game_chan = bot.config.TicTacToe.gamechannels
    log_chan = bot.config.TicTacToe.logchannels


# Called when the module gets configured
def configure(config):
    config.define_section("TicTacToe", TicTacToeConfigSection)
    config.TicTacToe.configure_setting("gamechannels", "In what channels is TicTacToe allowed to be played?")
    config.TicTacToe.configure_setting("logchannels", "In what channels will TicTacToe send logs?")


# Class with the settings for tictactoe
class TicTacToeConfigSection(StaticSection):
    gamechannels = ListAttribute("gamechannels")
    logchannels = ValidatedAttribute("logchannels")


"""
I didn't really understand how to link the code to the config file, so
you'll have to write the [ttt] section in the config file manually... :)
"""

# Format for the X, O and the word "TicTacToe" in-game
X = CONTROL_BOLD + CONTROL_COLOR + colors.LIGHT_CYAN + "X" + CONTROL_NORMAL
O = CONTROL_BOLD + CONTROL_COLOR + colors.RED + "O" + CONTROL_NORMAL
TRIS = CONTROL_BOLD + CONTROL_COLOR + colors.RED + "," + colors.WHITE + " Tic" + CONTROL_COLOR + colors.BLACK + "," + colors.WHITE + "Tac" + CONTROL_COLOR + colors.LIGHT_CYAN + "," + colors.WHITE + "Toe " + CONTROL_NORMAL

gridlist = ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]
lock = threading.RLock()
win_games = 3

"""
The following strings are provided in english. 
They can easily be translate to any language.

The link for the help sends to a .txt file. Can be easily changed with another type of link.
"""
string_help_eng = "https://www.scoutlink.net/tictactoe"
strings_eng = {"cant_join": "I'm sorry %s , the max number of players is 2. Wait until next match :)",
               "cant_play": "You are not inside the match, please do not disturb the other players :)",
               "start": "Players Reached! Let's play " + TRIS + "!!",
               "already_in": " %s you are already inside the match of " + TRIS + ".",
               "turn": "%s 's turn, please wait.", "noletter": "You typed '%s', must type A, B or C instead.",
               "nonumber": "You typed '%s', musts be 1, 2 or 3 instead.",
               "nogrid": "'%s' isn't a proper slot in the grid.", "yours": "This slot is already yours!",
               "other": "This slot belongs to the other player.", "ok": "%s in %s by %s!",
               "win": "%s made " + TRIS + "!!", "next_turn": "It's %s's turn now!",
               "final_win": "%s scored 3 wins and won the " + TRIS + " game!!",
               "endgame": CONTROL_BOLD + CONTROL_COLOR + colors.RED + "GAME OVER" + CONTROL_NORMAL + ". Start a new match if you wanna play again.",
               "game_started": "A new game of " + TRIS + " is started!",
               "adstop": CONTROL_BOLD + CONTROL_COLOR + colors.RED + "GAME OVER" + CONTROL_NORMAL + ". The game was stopped by an Admin.",
               "not_started": "The match hasn't started yet. Find another player to start.",
               "no_square": "Please put a slot after the command. e.g. 'A2'",
               "quit_stop": CONTROL_BOLD + CONTROL_COLOR + colors.RED + "GAME OVER" + CONTROL_NORMAL + ": a player left the match.",
               "draw_": "The match is a DRAW!", "missing": "A parameter is missing...try to write all together? :) ",
               "wrong_format": "You typed %s, which is wrong. Slot Example: 'A2' , 'C3' , 'B1' ."}


class tttgame:  # this class thinks about the "RULES" side of the game
    def __init__(self, trigger):
        self.strings = strings_eng  # default strings are in english
        self.starter = trigger.nick
        self.channel = trigger.sender
        self.players = {}  # Player's dict
        self.playerOrder = []  # List of players per order
        self.currentPlayer = 0
        self.started = False
        self.griglia = {"A1": "/", "A2": "/", "A3": "/",  # game grid
                        "B1": "/", "B2": "/", "B3": "/", "C1": "/", "C2": "/", "C3": "/"}

    def join(self, bot, trigger):
        with lock:
            if trigger.nick not in self.players:
                if len(self.players) == 2:
                    bot.say(self.strings["cant_join"] % trigger.nick)
                    return
                if self.started:
                    bot.say(self.strings["cant_play"])
                    return
                if len(self.players) == 0:  # if the player is the 1st, give him an X. Otherwise, O
                    self.players[trigger.nick] = {"squares": [], "sign": X, "score": 0}
                else:
                    self.players[trigger.nick] = {"squares": [], "sign": O, "score": 0}  # add player to players dict
                self.playerOrder.append(trigger.nick)  # add player to players order list
                if len(self.players) == 2:
                    self.started = True
                    bot.say(self.strings["start"])
                    self.print_grid(bot)
                    bot.say(self.strings['turn'] % self.playerOrder[self.currentPlayer])
            else:
                bot.say(self.strings["already_in"] % trigger.nick)  # player already in

    def play(self, bot, trigger):
        player = trigger.nick
        if not self.started:
            bot.say(self.strings["not_started"])
            return
        if player not in self.players:
            bot.notice(self.strings['cant_play'], player)
            return
        if player != self.playerOrder[self.currentPlayer]:
            bot.say(self.strings['turn'] % self.playerOrder[self.currentPlayer])
            return
        if not trigger.group(3):
            bot.say(self.strings["no_square"])
            return

        cmd = trigger.group(3).upper()

        if any([len(cmd) != 2, cmd[0] not in "ABC",
                cmd[1] not in "123"]):  # if at least one of these it's true, the it's wrong
            bot.say(self.strings["wrong_format"] % cmd)
            return

        cp = self.check_possible(player, cmd)  # Checks if it's possible to make the move. Check the function.
        if cp == 0:
            bot.say(self.strings["yours"])
            return
        elif cp == 2:
            bot.say(self.strings["other"])
            return

        bot.say(self.strings["ok"] % (self.players[player]["sign"], cmd, player))

        self.players[player]["squares"].append(cmd)
        self.griglia[cmd] = self.players[player]["sign"]
        self.print_grid(bot)
        # print(self.counter)
        if self.checkwin(player):  # Checks if the player won with the move. Check the function
            bot.say(self.strings["win"] % player)

            self.players[player]["score"] += 1
            self.reset(bot, trigger, place = trigger.sender)
        else:
            self.currentPlayer = 0 if self.currentPlayer == 1 else 1

            if "/" not in self.griglia.values():  # If the match gets to 9 moves without a win, it's a draw.
                bot.say(self.strings["draw_"])

                self.currentPlayer = 0 if self.currentPlayer == 1 else 1

                self.reset(bot, trigger, place = trigger.sender)
                return
            bot.say(self.strings["next_turn"] % self.playerOrder[self.currentPlayer])

    def reset(self, bot, trigger, place):  # after each game, reboots the game.
        for player in self.players:
            if self.players[player]["score"] == win_games:
                bot.say(self.strings["final_win"] % player)
                self.endgame(bot, trigger, player_win = player, place = place)
                return
            self.players[player]["squares"].clear()

            if self.players[player]["sign"] == X:
                self.players[player]["sign"] = O
            else:
                self.players[player]["sign"] = X

        self.currentPlayer = 0 if self.currentPlayer == 1 else 1

        self.griglia = {"A1": "/", "A2": "/", "A3": "/", "B1": "/", "B2": "/", "B3": "/", "C1": "/", "C2": "/",
                        "C3": "/"}

        self.print_grid(bot)
        bot.say(self.strings['turn'] % self.playerOrder[self.currentPlayer])

    def endgame(self, bot, trigger, player_win, place):  # game ends
        bot.say(self.strings["endgame"])
        forced = False
        tttbot.endgame(bot, trigger, player_win, place, forced)

    def checkwin(self, player):  # checks if the player won the game.
        squ = self.players[player]["squares"]
        check_dic = {"A": 0, "B": 0, "C": 0, "1": 0, "2": 0, "3": 0}

        for combination in squ:
            check_dic[combination[0]] += 1
            check_dic[str(combination[1])] += 1

        if any([max(check_dic.values()) == 3, all(["A1" in squ, "B2" in squ, "C3" in squ]),
                all(["A3" in squ, "B2" in squ, "C1" in squ])]):  # if the player has 3 letters or 3 numbers, it's a Win
            return True
        return False

    def check_possible(self, player, cmd):
        if self.griglia[cmd] == self.players[player]["sign"]:  # If the square belongs to the player
            return 0
        elif self.griglia[cmd] == "/":  # If the square is empty
            return 1
        return 2

    def print_grid(self, bot):
        dicgrid = self.griglia
        bot.say(dicgrid["A1"] + "   |   " + dicgrid["A2"] + "   |   " + dicgrid["A3"])
        bot.say("-------------")
        bot.say(dicgrid["B1"] + "   |   " + dicgrid["B2"] + "   |   " + dicgrid["B3"])
        bot.say("-------------")
        bot.say(dicgrid["C1"] + "   |   " + dicgrid["C2"] + "   |   " + dicgrid["C3"])


class tttbot:  # This class thinks about the "LOGISCIT" part of the game
    def __init__(self):
        self.games = {}
        self.strings = strings_eng

    def start(self, bot, trigger):

        if trigger.sender in self.games:
            self.join(bot, trigger)
        else:
            bot.say(self.strings['game_started'])
            bot.say(
                "[" + TRIS + "] : match" + CONTROL_COLOR + colors.LIME + " STARTED" + CONTROL_NORMAL + " in " +  # This log says where and by who a match is started
                trigger.sender + " by: " + CONTROL_COLOR + colors.LIGHT_CYAN + trigger.nick, log_chan)
            self.games[trigger.sender] = tttgame(trigger)
            self.join(bot, trigger)

    def endgame(self, bot, trigger, player_win, place, forced = False, partquit = False):
        if trigger.sender not in self.games:
            return
        if forced:
            # This log says where and by what admin the match is stopped
            bot.say(
                "[" + TRIS + "] : match" + CONTROL_COLOR + colors.RED + " STOPPED" + CONTROL_NORMAL + " in " + trigger.sender + " by: " + CONTROL_COLOR + colors.LIGHT_CYAN + trigger.nick,
                log_chan)
            bot.say(self.strings["adstop"])

        elif partquit:
            pl_win = ""
            for player in self.games[trigger.sender].players:
                if player != player_win:
                    pl_win += player
            bot.say(self.strings["quit_stop"])
            if not pl_win:
                pl_win = "NONE"
            bot.say(
                "[" + TRIS + "] : match" + CONTROL_COLOR + colors.YELLOW + " ENDED " + CONTROL_NORMAL + "in "  # Where and who won the match
                + place + ". Winner: " + CONTROL_COLOR + colors.LIGHT_CYAN + pl_win, log_chan)

        else:
            bot.say(
                "[" + TRIS + "] : match" + CONTROL_COLOR + colors.YELLOW + " ENDED " + CONTROL_NORMAL + "in "  # Where and who won the match
                + place + ". Winner: " + CONTROL_COLOR + colors.LIGHT_CYAN + player_win, log_chan)
        del self.games[place]

    def play(self, bot, trigger):
        if trigger.sender in self.games:
            self.games[trigger.sender].play(bot, trigger)
        else:
            bot.say(self.strings["not_started"])

    def join(self, bot, trigger):
        if trigger.sender in self.games:
            self.games[trigger.sender].join(bot, trigger)
        else:
            bot.say(self.strings['not_started'])

    def print_grid(self, bot, trigger):
        if trigger.sender in self.games:
            self.games[trigger.sender].print_grid(bot)
        else:
            bot.say(self.strings["not_started"])


ttt = tttbot()


@plugin.thread(True)
@plugin.commands("grid", "gr")
def grid(bot, trigger):
    if trigger.sender in game_chan:
        ttt.print_grid(bot, trigger)


@plugin.commands("ttt", "TicTacToe", "tictactoe")
def ttt_start(bot, trigger):
    if trigger.sender in game_chan:
        ttt.start(bot, trigger)


@plugin.commands("join", "jo")
def ttt_join(bot, trigger):
    if trigger.sender in game_chan:
        ttt.join(bot, trigger)


@plugin.commands("adstop")
@plugin.example(".adstop ttt", ".adstop tictactoe")
def adstop(bot, trigger):
    if trigger.sender in game_chan and trigger.group(3) == "ttt" or trigger.group(3) == "tictactoe":
        ttt.endgame(bot, trigger, forced = True, place = trigger.sender, partquit = False, player_win = None)


@plugin.commands("play", "pl")
@plugin.example(".play a2", ".pl C3")
def play(bot, trigger):
    if trigger.sender in game_chan:
        ttt.play(bot, trigger)


@plugin.commands("quit", "qu")
def quit(bot, trigger):
    if trigger.sender in game_chan:
        ttt.endgame(bot, trigger, forced = False, place = trigger.sender, partquit = True, player_win = trigger.nick)


@plugin.commands("help ttt", "help tictactoe")
@plugin.example(".help ttt", ".help tictactoe")
def brishelp(bot, trigger):
    if trigger.sender in game_chan:
        bot.notice(CONTROL_BOLD + CONTROL_COLOR + colors.YELLOW + "GUIDE: " + CONTROL_NORMAL + string_help_eng,
                   trigger.nick)


@plugin.event("PART")
def part(bot, trigger):
    if trigger.sender in game_chan:
        ttt.endgame(bot, trigger, forced = False, place = trigger.sender, partquit = True, player_win = trigger.nick)


@plugin.event("QUIT")
def quit_(bot, trigger):
    if trigger.sender in game_chan:
        ttt.endgame(bot, trigger, forced = False, place = trigger.sender, partquit = True, player_win = trigger.nick)
