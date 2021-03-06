import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time 
from grids import Grids
from queue import PriorityQueue

class Node:
    def __init__(self, parent_node, position):
        self.position = position
        self.parent = parent_node

        self.g = 0
        self.h = 0
        self.calc_f()
        
    def calc_f(self):
        self.f = self.g + self.h

    def __eq__(self, comparasion_node):
        return self.position == comparasion_node.position
    def __lt__(self,other):
        return self.f < other.f

def check_validity(occupancy_grid_shape, pos):
    shape = occupancy_grid_shape
    if (pos[0] > shape[0]-1) or (pos[0] < 0):
        return False
    if (pos[1] > shape[1]-1) or (pos[1] < 0):
        return False
    return True

def calc_heuristic(end_node, pos):
    return ((abs(end_node[0]-pos[0]) + abs(end_node[1] - pos[1])))

def astar_solver(occupancy_grid, start_pos, end_pos):
    # initialize open and closed list 
    open_list = PriorityQueue()
    closed_list = []
    # initialize start and end nodes
    start_node = Node(None, start_pos)
    end_node = Node(None, end_pos)
    # initialize other variables for speed
    children_moves = [(0, -1), (0, 1), (-1, 0), (1, 0)] # 4 directional movement
    occ_grid_shape = occupancy_grid.shape

    # Append the first node
    open_list.put(start_node)
    #open_list.append(start_node)
    
    while not open_list.empty():
        '''
        active_node = open_list[0]
        active_idx = 0

        # Search for the lowest cost node
        for index, node in enumerate(open_list):
            if node.f < active_node.f:
                active_idx = index
                active_node = node
        '''
        # Take the lowest score and add that noded to closed list
        #open_list.pop(active_idx)
        active_node = open_list.get()
        closed_list.append(active_node)

        # If we made it to the end node
        if active_node == end_node:
            path = []

            active = active_node
            while active is not None:
                path.append(active.position)
                active = active.parent
            
            return path[::-1]
        
        # If not continue and start creating successors
        children = []
        for move in children_moves:
            # Check if the space is occupied
            child_pos = tuple(a+b for (a,b) in zip(active_node.position,move))
            # Check if it is inside the scope
            if not check_validity(occ_grid_shape, child_pos):
                continue
            # Check if the space is walkable
            if occupancy_grid[child_pos] == 0:
                continue
            
            # Create successor node
            child = Node(active_node, child_pos)
            children.append(child)
        
        # Check each child
        for child in children:
            # See if it already is in the visited nodes list
            for closed_node in closed_list:
                if child == closed_node:
                    break
            else:
                # Calculate the g,h and f values
                child.g = active_node.g + 1
                child.h = 1.01*(abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1]))#calc_heuristic(end_node.position, child_pos)
                child.calc_f()
                # See if it already is in the open list
                for open_node in open_list.queue:
                    # See if it is a shorter path to this node
                    if (child == open_node) and (child.g >= open_node.g):
                        break
                else:
                    # if not; add it to the potential moves list
                    open_list.put(child)

def astar_animation(path, grid, CREATEGIF = False):
    
    fig = plt.figure()

    ax = plt.axes(xlim=(0, 100), ylim=(0, 100))

    pathplt = plt.plot([],[],'g',lw=1)[0]
    agent = ax.plot([],[],'ro')[0]

    patches = [pathplt, agent]
    xline, yline = [],[]


    def init():
        plt.imshow(grid.occupancy_grid)
        pathplt.set_data([],[])
        
        return patches

    def animate(i):
        agent.set_data([path[i][1]],[path[i][0]])
        xline.append(path[i][1])
        yline.append(path[i][0])
        pathplt.set_data(xline,yline)
        
        return patches

    anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=len(path), interval=10, blit=True, repeat=False)
    plt.gray()

    if CREATEGIF:
        anim.save('animation.gif', writer='imagemagick', fps=60)
    else:
        plt.show()

def eval(grid, N = 10):
    starttime = time.time()
    for i in range(N):
        print("Starting iteration {}/{}...".format(i+1, N))
        path = astar_solver(grid.occupancy_grid, grid.start, grid.end)

    print("Average executiontime run over {} iterations is: {} ms".format(N, int((time.time()-starttime)*1000)/N))
    return path 
  
def main():

    grids = Grids()
    grid = grids.grid5

    path = eval(grid, 15)
    print("---- Path is of length: {}".format(len(path)))

    astar_animation(path, grid)

    
    
if __name__ == '__main__':
    main()

