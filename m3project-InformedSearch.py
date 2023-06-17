
from abc import ABCMeta, abstractmethod
from queue import PriorityQueue
import random
import math


class Domino():
    """
    Implementation of a 4-sided domino tile.

    Methods
    -------
    is_above(other)
        Checks of the tile is above the other tile.
    is_under(other)
        Checks of the tile is under the other tile.
    is_on_the_left_of(other)
        Checks of the tile is on the left of the other tile.
    is_on_the_right_of(other)
        Checks of the tile is on the right of the other tile.
    """
    def __init__(self, top: int, right: int, bottom: int, left: int):
        assert isinstance(top, int) and isinstance(right, int) and isinstance(bottom, int) and isinstance(left, int), "Invalid tile value!"
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    def is_above(self, other):
        assert isinstance(other, Domino), "Invalid tile type!"
        return self.bottom == other.top
    
    def is_under(self, other):
        assert isinstance(other, Domino), "Invalid tile type!"
        return self.top == other.bottom
    
    def is_on_the_left_of(self, other):
        assert isinstance(other, Domino), "Invalid tile type!"
        return self.right == other.left
    
    def is_on_the_right_of(self, other):
        assert isinstance(other, Domino), "Invalid tile type!"
        return self.left == other.right

class Astar():
    """
    A* implementation

    Methods
    -------
    search(state)
        Runs A* starting from a given start state, and returns the list of actions to reach a goal state and the number of expanded states.
    successor(state)
        Finds the list of successors for a given state.
    goal_test(state)
        Checks if the current state is a goal state.
    """

    __metaclass__ = ABCMeta

    def search(self, state):
        """
        Runs A* starting from a given start state, and returns the list of actions to reach a goal state and the number of expanded states.

        Parameters
        ----------
        state
            A tuple describing a unique world configuration.

        Returns
        -------
        list
            A list of actions that must be applied in sequence to the start state to reach the goal state, or None if no solution was found.
        int
            The number of states expanded during the search.
        """

        num_expanded_states = 0 # number of states expanded during the search
        expanded_states = []    # path from the start state to the current state
        visited_states = set()  # set of states in the path from the start state to the current state

        states_to_expand = PriorityQueue()                        # stack of states to be expanded
        states_to_expand.put((math.inf, 0, state, -1, None))
        while not states_to_expand.empty():
            heur_cost, path_cost, state, parent, action = states_to_expand.get() # get next state to be expanded

            if state in visited_states:                           # ignore cycles
                continue

            num_expanded_states += 1                              # add current state to the solution
            visited_states.add(state)
            expanded_states.append((parent, action))

            if self.goal_test(state):                             # if current state is a goal state, return solution
                solution = []
                while parent != -1:
                    solution.append(action)
                    parent, action = expanded_states[parent]
                solution.reverse()
                return solution, path_cost, num_expanded_states
            
            for action, child, act_cost, heur_cost in self.successor(state): # add successors to the stack of states to be expanded
                heur_cost = self.heuristicfunction(child)
                path_cost = 1
                act_cost = 1
                states_to_expand.put((heur_cost+act_cost+path_cost, act_cost+path_cost, child, num_expanded_states-1, action))

        return None, math.inf, num_expanded_states                # if no solution is found, return None

    @abstractmethod
    def successor(self, state):
        """
        Finds the list of successors for a given state.

        Parameters
        ----------
        state
            A tuple describing a unique world configuration.

        Returns
        -------
        list
            A list of pairs (action,state) with all states that can be reached from the given state with a single action.
        """
        pass

    @abstractmethod
    def goal_test(self, state):
        """
        Checks if the current state is a goal state.

        Parameters
        ----------
        state
            A tuple describing a unique world configuration.

        Returns
        -------
        bool
             True if the given state is a goal state, and False otherwise.
        """
        pass
       
 
    def heuristicfunction(self, state):
        """
        This the heuristic for this informed search
        Calculates the number of dominos that are not in the goal state
        the number of dominoes that need to move 
         The more costly it is to attain the goal state so we should choose the 

        Parameters
        ----------
        state : one configuration of the NxN grid

        Returns
        -------
        int: the number of dominos that need to be moved to attain the goal state
        """
        tilecount = 0
        goal_state = self.goal_test
        for i in range(self.N):
            for j in range(self.N):
                if state[i][j] != self.goal_state[i][j]:
                    tilecount += 1

        return tilecount

