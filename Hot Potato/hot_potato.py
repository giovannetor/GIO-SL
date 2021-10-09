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

import time
from random import randint

from sopel.config.types import StaticSection, ListAttribute, ValidatedAttribute
from sopel.formatting import colors, CONTROL_BOLD, CONTROL_COLOR, CONTROL_NORMAL
from sopel.plugin import commands, priority, thread, event

LANGUAGE = "italiano"
GAME_CHAN = []
LOG_CHAN = None
HOTPOT_ADMINS = []


# Called when the module gets loaded
def setup(bot):
    bot.config.define_section("HotPotato", HotPotatoConfigSection)

    # Set the allowed game channels
    global LANGUAGE
    global GAME_CHAN
    global LOG_CHAN
    global HOTPOT_ADMINS
    LANGUAGE = bot.config.HotPotato.language
    GAME_CHAN = bot.config.HotPotato.gamechannels
    LOG_CHAN = bot.config.HotPotato.logchannels
    HOTPOT_ADMINS = bot.config.HotPotato.hotpot_admins


# Called when the module gets configured
def configure(config):
    config.define_section("HotPotato", HotPotatoConfigSection)
    config.HotPotato.configure_setting("language",
                                       "What language do you want to use in the game?")
    config.HotPotato.configure_setting("gamechannels",
                                       "In what channels is Hot Potato allowed to be played? (One per line)")
    config.HotPotato.configure_setting("logchannels",
                                       "In what channel will Hot Potato send logs? (Choose one)")
    config.HotPotato.configure_setting("hotpot_admins", "What accounts can operate on Hot Potato? (One per line)")


# Class with the settings for Elemental Adventure
class HotPotatoConfigSection(StaticSection):
    language = ValidatedAttribute("language")
    gamechannels = ListAttribute("gamechannels")
    logchannels = ValidatedAttribute("logchannels")
    hotpot_admins = ListAttribute("hotpot_admins")


potato_name = {"italiano": " PATATA BOLLENTE ",
               "english": "HOT POTATO"
               }

POTATO = " " + CONTROL_BOLD + CONTROL_COLOR + colors.ORANGE + "," + colors.BLACK + potato_name[
    LANGUAGE] + CONTROL_NORMAL + " "

min_players = 3  # DO NOT set to less than 3

help_ = {"italiano" : "https://webchat.duckie.chat/uploads/b0cdb3762d6dcd9c/paste.txt",
         "english" : "https://webchat.duckie.chat/uploads/e8e9b51897411a76/paste.txt"}

"""
The game only has string in Italian.
Strings can be translated by Teams willing to do so.
"""

# DO NOT translate the keys (what's before the ":"). ONLY translate the values (what's after the ":").
# DO NOT translate the "POTATO" value.
# DO NOT translate the CONTROL_BOLD, CONTROL_COLOR and colors values.

