import heapq
from PIL import Image, ImageDraw

class Node:
    def __init__(self, state, parent, action, cost=0):
        self.state = state  
        self.parent = parent
        self.action = action
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

class Maze:
    def __init__(self, filename):
        with open(filename) as f:
            self.maze = [list(line.rstrip()) for line in f]

        self.height = len(self.maze)
        self.width = max(len(row) for row in self.maze)
        self.start = self.goal = None
        self.walls = set()

        for i, row in enumerate(self.maze):
            for j, cell in enumerate(row):
                if cell == 'A':
                    self.start = (i, j)
                elif cell == 'B':
                    self.goal = (i, j)
                elif cell == '#':
                    self.walls.add((i, j))

        if self.start is None or self.goal is None:
            raise Exception("Maze must have a start and goal")

    def neighbors(self, state):
        row, col = state
        directions = [('up', (-1, 0)), ('down', (1, 0)), ('left', (0, -1)), ('right', (0, 1))]
        result = []
        for action, (dr, dc) in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.height and 0 <= c < self.width and (r, c) not in self.walls:
                result.append((action, (r, c)))
        return result

    def manhattan(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def solve(self, algorithm="greedy"):
        start = Node(self.start, None, None, 0)
        frontier = []
        frontier_states = {self.start}
        explored = set()

        if algorithm == "greedy":
            priority = self.manhattan(self.start, self.goal)
        elif algorithm == "astar":
            priority = start.cost + self.manhattan(self.start, self.goal)
        else:
            raise ValueError("Unknown algorithm")

        heapq.heappush(frontier, (priority, start))

        while frontier:
            _, current = heapq.heappop(frontier)
            frontier_states.discard(current.state)

            if current.state == self.goal:
                actions = []
                cells = []
                while current.parent is not None:
                    actions.append(current.action)
                    cells.append(current.state)
                    current = current.parent
                cells.reverse()
                return cells, explored

            explored.add(current.state)

            for action, next_state in self.neighbors(current.state):
                if next_state in explored or next_state in frontier_states:
                    continue

                cost = current.cost + 1
                new_node = Node(next_state, current, action, cost)

                if algorithm == "greedy":
                    priority = self.manhattan(next_state, self.goal)
                elif algorithm == "astar":
                    priority = cost + self.manhattan(next_state, self.goal)

                heapq.heappush(frontier, (priority, new_node))
                frontier_states.add(next_state)

        raise Exception("There is no path found")

    def draw_solution(self, path, explored, filename="maze_result.png"):
        cell_size = 20
        img = Image.new("RGB", (self.width * cell_size, self.height * cell_size), "white")
        draw = ImageDraw.Draw(img)

        for i in range(self.height):
            for j in range(self.width):
                x0, y0 = j * cell_size, i * cell_size
                x1, y1 = x0 + cell_size, y0 + cell_size

                if (i, j) in self.walls:
                    fill = "black"
                elif (i, j) == self.start:
                    fill = "green"
                elif (i, j) == self.goal:
                    fill = "red"
                elif (i, j) in path:
                    fill = "blue"
                elif (i, j) in explored:
                    fill = "lightgray"
                else:
                    fill = "white"

                draw.rectangle([x0, y0, x1, y1], fill=fill, outline="gray")

        img.save(filename)
        print(f"Saved output as {filename}")


if __name__ == "__main__":
    maze = Maze("maze.txt")

    print("Solving with Greedy Search")
    path, explored = maze.solve(algorithm="greedy")
    maze.draw_solution(path, explored, filename="maze_greedy.png")

    print("Solving with A Search")
    path, explored = maze.solve(algorithm="astar")
    maze.draw_solution(path, explored, filename="maze_astar.png")
