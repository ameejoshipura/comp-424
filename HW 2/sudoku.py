# -*- coding: utf-8 -*-

"""
TO RUN, execute:

python sudoku.py [player] [level]

where [player] = human, or agent (if you want your AI agent in solve_sudoku.py to play)
and   [level] = 0, 1, 2, or 3 (varying level difficulty)

"""

import copy, sys, re, time, pickle
import numpy as np

class Game:
    """    
    The method "play_game" simulates a game.
    """
    def __init__(self, start_state, fn_game, fn_transitions, fn_heuristic):
        self.initial_state = start_state
        self.goal = fn_game
        self.transitions = fn_transitions
        self.heuristic = fn_heuristic

    def play_game(self,player):
        state = self.initial_state
        
        print state
        for state in player(state, self.goal, self.transitions, self.heuristic):
            pass #Intermediate states don't matter

        print state #Print the full grid
        if self.goal(state):
            print 'You win!'
        else:
            print 'You lose!'

###################################
# Constraint Satisfaction Problem #
###################################
g_evaluation = []
class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        
    def arcs(self):
        return [(Xi, Xj) for Xi in self.constraints for Xj in self.constraints[Xi]]
        
    def copy(self):
        g_evaluation.append(self.domains)
        return CSP(self.variables, copy.deepcopy(self.domains), self.constraints)


###################################
# State, goal and csp for the Sudoku #
###################################
class SudokuState:

    def __init__(self, tableau=None):
        self.tableau = tableau
        if self.tableau is None:
            self.tableau = np.zeros([9,9],dtype='S1')
            self.tableau[:] = ' '

    # Find coordinates of target piece
    def find(self,case):
        return np.array(np.where(self.tableau == case))
    
    # Find cell coordinates except target piece
    def findNot(self,case):
        return np.array(np.where(self.tableau != case))
        
    # Place a value in grid at given position
    def place(self, coordinate, value):
        state = SudokuState()
        state.tableau = np.copy(self.tableau)
        state.tableau[coordinate] = value
        return state

    def __eq__(self,other):
        return (self.tableau == other.tableau).all()
        
    def __ne__(self,other):
        return not self == other
    
    def __hash__(self):
        return hash("".join(self.tableau.flat))
    
    def __str__(self):
        t = """
  012 345 678

0 {0}{1}{2}|{3}{4}{5}|{6}{7}{8}
1 {9}{10}{11}|{12}{13}{14}|{15}{16}{17}
2 {18}{19}{20}|{21}{22}{23}|{24}{25}{26}
  ---+---+---
3 {27}{28}{29}|{30}{31}{32}|{33}{34}{35}
4 {36}{37}{38}|{39}{40}{41}|{42}{43}{44}
5 {45}{46}{47}|{48}{49}{50}|{51}{52}{53}
  ---+---+---
6 {54}{55}{56}|{57}{58}{59}|{60}{61}{62}
7 {63}{64}{65}|{66}{67}{68}|{69}{70}{71}
8 {72}{73}{74}|{75}{76}{77}|{78}{79}{80}
"""
        return t.format(*self.tableau.flat)

