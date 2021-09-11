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

import sopel.plugins as module
import sopel.tools as tools
from sopel.formatting import colors, CONTROL_BOLD, CONTROL_COLOR, CONTROL_NORMAL

import random

import threading
from datetime import datetime
from sopel import config


settings = config.Config('/Users/giova/.sopel/default.cfg')  # replace with the config path

from sopel.config.types import StaticSection, ListAttribute, ValidatedAttribute

game_chan = None


# Called when the module gets loaded
def setup(bot):
    bot.config.define_section("Elemental_Adventure", ElementalAdventureConfigSection)

    # Set the allowed game channels
    global game_chan
    global log_chan
    game_chan = bot.config.Elemental_Adventure.gamechannels
    log_chan = bot.config.Elemental_Adventure.logchannels


# Called when the module gets configured
def configure(config):
    config.define_section("Elemental Adventure", ElementalAdventureConfigSection)
    config.Elemental_Adventure.configure_setting("gamechannels", "In what channels is Elemental Adventure allowed to be played?")
    config.Elemental_Adventure.configure_setting("logchannels", "In what channels will Elemental Adventure send logs?")


# Class with the settings for Elemental Adventure
class ElementalAdventureConfigSection(StaticSection):
    gamechannels = ListAttribute("gamechannels")
    logchannels = ValidatedAttribute("logchannels")

ELEMENTAL = CONTROL_BOLD + CONTROL_COLOR + colors.GREEN + "," + colors.WHITE + " B"  + CONTROL_COLOR + colors.ORANGE + "," + colors.WHITE +  "R"  + CONTROL_COLOR + colors.RED + "," + colors.WHITE +  "I"  + CONTROL_COLOR + colors.GRAY + "," + colors.WHITE +  "S"  + CONTROL_COLOR + colors.GREEN + "," + colors.WHITE +  "C"  + CONTROL_COLOR + colors.ORANGE + "," + colors.WHITE +  "O"+ CONTROL_COLOR + colors.RED + "," + colors.WHITE +  "L" + CONTROL_COLOR + colors.GRAY + "," + colors.WHITE +  "A " + CONTROL_NORMAL


hand_size = 3

min_player = 2
max_player = 4

NO = False
YES = True
WIN = True
lock = threading.RLock()

listpoint = ["NUMBER | ONTABLE | POINTS                         ",
             "1________11________11                              ",
             "2________2________0                            ",
             "3________10________10                              ",
             "4________4________0                             ",
             "5________5________0                          ",
             "6________6________0     ",
             "7________7________0",
             "8________8________2",
             "9________9________3",
             "10________10________4", ]

string_help_ita_notused = [
    " |||||   PAGINA DI AIUTO DI:   BRISCOLA    |||||",
    "═════════════════════════════════════════════════════════════════════════════════════════════════════════",
    "COMANDO  | COMANDO COMPRESSO | COSA FA?",
    "═════════════════════════════════════════════════════════════════════════════════════════════════════════",
    ".briscola  | .bris  .br | Apre la lobby. Non starta il gioco. ",
    ".join      | .jo | Ti unisce alla partita.",
    ".quit      | .qu | Abbandona la partita. ATTENZIONE! se la partita è iniziata, vincerà la squadra avversaria",
    ".deal      | .de | Starta la partita. Non si torna indietro. ",
    ".play      | .pl | Gioca una carta. ",
    ".cards     | .ca | Mostra le carte nella tua mano, e la Briscola. ",
    ".brishelp  |.brhelp | Come sei arrivato fino a qui senza saperlo? O.o ",
    ".rules     |.ru | Mostra le REGOLE del GIOCO ",
    ".language  |.lan| Cambia la lingua del gioco (disponibili english e italiano)",
    "═════════════════════════════════════════════════════════════════════════════════════════════════════════",
    "     ",
    "COME GIOCARE UNA CARTA: .play C S o .play S C (S = Seme della carta , V = Valore della carta)",
    "Semi possibili: S (spade) , M (mazze) , O (oro) , C (coppe)",
    "Valori possibili: ogni numero da 1 a 10"
]
string_help_ita = "https://usercontent.twoopy.nl/6d2bb7d2b15789f8/paste.txt"

string_help_eng_notused = [
    " ||||| HELP PAGE OF BRISCOLA |||||",
    "═════════════════════════════════════════════════════════════════════════════════════════════════════════ ",
    "COMMAND | COMPRESSED COMMAND | WHAT DOES IT DO?",
    "═════════════════════════════════════════════════════════════════════════════════════════════════════════ ",
    ".briscola | .bris .br | Opens the lobby. Don't start the game.",
    ".join     | .jo | Joins you in the game.",
    ".quit     | .qu | Leave the game. ATTENTION! if the game has started, the opposing team will win",
    ".deal     | .de | The game starts. There's no turning back.",
    ".play     | .pl | Play a card.",
    ".cards    | .ca | Show the cards in your hand, and the BRISCOLA.",
    ".brishelp | .brhelp | How did you get here without knowing it? O.o",
    ".rules    | .ru | Show the GAME RULES",
    ".pointlist|.poli| Show just the Table of the Value of Cards.",
    "═════════════════════════════════════════════════════════════════════════════════════════════════════════ ",
    "  ",
    "HOW TO PLAY A CARD: .play C S or .play S C (S = Card suit, V = Card value)",
    "Possible suits: S (spade), M (mazze), O (oro), C (coppe)",
    "Possible values: any number from 1 to 10"
]
string_help_eng = "https://usercontent.twoopy.nl/ae1d47e0066642d1/paste.txt"

