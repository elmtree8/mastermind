'''The playing algorithm is very simple. Once the user chooses the level 
they’d like to play a list of the appropriate size is made and populated as 
the user makes guesses and the computer checks these against the code. 
The pruning strategy uses a list (states) of all 6^4 = 1296 possible guesses 
in the game and as the user makes guesses this list is pruned to exclude 
impossible codes based on the results of the users guess. The pruning strategy 
uses the fact that the result of checkmove(guess, code) = checkmove(code, 
guess) so for a guess, the states list can be traversed and compare each 
state checkmove(state, guess) with checkmove(guess, code). If checkmove(state, 
guess) == checkmove(guess, code) it is possible that the state is the code, 
if not we can remove that state from the list of possible codes. 
The minimax algorithm uses the fact that every given result for checkmove(a, 
b) is unique so when all 1296 potstates are checked against any given state 
in the already pruned list, they can be broken into 14 disjoint groups. The 
choice for the best state to guess next is the state which gives the smallest 
maximum size of these disjoint groups since the worst case scenario (that the 
answer is in the biggest of these disjoint groups) is the smallest group.'''

import random

class MastermindGame:
  def __init__(self, difficulty):
    self.won = False
    self.letters = ['a', 'b', 'c', 'd', 'e', 'f']
    self.moves = []
    for i in range(0, difficulty):
      self.moves.append(['*', '*', '*', '*', '', ''])
    self.code = ['', '', '', '']
    self.code_dict = {'a':0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0}
    for i in range(0,4):
      self.code[i] = random.choice(self.letters)
      self.code_dict[self.code[i]] = self.code_dict[self.code[i]] + 1
    self.states = []
    self.stateset = []
    for letter1 in self.letters:
      state = []
      for letter2 in self.letters:
        for letter3 in self.letters:
          for letter4 in self.letters:
            state = [letter1, letter2, letter3, letter4]
            self.states.append(state)
            self.stateset.append(state)

  def showboard(self):
    print('\nGame board:')
    for i in range(0, len(self.moves)):
      print(self.moves[i][0]+' '+self.moves[i][1]+' '+self.moves[i][2]+' '+
        self.moves[i][3]+' '+self.moves[i][4]+' '+self.moves[i][5]+'\n')
    print('\n')

  def showsolution(self):
    return self.code[0]+' '+self.code[1]+' '+self.code[2]+' '+self.code[3]+'\n'

  def makemove(self, guess, guessno):
    if len(guess) != 4:
      print('Not a valid move, try again')
      return guessno
    black, white = 0, 0
    guess_dict = {}
    for i in range(0, 4):
      if guess[i] not in self.letters:
        print('Not a valid move, try again')
        self.moves[guessno] = ['*', '*', '*', '*', '', '']
        return guessno
      self.moves[guessno][i] = guess[i]
    black, white = self.checkmove(guess, self.code, self.code_dict, guessno, 'make')
    self.moves[guessno][4] = str(black)
    self.moves[guessno][5] = str(white)
    if black == 4:
      self.won = True
      return guessno + 1
    self.code_dict = {'a':0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0}
    for i in range(0, 4):
      self.code_dict[self.code[i]] = self.code_dict[self.code[i]] + 1
    self.updatestates(guess, guessno)
    return guessno + 1

  def updatestates(self, guess, guessno):
    i = 0
    while i < len(self.states):
      guess_dict = {}
      state = self.states[i]
      if state == guess:
        self.states.remove(state)
      else:
        for char in guess:
          if char in guess_dict.keys():
            guess_dict[char] = guess_dict[char] + 1
          else:
            guess_dict[char] = 1
        if self.checkmove(state, guess, guess_dict, guessno, 'update') == False:
          self.states.remove(state)
          i = i - 1
        i = i + 1
    return 1

  def checkmove(self, guess, code, code_dict, guessno, type):
    black, white = 0, 0
    guess_dict = {}
    for i in range(0, 4):
      if guess[i] in guess_dict.keys():
        guess_dict[guess[i]] = guess_dict[guess[i]] + 1
      else:
        guess_dict[guess[i]] = 1
      if guess[i] == code[i]:
        black = black + 1
        code_dict[guess[i]] = code_dict[guess[i]] - 1
        guess_dict[guess[i]] = guess_dict[guess[i]] - 1
    for key in code_dict.keys():
      if key in guess_dict.keys():
        white = white + min(guess_dict[key], code_dict[key])
    if type == 'update':
      if str(black) == self.moves[guessno][4]:
        if str(white) == self.moves[guessno][5]:
          return True
      return False
    return (black, white)

  def genmove(self, guessno):
    beststate = self.states[0]
    minmaxscoreset = 1296
    if len(self.states) == 1296:
      return 'a a b b'
    for i in range(0, len(self.states)):
      state = self.states[i]
      if self.genscoreset(state) < minmaxscoreset:
        beststate = state
        minmaxscoreset = self.genscoreset(state)
    return 'Suggested move: '+beststate[0]+' '+beststate[1]+' '+beststate[2]+' '+beststate[3]

  def genscoreset(self, state):
    scores = [[0, 0, 0], [0, 1, 0], [0, 2, 0], [0, 3, 0], [0, 4, 0], [1, 0, 0], [1, 1, 0], [1, 2, 0], 
    [1, 3, 0], [2, 0, 0], [2, 1, 0], [2, 2, 0], [3, 0, 0], [4, 0, 0]]
    maxscoreset = 0
    for potstate in self.stateset:
      postate_dict = {}
      for i in range(0, 4):
        if potstate[i] in postate_dict.keys():
          postate_dict[potstate[i]] = postate_dict[potstate[i]] + 1
        else:
          postate_dict[potstate[i]] = 1
      (black, white) = self.checkmove(state, potstate, postate_dict, 0, 'check')
      for i in range(0, len(scores)):
        if scores[i][0] == black and scores[i][1] == white:
          scores[i][2] = scores[i][2] + 1
    for score in scores:
      if score[2] > maxscoreset:
        maxscoreset = score[2]
    return maxscoreset

