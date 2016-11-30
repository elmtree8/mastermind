class MastermindGame
  def initialize(difficulty)
    rand = Random.new
    @won = false
    @letters = ['a', 'b', 'c', 'd', 'e', 'f']
    @moves = []
    for i in 0..difficulty - 1
      @moves.push(['*', '*', '*', '*', '', ''])
    end
    @code = ['', '', '', '']
    @code_dict = {'a'=>0, 'b'=>0, 'c'=>0, 'd'=>0, 'e'=>0, 'f'=>0}
    for i in 0..3
      pos = rand(6)
      @code[i] = @letters[pos]
      @code_dict[@code[i]] = @code_dict[@code[i]] + 1
    end
    @states = []
    @stateset = []
    for letter1 in @letters
      state = []
      for letter2 in @letters
        for letter3 in @letters
          for letter4 in @letters
            state = [letter1, letter2, letter3, letter4]
            @states.push(state)
            @stateset.push(state)
          end
        end
      end
    end
  end

  def won()
    return @won
  end

  def showboard()
    puts "\nGame board:"
    for i in 0..@moves.length - 1
      puts "#{@moves[i][0]} #{@moves[i][1]} #{@moves[i][2]} #{@moves[i][3]} #{@moves[i][4]} #{@moves[i][5]}"
    end
    print "\n"
  end

  def showsolution()
    return @code[0]+' '+@code[1]+' '+@code[2]+' '+@code[3]
  end

  def makemove(guess, guessno)
    if guess.length != 4
      puts "Not a valid move, try again"
      return guessno
    end
    black, white = 0, 0
    guess_dict = {}
    for i in 0..3
      if not @letters.include? guess[i]
        puts "Not a valid move, try again"
        @moves[guessno] = ['*', '*', '*', '*', '', '']
        return guessno
      end
      @moves[guessno][i] = guess[i]
    end
    black, white = checkmove(guess, @code, @code_dict, guessno, 'make')
    @moves[guessno][4] = black.to_s
    @moves[guessno][5] = white.to_s
    if black == 4
      @won = true
      return guessno + 1
    end
    @code_dict = {'a'=>0, 'b'=>0, 'c'=>0, 'd'=>0, 'e'=>0, 'f'=>0}
    for i in 0..3
      @code_dict[@code[i]] = @code_dict[@code[i]] + 1
    end
    updatestates(guess, guessno)
    return guessno + 1
  end

  def updatestates(guess, guessno)
    i = 0
    while i < @states.length
      guess_dict = {}
      state = @states[i]
      if state == guess
        @states.delete(state)
      else
        for char in guess
          if guess_dict.keys.include? char
            guess_dict[char] = guess_dict[char] + 1
          else
            guess_dict[char] = 1
          end
        end
        if checkmove(state, guess, guess_dict, guessno, 'update') == false
          @states.delete(state)
          i -= 1
        end
        i += 1
      end
    end
    return 1
  end

  def checkmove(guess, code, code_dict, guessno, type)
    black, white = 0, 0
    guess_dict = {}
    for i in 0..3
      if guess_dict.keys.include? guess[i]
        guess_dict[guess[i]] = guess_dict[guess[i]] + 1
      else
        guess_dict[guess[i]] = 1
      end
      if guess[i] == code[i]
        black = black + 1
        code_dict[guess[i]] = code_dict[guess[i]] - 1
        guess_dict[guess[i]] = guess_dict[guess[i]] - 1
      end
    end
    for key in code_dict.keys
      if guess_dict.keys.include? key
        white = white + [guess_dict[key], code_dict[key]].min
      end
    end
    if type == 'update'
      if black.to_s == @moves[guessno][4]
        if white.to_s == @moves[guessno][5]
          return true
        end
      end
      return false
    end
    return black, white
  end

  def genmove(guessno)
    beststate = @states[0]
    minmaxscoreset = 1296
    if @states.length == 1296
      return 'a a b b'
    end
    for i in 0..@states.length - 1
      state = @states[i]
      if genscoreset(state) < minmaxscoreset
        beststate = state
        minmaxscoreset = genscoreset(state)
      end
    end
    return beststate[0]+' '+beststate[1]+' '+beststate[2]+' '+beststate[3]
  end

  def genscoreset(state)
    scores = [[0, 0, 0], [0, 1, 0], [0, 2, 0], [0, 3, 0], [0, 4, 0], [1, 0, 0], [1, 1, 0], [1, 2, 0], 
    [1, 3, 0], [2, 0, 0], [2, 1, 0], [2, 2, 0], [3, 0, 0], [4, 0, 0]]
    maxscoreset = 0
    for potstate in @stateset
      postate_dict = {}
      for i in 0..3
        if postate_dict.keys.include? potstate[i]
          postate_dict[potstate[i]] = postate_dict[potstate[i]] + 1
        else
          postate_dict[potstate[i]] = 1
        end
      end
      black, white = checkmove(state, potstate, postate_dict, 0, 'check')
      for i in 0..scores.length - 1
        if scores[i][0] == black and scores[i][1] == white
          scores[i][2] = scores[i][2] + 1
        end
      end
    end
    for score in scores
      if score[2] > maxscoreset
        maxscoreset = score[2]
      end
    end
    return maxscoreset
  end
end


def playgame(g, difficulty)
  guess_number = 0
  while g.won() == false
    if guess_number == difficulty
      puts "You lost! The code was #{g.showsolution()}"
      return
    end
    g.showboard()
    guess = gets.chomp
    if guess.length == 0
      puts "Thanks for trying, the code was #{g.showsolution()}"
      return
    elsif guess == '?'
      instructionmenu()
    elsif guess == '!'
      puts "Suggested move: #{g.genmove(guess_number)}"
    else
      guess_number = g.makemove(guess.split(' '), guess_number)
    end
  end
  puts "You won in #{guess_number} moves!!"
  g.showboard()
end

def instructionmenu()
  puts "Difficulty levels:"
  puts "  e           Easy game (12 guesses)"
  puts "  i           Intermediate game (10 guesses)"
  puts "  h           Hard game (8 guesses)"
  puts "Commands:"
  puts "  ?           Display menu"
  puts "  !           Have a move suggested"
  puts "  [return]    Quit"
  puts "Instructions:"
  puts " To make a move, type four space-separated characters into the 
    command line.\nStones are represented by lower case letters a-f. 
    \nThe game board output shows all past guesses and their results . 
    The first number indicates each letter from the guess which was correct 
    in both letter and position and the second indicates the existence of a 
    correct letter placed in the wrong position."
  puts "Example move: b a f d would output 2 0 for the example code b e c d"
end

def mainmenu()
  puts "Choose a difficulty level"
  instructionmenu()
  while true
    diff = gets.chomp
    if diff.length == 0
      puts "Thanks for playing!"
      return
    elsif diff == 'e'
      g = MastermindGame.new(12)
      playgame(g, 12)
      return
    elsif diff == 'i'
      g = MastermindGame.new(10)
      playgame(g, 10)
      return
    elsif diff == 'h'
      g = MastermindGame.new(8)
      playgame(g, 8)
      return
    elsif diff == '?'
        instructionmenu()
    else
      puts "Not a valid command"
      instructionmenu()
    end
  end
end

mainmenu()