rules_ita_notused = [
    "                                     ════════════════════",
    "                                      REGOLE DI BRISCOLA",
    "                                     ════════════════════",
    " ",
    "--QUAL E' L'OBIETTIVO?--",
    "Due squadre (composte da 2 o 4 giocatori) si sfidano con un unico obiettivo: a fine partita,",
    "avere più punti dell'altra squadra. I punti massimi ottenibili sono 120.",
    "Il primo giocatore a iniziare il primo turno è scelto casualmente. Dal secondo in poi, il giocatore",
    "a iniziare il turno sarà il vincitore della mano precedente."
    " "
    "--COME SI VINCE UNA MANO--?",
    "Il giocatore a iniziare il turno gioca una carta. Questa carta deciderà il SEME DEL TURNO.",
    "Il giocatore successivo, per vincere il turno, deve giocare una carta dello STESSO SEME ma VALORE SUPERIORE",
    "es.  G1 gioca '4 di Mazze'.  G2 gioca '8 di Coppe'. vincitore -> G1 (anche se la carta di G2 ha VALORE SUPERIORE, ha un seme diverso.)",
    "es.  G1 gioca '6 di Oro'  .  G2 gioca '10 di Oro' . vincitore -> G2 (la carta del G2 ha lo STESSO SEME, e VALORE SUPERIORE)",
    "QUESTO ^ fa capire come il primo giocatore a giocare una carta abbia un vantaggio rispetto ai giocatori successivi. ",
    "Il vincitore del punto si prente TUTTE le carte sul tavolo, che andranno a costituire i suoi PUNTI",
    "ATTENZIONE: nel gioco sono presenti carte 'jolly' chiamate BRISCOLA. Queste carte, quando giocate, hanno la precedenza su tutte le altre.",
    "In caso di presenza di più BRISCOLE, vince la maggiore. Il seme della BRISCOLA è sorteggiato a inizio partita",
    "TUTTE le carte con lo stesso SEME della briscola, sono anch'esse BRISCOLE.",
    "es. BRISCOLA = MAZZE    G1 gioca '7 di Oro' . G2 gioca '2 di Mazze'. vincitore -> G2 (perchè il G2 ha giocato una BRISCOLA. Non importa il",
    "seme nè il valore della carta del G1, le briscole hanno SEMPRE la precedenza.",
    "es. BRISCOLA = COPPE    G1 gioca '8 di Coppe' . G2 gioca '9 di Coppe'. vincitore -> G2 (entrambi i giocatori hanno giocato BRISCOLE, quindi vince quella maggiore)",
    " ",
    "IMPORTANTE! Le carte hanno un valore diverso, a seconda che siano giocate sul tavolo o contate come punti alla fine del turno (vedi tabella)",
    " ",
    "NUMERO | TAVOLO | PUNTI                                      @@@ ESEMPI @@@  ",
    " 1         11       11                  |BRISCOLA = ORO per tutti gli esempi               |",
    " 2          2        0                  |G1 = 3 di Coppe    G2 = 5 di Coppe  vincitore = G1|",
    " 3         10       10                  |G1 = 3 di Coppe    G2 = 1 di Mazze  vincitore = G1|",
    " 4          4        0                  |G1 = 3 di Coppe    G2 = 2 di Oro    vincitore = G2|",
    " 5          5        0                  |G1 = 7 di Mazze    G2 = 9 di Mazze  vincitore = G2|",
    " 6          6        0                  |G1 = 10 di Mazze   G2 = 3 di Mazze  vincitore = G2|",
    " 7          7        0                  |G1 = 5 di Oro      G2 = 3 di Mazze  vincitore = G1|",
    " 8          8        2",
    " 9          9        3",
    "10         10        4",
    " ",
    "(p.s. : sia 3 che 10 valgono 10 sul tavolo. In caso di scontro, 3 > 10)",
    "Finite le carte del mazzo, si contano i punti secondo la colonna PUNTI. Chi ne ha di più vince la partita."
]
rules_ita = "https://usercontent.twoopy.nl/2b3fa889cd344877/paste.txt "

rules_eng_notused = [
    "════════════════════",
    "   BRISCOLA RULES",
    "════════════════════",
    "",
    "--WHAT IS THE GOAL?--",
    "Two teams (made up of 2 or 4 players) compete with one goal: at the end of the game,",
    "having more points than the other team. The maximum points achievable are 120.",
    "The first player to start the first round is chosen randomly. From the second on, ",
    "The winner of the previous hand will start the round."
    "===================================================================="
    "--HOW DO YOU WIN A HAND--?",
    "The player who starts the turn plays a card. This card will decide the SUIT OF THE TURN.",
    "The next player,in order to win the turn, must play a card of the SAME SUIT but HIGHER VALUE",
    "eg. G1 plays '4 di MAZZE'. G2 plays '8 di COPPE' . winner -> G1",
    "(even if G2's card has HIGHER VALUE, it has a different suit.)",
    "eg. G1 plays '6 di ORO'. G2 plays '10 di ORO'. winner -> G2 ",
    "(G2's card has the SAME SUIT, and HIGHER VALUE)",
    "THIS ^ shows how the first player to play a card has an advantage over subsequent players.",
    "The winner of the turn takes ALL the cards on the table, which will make up his POINTS",
    "=====================================================================",
    "ATTENTION: in the game there are SPECIAL cards called BRISCOLA. These cards, when played, take precedence over all the others.",
    "In case of more BRISCOLE, the largest wins. The BRISCOLA suit is drawn at the beginning of the game",
    "ALL the cards with the same SEED of the Briscola, are also BRISCOLE.",
    "eg. BRISCOLA = MAZZE. G1 plays '7 of ORO '. G2 plays '2 of MAZZE '. winner -> G2 (because G2 has played a BRISCOLA. It doesn't matter what",
    "suit nor the value of the G1 card, Briscolas ALWAYS take precedence.",
    "eg. BRISCOLA = COPPE. G1 plays '8 of COPPE'. G2 plays  '9 of COPPE' . Winner -> G2 (both players have played BRISCOLE, so the higher one wins)",
    "                  ",
    "IMPORTANT! The cards have a different value, depending on whether they are played on the table or counted as points at the end of the round (see table)",
    "                ",
    "NUMBER | ONTABLE | POINTS                          @@@ EXAMPLES @@@",
    "1    11    11                              | BRISCOLA = GOLD for all examples |",
    "2     2     0                              | G1 = 3 of COPPE. G2 = 5 of COPPE. winner = G1 |",
    "3    10    10                              | G1 = 3 of COPPE. G2 = 1 of MAZZE. winner = G1 |",
    "4     4     0                              | G1 = 3 of COPPE. G2 = 2 of ORO. winner = G2 |",
    "5     5     0                              | G1 = 7 of MAZZE. G2 = 9 of MAZZE. winner = G2 |",
    "6     6     0                              | G1 = 10 of MAZZE. G2 = 3 of MAZZE. winner = G2 |",
    "7     7     0                              | G1 = 5 of ORO. G2 = 3 of Clubs. winner = G1 |",
    "8     8     2",
    "9     9     3",
    "10    10    4",
    "                      ",
    "(ps: both 3 and 10 are worth 10 on the table. In case of a clash, 3 > 10)",
    "Once the cards in the deck are finished, the points are counted according to the POINTS column. Whoever has the most wins the game."
]
rules_eng = "https://usercontent.twoopy.nl/e95748df860adbb8/paste.txt"

