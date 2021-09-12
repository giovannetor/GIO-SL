"""
Woggle - bot framework

  Copyright (C) 2021 Giovanni Coci gio@scoutlink.net

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

import random
import threading
from datetime import datetime
from pprint import pprint
from time import  sleep
import sopel.plugin as module
import sopel.tools as tools
from sopel import config
from sopel.formatting import colors, CONTROL_BOLD, CONTROL_COLOR, CONTROL_NORMAL

settings = config.Config('/Users/giova/.sopel/default.cfg')  # replace with the config path

from sopel.config.types import StaticSection, ListAttribute, ValidatedAttribute

game_chan = None

NO = False
YES = True
WIN = True


# Called when the module gets loaded
def setup(bot):
    bot.config.define_section("ElementalAdventure", ElementalAdventureConfigSection)

    # Set the allowed game channels
    global game_chan
    global log_chan
    global elad_admins
    game_chan = bot.config.ElementalAdventure.gamechannels
    log_chan = bot.config.ElementalAdventure.logchannels
    elad_admins = bot.config.ElementalAdventure.elad_admins


# Called when the module gets configured
def configure(config):
    config.define_section("ElementalAdventure", ElementalAdventureConfigSection)
    config.ElementalAdventure.configure_setting("gamechannels",
                                                "In what channels is Elemental Adventure allowed to be played? (One per line)")
    config.ElementalAdventure.configure_setting("logchannels",
                                                "In what channel will Elemental Adventure send logs? (Choose one)")
    config.ElementalAdventure.configure_setting("elad_admins", "What accounts can operate on ElAd? (One per line)")


# Class with the settings for Elemental Adventure
class ElementalAdventureConfigSection(StaticSection):
    gamechannels = ListAttribute("gamechannels")
    logchannels = ValidatedAttribute("logchannels")
    elad_admins = ListAttribute("elad_admins")


ELEMENTAL = CONTROL_BOLD + CONTROL_COLOR + colors.BLACK + "," + colors.WHITE + " Elemental Adventure " + CONTROL_NORMAL
FIRE = CONTROL_BOLD + CONTROL_COLOR + colors.BLACK + "," + colors.RED
EARTH = CONTROL_BOLD + CONTROL_COLOR + colors.WHITE + "," + colors.GREEN
WATER = CONTROL_BOLD + CONTROL_COLOR + colors.WHITE + "," + colors.LIGHT_BLUE
AIR = CONTROL_BOLD + CONTROL_COLOR + colors.CYAN + "," + colors.WHITE

hand_size = 3

min_player = 2
max_player = 4

lock = threading.RLock()

string_help_ita = "https://webchat.duckie.chat/uploads/c42504e4eb0c2815/paste.txt "

string_help_eng = "https://webchat.duckie.chat/uploads/911a1a599b7ef006/paste.txt "

rules_ita = "https://webchat.duckie.chat/uploads/f3add99186e1c77c/paste.txt  "

rules_eng = "https://webchat.duckie.chat/uploads/2ab66fbf957ab02d/paste.txt "

strings_eng = {"nuovo_player": " %s joins the match as player: %s .",
               "impos_unirsi": "I'm sorry %s , the max number of players is 4. Wait until next match :)",
               "gia_dentro": " %s you are already inside the match of " + ELEMENTAL,
               "pronti": "Enough players, ready to start! Use .deal to begin.",
               "player_quit": " %s abandoned the match of " + ELEMENTAL + " .",
               "non_abbastanza": "Can't play alone, wait for someone else...",
               "iniziato": "Match already started.",
               "cant_play": "You are not inside the match, please wait for the next one.",
               "turno": " %s 's turn.",
               "non_hai": "%s you don't have this card: %s",
               "tue_carte": "Your cards: %s",
               "mano_win": CONTROL_BOLD + " %s  wins the hand!",
               "prossimo": CONTROL_BOLD + "ON TURN: ",
               "game_started": ELEMENTAL + " started. use .join to join .",
               "not_started": "Match not started yet.",
               "game_stopped": CONTROL_BOLD + "GAME OVER.",
               "admin_stop": CONTROL_BOLD + "AN ADMIN TERMINATED THE MATCH FROM REMOTE.",
               "cant_continue": "a player left the game. The other team wins!!",
               "win": "The winner team is made of %s   !!!. Play time: %s",
               "on_table": " %s's turn. Cards on table: %s  ",
               'SB_PLAYER': "%s (%d %s)",
               "bonus": "Enhanced Element %s",
               "cant_move": "Only an admin can move the match. ",
               'NEED_CHANNEL': "I need a channel name to move to.",
               'NOT_IN_CHANNEL': "I'm not in %s, so I can't move the game there.",
               'CHANNEL_IN_USE': "Channel %s already has a " + ELEMENTAL + " game in progress.",
               'MOVED_FROM': "Note: %s moved an " + ELEMENTAL + " game here from %s.",
               'GAME_MOVED': "%s " + ELEMENTAL + " game moved to %s.",
               "lan_done": "Succesfully changed " + ELEMENTAL + "language to %s .",
               "not_admin": "Only an admin can change this setting.",
               "joined": " %s joined the TEAM %s .",
               "team_comp": "Teams formed by:    TEAM 1: %s  *** TEAM 2: %s",
               "not_3": "The number of players can be 2 or 4, NOT 3. please wait for another player, or leave :)",
               "last_turn": "LAST TURN!! Play wisely your last 3 cards!!",
               "quit_win": "The player %s left the match. WINNER: %s .",
               "quit_ok": "The player %s left the match. Match has to be started again.",
               "change_time": CONTROL_BOLD + "TIME TO SWAP!! You have 10 seconds to see the cards of your  mate.",
               "change_cards": "Your mate's cards: %s",
               "team_earn": "TEAM %s earns  | %s |  reputation!",
               "player_list": "TEAM 1 : %s    TEAM 2 : %s",
               "local_stop": CONTROL_BOLD + "AN ADMIN STOPPED THE MATCH",
               "quit_warn": "If you leave the match, the opposite team will win. Use .quit to confirm. ",
               "idle_kick": "Player %s had been IDLE for 1 MINUTE. Going to be kicked from the match.",
               "idle_warn1": " %s your turn! Idle for: 15s",
               "idle_warn2": " %s your turn. Being Idle for more than 60 seconds will result in a kick. Idle for : 30s",
               "idle_warn3": " %s you here??? Do something or you'll be kicked in 15 secondi! Idle for: 45s",
               "idle_end": "Match terminated for inactivity."
               }
strings_ita = {"nuovo_player": " %s si unisce alla partita di " + ELEMENTAL + "  come giocatore: %s .",
               "impos_unirsi": "Mi spiace %s , il numero massimo di giocatori è 4. Aspetta l'inizio della prossima partita :)",
               "gia_dentro": " %s sei già dentro la partita di " + ELEMENTAL,
               "pronti": "Siamo abbastanza, pronti a partireeeee! Usa .deal per iniziare.",
               "player_quit": " %s ha abbandonato la partita di " + ELEMENTAL + " .",
               "non_abbastanza": "Non puoi giocare da solo, aspetta qualcun altro...",
               "iniziato": "La partita non è iniziata.",
               "cant_play": "Non sei dentro la partita, per favore non disturbare gli altri giocatori :)",
               "turno": "Turno di %s.",
               "non_hai": "%s non hai questa carta: %s",
               "tue_carte": "Le tue carte: : %s",
               "mano_win": " %s  vince il turno!",
               "prossimo": "E' il turno di: ",
               "game_started": ELEMENTAL + " iniziata. Usa .join per unirti .",
               "not_started": "La partita non è ancora iniziata.",
               "game_stopped": "GAME OVER.",
               "admin_stop": "Un admin ha forzatamente terminato la partita di " + ELEMENTAL + ".",
               "cant_continue": "Un giocatore ha lasciato la partita. Vince il team avversario!!",
               "win": "Il team vincitore è composto da: %s !!!. Tempo di gioco: %s",
               "on_table": " Turno di: %s.  Carte sul tavolo: %s  ",
               'SB_PLAYER': "%s (%d %s)",
               "bonus": ELEMENTAL + " : %s",
               "cant_move": "Solo un admin può muovere la partita. ",
               'NEED_CHANNEL': "Ok ma...dimmi dove andare.",
               'NOT_IN_CHANNEL': "Non sono dentro %s, quindi non posso muovere la partita là.",
               'CHANNEL_IN_USE': "Il canale %s ha già una partita di " + ELEMENTAL + " in corso.",
               'MOVED_FROM': "ATTENZIONE: %s ha mosso una partita di " + ELEMENTAL + " qui da %s.",
               'GAME_MOVED': "%s partita di " + ELEMENTAL + " mossa in %s.",
               "lan_done": "La lingua di " + ELEMENTAL + " è stata correttamente cambiata in %s .",
               "not_admin": "NON SEI UN ADMIN. VADE RETRO.",
               "joined": " %s si è unito al TEAM %s .",
               "team_comp": "I team sono formati da: TEAM 1: %s  *** TEAM 2: %s",
               "not_3": "Il numero di giocatori deve essere 2 o 4, NON 3. Per favore attendi un altro giocatore, o abbandona :)",
               "last_turn": "ULTIMO TURNO!! Gioca con saggezza le tue ultime 3 carte!!",
               "quit_win": "Il giocatore %s ha lasciato la partita. VINCITORE: %s .",
               "quit_ok": "Il giocatore %s ha lasciato la partita. La partita deve essere avviata di nuovo.",
               "change_time": CONTROL_BOLD + "ULTIMO TURNO!!! Hai 10 secondi di tempo per vedere le carte del compagno.",
               "change_cards": "Carte del tuo compagno: %s",
               "team_earn": "Il TEAM %s guadagna  | %s |  punti!",
               "player_list": "TEAM 1 : %s    TEAM 2 : %s",
               "local_stop": CONTROL_BOLD + "UN ADMIN HA FERMATO LA PARTITA",
               "quit_warn": "Se abbandoni, il team avversario vincerà. Usa .quit per confermare.",
               "idle_kick": "Il giocatore %s è stato IDLE per 1 MINUTO. Verrà rimosso dalla partita.",
               "idle_warn1": " %s è il tuo turno! Idle da: 15s",
               "idle_warn2": " %s è il tuo turno. Restare idle per più di 60 secondi causerà un kick. Idle da : 30s",
               "idle_warn3": " %s ci sei??? Fai qualcosa o sarai buttato fuori tra 15 secondi! Idle da: 45s",
               "idle_end": "Partita terminata per inattività."
               }

strings = strings_eng
rules = rules_eng
string_help = string_help_eng

elements = {"Fire": FIRE, "Earth": EARTH, "Air": AIR, "Water": WATER}

seedsstandard = ["M", "O", "C", "S"]

cards = {"1": {"id": 1, "name": "Giant", "atk": 13, "rep": 11, "seed": None, "seedstr": None, "owner": None},
         "2": {"id": 2, "name": "Minion", "atk": 2, "rep": 0, "seed": None, "seedstr": None, "owner": None},
         "3": {"id": 3, "name": "Dragon", "atk": 10, "rep": 10, "seed": None, "seedstr": None, "owner": None},
         "4": {"id": 4, "name": "Paladin", "atk": 4, "rep": 0, "seed": None, "seedstr": None, "owner": None},
         "5": {"id": 5, "name": "Mermaid", "atk": 5, "rep": 0, "seed": None, "seedstr": None, "owner": None},
         "6": {"id": 6, "name": "Elemental", "atk": 6, "rep": 0, "seed": None, "seedstr": None, "owner": None},
         "7": {"id": 7, "name": "Dwarf", "atk": 7, "rep": 0, "seed": None, "seedstr": None, "owner": None},
         "8": {"id": 8, "name": "Fairy", "atk": 8, "rep": 2, "seed": None, "seedstr": None, "owner": None},
         "9": {"id": 9, "name": "Sage", "atk": 9, "rep": 3, "seed": None, "seedstr": None, "owner": None},
         "0": {"id": 0, "name": "King", "atk": 10, "rep": 4, "seed": None, "seedstr": None, "owner": None}}


class ElAdGame:
    def __init__(self, trigger):
        self.strings = strings_ita
        self.string_help = string_help_ita
        self.rules = rules_ita
        self.starter = trigger.nick
        self.channel = trigger.sender
        self.deck = []
        self.players = {self.starter: {"cards": {}, "idletime": 0}}  # player's dict. each player will have a card list
        self.playerOrder = [self.starter]  # player order. it will mostly be used paired with self.currentPlayer
        self.currentPlayer = 0
        self.previousPlayer = None
        self.way = 1
        self.deck = []
        self.startTime = None
        self.dealt = False
        self.turncounter = 0  # turn counter
        self.ontable = []
        self.team1 = []  # team1 and team2 holds the team's members and each team's score with this format V
        self.team2 = []  # team1 = [player 1 , (player 2) , score]
        self.bonus = ""
        self.lastturn = False
        self.startcont = 0
        self.tempcont = 0
        self.firstpl = 0
        self.bonus_ontable = []
        self.changecount = 0

    def idlefunc(self, bot, game):
        for player in self.players:
            if player == self.playerOrder[self.currentPlayer]:
                self.players[player]["idletime"] += 1
        self.idlepenalty(bot, game)

    def idlepenalty(self, bot, game):
        for player in self.players:
            if self.players[player]["idletime"] == 30:
                bot.say(self.strings["idle_warn2"] % player, game)
            if self.players[player]["idletime"] == 45:
                bot.say(self.strings["idle_warn3"] % player, game)
            if self.players[player]["idletime"] == 60:
                bot.say(self.strings["idle_kick"] % player, game)
                if player in self.team1:
                    self.team2.append("WIN")
                else:
                    self.team1.append("WIN")
                return WIN

    def join(self, bot, trigger):
        if self.startcont == 0:
            self.team1.append(self.starter)
            bot.write(['MODE', trigger.sender, '+v', self.starter])
            self.startcont += 1
        with lock:
            if trigger.nick not in self.players:  # if the player is not in the game
                if len(self.players) == max_player:
                    bot.say(self.strings["impos_unirsi"] % trigger.nick)  # match full
                    return
                if self.dealt:
                    bot.say(self.strings["cant_play"])
                    return
                bot.write(['MODE', trigger.sender, '+v', trigger.nick])
                self.players[trigger.nick] = {"cards": {}, "idletime": 0}  # add player to players dict
                self.playerOrder.append(trigger.nick)  # add player to players order list

                if len(self.team2) < len(
                        self.team1):  # forms the teams (always have 2 teams. can't play in 3. team members = 1 or 2 each)
                    self.team2.append(
                        trigger.nick)  # a 3 player version exists, slightly different rules, maybe in the future
                    bot.say(self.strings["joined"] % (trigger.nick, "2"))
                elif len(self.team2) > len(self.team1):
                    self.team1.append(trigger.nick)
                    bot.say(self.strings["joined"] % (trigger.nick, "1"))
                else:
                    self.team1.append(trigger.nick)
                    bot.say(self.strings["joined"] % (trigger.nick, "1"))

                bot.say(self.strings['nuovo_player'] % (
                    trigger.nick, str(self.playerOrder.index(trigger.nick) + 1
                                      )))
                if len(self.players) > 1:
                    bot.say(self.strings['pronti'])  # at least 2 players, ready to deal
                str1 = ""
                str2 = ""
                for i in self.team1:
                    str1 += i + " "
                for h in self.team2:
                    str2 += h + " "
                bot.say(self.strings["team_comp"] % (str1, str2))
                self.startcont += 1
            else:
                bot.say(self.strings["gia_dentro"] % trigger.nick)  # player already in

    def quit(self, bot, trigger,
             idle=False):  # remove the player from the team. the other team wins. (need to add: if game not dealt, no one loses)
        if not idle:
            player = trigger.nick
            if player not in self.players:
                return
            with lock:
                bot.say(strings['player_quit'] % player)
                return #self.remove_player(bot, player)
        elif idle:
            return #self.remove_player(bot, trigger)

    def deal(self, bot, trigger):  # deal the game. everyone in the game can do it, owner not required.
        if trigger.nick not in self.players:
            bot.say(self.strings["cant_play"])
            return
        if len(self.players) < 2:
            bot.say(self.strings['non_abbastanza'])
            return
        if len(self.players) == 3:  # as said before, can't play in 3
            bot.say(self.strings["not_3"])
            return
        if len(self.deck):
            bot.say(self.strings['iniziato'])  # means the match is already going on, return
            return
        with lock:
            self.team1.append(
                0)  # once the teams are defined, appends a 0 in the -1 position. it'll be used to count the points each turn.
            self.team2.append(0)
            self.startTime = datetime.now()
            self.deck = self.create_deck()  # create the deck (check the function)
            self.bonus = random.choice(list(
                elements.keys()))  # make a "bonus" recognizable for the _render_coloured_cards method. e.g. bonus: "4M*"
            # adds the bonus to the bonus list. ONLY ONE CARD will be here, that will decide the seed of the bonus
            for player_list in self.players:
                while len(self.players[player_list]["cards"]) < 3:
                    card = self.get_card(bot)
                    self.players[player_list]["cards"][card[
                        "id"]] = card  # gives 3 cards to each player. sometimes it gets bugged, no idea why, and gives less cards
                for card_id in self.players[player_list]["cards"]:
                    self.players[player_list]["cards"][card_id]["owner"] = player_list
            self.dealt = YES
            self.currentPlayer = random.randrange(len(self.players))
            # il primo giocatore è scelto a caso
            self.show_on_turn(bot)

            if len(self.bonus) == 0:
                self.bonus = self.get_card(bot)
            for player in self.players:
                self.players[player]["idletime"] = 0
            bot.say("[" + ELEMENTAL + "] : DEAL in " + trigger.sender, log_chan)

    def play(self, bot, trigger):
        if trigger.nick not in self.players:
            bot.notice(self.strings['cant_play'], trigger.nick)
            return
        if trigger.nick != self.playerOrder[self.currentPlayer]:
            bot.say(self.strings['turno'] % self.playerOrder[self.currentPlayer])
            return
        self.players[self.playerOrder[self.currentPlayer]]["idletime"] = 0
        id = trigger.group(3)
        with lock:
            # this decides the INDEX of the current player in the self.playerOder LIST. giocatore = player (translation tip)
            if id not in self.players[trigger.nick]["cards"]:
                bot.notice(self.strings['non_hai'] % (id, trigger.nick), trigger.nick)
                return
            card = self.players[trigger.nick]["cards"][id]
            self.ontable.append(
                card)  # append the card ("4C giovannetor" format) to the "ontable" list. this list is temporary, gets emptied each full turn
            self.players[trigger.nick]["cards"].pop(
                id)  # removes from the player's card list the card in the "4C" format
            self.inc_player(bot, trigger)  # increase the player.
            self.show_on_turn(bot)  # shows who's the turn now

    def decidepoint(self, bot):  # decides who earns the point of the turn. THIS IS WHAT CREATES MOST OF THE PROBLEMS
        self.bonus_ontable.clear()  # creates a list of BRISCOLA on table (temporary, get emptied at the end)
        carcom = self.ontable[
            0]  # the first card in the self.ontable is the "command card". to win a turn, the other cards must have same seed and > number, OR be a bonus
        # bonus always wins. if there are more bonus, the highest wins

        for c in range(1,
                       len(self.ontable)):  # analyzes the cards in the .ontable one by one. if one of the same seed
            # has number > carcom, it becomes the new carcom
            card_sfid = self.ontable[c]  # c is just an index
            if card_sfid["seedstr"] == carcom["seedstr"]:
                if card_sfid["atk"] > carcom["atk"]:
                    carcom = card_sfid  # important! cards on the table have different value than when counted as points. ***
            elif card_sfid["seedstr"] == self.bonus:  # if he finds a bonus, he adds it in the bris_ontable list
                self.bonus_ontable.append(card_sfid)

        if len(self.bonus_ontable) > 1:  # if there are more than 1 bonus, it compares them and choose the highest
            carcom = self.bonus_ontable[0]
            for numero in range(1, len(self.bonus_ontable)):
                carsfid = self.bonus_ontable[
                    numero]  # ***e.g.  10 = 10 on table, but = 4 as point. 7 = 7 on table, but = 0 as point.
                if carsfid["atk"] > carcom[
                    "atk"]:  # 1 = 11 on table, and = 11 as point   (these are not errors, it's how the game is XD)
                    carcom = carsfid

            cardwin = carcom
        elif len(self.bonus_ontable) == 1:
            cardwin = self.bonus_ontable[0]
        else:
            cardwin = carcom  # if there are no bonus, the highest normal card wins
        plwin = cardwin[
            "owner"]  # remember that the cards are in the format "4C giovannetor". bonus are in the format "5M* Mina". the "*" for all the bonus gets
        # added in the self.getcard(), and it's only used to render the colours
        return plwin  # <-- this is the main problem. This should be a nick, but it's a NoneType, which makes the whole program crash (or i think this is the problem)

    def givepoint(self, bot,
                  plwin):  # the past funcion decided WHO earned the points. this one decides how many points the team earns. it takes the "plwin" from the part function
        punti1prima = self.team1[-1]
        punti2prima = self.team2[-1]
        if plwin in self.team1:  # if player in team 1
            for card_dict in self.ontable:  # for card in the .ontable list (not yet emptied)
                numero = card_dict["rep"]  # takes the number of the card (remember, format "9S giovannetor"
                self.team1[-1] += int(
                    numero)  # the dict valori contains the point value of cards. remeber that the team1 list has an empty int at the end.
            bot.say(self.strings["team_earn"] % ("1", str(self.team1[-1] - punti1prima)))

        else:
            for card_dict in self.ontable:
                numero = card_dict["rep"]
                self.team2[-1] += int(numero)
            bot.say(self.strings["team_earn"] % ("2", str(self.team2[-1] - punti2prima)))

    def show_on_turn(self, bot):  # shows the cards atm on the table.
        with lock:
            giocatore = self.playerOrder[self.currentPlayer]
            bot.say(self.strings['on_table'] % (giocatore, self._render_list_cards(self.ontable)))
            self.send_cards(bot, self.playerOrder[self.currentPlayer])
        # self.send_next(bot)

    def send_cards(self, bot, trigger):  # shows the cards in your hand, and the match's bonus card
        with lock:
            if not self.startTime:
                bot.notice(self.strings['not_started'], trigger.nick)
                return
            if trigger not in self.players:
                bot.notice(self.strings['cant_play'], trigger.nick)
                return
            self.players[trigger]["idletime"] = 0
            cards = []
            bonus = self.bonus
            for i in self.players[trigger]["cards"]:
                cards.append(i)

                # trova le carte nel dizionario, renderizzate sotto V
            bot.notice("=========================================", trigger)
            bot.notice(self.strings['tue_carte'] % (str(self._render_colored_cards(self.players[trigger]["cards"]))),
                       trigger)
            bot.notice(self.strings["bonus"] % (str(self._render_bonus(bonus))), trigger)
            bot.notice("=========================================", trigger)
            # importante! le info personali vanno mandate come notifica, non con .say

    def inc_player(self, bot, trigger):  # actually send the next player to play
        with lock:

            if len(self.players) == 2:  # important part!! a turn consist of each player paying a card, then counting who wins the turn, then starting another turn till the
                if len(self.ontable) == 2:  # cards in the deck are done. i used self.turncounter == 2, but for some reason it triggered at 1st turn instead of 2nd
                    # this piece is for 2 player match. later there's the 4 players module

                    self.currentPlayer = self.playerOrder.index(self.decidepoint(bot))
                    self.givepoint(bot, self.playerOrder[
                        self.currentPlayer])  # adds the points to the team of the winner decided by .decidepoint

                    self.ontable.clear()
                    if len(self.deck) != 0:
                        for player_list in self.players:
                            while len(self.players[player_list]["cards"]) < 3:
                                card = self.get_card(bot)
                                self.players[player_list]["cards"][card[
                                    "id"]] = card  # gives 3 cards to each player. sometimes it gets bugged, no idea why, and gives less cards
                            for card_id in self.players[player_list]["cards"]:
                                self.players[player_list]["cards"][card_id]["owner"] = player_list

                    if self.team1[-1] + self.team2[-1] == 120:
                        if self.team1[-1] > self.team2[-1]:
                            self.team1.append("WIN")  # adds the string "WIN" to the team's list.
                            return WIN  # return win and stops the game
                        elif self.team1[-1] < self.team2[-1]:
                            self.team2.append("WIN")
                            return WIN
                        else:
                            self.team1.append("DRAW")
                            self.team2.append("DRAW")
                            return WIN

                else:
                    self.previousPlayer = self.currentPlayer  # if not all the players have played a card, the turn goes on as normal.
                    self.currentPlayer += 1
                if self.currentPlayer >= len(self.players):
                    self.currentPlayer = 0

            if len(self.players) == 4:  # important part!! a turn consist of each player paying a card, then counting who wins the turn, then starting another turn till the
                if len(self.ontable) == 4:  # cards in the deck are done. i used self.turncounter == 2, but for some reason it triggered at 1st turn instead of 2nd
                    # this piece is for 2 player match. later there's the 4 players module

                    self.currentPlayer = self.playerOrder.index(
                        self.decidepoint(bot))  # PROBLEM! .currentPlayer shall be an index, but it's NoneType.
                    # game rule i forgot to explain: who wins the turn, is the first one to start and draw the next one
                    # at the end of each turn, all the players draw a card. always 3 cards in the hand, no more, no less
                    # except for the last 3 turns.
                    self.givepoint(bot, self.playerOrder[
                        self.currentPlayer])  # adds the points to the team of the winner decided by .decidepoint
                    bot.say(self.strings["mano_win"] % (self.playerOrder[self.currentPlayer]))
                    self.ontable.clear()
                    if len(self.deck) != 0:
                        for player_list in self.players:
                            while len(self.players[player_list]["cards"]) < 3:
                                card = self.get_card(bot)
                                self.players[player_list]["cards"][card[
                                    "id"]] = card  # gives 3 cards to each player. sometimes it gets bugged, no idea why, and gives less cards
                            for card_id in self.players[player_list]["cards"]:
                                self.players[player_list]["cards"][card_id]["owner"] = player_list

                    if self.lastturn and self.changecount == 0:
                        bot.say(strings["change_time"])
                        bot.notice(strings["change_cards"] % (
                            self._render_colored_cards(self.players[self.team1[0]]["cards"])),
                                   self.team1[1])
                        bot.notice(strings["change_cards"] % (
                            self._render_colored_cards(self.players[self.team1[1]]["cards"])),
                                   self.team1[0])
                        bot.notice(strings["change_cards"] % (
                            self._render_colored_cards(self.players[self.team2[0]]["cards"])),
                                   self.team2[1])
                        bot.notice(strings["change_cards"] % (
                            self._render_colored_cards(self.players[self.team2[1]]["cards"])),
                                   self.team2[0])
                        sleep(15)
                        self.changecount += 1

                    if self.team1[-1] + self.team2[-1] == 120:
                        if self.team1[-1] > self.team2[-1]:
                            self.team1.append("WIN")  # adds the string "WIN" to the team's list.
                            return WIN  # return win and stops the game
                        elif self.team1[-1] < self.team2[-1]:
                            self.team2.append("WIN")
                            return WIN
                        else:
                            self.team1.append("DRAW")
                            self.team2.append("DRAW")
                            return WIN

                else:
                    self.previousPlayer = self.currentPlayer
                    self.currentPlayer += 1
                if self.currentPlayer >= len(self.players):
                    self.currentPlayer = 0
        self.players[self.playerOrder[self.currentPlayer]]["idletime"] = 0

    def get_player(self):
        if "WIN" in self.team1 or "WIN" in self.team2 or "DRAW" in self.team1:

            return True
        else:
            return False

    def render_counts(self, full=NO):
        with lock:
            if full:
                stop = len(self.players)
                inc = abs(self.way)
                plr = 0
            else:
                stop = self.currentPlayer
                inc = self.way
                plr = stop + inc
                if plr == len(self.players):
                    plr = 0
                if plr < 0:
                    plr = len(self.players) - 1
            arr = []
            while plr != stop:
                cards = len(self.players[self.playerOrder[plr]]["cards"])
                g_cards = "carta" if cards == 1 else "carte"
                arr.append(self.strings['SB_PLAYER'] % (self.playerOrder[plr], cards, g_cards))
                plr += inc
                if plr == len(self.players) and not full:
                    plr = 0
                if plr < 0:
                    plr = len(self.players) - 1
        return ' - '.join(arr)

    def game_moved(self, bot, who, oldchan, newchan):
        with lock:
            self.channel = newchan
            bot.msg(self.channel, self.strings['MOVED_FROM'] % (who, oldchan))
            for player in self.players:
                bot.notice(self.strings['GAME_MOVED'] % (oldchan, newchan), player)
            bot.msg(oldchan, self.strings['GAME_MOVED'] % (oldchan, newchan))

    @staticmethod
    def _render_bonus(bonus):
        ret = elements[bonus] + " " + bonus + " " + CONTROL_NORMAL
        return ret

    def _render_list_cards(self, cards):
        with lock:
            ret = []
            for card in cards:
                CARTA = card
                if CARTA["seedstr"] == self.bonus:  # distingue le briscole per seme. DA OTTIMIZZARE
                    ret.append(CARTA["seed"] + " ** [%s] %s %s |⚔ %s|✪ %s| ** " % (
                        CARTA["id"], CARTA["seedstr"], CARTA["name"], str(CARTA["atk"]),
                        str(CARTA["rep"])) + CONTROL_NORMAL + "  ")
                else:
                    ret.append(CARTA["seed"] + " [%s] %s %s |⚔ %s|✪ %s| " % (
                        CARTA["id"], CARTA["seedstr"], CARTA["name"], str(CARTA["atk"]),
                        str(CARTA["rep"])) + CONTROL_NORMAL + "  ")

        return ''.join(ret) + CONTROL_NORMAL

    def _render_colored_cards(self, cards):  # renderizza colori carte

        with lock:
            ret = []
            for card in cards:
                CARTA = cards[card]
                if CARTA["seedstr"] == self.bonus:  # distingue le briscole per seme. DA OTTIMIZZARE
                    ret.append(CARTA["seed"] + " ** [%s] %s %s |⚔ %s|✪ %s| ** " % (
                        CARTA["id"], CARTA["seedstr"], CARTA["name"], str(CARTA["atk"]),
                        str(CARTA["rep"])) + CONTROL_NORMAL + "  ")
                else:
                    ret.append(CARTA["seed"] + " [%s] %s %s |⚔ %s|✪ %s| " % (
                        CARTA["id"], CARTA["seedstr"], CARTA["name"], str(CARTA["atk"]),
                        str(CARTA["rep"])) + CONTROL_NORMAL + "  ")

        return ''.join(ret) + CONTROL_NORMAL

    def get_card(self, bot):

        with lock:
            if not self.deck:
                self.deck = self.create_deck()
            key = random.choice(list(self.deck.keys()))
            ret = self.deck.pop(str(key))
            if len(self.players) == 2:
                if len(self.deck) == 0:
                    bot.say(self.strings["last_turn"])
                    self.lastturn = True
            if len(self.players) == 4:
                if len(self.deck) == 0:
                    bot.say(self.strings["last_turn"])
                    self.lastturn = True
        print(ret)
        return ret

    def create_deck(self):
        new_deck = {}
        id = 1
        for element in elements:
            for card in cards:
                new_deck[str(id)] = {}
                new_deck[str(id)]["id"] = str(id)
                new_deck[str(id)]["name"] = cards[card]["name"]
                new_deck[str(id)]["atk"] = cards[card]["atk"]
                new_deck[str(id)]["rep"] = cards[card]["rep"]
                new_deck[str(id)]["seed"] = elements[element]
                new_deck[str(id)]["seedstr"] = element
                id += 1
        print(new_deck)
        return new_deck

    def teams(self, bot, trigger):
        bot.notice(self.strings["player_list"] % (str(self.team1[-1]), str(self.team2[-1])), trigger.nick)


class ElAdBot:
    def __init__(self):  # ,scorefile
        # self.afkcounter = 0
        self.contatore = 0
        self.games = {}
        self.win = False
        self.draw = False
        self.strings = strings_ita

        # self.scoreFile = scorefile

    def checkidle(self, bot):

        for game in self.games:
            if self.games[game].get_player():
                self.play(bot, game, stop=True, idle=True)

    def afktime(self, bot):
        for game in self.games:
            self.games[game].idlefunc(bot, game)

    def language(self, bot, trigger):
        try:
            self.games[trigger.sender]
        except:
            bot.say("Need to start the game first.")
            return
        game = self.games[trigger.sender]

        if game.dealt:
            bot.say("Can't change now.")
            return
        else:
            if trigger.group(3) == "italiano":
                game.strings = strings_ita
                self.strings = strings_ita
                game.rules = rules_ita
                game.string_help = string_help_ita
                bot.say(self.strings["lan_done"] % trigger.group(3))
            elif trigger.group(3) == "english":
                game.strings = strings_eng
                self.strings = strings_eng
                game.rules = rules_eng
                game.string_help = string_help_eng
                bot.say(self.strings["lan_done"] % trigger.group(3))

    def start(self, bot, trigger):

        if trigger.sender in self.games:
            self.join(bot, trigger)
        else:
            self.games[trigger.sender] = ElAdGame(trigger)
            bot.say(self.strings['game_started'])

    def join(self, bot, trigger):
        if trigger.sender in self.games:
            self.games[trigger.sender].join(bot, trigger)
        else:
            bot.say(self.strings['not_started'])

    def stop(self, bot, trigger, forced=False):
        chan = trigger.sender
        if chan not in self.games:
            bot.notice(self.strings['not_started'], trigger.nick)
            return
        game = self.games[chan]
        if trigger.admin or forced:
            if not forced:
                bot.say(self.strings['game_stopped'])
                if trigger.sender != chan:
                    bot.say(self.strings['admin_stop'], chan)
                else:
                    bot.say(self.strings["local_stop"], chan)

            else:
                if not game.dealt:
                    bot.say(strings["quit_ok"] % (trigger.nick))
                    del self.games[trigger.sender]
                    return
                if trigger.nick in game.team1:
                    bot.say(self.strings["quit_win"] % (trigger.nick, "TEAM 2"))
                    game.team2.append("WIN")
                    self.play(bot, trigger, stop=True)
                elif trigger.nick in game.team2:
                    bot.say(self.strings["quit_win"] % (trigger.nick, "TEAM 1"))
                    game.team1.append("WIN")
                    self.play(bot, trigger, stop=True)

            for player in game.players:
                bot.write(['MODE', trigger.sender, '-v', player])
            try:
                del self.games[chan]
            except:
                print("uh oh")
        else:
            bot.say("Can't be stopped.")

    def quit(self, bot, trigger):
        if trigger.sender in self.games:
            if self.contatore == 0:
                bot.say(self.strings["quit_warn"])
                self.contatore += 1
                return
            game = self.games[trigger.sender]

            self.contatore = 0
            self.stop(bot, trigger, forced=True)

    def deal(self, bot, trigger):
        if trigger.sender not in self.games:
            bot.say(self.strings['not_started'])
            return
        self.games[trigger.sender].deal(bot, trigger)

    def play(self, bot, trigger, stop=False, idle=False):
        self.contatore = 0
        loser = winner = punteggiowin = punteggiolose = 0
        if stop == False:
            if trigger.sender not in self.games:
                return
        if idle:
            game = self.games[trigger]
            place = trigger
        else:
            game = self.games[trigger.sender]
            place = trigger.sender
        winner = game.currentPlayer
        if stop == False:
            game.play(bot, trigger)
        if game.get_player():
            print(game.team1, game.team2)
            try:
                if "WIN" in game.team1:
                    if len(game.team1) == 3:
                        winner = str(game.team1[0])
                        loser = str(game.team2[0])
                    else:
                        winner = str(game.team1[0]) + "  " + str(game.team1[1])
                        loser = str(game.team2[0]) + "  " + str(game.team2[1])
                    self.win = True
                    punteggiowin = str(game.team1[-2])
                    punteggiolose = str(game.team2[-1])
                elif "WIN" in game.team2:
                    if len(game.team2) == 3:
                        winner = str(game.team2[0])
                        loser = str(game.team1[0])
                    else:
                        winner = str(game.team2[0]) + "  " + str(game.team2[1])
                        loser = str(game.team1[0]) + "  " + str(game.team1[1])
                    punteggiowin = str(game.team2[-2])
                    punteggiolose = str(game.team1[-1])
                    self.win = True

                elif "DRAW" in game.team1:
                    self.draw = True
            except:
                self.game_ended(bot, trigger)
                print("AFK NOT STARTED OK")
                bot.say(self.strings["idle_end"], trigger)
                return

            # winner = game.playerOrder[winner]
            game_duration = datetime.now() - game.startTime
            hours, remainder = divmod(game_duration.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            game_duration = '%.2d:%.2d:%.2d' % (hours, minutes, seconds)

            if self.win:
                try:
                    bot.say(self.strings['win'] % (winner, game_duration), trigger.sender)
                except:
                    bot.say(self.strings['win'] % (winner, game_duration), trigger)
                for playerwin in winner.split():
                    try:
                        stats = eval(bot.db.get_plugin_value("Elemental_Adventure_Stats", playerwin,
                                                             default={"score": 0, "win": 0, "tot": 0, "win_rate": 0}))
                    except:
                        stats = bot.db.get_plugin_value("Elemental_Adventure_Stats", playerwin)
                    pprint(stats)
                    score = stats["score"] + int(punteggiowin)
                    win = stats["win"] + 1
                    tot = stats["tot"] + 1
                    win_rate = round((win * 100 / tot), 2)
                    stats = {"score": score, "win": win, "tot": tot, "win_rate": win_rate}
                    bot.db.set_plugin_value("Elemental_Adventure_Stats", playerwin, stats)

                for playerlose in loser.split():
                    try:
                        stats = eval(bot.db.get_plugin_value("Elemental_Adventure_Stats", playerlose,
                                                             default={"score": 0, "win": 0, "tot": 0, "win_rate": 0}))
                    except:
                        stats = bot.db.get_plugin_value("Elemental_Adventure_Stats", playerlose)
                    print(stats)
                    score = stats["score"] + int(punteggiolose)
                    win = stats["win"]
                    tot = stats["tot"] + 1
                    win_rate = round((win * 100 / tot), 2)
                    stats = {"score": score, "win": win, "tot": tot, "win_rate": win_rate}
                    bot.db.set_plugin_value("Elemental_Adventure_Stats", playerlose, stats)

                bot.say("[" + ELEMENTAL + "] : partita finita in WIN per " + winner + " in " + place, log_chan)

            if self.draw:
                bot.say("NO ONE WINS")
                for totplayer in game.players:
                    stats = bot.db.get_nick_value(totplayer, "elad_stats",
                                                  default={"score": 0, "win": 0, "tot": 0, "win_rate": 0})
                    print(stats)
                    score = stats["score"] + 60
                    win = stats["win"]
                    tot = stats["tot"] + 1
                    win_rate = round((win * 100 / tot), 2)
                    stats = {"score": score, "win": win, "tot": tot, "win_rate": win_rate}
                    bot.db.set_nick_value(totplayer, "elad_stats", stats)

                bot.say("[" + ELEMENTAL + "] : match ended in DRAW in " + place, log_chan)

            self.game_ended(bot, place)

    def send_cards(self, bot, trigger):
        if trigger.sender not in self.games:
            return
        game = self.games[trigger.sender]
        game.send_cards(bot, trigger.nick)

    def send_counts(self, bot, trigger):
        if trigger.sender not in self.games:
            return
        game = self.games[trigger.sender]
        game.send_counts(bot)

    def game_ended(self, bot, place):
        with lock:
            game = self.games[place]
            for player in game.players:
                bot.write(['MODE', place, '-v', player])

            del self.games[place]

    def move_game(self, bot, trigger):
        who = trigger.nick
        oldchan = trigger.sender
        newchan = tools.Identifier(trigger.group(3))
        if newchan[0] != '#':
            newchan = tools.Identifier('#' + newchan)
        if oldchan not in self.games:
            bot.reply(self.strings['not_started'])
            return

        if not trigger.admin:
            bot.reply(self.strings['cant_move'])

            return
        if not newchan:
            bot.reply(self.strings['NEED_CHANNEL'])
            return
        if newchan == oldchan:
            return
        if newchan.lower() not in bot.privileges:
            bot.reply(strings['NOT_IN_CHANNEL'] % newchan)
            bot.say(
                "[" + ELEMENTAL + "] : " + trigger.nick + " tried to move a game from " + oldchan + " to " + newchan + ", but $nickname isn't in " + oldchan + "...",
                log_chan)

            return
        if newchan in self.games:
            bot.reply(strings['CHANNEL_IN_USE'] % newchan)
            bot.say(
                "[" + ELEMENTAL + "] : " + trigger.nick + " tried to move a game from " + oldchan + " to " + newchan + ", but the chan is full.",
                log_chan)
            return
        game = self.games.pop(oldchan)
        self.games[newchan] = game
        game.game_moved(bot, who, oldchan, newchan)

    def teams(self, bot, trigger):
        if trigger.sender not in self.games:
            return
        game = self.games[trigger.sender]
        game.teams(bot, trigger)


elad = ElAdBot()


@module.thread(True)
@module.commands("rank")
@module.example(".rank")
def rank(bot, trigger):
    bot.notice(str(bot.db.get_plugin_value("Elemental_Adventure_Stats", trigger.nick,
                                           default={"score": 0, "win": 0, "tot": 0, "win_rate": 0})), trigger.nick)
    bot.say("[" + ELEMENTAL + "] : " + trigger.nick + " requestes their RANK.", log_chan)


@module.commands("adrank")
@module.example(".rank")
@module.require_admin()
def adrank(bot, trigger):
    bot.notice(str(bot.db.get_plugin_value("Elemental_Adventure_Stats", trigger.group(3),
                                           default={"score": 0, "win": 0, "tot": 0, "win_rate": 0})), trigger.nick)
    bot.say("[" + ELEMENTAL + "] : " + trigger.nick + " requestes the RANK of " + trigger.group(3), log_chan)


@module.commands("elemental adventure", "elad", "ElAd")
@module.example(".Elemental Adventure")
@module.priority('high')
@module.require_chanmsg("Ehy hi, please use this command in a chan.")
def start(bot, trigger):
    if trigger.sender in game_chan:
        elad.start(bot, trigger)
        bot.say("[" + ELEMENTAL + "] : START in " + trigger.sender + " da " + trigger.nick, log_chan)


@module.commands("language", "lan")
@module.example(".language italiano", ".lan english")
def language(bot, trigger):
    if trigger.sender in game_chan:
        elad.language(bot, trigger)


@module.commands('adstop elad')
@module.example(".adstop")
@module.priority('high')
def eladstop(bot, trigger):
    if trigger.sender in game_chan and trigger.account in elad_admins:
        elad.stop(bot, trigger)
        bot.say("[" + ELEMENTAL + "] : Admin ha fermato una partita in  " + trigger.sender, log_chan)


@module.commands('jo', "join")
@module.priority('high')
@module.require_chanmsg
def brisjoin(bot, trigger):
    if trigger.sender in game_chan:
        elad.join(bot, trigger)


@module.commands('quit', "qu")
@module.priority('high')
@module.require_chanmsg
def brisquit(bot, trigger):
    if trigger.sender in game_chan:
        elad.quit(bot, trigger)


@module.commands('eladmove')
@module.priority('high')
@module.require_admin("You're not an admin.")
@module.example('.brismove #anotherchannel')
def brismove(bot, trigger):
    if trigger.sender in game_chan:
        elad.move_game(bot, trigger)


@module.commands('deal', "de")
@module.priority('medium')
@module.require_chanmsg
def brisdeal(bot, trigger):
    if trigger.sender in game_chan:
        elad.deal(bot, trigger)


@module.commands('play', "pl")
@module.priority('medium')
@module.require_chanmsg
def unoplay(bot, trigger):
    if trigger.sender in game_chan:
        elad.play(bot, trigger)


@module.commands("teams", "tm")
@module.require_admin("Only admins can see team reputation.")
def teams(bot, trigger):
    if trigger.sender in game_chan:
        elad.teams(bot, trigger)


@module.commands('cards', "ca", "card")
@module.example(".cards")
@module.priority('medium')
@module.require_chanmsg
def unocards(bot, trigger):
    if trigger.sender in game_chan:
        elad.send_cards(bot, trigger)


@module.commands('help')
@module.example(".help elad italiano")
@module.priority('low')
def brishelp(bot, trigger):
    if trigger.group(3).lower() == "elad":
        if trigger.sender in game_chan:
            if "italiano" in trigger.group(2).lower():
                bot.notice("GUIDA: " + string_help_ita, trigger.nick)
                bot.notice("REGOLE DEL GIOCO: " + rules_ita, trigger.nick)
            else:
                bot.notice("GUIDE: " + string_help_eng, trigger.nick)
                bot.notice("GAME'S RULES: " + rules_eng, trigger.nick)


@module.commands('eladgames', "eladgm")
@module.priority('high')
@module.require_admin
def eladgames(bot, trigger):
    chans = []
    active = 0
    pending = 0
    with lock:
        for chan, game in elad.games.items():
            if game.startTime:
                chans.append(chan)
                active += 1
            else:
                chans.append(chan + " (pending)")
                pending += 1
    if not len(chans):
        bot.say('No ' + ELEMENTAL + ' games in progress, %s.' % trigger.nick)
        return
    g_active = "channel" if active == 1 else "channels"
    g_pending = "channel" if pending == 1 else "channels"
    chanlist = ", ".join(chans[:-2] + [" and ".join(chans[-2:])])
    bot.reply(
        ELEMENTAL + " is pending deal in %d %s and in progress in %d %s: %s. "
        % (pending, g_pending, active, g_active, chanlist))


@module.interval(1)
def afktime(bot):
    elad.afktime(bot)
    elad.checkidle(bot)
