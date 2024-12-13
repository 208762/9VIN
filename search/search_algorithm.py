# simple search algorithm 

import pygame
import time

class Node():
    def __init__(self, state, parent, action, cost, past_cost): # initialization
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.past_cost = past_cost
        
        # usage of class object for Node to be able to SAVE Node's state, parent and action
        # which will be needed later
        
        # NODES are data structures which keep track of a state, parent (node that generated)
        # this node, an action (action applied to the parent to get to this node / to generate
        # this node) and a path cost (cost of a path from initial state to the node)
        
        # this type of Node class does not have the path cost variable, because this type of 
        # algorithm is able to calculate path cost directly later 
        
class StackFrontier():
    def __init__(self):
        self.frontier = []

        # usage of class object for StackFrontier wich represents last-in first-out
        # data structure, that can be seen in "remove" function of this class
        # StackFrontier is used for taking another step and defines in which way
        # the BOT takes another step
        
    def add(self, node):
        self.frontier.append(node)
        
        # "add" function definition for the BOT being able to take another step
        # taking another step is represented by adding another node to the frontier
       
        
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

        # "contains_state" function definition for the BOT being able to tell which positions
        # he has already been to
        
    def empty(self):
        return len(self.frontier) == 0

        # "empty" function definition for the BOT being able to tell if the frontier is empty,
        # if the frontier is empty, there is NO SOLUTION
        
    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
        
        # "remove" function for removal of the last (last-in first-out) node which should be
        # then explored / explored next
        
class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")   
        else:
            node = self.frontier[0] 
            self.frontier = self.frontier[1:]
            return node
        
        # another "remove" function in new class QueueFrontier inheriting from the original 
        # StackFrontier class. the new class represents first-in first-out data structure
        
class MinimumFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            node = min(self.frontier, key = lambda node: node.cost)
            self.frontier.remove(node)
            return node
        
class A_Frontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            node = min(self.frontier, key = lambda node: node.cost + node.past_cost)
            self.frontier.remove(node)
            return node