strings_eng = {"nuovo_player": " %s joins the match as player: %s .",
               "impos_unirsi": "I'm sorry %s , the max number of players is 4. Wait until next match :)",
               "gia_dentro": " %s you are already inside the match of " + bris + " O.o",
               "pronti": "Enough players, ready to deeeeal.",
               "player_quit": " %s abandoned the match of " +bris + " .",
               "non_abbastanza": "Can't play alone, wait for someone else...",
               "iniziato": "Match already started.",
               "cant_play": "You are not inside the match, please do not disturb the other players :)",
               "turno": " %s 's turn.",
               "non_hai": "%s you don't have this card: %s",
               "tue_carte": "Your cards: %s",
               "mano_win": CONTROL_BOLD + " %s  wins the hand!",
               "prossimo": CONTROL_BOLD + "ON TURN: ",
               "game_started": bris+ " started. use .join to join .",
               "not_started": "Match not started yet.",
               "game_stopped": CONTROL_BOLD + "GAME OVER.",
               "admin_stop": CONTROL_BOLD + "AN ADMIN TERMINATED THE MATCH FROM REMOTE.",
               "cant_continue": "a player left the game. The other team wins!!",
               "win": "The winner team is made of %s   !!!. Play time: %s",
               "on_table": " %s's turn. Cards on table: %s  ",
               'SB_PLAYER': "%s (%d %s)",
               "briscola": bris + " : %s",
               "cant_move": "Only an admin can move the match. ",
               'NEED_CHANNEL': "I need a channel name to move to.",
               'NOT_IN_CHANNEL': "I'm not in %s, so I can't move the game there.",
               'CHANNEL_IN_USE': "Channel %s already has a " + bris + " game in progress.",
               'MOVED_FROM': "Note: %s moved an " + bris + " game here from %s.",
               'GAME_MOVED': "%s " + bris + " game moved to %s.",
               "lan_done": "Succesfully changed " + bris + "language to %s .",
               "not_admin": "Only an admin can change this setting.",
               "joined": " %s joined the TEAM %s .",
               "wrong_seed": "Suits can be ORO(o) , MAZZE(m) , COPPE(c) or SPADE(s), not %s .",
               "team_comp": "Teams formed by:    TEAM 1: %s  *** TEAM 2: %s",
               "not_3": "The number of players can be 2 or 4, NOT 3. please wait for another player, or leave :)",
               "wrong_value": "values go from 1 to 10. %s is not ok.",
               "last_turn": "LAST TURN!! Play wisely your last 3 cards!!",
               "quit_win": "The player %s left the match. WINNER: %s .",
               "quit_ok": "The player %s left the match. Match has to be started again.",
               "change_time": CONTROL_BOLD + "TIME TO SWAP!! You have 10 seconds to see the cards of your  mate.",
               "change_cards": "Your mate's cards: %s",
               "team_earn": "TEAM %s earns  | %s |  points!" ,
               "player_list": "TEAM 1 : %s    TEAM 2 : %s",
               "local_stop": CONTROL_BOLD + "AN ADMIN STOPPED THE MATCH",
               "quit_warn": "If you leave the match, the opposite team will win. Use .quit to confirm. ",
               "idle_kick" : "Player %s had been IDLE for 1 MINUTE. Going to be kicked from the match.",
               "idle_warn1" : " %s your turn! Idle for: 15s",
               "idle_warn2" : " %s your turn. Being Idle for more than 60 seconds will result in a kick. Idle for : 30s",
               "idle_warn3" : " %s you here??? Do something or you'll be kicked in 15 secondi! Idle for: 45s",
               "idle_end" : "Match terminated for inactivity."
               }