class SudokuUtil:
    @staticmethod
    def generate(seed):
        if seed is None:
            # Initialization of Sudoku for validation (Difficult).
            txt = "     4  7" + \
                  " 1       " + \
                  "796 3    " + \
                  "4    2   " + \
                  " 3  6  5 " + \
                  "   7    1" + \
                  "    5 932" + \
                  "       6 " + \
                  "2  8     "
                  
        elif seed == 1:
            #Sudoku - Beginner
            txt = "  74  1  " + \
                  " 4 8   2 " + \
                  " 8  29 7 " + \
                  "  5    41" + \
                  "  2   6  " + \
                  "93    5  " + \
                  " 2 75  1 " + \
                  " 5   6 3 " + \
                  "  8  34  "
        elif seed == 2:
            #Sudoku - Medium
            txt = "  53     " + \
                  "8      2 " + \
                  " 7  1 5  " + \
                  "4    53  " + \
                  " 1  7   6" + \
                  "  32   8 " + \
                  " 6 5    9" + \
                  "  4    3 " + \
                  "     97  "
        elif seed == 3:
            #Sudoku - Very difficult
            txt = "85   24  " + \
                  "72      9" + \
                  "  4      " + \
                  "   1 7  2" + \
                  "3 5   9  " + \
                  " 4       " + \
                  "    8  7 " + \
                  " 17      " + \
                  "    36 4 "
        else:
            #Sudoku - Very beginner
            txt = "3 1286 75" + \
                  "47 359 8 " + \
                  "86 174392" + \
                  "6 7823 1 " + \
                  "238 41567" + \
                  "9 47  238" + \
                  "7 349 156" + \
                  "1 65 7 49" + \
                  "54  18723"

        return SudokuState(SudokuUtil.convert(txt))

    @staticmethod
    def convert(txt):
        return np.array(list(txt),dtype="S1").reshape(9,9)

    @staticmethod
    def csp2state(csp, assignments={}):
        state = SudokuState()
        for pos,d in csp.domains.items():
            if len(d) == 1:
                state = state.place(pos, d[0])
                
        for pos,v in assignments.items():
            state = state.place(pos, v)
            
        return state
        
def allUnique(sequence):
    sequence = sequence.flatten()
    for i,value in enumerate(sequence):
        if value in sequence[i+1:]:
            return False

    return True

def sudoku_goal(state):
    if state.find(' ').shape[1] != 0:
        return False

    isDone = True
    for i in range(9):
        isDone &= allUnique(state.tableau[i,:])
        isDone &= allUnique(state.tableau[:,i])
        subY,subX = i//9, (i%3)*3
        isDone &= allUnique(state.tableau[subY:subY+3,subX:subX+3])

    return isDone

def sudoku_solution(state, noGame):
    if noGame is None:
        return "".join(map(str, state.tableau.flatten())) == "382514697514976823796238514451392786837461259629785341148657932975123468263849175"
        
    if noGame == 1:
        return "".join(map(str, state.tableau.flatten())) == "297435168143867925586129374865392741712548693934671582329754816451986237678213459"
    
    if noGame == 2:
        return "".join(map(str, state.tableau.flatten())) == "145327698839654127672918543496185372218473956753296481367542819984761235521839764"
    
    if noGame == 3:
        return "".join(map(str, state.tableau.flatten())) == "859612437723854169164379528986147352375268914241593786432981675617425893598736241"
        
    return "".join(map(str, state.tableau.flatten())) == "391286475472359681865174392657823914238941567914765238783492156126537849549618723"