strings = {"italiano":
               {"already_in": "%s sei già all'interno della partita di" + POTATO,
                "already_started": "Mi spiace %s, ma la partita di" + POTATO + "è già iniziata.",
                "not_enough": "La partita di" + POTATO + "richiede un minimo di %d giocatori per iniziare.",
                "not_in": "%s non sei all'interno della partita di" + POTATO + ". Usa .join per unirti!",
                "time_counter": POTATO + "| Sono passati %d secondi su %d in %s .",
                "stop_timer": CONTROL_BOLD + CONTROL_COLOR + colors.RED + "STOP AL TEMPO!!! ",
                "kaboom_1": "Qualcuno ha una" + POTATO + "per le mani!",
                "kaboom_2": "si gira a guardare %s.",
                "kaboom": "KABOOM! %s è stato eliminato dal gioco.",
                "cant_pass": "Pssst il tempo si è fermato, se hai tu la patata... beh mi spiace!",
                "cant_play": "%s per favore non disturbare la partita degli altri giocatori. Puoi unirti alla prossima!",
                "not_have_potato": "%s non hai la" + POTATO + ". Fortunello!",
                "no_previous": "Mi spiace %s ma non si può passare la" + POTATO + "al giocatore che te l'ha appena data. TIC TAC!",
                "potato_received": ["%s ha ricevuto la" + POTATO,
                                    "%s adesso hai tu la" + POTATO + ". OUCH SCOTTA!",
                                    "%s presto! La" + POTATO + "scotta!!",
                                    "La" + POTATO + "ha scelto %s come suo nuovo proprietario.",
                                    "%s prende la" + POTATO + "al volo. Ottima presa!",
                                    "%s hai la" + POTATO + ". Il tempo scorre PRESTO!!",
                                    "%s usa .give <nick> per dare la patata a qualcun altro. TIC TAC!",
                                    "%s sbrigati a passare la" + POTATO + ". Non mi pagano abbastanza per fare anche l'infermiere XD",
                                    "%s ha avuto in dono la" + POTATO,
                                    "%s ha la" + POTATO + "adesso!"],
                "quit": "%s ha deciso di lasciare la partita.",
                "emergency_give": "Oh no, %s aveva la" + POTATO + "! Lancio di emergenza a %s!",
                "congrats_win": "Complimenti %s e %s, siete i due sopravvissuti! Avete vinto la partita"
                                " di" + POTATO + " sopravvivendo a ben %d turni!!!!",
                "new_turn": "Inizia il prossimo turnoooo",
                "potato_given": "%s inizia con la" + POTATO + ". Presto passala a qualcuno!",
                "game_started": "Una partita di" + POTATO + "è iniziata. Usa .join per unirti!",
                "not_started": "La partita di" + POTATO + "non è ancora iniziata.",
                "admin_stop": "Un ADMIN ha fermato la partita di" + POTATO,
                "quit_ok": "Un giocatore ha lasciato la partita." + POTATO + "deve essere iniziata di nuovo.",
                "receiver_missing": "Non hai scritto a chi vuoi passare la" + POTATO,
                "joined": "%s si unisce alla partita!!",
                "deal": "Partita iniziata! %s has la" + POTATO,
                "not_in_game": "%s non fa parte della partita. Passa la" + POTATO + "ai giocatori Voiced (+ davanti al nome).",
                "time_interaction": ["TIC TAC il tempo scorre.",
                                     "Chi sarà il prossimo a essere eliminato?!",
                                     "TEMPO SCADUTO... ahah scherzavo",
                                     "TIC TAC",
                                     "Ci siamo quasi...",
                                     "Chissà quando scadrà il tempo",
                                     "Uh oh, qualcuno sta per essere eliminato",
                                     "Più veloci, il tempo scorre!",
                                     "Manca poco! Più veloci!",
                                     "Il tempo corre veloce...",
                                     "Dai su, facciamola girare questa Patata"],
                "turns_no": "I seguenti giocatori non ricevono la" + POTATO + "da un po'. Provate a includerli nel gioco: " + CONTROL_BOLD + "%s.",
                "who": "La" + POTATO + "è in mano a %s.",
                "ingame": "I giocatori %s sono ancora in gioco."
                }
           }