strings_ita = {"nuovo_player": " %s si unisce alla partita di " + bris + "  come giocatore: %s .",
               "impos_unirsi": "Mi spiace %s , il numero massimo di giocatori è 4. Aspetta l'inizio della prossima partita :)",
               "gia_dentro": " %s sei già dentro la partita di " + bris + " O.o",
               "pronti": "Siamo abbastanza, pronti a partireeeee! ",
               "player_quit": " %s ha abbandonato la partita di " + bris + " .",
               "non_abbastanza": "Non puoi giocare da solo, aspetta qualcun altro...",
               "iniziato": "La partita non è iniziata.",
               "cant_play": "Non sei dentro la partita, per favore non disturbare gli altri giocatori :)",
               "turno": "Turno di %s.",
               "non_hai": "%s non hai questa carta: %s",
               "tue_carte": "Le tue carte: : %s",
               "mano_win": " %s  vince la mano!",
               "prossimo": "E' il turno di: ",
               "game_started": bris + " iniziata. Usa .join per unirti .",
               "not_started": "La partita non è ancora iniziata.",
               "game_stopped": "GAME OVER.",
               "admin_stop": "Un admin ha forzatamente terminato la partita di " + bris + ".",
               "cant_continue": "Un giocatore ha lasciato la partita. Vince il team avversario!!",
               "win": "Il team vincitore è composto da: %s !!!. Tempo di gioco: %s",
               "on_table": " Turno di: %s.  Carte sul tavolo: %s  ",
               'SB_PLAYER': "%s (%d %s)",
               "briscola": bris + " : %s",
               "cant_move": "Solo un admin può muovere la partita. ",
               'NEED_CHANNEL': "Ok ma...dimmi dove andare.",
               'NOT_IN_CHANNEL': "Non sono dentro %s, quindi non posso muovere la partita là.",
               'CHANNEL_IN_USE': "Il canale %s ha già una partita di " + bris + " in corso.",
               'MOVED_FROM': "ATTENZIONE: %s ha mosso una partita di " + bris + " qui da %s.",
               'GAME_MOVED': "%s partita di " + bris + " mossa in %s.",
               "lan_done": "La lingua di " + bris + " è stata correttamente cambiata in %s .",
               "not_admin": "NON SEI UN ADMIN. VADE RETRO.",
               "joined": " %s si è unito al TEAM %s .",
               "wrong_seed": "I semi possono essere ORO(o) , MAZZE(m) , COPPE(c) o SPADE(s), non %s .",
               "team_comp": "I team sono formati da: TEAM 1: %s  *** TEAM 2: %s",
               "not_3": "Il numero di giocatori deve essere 2 o 4, NON 3. Per favore attendi un altro giocatore, o abbandona :)",
               "wrong_value": "I valori vanno da 1 a 10. Quindi %s non va bene",
               "last_turn": "ULTIMO TURNO!! Gioca con saggezza le tue ultime 3 carte!!",
               "quit_win": "Il giocatore %s ha lasciato la partita. VINCITORE: %s .",
               "quit_ok": "Il giocatore %s ha lasciato la partita. La partita deve essere avviata di nuovo.",
               "change_time": CONTROL_BOLD +  "ULTIMO TURNO!!! Hai 10 secondi di tempo per vedere le carte del compagno.",
               "change_cards": "Carte del tuo compagno: %s",
               "team_earn": "Il TEAM %s guadagna  | %s |  punti!" ,
               "player_list": "TEAM 1 : %s    TEAM 2 : %s",
               "local_stop": CONTROL_BOLD + "UN ADMIN HA FERMATO LA PARTITA",
               "quit_warn": "Se abbandoni, il team avversatio vincerà. Usa .quit per confermare.",
               "idle_kick" : "Il giocatore %s è stato IDLE per 1 MINUTO. Verrà rimosso dalla partita.",
               "idle_warn1" : " %s è il tuo turno! Idle da: 15s",
               "idle_warn2" : " %s è il tuo turno. Restare idle per più di 60 secondi causerà un kick. Idle da : 30s",
               "idle_warn3" : " %s ci sei??? Fai qualcosa o sarai buttato fuori tra 15 secondi! Idle da: 45s",
               "idle_end" : "Partita terminata per inattività."
               }


strings = strings_eng
rules = rules_eng
string_help = string_help_eng

seeds = {"MAZZE": " di MAZZE  ", "COPPE": " di COPPE  ", "SPADE": " di SPADE  ",
         "ORO": " di ORO  ", "O": " di ORO  ", "C": " di COPPE  ", "M": " di MAZZE  ", "S": " di SPADE  "}

seedsstandard = ["M", "O", "C", "S"]
valoristandard = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

numbers = {"1": "1", "ASSO": "ASSO", "2": "2", "3": "3", "4": "4", "5": "5",
           "6": "6", "7": "7", "8": "8", "DONNA": "DONNA",
           "9": "9 ", "CAVALLO": "CAVALLO ", "0": "10", "RE": "RE "}

valori = {"1": 11, "ASSO": 11, "2": 0, "3": 10, "4": 0, "5": 0,
          "6": 0, "7": 0, "8": 2, "DONNA": 2,
          "9": 3, "CAVALLO": 3, "0": 4, "RE": 4}

valori_tavolo = {"1": 11, "2": 2, "3": 10.5, "4": 4, "5": 5,
                 "6": 6, "7": 7, "8": 8, "9": 9, "0": 10}