def createCSP(state):
    #Variables represent empty cells
    variables = zip(*state.find(' '))
    
    #The domain of empty cells is all values [1-9]
    domains = {}
    for V in variables:
        domains[V] = [str(i) for i in range(1,10)]
        
    #For filled cells, the domain is the assigned value
    for V in zip(*state.findNot(' ')):
        domains[V] = [state.tableau[V],]
        variables.append(V)

    #Constraints are added for all associated variables.
    constraints = {}
    for V in variables:
        y,x = V
        constraints[V] = []
        constraints[V] += [(y,i) for i in range(9)] #Line constraints
        constraints[V] += [(i,x) for i in range(9)] #Column constraints
        
        blockY, blockX = (y//3)*3, (x//3)*3
        constraints[V] += [(blockY+i//3, blockX+i%3) for i in range(9)] #Block constraints
        
        constraints[V] = set(constraints[V]) #Constraints must be unique
        constraints[V].remove(V) #No self-constraints
        
    return CSP(variables, domains, constraints)

            
###########################
# Alternate player(s) #
###########################
regex_action = r'^\(([0-8]),([0-8])\)\s*=\s*([1-9])$'

def is_move_legal(X,v, state):
    isLegal = True
    isLegal &= v not in state.tableau[X[0],:] #Line constraints
    isLegal &= v not in state.tableau[:,X[1]] #Column constraints
    blockY,blockX = (X[0]//3)*3, (X[1]//3)*3 
    isLegal &= v not in state.tableau[blockY:blockY+3, blockX:blockX+3] #Block constraints
    return isLegal

def player_human(start_state, fn_game, fn_transitions, fn_heuristic):
    state = start_state
    while not fn_game(state):
        action = raw_input('Enter a coordinate and a value. (ex. (Y,X) = V)\n')
        while True:
            try:
                y,x,v = re.match(regex_action, action).groups()
                y,x = int(y),int(x)

                if (y,x) not in fn_transitions(state):
                    raise NamedError('Illegal move!')

                if not is_move_legal((y,x), v, state):
                    print "Illegal move!"
                    raise NamedError('Illegal move!')
                    
                break
            except:
                action = raw_input('Sudoku game not configured for human play at this time. Sorry!\n')

        state = state.place((y,x), v)
        yield state

##############################
# Execution script
##############################
def main():
    usage = """Usage: python sudoku.py player [level]

where "player" is "human" or "agent"
and "level" is a number [0-3] (optional).
    -> 0: Very beginner
    -> 1: Beginner
    -> 2: Intermediate
    -> 3: Very difficult
    -> Default: Difficult + Evaluation"""

    if not (len(sys.argv) == 2 or len(sys.argv) == 3):
        print usage
        return

    player = sys.argv[1]
    level = None
    
    if len(sys.argv) == 3:
        try:
            level = int(sys.argv[2])
        except ValueError:
            print usage
            return
        
    if player not in ['human','agent']:
        print usage
        return

    sudokuState = SudokuUtil.generate(level)
        
    # Play a game of Sudoku
    sudoku = Game(sudokuState, sudoku_goal, None, None)
    
    # For human play
    if player == 'human':
        sudoku.play_game(player_human)
    
    # For playing with AI agent
    if player == 'agent':
        import solve_sudoku as solution
        
        # Simulate player using assignemnts returned by backtracking_search
        def playerAgent(start_state, fn_finalState, fn_transitions, fn_heuristic):
            assignments = solution.backtracking_search(createCSP(start_state))
            
            #Generate states from assignments
            def iterStates():
                state = start_state
                for pos,v in assignments.items():
                    state = state.place(pos,v)
                    yield state

            return iterStates()

        timeBegin = time.time()
        sudoku.play_game(playerAgent)
            
        ##### Evaluation #####
        print "\n#########\n# Infos #\n#########"
        
        nbEmptyCells = len(sudokuState.find(' ')[0])
        nbMoves = len(g_evaluation)
        taillesDomaine = np.array(map(lambda e:sum(map(len, dict(e).values())), g_evaluation))
        nbBacktracks = nbMoves - nbEmptyCells
            
        print "Nb. empty cells: {0}".format(nbEmptyCells)
        print "Nb. moves: {0}".format(nbMoves)

        if nbMoves == 0:
            print "* No moves made.  Be careful, the CSP object must be passed to the backtracking search by copy. -> csp.copy() <-"
            return

        print "Nb. backtracks: {0}".format(nbBacktracks)
        print "Time elapsed: %0.2f sec." % (time.time()-timeBegin)        

        solutionFound = SudokuUtil.csp2state(CSP([],dict(g_evaluation[-1]),[]))
        if not sudoku_goal(solutionFound):
            print "* The solution found is not valid!"
            
        if not sudoku_solution(solutionFound, level):
            print "* The solution found is incorrect!"

        if level is None:
            print "\n###############\n# Validations #\n###############"
            #sol_nbMoves = len(g_evaluation)
            #sol_nbBacktracks = sol_nbMoves - len(sudokuState.find(' ')[0])
            #pickle.dump((sol_nbMoves, sol_nbBacktracks), open('sudoku_solution.pkl', 'w'))
            
            sol_nbMoves, sol_nbBacktracks = pickle.load(open('sudoku_solution.pkl'))
            
            print "Nb. moves: {0} vs. {1}".format(nbMoves,sol_nbMoves)
            if sol_nbMoves < nbMoves:
                print "* Your number of tries ({0}) can be improved (Objectif: {1})!".format(nbBacktracks,sol_nbBacktracks)

            print "Nb. backtracks: {0} vs. {1}".format(nbBacktracks,sol_nbBacktracks)
            if sol_nbBacktracks < nbBacktracks:
                print "* Your number of backtracks ({0}) can be reduced (Objectif: {1})!".format(nbBacktracks,sol_nbBacktracks)


if __name__ == "__main__":
    main()