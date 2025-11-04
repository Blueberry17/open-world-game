import math

grids = [
    [["#", "#", "#", "#", "#", "#", "#", "#"],
     ["#", "S", ".", ".", ".", ".", ".", "#"],
     ["#", "#", ".", "#", ".", "#", ".", "#"],
     ["#", ".", ".", "#", ".", "#", ".", "#"],
     ["#", ".", ".", "#", ".", ".", ".", "#"],
     ["#", ".", "#", "#", ".", "#", "#", "#"],
     ["#", ".", ".", ".", ".", ".", "E", "#"],
     ["#", "#", "#", "#", "#", "#", "#", "#"]],
    [["#", "#", "#", "#", "#", "#", "#", "#"],
     ["#", "S", ".", ".", ".", "#", ".", "#"],
     ["#", "#", ".", "#", ".", "#", ".", "#"],
     ["#", ".", ".", "#", ".", "#", ".", "#"],
     ["#", ".", ".", "#", "#", "#", "#", "#"],
     ["#", ".", "#", "#", "#", ".", "#", "#"],
     ["#", ".", ".", ".", "#", ".", "E", "#"],
     ["#", "#", "#", "#", "#", "#", "#", "#"]]
]


def test(grid_index):
    """Selects a grid from <test_grids> and calls A_Star() to find a path from S (start) to E (end)"""

    grid = grids[grid_index]
    path = A_Star((1, 1), (6, 6), grid)

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "." and (col, row) in path:
                print("O", end="")
            else:
                print(grid[row][col], end="")
        print()
    print()


def A_Star(start, end, grid):
    """Implementation of A* algorithm for a 2D grid of values indicating whether each cell in the grid is an obstacle or
    not, returning the almost perfectly optimised path from a start to end location in the grid, using heuristics"""

    def heuristic(start, end):
        """Heuristic for A* algorithm, calculating the Pythagorean distance between two 2D grid points"""

        return math.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)

    open_set = PriorityQueue() # nodes to be evaluated
    open_set.enqueue(start, 0)

    path = dict() # stores the best path to a node
    gScore = dict() # cost from one node to another node
    gScore[start] = 0
    fScore = dict() # estimated total cost (gScore + heuristic)
    fScore[start] = heuristic(start, end)

    while not open_set.isEmpty():
        current_node = open_set.pop() # pop the element with the lowest priority

        if current_node == end:
            # if a path has been found from the start to the end, reconstruct and return this path
            sequence = []
            while current_node in path:
                sequence.append(current_node)
                current_node = path[current_node]
            return list(reversed(sequence))

        neighbours = []
        for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x_pos, y_pos = current_node[0] + direction[0], current_node[1] + direction[1]
            # checks if in bounds and not an obstacle
            if 0 <= x_pos < len(grid[0]) and 0 <= y_pos < len(grid) and grid[y_pos][x_pos] != "#":
                neighbours.append((x_pos, y_pos))

        for neighbour in neighbours:
            # new cost from <current_node> to <neighbour>
            new_gScore = gScore[current_node] + 1

            # check whether the new cost is the minimum cost
            if neighbour not in gScore or new_gScore < gScore[neighbour]:
                # update the cost from <current_node> to <neighbour> & the heuristic cost from <start> to <neighbour>
                gScore[neighbour] = new_gScore
                fScore[neighbour] = gScore[neighbour] + heuristic(neighbour, end)
                path[neighbour] = current_node

                # if the neighbour has not yet been explored at all, add it to the priority queue
                if neighbour not in open_set:
                    open_set.enqueue(neighbour, fScore[neighbour])

    # if no path can be found, the mob cannot move towards the player
    return []


class PriorityQueue(object):
    """Priority queue implementation as required by the A* algorithm, popping the lowest priority items first"""

    def __init__(self):
        self.queue = []

    def __iter__(self):
        """Returns an iterable object so that iterable methods like 'in' can be used on the queue"""

        return iter(self.queue)

    def isEmpty(self):
        """Returns a boolean for whether the queue is empty"""

        return len(self.queue) == 0

    def enqueue(self, data, priority):
        """Adds a new element to the priority queue"""

        self.queue.append((data, priority))

    def pop(self):
        """Pops the lowest priority item in the priority queue"""

        min_priority = float("inf")
        for item in self.queue:
            # if the item has a lower priority, it becomes the prospective item to pop
            if item[1] < min_priority:
                min_data, min_priority = item
        self.queue.remove((min_data, min_priority))

        return min_data


if __name__ == "__main__":
    test(0)
    test(1)