class BrisGame:
    def __init__(self, trigger):
        self.strings = strings_eng
        self.string_help = string_help_eng
        self.rules = rules_eng
        self.starter = trigger.nick
        self.channel = trigger.sender
        self.deck = []
        self.players = {self.starter: {"cards" : [] , "idletime" : 0}}  # player's dict. each player will have a card list
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
        self.briscola = []
        self.lastturn = False
        self.startcont = 0
        self.tempcont = 0
        self.firstpl = 0
        self.bris_ontable = []
        self.changecount = 0

    def idlefunc(self , bot , game):
        for player in self.players:
            if player == self.playerOrder[self.currentPlayer]:
                self.players[player]["idletime"] += 1
        self.idlepenalty(bot , game)

    def idlepenalty(self , bot , game):
        for player in self.players:
            if self.players[player]["idletime"] == 15:
                bot.say(self.strings["idle_warn1"] % player , game)
            if self.players[player]["idletime"] == 30:
                bot.say(self.strings["idle_warn2"] % player , game)
            if self.players[player]["idletime"] == 45:
                bot.say(self.strings["idle_warn3"] % player , game)
            if self.players[player]["idletime"] == 60:
                bot.say(self.strings["idle_kick"] % player , game)
                #self.quit(bot , player , idle = True)
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
                self.players[trigger.nick] = {"cards" : [] , "idletime" : 0}  # add player to players dict
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

    def quit(self, bot, trigger , idle = False):  # remove the player from the team. the other team wins. (need to add: if game not dealt, no one loses)
        if not idle:
            player = trigger.nick
            if player not in self.players:
                return
            with lock:
                bot.say(strings['player_quit'] % player)
                return self.remove_player(bot, player)
        elif idle:
            return self.remove_player(bot , trigger)

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
            self.deck = self.create_deck()  # create the deck (check the functino)
            briscola = str(
                self.get_card(
                    bot)) + "*"  # make a "briscola" recognizable for the _render_coloured_cards method. e.g. briscola: "4M*"
            self.briscola.append(
                briscola)  # adds the briscola to the briscola list. ONLY ONE CARD will be here, that will decide the seed of the briscola
            for player_list in self.players:
                while len(self.players[player_list]["cards"]) < 3:
                    self.players[player_list]["cards"].append(self.get_card(
                        bot))  # gives 3 cards to each player. sometimes it gets bugged, no idea why, and gives less cards

            self.dealt = YES
            self.currentPlayer = random.randrange(len(self.players))
            # il primo giocatore è scelto a caso
            self.show_on_turn(bot)

            if len(self.briscola) == 0:
                self.briscola.append(self.get_card(bot))
            for player in self.players:
                self.players[player]["idletime"] = 0
            bot.say("[" + bris + "] : DEAL di BRISCOLA in " + trigger.sender, "#trinacry-logs")

    def play(self, bot, trigger):

        if trigger.nick not in self.players:
            bot.notice(self.strings['cant_play'], trigger.nick)
            return
        if trigger.nick != self.playerOrder[self.currentPlayer]:
            bot.say(self.strings['turno'] % self.playerOrder[self.currentPlayer])
            return
        self.players[self.playerOrder[self.currentPlayer]]["idletime"] = 0
        try:
            seed, number = trigger.group(3).upper(), trigger.group(
                4).upper()  # here, he takes commands like .play 4 c and creates the card "4C"
            if number == "10":
                number = "0"
            if seed == "10":
                seed = "0"

            if seed not in seedsstandard:
                seed, number = number, seed
            elif number not in valoristandard:  # allows both .play 4 c and .play c 4
                seed, number = number, seed
            if seed in seedsstandard and number in valoristandard:
                searchcard = number + seed  # important!! the output card must always have number + seed. The card in the format e.g. "4C" is called searchcard

            else:
                if seed not in seeds:
                    bot.notice(self.strings["wrong_seed"] % seed, trigger.nick)

                elif number not in numbers:  # if something is not working, explains what
                    bot.notice(self.strings["wrong_value"] % number, trigger.nick)

                return  # card not existing
        except (AttributeError):
            return
        if searchcard[1] == self.briscola[0][1] and "*" not in searchcard:
            searchcard += "*"
        with lock:
            # this decides the INDEX of the current player in the self.playerOder LIST. giocatore = player (translation tip)
            if searchcard not in self.players[trigger.nick]["cards"]:
                # if the card is not in the player's list, return
                bot.notice(self.strings['non_hai'] % (searchcard, trigger.nick), trigger.nick)
                return

            playcard = searchcard + " " + str(
                trigger.nick)  # from now on, each card will be in the format e.g. "4C giovannetor" . this is essential to understand who
            self.ontable.append(
                playcard)  # append the card ("4C giovannetor" format) to the "ontable" list. this list is temporary, gets emptied each full turn
            self.players[trigger.nick]["cards"].remove(
                searchcard)  # removes from the player's card list the card in the "4C" format
            # ecample self.ontable = ["4C giovannetor" , "7O yorick"]

            self.inc_player(bot, trigger)  # increase the player.
            self.show_on_turn(bot)  # shows who's the turn now

    def decidepoint(self, bot):  # decides who earns the point of the turn. THIS IS WHAT CREATES MOST OF THE PROBLEMS
        self.bris_ontable.clear()  # creates a list of BRISCOLA on table (temporary, get emptied at the end)
        carcom = self.ontable[
            0]  # the first card in the self.ontable is the "command card". to win a turn, the other cards must have same seed and > number, OR be a briscola
        # briscola always wins. if there are more briscola, the highest wins

        for c in range(1, len(
                self.ontable)):  # analyzes the cards in the .ontable one by one. if one of the same seed has number > carcom, it becomes the new carcom
            card_sfid = self.ontable[c]  # c is just an index
            if card_sfid[1] == carcom[1]:
                if valori_tavolo[card_sfid[0]] > valori_tavolo[carcom[0]]:  # valore = value (translate tip)   valori_tavolo is a dict, shows the value of cards on the table
                    carcom = card_sfid  # important! cards on the table have different value than when counted as points. ***
            elif card_sfid[1] == self.briscola[0][1]:  # if he finds a briscola, he adds it in the bris_ontable list
                self.bris_ontable.append(card_sfid)
        if len(self.bris_ontable) > 1:  # if there are more than 1 briscola, it compares them and choose the highest
            briscom = self.bris_ontable[0]
            for numero in range(1, len(self.bris_ontable)):
                briscsfid = self.bris_ontable[
                    numero]  # ***e.g.  10 = 10 on table, but = 4 as point. 7 = 7 on table, but = 0 as point.
                if valori_tavolo[briscsfid[0]] > valori_tavolo[
                    briscom[0]]:  # 1 = 11 on table, and = 11 as point   (these are not errors, it's how the game is XD)
                    briscom = briscsfid

            cardwin = briscom
        elif len(self.bris_ontable) == 1:
            cardwin = self.bris_ontable[0]
        else:
            cardwin = carcom  # if there are no briscola, the highest normal card wins
        not_necessary, plwin = cardwin.split()  # remember that the cards are in the format "4C giovannetor". briscola are in the format "5M* Mina". the "*" for all the briscola gets
        # added in the self.getcard(), and it's only used to render the colours
        return plwin  # <-- this is the main problem. This should be a nick, but it's a NoneType, which makes the whole program crash (or i think this is the problem)

    def givepoint(self, bot,
                  plwin):  # the past funcion decided WHO earned the points. this one decides how many points the team earns. it takes the "plwin" from the part function
        punti1prima = self.team1[-1]
        punti2prima = self.team2[-1]
        if plwin in self.team1:  # if player in team 1
            for i in self.ontable:  # for card in the .ontable list (not yet emptied)
                numero = i[0]  # takes the number of the card (remember, format "9S giovannetor"
                self.team1[-1] += int(valori[str(
                    numero)])  # the dict valori contains the point value of cards. remeber that the team1 list has an empty int at the end.
            bot.say(self.strings["team_earn"] % ("1", str(self.team1[-1] - punti1prima)))
            # bot.say(self.strings["mano_win"] % (self.playerOrder[self.currentPlayer]))
            # bot.say("Team 1 earns " + str(self.team1[-1] - punti1prima) + " points! Gets to " + str(self.team1[-1]))
        else:
            for i in self.ontable:
                numero = i[0]
                self.team2[-1] += int(valori[str(numero)])
            bot.say(self.strings["team_earn"] % ("2", str(self.team2[-1] - punti2prima)))
            # bot.say("Team 2 earns " + str(self.team2[-1] - punti2prima) + " points! Gets to " + str(self.team2[-1]))

    def show_on_turn(self, bot):  # shows the cards atm on the table.
        with lock:
            giocatore = self.playerOrder[self.currentPlayer]
            bot.say(self.strings['on_table'] % (giocatore, self._render_colored_cards(self.ontable)))

            self.send_cards(bot, self.playerOrder[self.currentPlayer])
        # self.send_next(bot)

    def send_cards(self, bot, trigger):  # shows the cards in your hand, and the match's briscola card
        with lock:
            if not self.startTime:
                bot.notice(self.strings['not_started'], trigger.nick)
                return
            if trigger not in self.players:
                bot.notice(self.strings['cant_play'], trigger.nick)
                return
            self.players[trigger]["idletime"] = 0
            cards = []
            briscola = []
            for i in self.players[trigger]["cards"]:
                cards.append(i)
            for i in self.briscola:
                briscola.append(str(i))

                # trova le carte nel dizionario, renderizzate sotto V
            bot.notice("=========================================", trigger)
            bot.notice(self.strings['tue_carte'] % (str(self._render_colored_cards(self.players[trigger]["cards"]))), trigger)
            bot.notice(self.strings["briscola"] % (str(self._render_colored_cards(self.briscola))), trigger)
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
                                carta = self.get_card(bot)
                                self.players[player_list]["cards"].append(carta)

                    if self.lastturn:  # if last turn, choose the total winner
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
                # if self.currentPlayer < 0:
                # self.currentPlayer = len(self.players) - 1

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
                                self.players[player_list]["cards"].append(self.get_card(bot))

                    if self.lastturn and self.changecount == 0:
                        bot.say(strings["change_time"])
                        bot.notice(strings["change_cards"] % (self._render_colored_cards(self.players[self.team1[0]]["cards"])),
                                   self.team1[1])
                        bot.notice(strings["change_cards"] % (self._render_colored_cards(self.players[self.team1[1]]["cards"])),
                                   self.team1[0])
                        bot.notice(strings["change_cards"] % (self._render_colored_cards(self.players[self.team2[0]]["cards"])),
                                   self.team2[1])
                        bot.notice(strings["change_cards"] % (self._render_colored_cards(self.players[self.team2[1]]["cards"])),
                                   self.team2[0])
                        time.sleep(15)
                        self.changecount += 1
                    if self.lastturn:  # if last turn, choose the total winner
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
            # if self.currentPlayer < 0:
            #    self.currentPlayer = len(self.players) - 1

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
    def _render_colored_cards(cards):  # renderizza colori carte

        background = ''

        sword_code = colors.GRAY
        mace_code = colors.GREEN
        coin_code = colors.YELLOW
        cup_code = colors.RED
        briscola_code = colors.BLACK
        white = colors.WHITE
        black = colors.BLACK
        with lock:
            ret = []
            for card in cards:
                if "*" in card:  # distingue le briscole per seme. DA OTTIMIZZARE
                    if card[1] == "M":
                        ret.append(CONTROL_COLOR + white + "," + briscola_code + " ** " +
                                   CONTROL_COLOR + white + "," + mace_code + numbers[card[0]] +
                                   CONTROL_COLOR + white + "," + mace_code + seeds[card[1]] +
                                   CONTROL_COLOR + white + "," + briscola_code + " ** " +
                                   CONTROL_NORMAL + "   ")

                    if card[1] == "C":
                        ret.append(CONTROL_COLOR + white + "," + briscola_code + " ** " +
                                   CONTROL_COLOR + white + "," + cup_code + numbers[card[0]] +
                                   CONTROL_COLOR + white + "," + cup_code + seeds[card[1]] +
                                   CONTROL_COLOR + white + "," + briscola_code + " ** " +
                                   CONTROL_NORMAL + "   ")

                    if card[1] == "S":
                        ret.append(CONTROL_COLOR + white + "," + briscola_code + " ** " +
                                   CONTROL_COLOR + black + "," + sword_code + numbers[card[0]] +
                                   CONTROL_COLOR + black + "," + sword_code + seeds[card[1]] +
                                   CONTROL_COLOR + white + "," + briscola_code + " ** " +
                                   CONTROL_NORMAL + "   ")

                    if card[1] == "O":
                        ret.append(CONTROL_COLOR + white + "," + briscola_code + " ** " +
                                   CONTROL_COLOR + black + "," + coin_code + numbers[card[0]] +
                                   CONTROL_COLOR + black + "," + coin_code + seeds[card[1]] +
                                   CONTROL_COLOR + white + "," + briscola_code + " ** " +
                                   CONTROL_NORMAL + "   ")

                else:

                    if card[1] == "M":
                        ret.append(CONTROL_COLOR + white + "," + mace_code + numbers[card[0]]
                                   + CONTROL_COLOR + white + "," + mace_code + seeds[card[1]] +
                                   CONTROL_NORMAL + "   ")
                    if card[1] == "C":  # colora le altre carte, abbastanza ez
                        ret.append(CONTROL_COLOR + white + "," + cup_code + numbers[card[0]]
                                   + CONTROL_COLOR + white + "," + cup_code + seeds[card[1]] +
                                   CONTROL_NORMAL + "   ")
                    if card[1] == "S":
                        ret.append(CONTROL_COLOR + black + "," + sword_code + numbers[card[0]]
                                   + CONTROL_COLOR + black + "," + sword_code + seeds[card[1]] +
                                   CONTROL_NORMAL + "   ")
                    if card[1] == "O":
                        ret.append(CONTROL_COLOR + black + "," + coin_code + numbers[card[0]]
                                   + CONTROL_COLOR + black + "," + coin_code + seeds[card[1]] +
                                   CONTROL_NORMAL + "   ")

        return ''.join(ret) + CONTROL_NORMAL

    def get_card(self, bot):

        with lock:
            if not self.deck:
                self.deck = self.create_deck()

            ret = self.deck.pop(0)
            try:
                if ret[1] == self.briscola[0][1]:
                    ret = ret + "*"
            except:
                print("uhoh")

            if len(self.players) == 2:
                if len(self.deck) == 0:
                    bot.say(self.strings["last_turn"])
                    self.lastturn = True
            if len(self.players) == 4:
                if len(self.deck) == 0:
                    bot.say(self.strings["last_turn"])
                    self.lastturn = True
        return ret

    def create_deck(self):
        new_deck = []
        for seed in seedsstandard:
            for valores in valoristandard:
                new_deck.append(valores + seed)
        random.shuffle(new_deck)
        random.shuffle(new_deck)
        random.shuffle(new_deck)
        new_deck.append(new_deck[0])
        return new_deck

    def teams(self, bot, trigger):
        bot.notice(self.strings["player_list"] % (str(self.team1[-1]), str(self.team2[-1])) , trigger.nick)