def playgame(g, difficulty):
  guess_number = 0
  while g.won == False:
    if guess_number == difficulty:
      print('You lost! The code was ' + g.showsolution())
      return
    g.showboard()
    guess = input()
    if len(guess) == 0:
      print('\nThanks for trying, the code was ' + g.showsolution())
      return
    elif guess == '?':
      instructionmenu()
    elif guess == '!':
      print(g.genmove(guess_number))
    else:
      guess_number = g.makemove(guess.split(' '), guess_number)
  print('You won in ' + str(guess_number) + ' moves!!')
  g.showboard()

def instructionmenu():
  print('Difficulty levels:')
  print('   e           Easy game (12 guesses)')
  print('   i           Intermediate game (10 guesses)')
  print('   h           Hard game (8 guesses)')
  print('Commands:')
  print('   ?           Display menu')
  print('   !           Have a move suggested')
  print('   [return]    Quit')
  print('Instructions:')
  print('To make a move, type four space-separated characters into the '
    'command line.\nStones are represented by lower case letters a-f. '
    '\nThe game board output shows all past guesses and their results . '
    'The first number indicates each letter from the guess which was correct '
    'in both letter and position and the second indicates the existence of a '
    'correct letter placed in the wrong position')
  print('Example move: b a f d would output 2 0 for the example code b e c d')

def mainmenu():
  print('\nChoose a difficulty level')
  instructionmenu()
  while True:
    diff = input()
    if len(diff) == 0:
      print('\nThanks for playing!\n')
      return
    elif diff == 'e':
      g = MastermindGame(12)
      playgame(g, 12)
      return
    elif diff == 'i':
      g = MastermindGame(10)
      playgame(g, 10)
      return
    elif diff == 'h':
      g = MastermindGame(8)
      playgame(g, 8)
      return
    elif diff == '?':
        instructionmenu()
    else:
      print('Not a valid command')
      instructionmenu()

mainmenu()