class PotatoGame:
    def __init__(self, trigger):
        self.players = {}  # Dict of players
        self.strings = strings[LANGUAGE]  # default strings are in italian
        self.started = False  # Says if the game has started.
        self.has_potato = None  # Player holding the POTATO!!!
        # self.playerlist = []  # Iterable list
        self.canpass = False  # Says if it's a moment when players can pass or not.
        self.timecounter = 0  # Used for logs.
        self.stop_game = False  # Used to stop the timer.
        self.channel = None  # Game chan, set in Deal
        self.max_turn_no = 0  # max of turns a player can not receive a potato before repeating a warn

    def join(self, bot, trigger):
        if trigger.nick in self.players:
            bot.say(self.strings["already_in"] % trigger.nick)
            return
        if self.started:
            bot.notice(self.strings["already_started"] % trigger.nick, trigger.nick)
            return
        bot.say(self.strings["joined"] % trigger.nick)
        self.players[trigger.nick.lower()] = {"turns_alive": 0, "giver": None,
                                              "turn_no": 0}  # Players get added to the match.
        # self.playerlist.append(trigger.nick)
        bot.write(['MODE', trigger.sender, '+v', trigger.nick])  # Players are voiced

    def deal(self, bot, trigger):
        if len(self.players) < min_players:
            bot.say(self.strings["not_enough"] % min_players)
            return
        if self.started:
            bot.say(self.strings["already_started"])
            return
        if trigger.nick.lower() not in self.players:
            bot.say(self.strings["not_in"])
            return
        self.has_potato = list(self.players)[
            randint(0, len(list(self.players)) - 1)]  # The 1st player having the potato is random
        bot.say(self.strings["deal"] % self.has_potato)
        self.started = True
        self.canpass = True
        self.chan = trigger.sender
        self.max_turn_no = (len(self.players) + 3)  # we add +3 to give players a bit more gameplay freedom
        print(self.max_turn_no)
        self.timer_function(bot, randint(10, 100))  # starts the timer.

    @thread(True)
    def timer_function(self, bot, seconds: int):
        chan = self.chan
        def_seconds = seconds
        while seconds:
            if self.stop_game:  # if the game is stopped, the timer stops.
                break
            print(seconds)
            time.sleep(1)
            seconds -= 1
            self.timecounter += 1
            if self.timecounter % 15 == 0:  # every 15 seconds, notices to the log chan and sends a random sentence.
                bot.say(self.strings["time_interaction"][randint(0, len(self.strings["time_interaction"]) - 1)], chan)
                bot.say(self.strings["time_counter"] % (self.timecounter, def_seconds, chan), LOG_CHAN)

        if not self.stop_game:  # same as above.
            self.explode_potato(bot, chan)

    def explode_potato(self, bot, chan):
        self.canpass = False  # temporarily players can't pass
        kaboom_player = self.has_potato
        bot.say(self.strings["stop_timer"])
        time.sleep(1)
        bot.say(self.strings["kaboom_1"])
        time.sleep(1)
        bot.action(self.strings["kaboom_2"] % kaboom_player)
        time.sleep(1)
        bot.say(self.strings["kaboom"] % kaboom_player)
        self.remove_player(bot, chan, kaboom_player)  # player holding the potato makes kaboom!
        self.reset(bot, chan)  # reset the turn.

    def give(self, bot, giver, receiver, emergency=False):

        if not self.canpass:
            bot.notice(self.strings["cant_pass"], giver)
            return
        if giver not in self.players:
            bot.say(self.strings["cant_play"] % giver)
            return
        if receiver not in self.players:
            bot.say(self.strings["not_in_game"] % receiver)
            return
        if not self.started:
            bot.say(self.strings["already_started"])
            return
        if giver != self.has_potato:
            bot.say(self.strings["not_have_potato"] % giver)
            return
        if receiver == self.players[giver]["giver"]:  # suggested by Tony. To avoid ganging up against a player.
            bot.say(self.strings["no_previous"] % giver)
            return

        self.players[receiver]["giver"] = giver
        if not emergency:  # emergency = player holding the potato quits
            self.players[giver]["giver"] = None
        self.has_potato = receiver
        self.players[receiver]["turn_no"] = 0  # resets the not played turns of a player
        bot.say(self.strings["potato_received"][randint(0, len(self.strings["potato_received"]) - 1)] % receiver)

        for player in self.players:
            if player != receiver:
                self.players[player]["turn_no"] += 1

        self.check_turn_no(bot)

    def check_turn_no(self, bot):
        turn_no_list = ""
        for player in self.players:
            if self.players[player]["turn_no"] >= self.max_turn_no:
                turn_no_list += f"{player} ({self.players[player]['turn_no']}), "

        if not turn_no_list:  # if all the players are behaving nicely
            return

        turn_no_list.rstrip(",")  # we like nice format
        bot.say(self.strings["turns_no"] % str(turn_no_list))

    def who(self, bot, trigger):
        bot.say(self.strings["who"] % self.has_potato)
        bot.say(self.strings["ingame"] % str(list(self.players)))

    def quit(self, bot, trigger):
        player = trigger.nick.lower
        if player not in self.players:
            bot.say(self.strings["cant_play"] % trigger.nick)
            return
        chan = trigger.sender

        self.remove_player(bot, chan, player)
        bot.say(self.strings["quit"] % trigger.nick)

        if player == self.has_potato:
            emergency_player = list(self.players)[randint(0, len(list(self.players)))]
            bot.say(self.strings["emergency_give"] % (player, emergency_player))
            self.give(bot, player, emergency_player, emergency=True)

    def reset(self, bot, chan):
        for player in self.players:
            self.players[player]["turns_alive"] += 1
            self.players[player]["giver"] = None

        if len(self.players) == 2:  # the game ends when there are 2 players left
            plwin1, plwin2 = list(self.players)[0], list(self.players)[1]
            stats = self.players[plwin1]["turns_alive"]
            bot.say(self.strings["congrats_win"] % (plwin1, plwin2, stats))
            potato.stop(bot, chan, forced=False)
            return

        bot.say(self.strings["new_turn"])
        self.canpass = True
        self.timecounter = 0
        self.has_potato = list(self.players)[randint(0, len(list(self.players)) - 1)]
        bot.say(self.strings["potato_given"] % self.has_potato)
        self.timer_function(bot, randint(10, 100))

    def remove_player(self, bot, chan, player):
        stat = self.players[player]["turns_alive"]  # removed players get their stats updated
        potato.update_stats(bot, player, stat)
        self.players.pop(player)
        # self.playerlist.remove(player)
        bot.write(['MODE', chan, '-v', player])