class Maze():
    # class which takes the .txt file and creates a maze from it
    def __init__(self):
        filename = "maze4.txt" # chosen maze
        self.length = 0

        with open(filename) as f:
            maze_txt = f.read()

        # Validation of the MAZE
        if maze_txt.count("A") != 1:
            raise Exception("Maze must have exactly one start point!")
        if maze_txt.count("B") != 1:
            raise Exception("Maze must have exactly one goal!")
        
        # Height and width of the MAZE
        maze_txt = maze_txt.splitlines()
        self.height = len(maze_txt)
        self.width = max(len(line) for line in maze_txt)

        # Creating the walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if maze_txt[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif maze_txt[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif maze_txt[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)
        self.solution = None
        
    def manhattan(self, state):
        row, col = state
        return abs(self.goal[0] - row) + abs(self.goal[1] - col)
    
    # Printing the maze
    def visualize_maze(self):
        self.cell_size = 50
        self.cell_border = 1
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 24)
        self.font.set_bold(True)
        
        # Start
        start_letter = "S"
        start_text_surface = self.font.render(start_letter, True, (255, 255, 255))
        start_text_rect = start_text_surface.get_rect()
        
        # Finish
        finish_letter = "F"
        finish_text_surface = self.font.render(finish_letter, True, (255, 255, 255))
        self.finish_text_rect = finish_text_surface.get_rect()
        
        self.screen = pygame.display.set_mode((self.width * self.cell_size, self.height * self.cell_size))
        pygame.display.set_caption("Maze Solver")
        
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    fill = (40, 40, 40)
                    pygame.draw.rect(self.screen, fill, (j * self.cell_size + self.cell_border, i * self.cell_size + self.cell_border, self.cell_size - 2 * self.cell_border, self.cell_size - 2 * self.cell_border))
                elif (i, j) == self.start:
                    start_text_rect.center = (j * self.cell_size + self.cell_size // 2, i * self.cell_size + self.cell_size // 2)
                    fill = (255, 102, 102)
                    pygame.draw.rect(self.screen, fill, (j * self.cell_size + self.cell_border, i * self.cell_size + self.cell_border, self.cell_size - 2 * self.cell_border, self.cell_size - 2 * self.cell_border))
                    self.screen.blit(start_text_surface, start_text_rect)
                elif (i, j) == self.goal:
                    self.finish_text_rect.center = (j * self.cell_size + self.cell_size // 2, i * self.cell_size + self.cell_size // 2)
                    fill = (0, 171, 100)
                    pygame.draw.rect(self.screen, fill, (j * self.cell_size + self.cell_border, i * self.cell_size + self.cell_border, self.cell_size - 2 * self.cell_border, self.cell_size - 2 * self.cell_border))
                    self.screen.blit(finish_text_surface, self.finish_text_rect)
                else:
                    fill = (237, 240, 252)
                    pygame.draw.rect(self.screen, fill, (j * self.cell_size + self.cell_border, i * self.cell_size + self.cell_border, self.cell_size - 2 * self.cell_border, self.cell_size - 2 * self.cell_border))
                
                pygame.display.update()

    def visualize_move(self, state):
        if state != self.goal and state != self.start:
            i, j = state
            pygame.draw.rect(self.screen, (255, 255, 170), (j * self.cell_size + self.cell_border, i * self.cell_size + self.cell_border, self.cell_size - 2 * self.cell_border, self.cell_size - 2 * self.cell_border))
            pygame.display.update()
            time.sleep(0.1)
        elif state == self.goal:
            i, j = state
            finish_letter_change = "F"
            finish_letter_change_surface = self.font.render(finish_letter_change, True, (255, 102, 102))
            self.finish_text_rect = finish_letter_change_surface.get_rect()
            self.finish_text_rect.center = (j * self.cell_size + self.cell_size // 2, i * self.cell_size + self.cell_size // 2)
            pygame.draw.rect(self.screen, (0, 171, 28), (j * self.cell_size + self.cell_border, i * self.cell_size + self.cell_border, self.cell_size - 2 * self.cell_border, self.cell_size - 2 * self.cell_border))
            self.screen.blit(finish_letter_change_surface, self.finish_text_rect)
            pygame.display.update()
            
    def visualize_best_route(self):
        solution = self.solution[1] if self.solution is not None else None 
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if (i, j) not in solution and (i, j) != self.goal and (i, j) != self.start and col == False and (i, j) in self.explored:
                    pygame.draw.rect(self.screen, (100, 100, 100), (j * self.cell_size + self.cell_border, i * self.cell_size + self.cell_border, self.cell_size - 2 * self.cell_border, self.cell_size - 2 * self.cell_border))
                    pygame.display.update()
                    
    def visualize_cost(self, state, cost, past_cost):
        if state != self.goal and state != self.start:
            i, j = state
            cost = f"{cost + past_cost}"
            cost_surface = self.font.render(cost, True, (0, 0, 0))
            cost_surface_rect = cost_surface.get_rect()
            cost_surface_rect.center = (j * self.cell_size + self.cell_size // 2, i * self.cell_size + self.cell_size // 2)
            self.screen.blit(cost_surface, cost_surface_rect)
                    
    # Keeping track of neighbors
    def neighbors(self, state):
        row, col = state
        
        # Defining all the possible actions
        possible_actions = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        # Making sure all the actions are valid
        result = []
        for action, (r, c) in possible_actions:
            try:
                if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                    result.append((action, (r, c)))
            except IndexError:
                continue
        return result
        
    def solve(self):
        # Finding a solution to maze if exists
        
        # Keeping the track of the number of states explored jus to be able to pick the most optimal solution
        self.num_explored = 0

        # Initialization of the frontier to the starting position
        start = Node(state = self.start, parent = None, action = None, cost = 0, past_cost = 0)
        frontier = A_Frontier() # Frontier now, can change later
        # frontier = StackFrontier()
        # frontier = QueueFrontier()
        frontier.add(start) # Adding the first node
        
        # Initialize an empty explored set
        self.explored = set()

        # Main loop until solution is find
        while True:
            
            # If nothing is left in the frontier, then there is no right PATH
            if frontier.empty():
                raise Exception("No solution")

            # Choosing a node from a frontier
            node = frontier.remove()
            self.visualize_move(state = node.state)
            self.visualize_cost(state = node.state, cost = node.cost, past_cost = node.past_cost)
            node.past_cost += 1
                        
            # If the node is the GOAL, then we have a SOLUTION
            if node.state == self.goal:
                actions = []
                cells = []

                # Backtracking t he path to find out the path which leads to the GOAL
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                
                actions.reverse() # to get the actions from the initial state to the goal, same with cells
                cells.reverse()
                self.solution = (actions, cells)
                self.visualize_best_route()
                return
        
            # If the nodes states is not the goal, just add the nodes state to the explored states
            self.explored.add(node.state)
            
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state = state, parent = node, action = action, cost = self.manhattan(state), past_cost = node.past_cost)
                    frontier.add(child)
                    
m = Maze()
m.visualize_maze()
m.solve()