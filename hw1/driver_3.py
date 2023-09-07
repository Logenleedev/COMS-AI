import sys
import heapq as hq
import time 
import resource
from collections import deque

'''
class
----------------------------------------------------------------
'''

class Movement:
    def __init__(self, board):
        self.board = board
        

    
    def moveUp(self):
        copy_board = self.board.state[:]
        tile = copy_board.index(0)
        temp = copy_board[tile]
        copy_board[tile] = copy_board[tile - 3]
        copy_board[tile - 3] = temp
        update_node = Node(copy_board, self.board, "Up", self.board.depth + 1)
        return update_node
        


    def moveDown(self):
        copy_board = self.board.state[:]
        tile = copy_board.index(0)
        temp = copy_board[tile]
        copy_board[tile] = copy_board[tile + 3]
        copy_board[tile + 3] = temp
        update_node = Node(copy_board, self.board, "Down", self.board.depth + 1)
        return update_node

    def moveLeft(self):
        copy_board = self.board.state[:]
        tile = copy_board.index(0)
        temp = copy_board[tile]
        copy_board[tile] = copy_board[tile - 1]
        copy_board[tile - 1] = temp
        update_node = Node(copy_board, self.board, "Left", self.board.depth + 1)
        return update_node

    def moveRight(self):
        copy_board = self.board.state[:]
        tile = copy_board.index(0)
        temp = copy_board[tile]
        copy_board[tile] = copy_board[tile + 1]
        copy_board[tile + 1] = temp
       
        update_node = Node(copy_board, self.board, "Right", self.board.depth + 1)
        return update_node


class Frontier:
    def __init__(self):
        self.myque = deque()
        self.visited = set()

    def pop(self):
        node = self.myque.pop()
        if str(node.state) in self.visited:
            self.visited.remove(str(node.state))
        return (node)
        
    def push(self, node):
        self.myque.append(node)
        self.visited.add(str(node.state))

    def enqueue(self, node):
        self.myque.append(node)
        self.visited.add(str(node.state))
    
    def dequeue(self):
        node = self.myque.popleft()
        self.visited.discard(str(node.state))
        return(node)

    def search(self, node):
        flag = False
        
        if node in self.visited:
            flag = True
            
        return flag
    
    def size(self):
        return len(self.visited)
    
    

class Node:
    def __init__(self, state, parent, action, depth):
        self.path_cost = 0
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
'''
variables
----------------------------------------------------------------
'''


target = [0, 1, 2, 3, 4, 5, 6, 7, 8]
frontier_BFS = Frontier()
frontier_DFS = Frontier()


'''
Method
----------------------------------------------------------------
'''

def bfs(board):
    begin = time.time()

    explored = set()
    counter = -1
    maxDepth = 0 
    root = Node(board, None, None, 0)
    frontier_BFS.enqueue(root)

    endNode = None
    while frontier_BFS.size() != 0:
        
        node = frontier_BFS.dequeue()
        explored.add(node)
        counter += 1

        if node.state == target:
            # find the answer
        
            endNode = node

            path = []
            
            start = node
           
            while node.parent != None:
                
                path.append(node.action)
                node = node.parent
            
            path = path[::-1]
        
            break


        else:
            # get children
            child = get_child(node)

            for v in child:
                
                if (v not in explored) and (frontier_BFS.search(v) == False):
                    maxDepth = max(maxDepth, v.depth)
                    frontier_BFS.enqueue(v)


            

        
 
    end = time.time()
    diff = end - begin
    ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    outputanswer(path, counter, endNode, maxDepth,diff,ram)

def dfs(board):
    pass

def astar(board):

    pass

def get_child(node):
    tile = node.state.index(0)
    
    movement = Movement(node)

    if tile == 0:
        return [movement.moveDown(), movement.moveRight()]

    elif tile == 1:
        return [movement.moveLeft(), movement.moveDown(), movement.moveRight()]

    elif tile == 2:
        return [movement.moveLeft(), movement.moveDown()]

    elif tile == 3:
         return [movement.moveUp(), movement.moveDown(), movement.moveRight()]

    elif tile == 4:
        return [movement.moveUp(), movement.moveDown(), movement.moveRight(), movement.moveLeft()]

    elif tile == 5:
        return [movement.moveUp(), movement.moveDown(), movement.moveLeft()]

    elif tile == 6:
        return [movement.moveUp(), movement.moveRight()]

    elif tile == 7:
 
        return [movement.moveUp(), movement.moveLeft(), movement.moveRight()]

    elif tile == 8:
        return [movement.moveUp(), movement.moveLeft()]
    

    




def outputanswer(path, nodes_Expanded, node, max_Depth, diff, ram):
    file = open("output_mine.txt", "w")
    
    file.write("path_to_goal: "+ str(path)+"\n")
    file.write("cost_of_path: "+ str(len(path))+"\n")
    file.write("nodes_expanded: "+ str(nodes_Expanded)+"\n")
    file.write("search_depth: "+ str(node.depth)+"\n")
    file.write("max_search_depth: "+ str(max_Depth)+"\n")
    file.write("running_time: "+ str(diff)+"\n")
    file.write("max_ram_usage:" + str(ram / (1024 * 1024)) + "\n")
    
    file.close()

'''
Main function 
----------------------------------------------------------------
'''
def main():
    # example cmd input:
    # python3 driver_3.py bfs 3,1,2,0,4,5,6,7,8
    # python3 driver_3.py dfs 3,1,2,0,4,5,6,7,8
    # python3 driver_3.py ast 3,1,2,0,4,5,6,7,8


    search_algo = str(sys.argv[1])
    input_state = sys.argv[2].split(",")

    # convert input state to int list e.g. [3,1,2,0,4,5,6,7,8]
    for i in range(len(input_state)):
        input_state[i] = int(input_state[i])
    

    # mode activation
    if search_algo == 'bfs':
        print('bfs is activated')
        bfs(input_state)


    elif search_algo == 'ast':
        print('A star is activated')
        astar(input_state)

    elif search_algo == 'dfs':
        print('dfs is activated')
        dfs(input_state)

        
    print("check the txt file for the output")


if __name__ == "__main__":
    main()