"""
This implementation is provided as a starting point. Feel free to change it as needed.
"""
class FourDominoes(Astar):
    """
    Implementation of the 4-sided dominoes puzzle.

    Methods
    -------
    show()
        Visualize the current state.
    move(action)
        Apply an action to the current state.
    successor(state)
        Finds the list of successors for a given state.
    goal_test(state)
        Checks if the current state is a goal state.
    """

    def __init__(self, N, state=None, goal_state=None):
        """
        Parameters
        ----------
        N
            Grid size (puzzle contains N^2 tiles)
        state
            Initial state configuration. If None is provided, a random one is created.
        """
        assert N >= 2 and N <= 4, "Invalid grid size!"
        self.N = N

        if state is not None:
            assert len(state) == self.N, "Invalid state size!"
            for row in state:
                assert len(row) == self.N, "Invalid state size!"
                for tile in row:
                    assert isinstance(tile, Domino), "Invalid state type!"
            self.state = state
        else:
            self.state, self.goal_state = self.__get_random_state()
            print(self.state)
            print(self.goal_state)
    
    def __get_random_state(self):
        """
        Generates a random puzzle configuration (grid of dominoes)

        Return
        ----------
        tuple
            A tuple describing a unique puzzle configuration.
        """
        temp = []
        for i in range(self.N):
            for j in range(self.N):
                domino = Domino(
                    random.randint(1,9) if i == 0 else temp[(i-1)*self.N+j].bottom, # top
                    random.randint(1,9),                                            # right
                    random.randint(1,9),                                            # bottom
                    random.randint(1,9) if j == 0 else temp[i*self.N+j-1].right     #left
                )
                temp.append(domino)
        temp_goal_state = list(temp) 
        random.shuffle(temp) # if you comment this line, the state will be a final state (solution)
        return (tuple(tuple(temp[i*self.N:(i+1)*self.N]) for i in range(self.N)), 
                tuple(tuple(temp_goal_state[i*self.N:(i+1)*self.N]) for i in range(self.N))
        )
    


    def show(self):
        """
        Prints the current state.
        """
        #line
        print('╔', end='')
        for i in range(self.N):
            print('═══', end='╦' if i < self.N-1 else '╗\n')
        for i in range(self.N):
            # first line of tile
            print('║', end='')
            for j in range(self.N):
                print('╲{}╱║'.format(self.state[i][j].top), end='' if j < self.N-1 else '\n')
            # second line of tile
            print('║', end='')
            for j in range(self.N):
                print('{}╳{}║'.format(self.state[i][j].left, self.state[i][j].right), end='' if j < self.N-1 else '\n')
            # third line of tile
            print('║', end='')
            for j in range(self.N):
                print('╱{}╲║'.format(self.state[i][j].bottom), end='' if j < self.N-1 else '\n')
            # line
            print('╠' if i < self.N-1 else '╚', end='')
            for j in range(self.N):
                print('═══', end='╬' if i < self.N-1 and j < self.N-1 else '╩' if i == self.N-1 and j < self.N-1 else '╣\n' if i < self.N-1 else '╝\n')

    def show_goal_state(self):
        """
        Prints the goal state.
        """
        #line
        print('╔', end='')
        for i in range(self.N):
            print('═══', end='╦' if i < self.N-1 else '╗\n')
        for i in range(self.N):
            # first line of tile
            print('║', end='')
            for j in range(self.N):
                print('╲{}╱║'.format(self.goal_state[i][j].top), end='' if j < self.N-1 else '\n')
            # second line of tile
            print('║', end='')
            for j in range(self.N):
                print('{}╳{}║'.format(self.goal_state[i][j].left, self.goal_state[i][j].right), end='' if j < self.N-1 else '\n')
            # third line of tile
            print('║', end='')
            for j in range(self.N):
                print('╱{}╲║'.format(self.goal_state[i][j].bottom), end='' if j < self.N-1 else '\n')
            # line
            print('╠' if i < self.N-1 else '╚', end='')
            for j in range(self.N):
                print('═══', end='╬' if i < self.N-1 and j < self.N-1 else '╩' if i == self.N-1 and j < self.N-1 else '╣\n' if i < self.N-1 else '╝\n')

    def move(self, action):
        """
        Uses a given action to update the current state of the puzzle. Assumes the action is valid.

        Parameters
        ----------
        action
            Tuple with coordinates of two tiles to be swapped ((row1,col1), (row2,col2))
        """
        assert len(action) == 2 and all(len(coord) == 2 for coord in action) and all(isinstance(x, int) and x >= 0 and x < self.N for coord in action for x in coord), "Invalid action!"
        (r1, c1), (r2, c2) = action
        temp = [list(row) for row in self.state]
        temp[r1][c1], temp[r2][c2] = temp[r2][c2], temp[r1][c1]
        self.state = tuple(tuple(x) for x in temp)

    def successor(self, state):
        """
        Finds the list of successors for a given state.

        Parameters
        ----------
        state
            A tuple describing a unique puzzle configuration.

        Returns
        -------
        list
            A list of pairs (action,state) with all states that can be reached from the given state with a single action.
        """

        successors = []
        for i in range(self.N*self.N):
            r1 = i//self.N
            c1 = i%self.N
            for j in range(i+1, self.N*self.N):
                r2 = j//self.N
                c2 = j%self.N
                action = ((r1,c1), (r2,c2))
                copy = FourDominoes(self.N, state)
                copy.move(action)
                cost = copy.heuristicfunction(copy.state) + 1  # Update the cost calculation based on your heuristic
                
                successors.append((action,copy.state))
        return successors

    def goal_test(self, state):
        """
        Checks if the given state is a goal state.

        Parameters
        ----------
        state
            A tuple describing a unique puzzle configuration.

        Returns
        -------
        bool
             True if the given state is a goal state, and False otherwise.
        """

        for i in range(self.N):
            for j in range(self.N):
                if i > 0 and not state[i][j].is_under(state[i-1][j]):
                    return False
                if j > 0 and not state[i][j].is_on_the_right_of(state[i][j-1]):
    
                    return False
        return True

N = 3
x = FourDominoes(N)
x.show()
x.show_goal_state()

# for N in range(2,5):
#     print('-----------------')
#     print('{}x{} grid of tiles'.format(N,N))
#     print('-----------------')

#     x = FourDominoes(N)
#     x.show()

#     print('This state has {} successors!'.format(len(x.successor(x.state))))
#     if(x.goal_test(x.state)):
#         print('This state is a goal state!')
#     else:
#         print('This state is not a goal state!')

#     x.move(((0,0),(1,1)))
#     x.show()
#     #search
#     solution, num_expanded_states = x.search(x.state)
#     print('This state has {} successors!'.format(len(x.successor(x.state))))
#     if(x.goal_test(x.state)):
#         print('This state is a goal state!')
#     else:
#         print('This state is not a goal state!')
    
#     print()