class PotatoBot:
    def __init__(self):
        self.games = {}
        self.strings = strings[LANGUAGE]

    def start(self, bot, trigger):
        if trigger.sender in self.games:
            self.join(bot, trigger)
        else:
            self.games[trigger.sender] = PotatoGame(trigger)
            bot.say(self.strings["game_started"])
            bot.say(f"{POTATO} : match STARTED in {trigger.sender} by {trigger.nick}",
                    LOG_CHAN)  # happy? f strings \(^^)/
            self.join(bot, trigger)
            bot.write(['MODE', trigger.sender, '+N'])  # While playing, nicks cannot be changed.

    def join(self, bot, trigger):
        if trigger.sender in self.games:
            self.games[trigger.sender].join(bot, trigger)

    def stop(self, bot, channel, forced=False):
        if channel not in self.games:
            bot.notice(self.strings["not_started"])
            return
        game = self.games[channel]
        game.stop_game = True
        if forced:
            bot.say(self.strings["admin_stop"])
            bot.say(f"{POTATO} : match forcefully STOPPED in {channel}", LOG_CHAN)
        elif not game.started:
            bot.say(self.strings["quit_ok"])

        for player in game.players:
            bot.write(['MODE', channel, '-v', player])
            stat = game.players[player]["turns_alive"]
            self.update_stats(bot, player, stat)

        bot.write(['MODE', channel, '-N'])
        del self.games[channel]

    def update_stats(self, bot, player, stat):
        stats = bot.db.get_nick_value("hot_potato", player, default=0)
        stats += stat
        bot.db.set_nick_value("hot_potato", player, stats)
        bot.say(f"{POTATO} : stats of {player} updated successfully.", LOG_CHAN)

    def quit(self, bot, trigger):
        if trigger.sender in self.games:
            game = self.games[trigger.sender]
            game.quit(bot, trigger)

            if len(game.players) == 0:
                self.stop(bot, trigger.sender)

    def deal(self, bot, trigger):
        if trigger.sender not in self.games:
            return
        self.games[trigger.sender].deal(bot, trigger)

    def who(self, bot, trigger):
        if trigger.sender not in self.games:
            return
        self.games[trigger.sender].who(bot, trigger)

    def give(self, bot, trigger):
        if trigger.sender not in self.games:
            return
        try:
            receiver = trigger.group(3).lower()
            print(receiver)
        except:
            bot.say(self.strings["receiver_missing"])
            return

        self.games[trigger.sender].give(bot, trigger.nick.lower(), receiver)