class BrisBot:
    def __init__(self):  # ,scorefile
        #self.afkcounter = 0
        self.contatore = 0
        self.games = {}
        self.win = False
        self.draw = False
        self.strings = strings_eng

        # self.scoreFile = scorefile
    def checkidle(self , bot):

        for game in self.games:
            if self.games[game].get_player():
                self.play(bot , game ,  stop = True , idle = True)



    def afktime(self , bot):
        for game in self.games:
            self.games[game].idlefunc(bot , game)




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
            self.games[trigger.sender] = BrisGame(trigger)
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
                print("oh no, sticazzi")
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

    def play(self, bot, trigger, stop=False , idle = False):
        self.contatore = 0
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
            print(game.team1 , game.team2)
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
                self.game_ended(bot , trigger)
                print("AFK NOT STARTED OK")
                bot.say(self.strings["idle_end"])
                return

            # winner = game.playerOrder[winner]
            game_duration = datetime.now() - game.startTime
            hours, remainder = divmod(game_duration.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            game_duration = '%.2d:%.2d:%.2d' % (hours, minutes, seconds)
            if self.win:
                bot.say(self.strings['win'] % (winner, game_duration) , trigger or trigger.sender)
                for playerwin in winner.split():
                    db_manager.update_players([playerwin], win=True, punteggio=punteggiowin, minutes=minutes,
                                              seconds=seconds)
                for playerlose in loser.split():
                    db_manager.update_players([playerlose], win=False, punteggio=punteggiolose, minutes=minutes,
                                              seconds=seconds)
                bot.say("[" + bris + "] : partita finita in WIN per " + winner + " in TEST " + place,log_chan)
            if self.draw:
                bot.say("NO ONE WINS")
                for totplayer in game.players:
                    db_manager.update_players([totplayer], win=False, punteggio=60, minutes=minutes, seconds=seconds)
                bot.say("[" + bris + "] : partita finita in DRAW in " + place, log_chan)

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
                "[" + bris + "] : " + trigger.nick + " ha provato a spostare una partita di BRISCOLA da " + oldchan + " a " + newchan + ", ma Trinacry non sta in " + oldchan + "...",
                log_chan)

            return
        if newchan in self.games:
            bot.reply(strings['CHANNEL_IN_USE'] % newchan)
            bot.say(
                "[" + bris + "] : " + trigger.nick + " ha provato a spostare una partita di BRISCOLA da " + oldchan + " a " + newchan + ", ma il canale era già occupato.",
                log_chan)
            return
        game = self.games.pop(oldchan)
        self.games[newchan] = game
        game.game_moved(bot, who, oldchan, newchan)

    def teams(self, bot, trigger):
        if trigger.sender not in self.games:
            return
        game = self.games[trigger.sender]
        game.teams(bot, trigger.nick)


