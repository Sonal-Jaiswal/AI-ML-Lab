import heapq

class PuzzleState:
    def __init__(self, board, parent=None, move="", depth=0, cost=0):
        self.board = board
        self.parent = parent  # To reconstruct the path
        self.move = move  # Move that led to this state
        self.depth = depth  # Number of moves taken
        self.cost = cost  # Total cost (g(n) + h(n))

    def __lt__(self, other):
        """ Allows priority queue to compare states based on cost """
        return self.cost < other.cost

    def __eq__(self, other):
        """ Equality check based on board state """
        return self.board == other.board

    def __hash__(self):
        """ Hashing function to store visited states in a set """
        return hash(str(self.board))

def find_empty_tile(board):
    """ Find the position of the empty tile (0) """
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                return i, j  # Row, Column

def get_possible_moves(board):
    """ Returns all possible moves (children states) from the current board """
    row, col = find_empty_tile(board)
    moves = []
    directions = {
        "Up": (-1, 0),
        "Down": (1, 0),
        "Left": (0, -1),
        "Right": (0, 1)
    }

    for move, (dr, dc) in directions.items():
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_board = [row[:] for row in board]  # Create a copy
            new_board[row][col], new_board[new_row][new_col] = new_board[new_row][new_col], new_board[row][col]
            moves.append((move, new_board))

    return moves

def misplaced_tiles(board, goal):
    """ Returns the number of misplaced tiles compared to the goal state """
    return sum(1 for i in range(3) for j in range(3) if board[i][j] and board[i][j] != goal[i][j])

def manhattan_distance(board, goal):
    """ Returns the sum of Manhattan distances of all tiles from their goal positions """
    distance = 0
    goal_positions = {goal[i][j]: (i, j) for i in range(3) for j in range(3)}

    for i in range(3):
        for j in range(3):
            if board[i][j] != 0:  # Ignore empty space
                goal_x, goal_y = goal_positions[board[i][j]]
                distance += abs(goal_x - i) + abs(goal_y - j)

    return distance

def a_star_search(start, goal, heuristic):
    """ A* algorithm to solve the 8-puzzle """
    start_state = PuzzleState(start, cost=heuristic(start, goal))
    goal_state = PuzzleState(goal)

    frontier = []  # Priority queue (min-heap)
    heapq.heappush(frontier, start_state)

    visited = set()  # To track visited states
    nodes_explored = 0  # Count how many nodes we visit

    while frontier:
        current = heapq.heappop(frontier)
        nodes_explored += 1

        if current.board == goal_state.board:
            return reconstruct_path(current), nodes_explored, current.depth

        visited.add(current)

        for move, new_board in get_possible_moves(current.board):
            new_state = PuzzleState(
                new_board,
                parent=current,
                move=move,
                depth=current.depth + 1,
                cost=current.depth + 1 + heuristic(new_board, goal)  # g(n) + h(n)
            )

            if new_state not in visited:
                heapq.heappush(frontier, new_state)
                visited.add(new_state)

    return None, nodes_explored, -1  # No solution found

def reconstruct_path(state):
    """ Traces back the moves from goal to start """
    path = []
    while state.parent:
        path.append(state.move)
        state = state.parent
    return path[::-1]  # Reverse the path to get the correct order

# Define start and goal states
start_state = [
    [1, 2, 3],
    [4, 0, 5],
    [7, 8, 6]
]

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

# Run A* with H1 (Misplaced Tiles)
path_h1, nodes_h1, depth_h1 = a_star_search(start_state, goal_state, misplaced_tiles)
print("\nA* with H1 (Misplaced Tiles):")
print(f"Solution Path: {path_h1}")
print(f"Nodes Explored: {nodes_h1}")
print(f"Solution Depth: {depth_h1}")

# Run A* with H2 (Manhattan Distance)
path_h2, nodes_h2, depth_h2 = a_star_search(start_state, goal_state, manhattan_distance)
print("\nA* with H2 (Manhattan Distance):")
print(f"Solution Path: {path_h2}")
print(f"Nodes Explored: {nodes_h2}")
print(f"Solution Depth: {depth_h2}")