potato = PotatoBot()


@thread(True)
@commands("potato", "pot", "hot potato")
def start(bot, trigger):
    if trigger.sender in GAME_CHAN:
        potato.start(bot, trigger)


@commands("adstop potato")
@priority("high")
def stop(bot, trigger):
    if trigger.sender in GAME_CHAN and trigger.account in HOTPOT_ADMINS:
        potato.stop(bot, trigger.sender, forced=True)


@commands("join", "jo")
def join(bot, trigger):
    if trigger.sender in GAME_CHAN:
        potato.join(bot, trigger)


@commands("quit", "qu")
def quit(bot, trigger):
    if trigger.sender in GAME_CHAN:
        potato.quit(bot, trigger)


@commands('deal', "de")
def deal(bot, trigger):
    if trigger.sender in GAME_CHAN:
        potato.deal(bot, trigger)


@commands("give", "pass", "pa", "gi")
def give(bot, trigger):
    if trigger.sender in GAME_CHAN:
        potato.give(bot, trigger)


@commands("help")
def help(bot, trigger):
    if trigger.group(2).lower() in ["potato", "hot_potato", "hot potato", "hotpot"]:
        if trigger.sender in GAME_CHAN:
            bot.notice(f"GUIDA: {help_[LANGUAGE]}")  # just swap with the right dict when translating.


@commands("potgames", "pg")
def potgames(bot, trigger):
    if trigger.account in HOTPOT_ADMINS and trigger.sender == LOG_CHAN:
        chans = []
        active = 0
        pending = 0
        for chan, game in potato.games.items():
            if game.started:
                chans.append(chan)
                active += 1
            else:
                chans.append(chan + " (pending)")
                pending += 1
        if not len(chans):
            bot.say(f'No {POTATO} games in progress {trigger.nick}')
            return
        g_active = "channel" if active == 1 else "channels"
        g_pending = "channel" if pending == 1 else "channels"
        chanlist = ", ".join(chans[:-2] + [" and ".join(chans[-2:])])
        bot.reply(
            f"{POTATO} is pending deal in {pending} {g_pending} and in progress in {active} {g_active}: {chanlist}.")


@commands("potatostats", "ps")
def stats(bot, trigger):
    stats = bot.db.get_nick_value("hot_potato", trigger.nick.lower(), default=0)
    bot.notice(POTATO + "STATS: Turns Alive: " + str(stats), trigger.nick)
    bot.say(f"{POTATO}: {trigger.nick} requested their STATS.", LOG_CHAN)


@commands("adpotatostats", "adps")
def admin_stats(bot, trigger):
    if trigger.account in HOTPOT_ADMINS:
        try:
            stats = bot.db.get_nick_value("hot_potato", trigger.group(3), default=0)
        except:
            bot.reply("Specify a nick to search.")
            return
        bot.notice(f"{POTATO} STATS of {trigger.group(3)}: Turns Alive: {stats}", trigger.nick)
        bot.say(f"{POTATO}: {trigger.nick} requested the STATS of {trigger.group(3)}.", LOG_CHAN)


@commands("who")
def who(bot, trigger):
    if trigger.sender in GAME_CHAN:
        potato.who(bot, trigger)


@event("PART")
def part(bot, trigger):
    if trigger.sender in GAME_CHAN:
        potato.quit(bot, trigger)


@event("QUIT")
def quit_(bot, trigger):
    if trigger.sender in GAME_CHAN:
        potato.quit(bot, trigger)