brisbot = BrisBot()


@module.thread(True)
@module.commands("delplayer")
@module.example(".delplayer yorick")
@module.require_owner("OWNER REQUIRED")
@module.require_privmsg()
def delplayer(bot, trigger):
    try:
        db_manager.delete_player(trigger.group(3))
        bot.say("CANCELLAMENTO AVVENUTO CON SUCCESSO")
        bot.say("[" + bris + "] : Un admin (" + trigger.nick + ") ha cancellato " + trigger.group(3) + " dal database",
               log_chan)
    except:
        bot.say("OH NO!! ABBIAMO UN PROBLEMA COL DB!!")
        bot.say("[" + bris + "] : ERRORE DI CANCELLAZIONE DB causato da " + trigger.nick, log_chan)


@module.commands("adrank")
@module.example(".adrank tot")
@module.require_admin()
@module.require_privmsg()
def brisdbad(bot, trigger):
    if trigger.group(3) == "player":
        bot.say(db_manager.show_stats_admin(stat=AdminStats.PLAYER, username=trigger.group(4)))
        bot.say("[" + bris + "] : Un admin (" + trigger.nick + ") ha richiesto le stats di " + trigger.group(4), log_chan)
    else:
        stat_map = {
        "time": AdminStats.TIME,
        "win": AdminStats.WIN,
        "tot": AdminStats.TOT,
        "score": AdminStats.SCORE,
      }
        bot.say(db_manager.show_stats_admin(stat=stat_map[trigger.group(3)]))
        bot.say("[" + bris + "] : Un admin (" + trigger.nick + ") ha richiesto " + trigger.group(3), log_chan)



