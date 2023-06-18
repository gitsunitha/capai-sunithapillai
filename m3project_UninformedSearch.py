#!/usr/bin/env python
# coding: utf-8

# In[1]:


from abc import ABCMeta, abstractmethod
import random
import math, sys
import datetime, time

class DepthLimitedDFS():
    """
    Depth-limited DFS implementation

    Methods
    -------
    search(state, limit)
        Runs DFS starting from a given start state, and returns the list of actions to reach a goal state and the number of expanded states,
        but does not let the search go beyond the limit number of steps.
    successor(state)
        Finds the list of successors for a given state.
    goal_test(state)
        Checks if the current state is a goal state.
    """

    __metaclass__ = ABCMeta

    def search(self, state, limit):
        """
        Runs DFS starting from a given start state, and returns the list of actions to reach a goal state and the number of expanded states,
        but does not let the search go beyond the limit number of steps.
        Keeps the states on the path from the start state to the current state on memory to avoid cycles.

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
        path = []               # path from the start state to the current state
        solution = []           # sequence of actions from the start state to the current state
        visited_states = set()  # set of states in the path from the start state to the current state

        states_to_expand = [(state, 0, None)]                     # stack of states to be expanded
        while states_to_expand:
            state, depth, action = states_to_expand.pop()         # get next state to be expanded

            if state in visited_states or depth > limit:         # ignore cycles and states whose depth is greater than the limit
                continue

            while len(solution) > depth:                          # clean solution by removing states that are no longer used
                solution.pop()
                visited_states.remove(path.pop())

            num_expanded_states += 1                              # add current state to the solution
            visited_states.add(state)
            solution.append(action)
            path.append(state)

            if self.goal_test(state):                             # if current state is a goal state, return solution
                return solution[1:], num_expanded_states
            
            for action, child in self.successor(state):           # add successors to the stack of states to be expanded
                #print(states_to_expand.count)
                states_to_expand.append((child, depth+1, action))
            # if num_expanded_states >= 1500: 
            #     return None, num_expanded_states 
                # SP MOD :-  truncating search here

        return None, num_expanded_states                          # if no solution is found, return None

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


class IterativeDeepening(DepthLimitedDFS):
    """
    Iterative Deepening implementation

    Methods
    -------
    search(state, limit)
        Runs Iterative Deepening starting from a given start state, and returns the list of actions to reach a goal state and the number of expanded states.
    successor(state)
        Finds the list of successors for a given state.
    goal_test(state)
        Checks if the current state is a goal state.
    """

    __metaclass__ = ABCMeta

    def search(self, state):
        """
        Runs Iterative Deepening starting from a given start state, and returns the list of actions to reach a goal state and the number of expanded states.
        Keeps the states on the path from the start state to the current state on memory to avoid cycles.

        ----------
        Parameters
        state
            A tuple describing a unique world configuration.

        Returns
        -------
        list
            A list of actions that must be applied in sequence to the start state to reach the goal state, or None if no solution was found.
        int
            The number of states expanded during the search.
        """

        total_expanded_states = 0
        last_expanded_states = -1
        limit=0
        max_limit = 3 #LIMIT
        # Add a variable to keep track of the number of successor states
        num_successor_states = []
        # while True:
        while limit <= max_limit:

            if total_expanded_states >= 50000:
                #print("reached max state"+ str(limit)+" "+ str(total_expanded_states))
                break
    
            #print("current time:-", str(datetime.datetime.now()))
            solution, num_expanded_states = super(IterativeDeepening, self).search(state, limit)
            #print ("limit reached:"+str(limit)+" num_expanded_states"+str(num_expanded_states))

            if num_expanded_states == last_expanded_states :
                break

            last_expanded_states = num_expanded_states
            total_expanded_states += num_expanded_states


            # Append the number of successor states to the list
            num_successor_states.append(len(self.successor(state)))

            if solution is not None:
                return solution, total_expanded_states
            limit += 1
            #print ("limit reached:"+str(limit)+str(datetime.datetime.now()))

        #print("Number of successor states at each limit:", num_successor_states)
            
        return None, total_expanded_states

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



"""
This implementation is provided as a starting point. Feel free to change it as needed.
"""
class FourDominoes(IterativeDeepening):
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

    def __init__(self, N, state=None):
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
            self.state = self.__get_random_state()
    
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
        random.shuffle(temp) # if you comment this line, the state will be a final state (solution)
        return tuple(tuple(temp[i*self.N:(i+1)*self.N]) for i in range(self.N))

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

#sys.stdout = open('result.txt', 'w')

limit_states = 50000
uninformed_data = []
avg_expanded_states = 0;
goal_achieved = 0;
failed_to_reach_goal = 0;
reached_max_states = 0;
# Print the table headers
print("| Puzzle size || Uninformed    ||         ||         ||         || ")
print("|-------------||-------||------||---------||---------||---------||")
print("|             || Avg   || Goal || Fail #1 || Fail #2 || Avg time ")

for N in range(2,5):
    # run each 10 times
    avg_expanded_states = 0;
    goal_achieved = 0;
    failed_to_reach_goal = 0;
    reached_max_states = 0;
    for eachrun in range(0,10):
        #print("Start Run #:{}", eachrun)
        starttime = time.time()
        x = None
        x = FourDominoes(N)
        #x.show()

        # print('This state has {} successors!'.format(len(x.successor(x.state))))
        # if(x.goal_test(x.state)):
        #     print('This state is a goal state!')
        # else:
        #     print('This state is not a goal state!')

        solution, num_expanded_states = x.search(x.state)
        #print("Number of expanded states:", num_expanded_states)

        # if solution is not None:
        #     print("Solution found!")
        avg_expanded_states += (num_expanded_states/10)

        if solution is not None:
            # print("Actions:", solution)
            # for action in solution:
            #     print (action)
            #     x.move( action)
            #     x.show()    

            goal_achieved += 1;
        else:
            failed_to_reach_goal +=1;
            if num_expanded_states >= limit_states:
                reached_max_states += 1;
            #print("No solution found.")
        endtime = time.time()
        time_taken = (endtime - starttime)/10
    # x.move(((0,0),(1,1)))
    # x.show()

    # print('This state has {} successors!'.format(len(x.successor(x.state))))
    # if(x.goal_test(x.state)):
    #     print('This state is a goal state!')
    # else:
    #     print('This state is not a goal state!')
    
    # print()
    print("| {0}x{0}         || {1}     || {2}   || {3}       || {4}       || {5}   |".format(N, 
    round(avg_expanded_states), goal_achieved, failed_to_reach_goal, reached_max_states,round(time_taken)))


# Close the file
#sys.stdout.close()
