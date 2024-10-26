import numpy as np

class CostMatrixState:
    def __init__(self, teammate_positions, formation_positions):
        self.teammate_positions = np.array(teammate_positions)
        self.formation_positions = np.array(formation_positions)
        self.cost_matrix = self.calculateCostMatrix()
        self.Copy = self.cost_matrix.copy()

        self.row_uncovered = np.ones(len(teammate_positions), dtype=bool)
        self.col_uncovered = np.ones(len(formation_positions), dtype=bool)
        self.Z0_r = 0
        self.Z0_c = 0
        self.path = np.zeros((len(teammate_positions) + len(formation_positions), 2), dtype=int)
        self.marked = np.zeros(self.cost_matrix.shape, dtype=int)

    def calculateCostMatrix(self):
        rows, columns = len(self.teammate_positions), len(self.formation_positions)
        cost_matrix = np.zeros((rows, columns))
        for i in range(rows):
            for j in range(columns):
                cost_matrix[i, j] = np.linalg.norm(self.teammate_positions[i] - self.formation_positions[j])
        return cost_matrix

    def clearCovers(self):
        self.row_uncovered[:] = True
        self.col_uncovered[:] = True

    def findPrime(self, row):
        column = np.argmax(self.marked[row] == 2)
        if self.marked[row, column] != 2:
            column = -1
        return column

def subtractMinima(state):

    state.Copy -= state.Copy.min(axis=1)[:, np.newaxis] # subtract a column minimum from all elements in column
    state.Copy -= state.Copy.min(axis=0)[np.newaxis, :] # subtract a row minimum from all elements in row

    for i, j in zip(*np.where(state.Copy == 0)): # looks for elements that are equal to zero
        if state.col_uncovered[j] and state.row_uncovered[i]: # if row and column of zero element are uncovered
            state.marked[i, j] = 1
            state.col_uncovered[j] = False
            state.row_uncovered[i] = False

    state.clearCovers()
    return countCoveredRows

def countCoveredRows(state):
    marked = (state.marked == 1)
    state.col_uncovered[np.any(marked, axis=0)] = False

    if marked.sum() < state.Copy.shape[0]:
        return additionalZeros

def additionalZeros(state):
    C = (state.Copy == 0).astype(int)
    covered_C = C * state.row_uncovered[:, np.newaxis]
    covered_C *= state.col_uncovered.astype(dtype=int, copy=False)
    rows = state.Copy.shape[0]
    columns = state.Copy.shape[1]
    while True:
        row, col = np.unravel_index(np.argmax(covered_C), (rows, columns))
        if covered_C[row, col] == 0:
            return adjustMatrix
        else:
            state.marked[row, col] = 2
            star_col = np.argmax(state.marked[row] == 1)
            if not state.marked[row, star_col] == 1:
                state.Z0_r = row
                state.Z0_c = col
                return buildPath
            else:
                col = star_col
                state.row_uncovered[row] = False
                state.col_uncovered[col] = True
                covered_C[:, col] = C[:, col] * (
                    state.row_uncovered.astype(dtype=int, copy=False))
                covered_C[row] = 0

def buildPath(state):
    count = 0
    path = state.path
    path[count, 0] = state.Z0_r
    path[count, 1] = state.Z0_c

    while True:
        row = np.argmax(state.marked[:, path[count, 1]] == 1)
        if not state.marked[row, path[count, 1]] == 1:
            break
        else:
            count += 1
            path[count, 0] = row
            path[count, 1] = path[count - 1, 1]

        col = np.argmax(state.marked[path[count, 0]] == 2)
        if state.marked[row, col] != 2:
            col = -1
        count += 1
        path[count, 0] = path[count - 1, 0]
        path[count, 1] = col

    for i in range(count + 1):
        if state.marked[path[i, 0], path[i, 1]] == 1:
            state.marked[path[i, 0], path[i, 1]] = 0
        else:
            state.marked[path[i, 0], path[i, 1]] = 1

    state.clearCovers()
    state.marked[state.marked == 2] = 0
    return countCoveredRows

def adjustMatrix(state):
    if np.any(state.row_uncovered) and np.any(state.col_uncovered):
        minval = np.min(state.Copy[state.row_uncovered], axis=0)
        minval = np.min(minval[state.col_uncovered])
        state.Copy[np.logical_not(state.row_uncovered)] += minval
        state.Copy[:, state.col_uncovered] -= minval
    return additionalZeros

def hungarianAlgorithm(teammate_positions, formation_positions):

    State = CostMatrixState(teammate_positions, formation_positions)

    step = subtractMinima

    while step is not None:
        step = step(State)

    results = np.array(np.where(State.marked == 1)).T

    return results

def role_assignment(teammate_positions, formation_positions): 

    # Input : Locations of all teammate locations and positions
    # Output : Map from unum -> positions
    #-----------------------------------------------------------#
    
    assignments = hungarianAlgorithm(teammate_positions, formation_positions)

    point_preferences = {}
    for i in range(len(assignments)):
        player_assignment = assignments[i][1] # formation position assigned to player i
        point_preferences[i+1] = np.array([formation_positions[player_assignment][0], formation_positions[player_assignment][1]])
    return point_preferences


def pass_reciever_selector(player_unum, teammate_positions, final_target):
    
    # Input : Locations of all teammates and a final target you wish the ball to finish at
    # Output : Target Location in 2d of the player who is recieveing the ball
    #-----------------------------------------------------------#

    # Example
    pass_reciever_unum = player_unum + 1                  #This starts indexing at 1, therefore player 1 wants to pass to player 2

    close_enough = np.linalg.norm(teammate_positions[player_unum - 1] - np.array([15, 0])) <= 7

    if close_enough:
        target = (15, 0)
    elif pass_reciever_unum != 12:
        target = teammate_positions[pass_reciever_unum-1] #This is 0 indexed so we actually need to minus 1
    else:
        target = final_target
    
    return target