@module.commands("rank")
@module.example(".rank")
def rank(bot, trigger):
    try:
        bot.notice(db_manager.show_stats(username=trigger.nick) , trigger.nick)
        bot.say("[" + bris + "] : " + trigger.nick + " ha ottenuto il suo RANK. ", log_chan)
    except:
        bot.say("You are not in the db. Contact an admin if you feel this is an error.")
        bot.say("[" + bris + "] : " + trigger.nick + " ha provato a cercare il suo RANK, ma non esiste.", log_chan)


@module.commands("pointlist", "poli")
@module.priority("low")
def pointlist(bot, trigger):
    if trigger.sender in game_chan:
        for line in listpoint:
            bot.notice(line, trigger.nick)


@module.commands("briscola", "bris", "br")
@module.example(".briscola")
@module.priority('high')
@module.require_chanmsg
def start(bot, trigger):
    if trigger.sender in game_chan:
        brisbot.start(bot, trigger)
        bot.say("[" + bris + "] : START in " + trigger.sender + " da " + trigger.nick, log_chan)


@module.commands("language", "lan")
@module.example(".language italiano", ".lan english")
def language(bot, trigger):
    if trigger.sender in game_chan:
        brisbot.language(bot, trigger)


@module.commands('adminstop')
@module.example(".adminstop")
@module.priority('high')
def brisstop(bot, trigger):
    if trigger.sender in game_chan:
        brisbot.stop(bot, trigger)
        bot.say("[" + bris + "] : Admin ha fermato una partita in  " + trigger.sender, log_chan)


@module.commands('jo', "join")
@module.priority('high')
@module.require_chanmsg
def brisjoin(bot, trigger):
    if trigger.sender in game_chan:
         brisbot.join(bot, trigger)


@module.commands('quit', "qu")
@module.priority('high')
@module.require_chanmsg
def brisquit(bot, trigger):
    if trigger.sender in game_chan:
         brisbot.quit(bot, trigger)


@module.commands("rules", "ru")
@module.example(".ru italiano")
@module.priority("low")
def sendrules(bot, trigger):
    if trigger.sender in game_chan:
        if trigger.group(3) == "italiano":
            bot.notice("REGOLE DEL GIOCO: " + rules_ita, trigger.nick)
        else:
            bot.notice("GAME'S RULES: " + rules_eng, trigger.nick)


@module.commands('brismove', "brmove")
@module.priority('high')
@module.require_admin("You're not an admin.")
@module.example('.brismove #anotherchannel')
def brismove(bot, trigger):
    if trigger.sender in game_chan:
        brisbot.move_game(bot, trigger)


@module.commands('deal', "de")
@module.priority('medium')
@module.require_chanmsg
def brisdeal(bot, trigger):
    if trigger.sender in game_chan:
        brisbot.deal(bot, trigger)


@module.commands('play', "pl")
@module.priority('medium')
@module.require_chanmsg
def unoplay(bot, trigger):
    if trigger.sender in game_chan:
        brisbot.play(bot, trigger)


@module.commands("teams", "tm")
@module.require_admin("Only admins can see team scores.")
def teams(bot, trigger):
    if trigger.sender in game_chan:
        brisbot.teams(bot, trigger)


@module.commands('cards', "ca", "card")
@module.example(".cards")
@module.priority('medium')
@module.require_chanmsg
def unocards(bot, trigger):
    if trigger.sender in game_chan:
        brisbot.send_cards(bot, trigger)


@module.commands('brishelp', "brhelp")
@module.example(".brishelp italiano")
@module.priority('low')
def brishelp(bot, trigger):
    if trigger.sender in game_chan:
        if trigger.group(3) == "italiano":
            bot.notice("GUIDA: " + string_help_ita, trigger.nick)
        else:
            bot.notice("GUIDE: " + string_help_eng, trigger.nick)


@module.commands('brisgames', "brgm")
@module.priority('high')
@module.require_admin
def brisgames(bot, trigger):
    chans = []
    active = 0
    pending = 0
    with lock:
        for chan, game in brisbot.games.items():
            if game.startTime:
                chans.append(chan)
                active += 1
            else:
                chans.append(chan + " (pending)")
                pending += 1
    if not len(chans):
        bot.say('No ' + bris + ' games in progress, %s.' % trigger.nick)
        return
    g_active = "channel" if active == 1 else "channels"
    g_pending = "channel" if pending == 1 else "channels"
    chanlist = ", ".join(chans[:-2] + [" and ".join(chans[-2:])])
    bot.reply(
        bris + " is pending deal in %d %s and in progress in %d %s: %s. "
        % (pending, g_pending, active, g_active, chanlist))

@module.interval(1)
def afktime(bot):
    brisbot.afktime(bot)
    brisbot.checkidle(bot)