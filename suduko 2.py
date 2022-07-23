from turtle import pu
import pygame
from sys import exit
import random
from copy import  deepcopy
from functools import cmp_to_key
import numpy as np
from random import randint


pygame.init()


grid = [[0 for _ in range(9)] for _ in range(9)]
grid =[
        [0, 3, 1, 0, 0, 2, 0, 0, 8],
        [6, 0, 0, 0, 8, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 3, 1],
        [7, 5, 0, 0, 0, 0, 0, 6, 9],
        [0, 9, 0, 0, 1, 0, 0, 2, 0],
        [0, 0, 8, 0, 3, 6, 0, 0, 0],
        [9, 0, 0, 0, 0, 5, 0, 0, 0],
        [0, 7, 0, 2, 0, 0, 0, 0, 0],
        [1, 0, 0, 6, 0, 0, 4, 0, 0]
    ]
# grid = [[4,6,7,1,5,2,3,8,9],
#         [1,9,2,3,8,6,4,7,5],
#         [5,3,8,7,9,4,1,6,2],
#         [3,5,6,2,4,8,7,9,1],
#         [9,8,1,6,3,7,5,2,4],
#         [2,7,4,5,1,9,8,3,6],
#         [8,4,5,9,2,3,6,1,7],
#         [7,1,9,8,6,5,2,0,0],
#         [6,2,3,4,0,1,9,5,8]
#         ]
filled_pos = []
for row in range(9):
    for col in range(9):
        if grid[row][col]!=0:
            filled_pos.append(row*9 + col)


def print_board(grid):
  for row in range(0,9):
    for col in range(0,9):
      print(grid[row][col],end = ' ')
    print()

def valid(grid,row,col,ele):
  #checking row
  grid[row][col] = ele
  for coll in range(0,9):
    if grid[row][coll]==ele and coll!=col:
      grid[row][col] = 0
      
      return False
  #checking colsss
  for roww in range(0,9):
    if grid[roww][col]==ele and roww!=row:
      grid[row][col] = 0
      return False

  #checking subgrid
  subgrid_row = int(row/3)*3
  subgrid_col = int(col/3)*3

  for roww in range(subgrid_row,subgrid_row+3):
    for coll in range(subgrid_col,subgrid_col+3):
      if grid[roww][coll]==ele:
        if roww==row and coll==col:
          continue
        else:
          grid[row][col] = 0
          return False
  grid[row][col] = 0
  return True

def nearest_not_filled(grid):
  for i in range(0,9):
    for j in range(0,9):
      if grid[i][j] == 0:
        return i*9 + j
  return -1

def isvalid(grid):
  if nearest_not_filled(grid)>=0:
    # print("F4")
    return False
  for i in range(0,9):
    temp_set = []
    for j in range(0,9):
      temp_set.append(grid[i][j])
    temp_set = set(temp_set)
    if len(temp_set)<9:
      # print("F1")
      return False

  for i in range(0,9):
    temp_set = []
    for j in range(0,9):
      temp_set.append(grid[j][i])
    temp_set = set(temp_set)
    if len(temp_set) < 9:
      # print("F2")
      return False

  for i in range(0,9,3):
    for j in range(0,9,3):
      # print(i,j)
      temp_set = []
      for k1 in range(i,i+3):
        for k2 in range(j,j+3):
          temp_set.append(grid[k1][k2])
      temp_set = set(temp_set)
      if len(temp_set) < 9:
        return False
  return True               
    
          
          
          

def generate_random(grid):
    if nearest_not_filled(grid)==-1:
        return True
    numbers_list = [i for i in range(1,10)]
    pos = nearest_not_filled(grid)
    if pos == -1:
        return True
    
    pos_row = pos//9
    pos_col = pos%9

    curr = 1
    numbers_list = [i for i in range(1,10)]
    random.shuffle(numbers_list)
    for curr in numbers_list:
        if valid(grid,pos_row,pos_col,curr):
            grid[pos_row][pos_col] = curr
            if generate_random(grid)==True:
                return True
            grid[pos_row][pos_col] = 0
        

    return False

def draw_grid(grid):


    for i in filled_pos:
        roww = i//9
        coll = i%9
        pygame.draw.rect(screen,(255,158,14),pygame.Rect(coll*80, roww*80, 80, 80))
    for i in range(0,10):
        #(screen,color,start,end,size)
        boldness = 1
        if i%3==0:
            boldness = 5
        pygame.draw.line(screen,'Black',(0,i*80),(720,i*80),boldness)
    for i in range(0,10):
        boldness = 1
        if i%3==0:
            boldness = 5
        pygame.draw.line(screen,'Black',(i*80,0),(i*80,720),boldness)        

    for i in range (9):
        for j in range (9):
            if grid[j][i]!= 0:
                font = pygame.font.Font('freesansbold.ttf', 32)
                text = font.render(str(grid[j][i]), 1, 'Black')
                screen.blit(text, (i * 80 + 35, j * 80 + 35))

    

def highlight_cell(row,col,color):
    pygame.draw.line(screen,color,(row*80,col*80),((row+1)*80,(col)*80),4)
    pygame.draw.line(screen,color,(row*80,col*80),((row)*80,(col+1)*80),4)
    pygame.draw.line(screen,color,((row+1)*80,col*80),((row+1)*80,(col+1)*80),4)
    pygame.draw.line(screen,color,(row*80,(col+1)*80),((row+1)*80,(col+1)*80),4)
    pass



#####MODIFIED CSP


def solve_grid_using_CSP_modified(grid):
    
    if nearest_not_filled(grid)==-1:
        return True
    
    
    domain = {}
    score = {}
    
    for i in range(1,10):
        score[i]=0
    
    
    for i in range(0,9):
        for j in range(0,9):
            if grid[i][j]==0:
                domain[i*9+j]=[]
                
                for x in range(1,10):
                    if valid(grid,i,j,x):
                        domain[i*9+j].append(x)
                        score[x]+=1
                        
    pos = -1
    
    for k in domain:
        if pos==-1:
            pos=k
        elif len(domain[k])<len(domain[pos]):
            pos=k
        elif len(domain[k])==len(domain[pos]):
            total_score_pos=0
            total_score_k=0
            
            for x in domain[pos]:
                total_score_pos+=score[x]
                
            for x in domain[k]:
                total_score_k+=score[x]
                
            if total_score_pos>total_score_k:
                pos=k
            
                
    pos_row = pos//9
    pos_col = pos%9
    
    for j in range(len(domain[pos])):
        for i in range(len(domain[pos])):
            if score[domain[pos][j]]>score[domain[pos][i]]:
                domain[pos][j],domain[pos][i] = domain[pos][i],domain[pos][j]
                
                
    for ele in domain[pos]:
        screen.fill('White')
        grid[pos_row][pos_col] = ele
        draw_grid(grid)
        
        if valid(grid,pos_row,pos_col,ele):
            grid[pos_row][pos_col] = ele
            screen.fill('White')
            draw_grid(grid)
            highlight_cell(pos_col,pos_row,'Green')

            pygame.display.update()
            pygame.time.delay(100)

            if solve_grid_using_CSP_modified(grid)==True:
                return True
            else:
                grid[pos_row][pos_col] = 0
                
        else:
            highlight_cell(pos_col,pos_row,'Red')
            pygame.display.update()
            pygame.time.delay(100)
        
        
        grid[pos_row][pos_col] = 0
        screen.fill('White')
        draw_grid(grid)
        pygame.display.update()
        pygame.time.delay(100)
        
    return False
        
####### SINGLE HEURISTIC CSP


def solve_grid_using_CSP(grid):
    
    if nearest_not_filled(grid)==-1:
        return True
    
    
    domain = {}
    
    for i in range(0,9):
        for j in range(0,9):
            if grid[i][j]==0:
                domain[i*9+j]=[]
                
                for x in range(1,10):
                    if valid(grid,i,j,x):
                        domain[i*9+j].append(x)
                        
    pos = -1
    
    for k in domain:
        if pos==-1:
            pos=k
        else:
            if len(domain[k])<len(domain[pos]):
                pos=k
                
    pos_row = pos//9
    pos_col = pos%9
    
    for ele in domain[pos]:
        screen.fill('White')
        grid[pos_row][pos_col] = ele
        draw_grid(grid)
        
        if valid(grid,pos_row,pos_col,ele):
            grid[pos_row][pos_col] = ele
            screen.fill('White')
            draw_grid(grid)
            highlight_cell(pos_col,pos_row,'Green')

            pygame.display.update()
            pygame.time.delay(100)

            if solve_grid_using_CSP(grid)==True:
                return True
            else:
                grid[pos_row][pos_col] = 0
                
        else:
            highlight_cell(pos_col,pos_row,'Red')
            pygame.display.update()
            pygame.time.delay(100)
        
        
        grid[pos_row][pos_col] = 0
        screen.fill('White')
        draw_grid(grid)
        pygame.display.update()
        pygame.time.delay(100)
        
    return False


#
# 
# BACKTRACKING
# 
#         

def solve_grid(grid):

    if nearest_not_filled(grid)==-1:
        return True
    pos = nearest_not_filled(grid)
    pos_row = pos//9
    pos_col = pos%9
    for ele in range(1,10):
        screen.fill('White')
        grid[pos_row][pos_col] = ele
        draw_grid(grid)
        highlight_cell(pos_col,pos_row,'Red')
        pygame.display.update()
        pygame.time.delay(100)
        if valid(grid,pos_row,pos_col,ele):
            grid[pos_row][pos_col] = ele
            screen.fill('White')
            draw_grid(grid)
            highlight_cell(pos_col,pos_row,'Green')
            pygame.display.update()
            pygame.time.delay(100)

            if solve_grid(grid)==True:
                return True
            else:
                grid[pos_row][pos_col] = 0
        
        
        grid[pos_row][pos_col] = 0
        screen.fill('White')
        draw_grid(grid)
        pygame.display.update()
        pygame.time.delay(100)

    return False


## EXHAUSTIVE SEARCH

def exhaust_solve(grid):
  pos = nearest_not_filled(grid)
  if pos == -1:
    return isvalid(grid)
  pos_row = pos//9
  pos_col = pos%9

  curr = 1
  while curr<10:
    screen.fill('White')
    grid[pos_row][pos_col] = curr
    draw_grid(grid)
    highlight_cell(pos_col,pos_row,'Green')
    pygame.display.update()
    pygame.time.delay(100)
    if exhaust_solve(grid)==True:
      return True
    grid[pos_row][pos_col] = 0
    screen.fill('White')
    draw_grid(grid)
    pygame.display.update()
    pygame.time.delay(100)
    curr+=1
  return isvalid(grid)





### GENETIC ALGORITHM


def missing(num_array):
    flags = [1] * 9
    for num in range(1, 10):
        if num in num_array:
            flags[num-1] = 0
    return sum(flags)

def check_square(board, row, col):
    rows = missing(board[row])
    xboard = np.array(board)
    cols = missing(xboard[:, col])
    box_list = []
    mul_row = row // 3
    mul_col = col // 3
    for i in range(0, 3):
        for j in range(0, 3):
            row_idx = (col + j) % 3 + 3 * mul_col
            col_idx = (row + i) % 3 + 3 * mul_row
            box_list.append(board[row_idx][col_idx]) 
    boxes = missing(box_list)  
    return (rows + cols + boxes) == 0

def fitness_function(board):
    rows = sum([missing(row) for row in board])
    cols = sum([missing(column) for column in zip(*board)])
    boxes = 0
    for row_idx in range(0, 3):
        for col_idx in range(0, 3):
            box = [row[row_idx*3:(row_idx+1)*3] for row in board[col_idx*3:(col_idx+1)*3]]
            boxes += missing(sum(box, []))
    return rows + cols + boxes

def mutation_operator(board_list, edit_map):
    fitness_list = [fitness_function(board) for board in board_list]
    initial_fitness = max(fitness_list)
    worst_board = board_list[fitness_list.index(initial_fitness)]
    row = randint(0, 8)
    col = edit_map[row].index(min(x for x in edit_map[row] if x > 0))
    worst_board[row][col] = (worst_board[row][col] + 1) % 9
    if worst_board[row][col] == 0:
        worst_board[row][col] = 9
    edit_map[row][col] += 1
    if check_square(worst_board, row, col):
        for board in board_list:
            board[row][col] = worst_board[row][col]
    return board_list, edit_map


def crossover_operator(board_list, edit_map):
    fitness_values = [fitness_function(board) for board in board_list]
    while sum(fitness_values) > 0:
        least_fit_idx = fitness_values.index(max(fitness_values))
        most_fit_idx = fitness_values.index(min(x for x in fitness_values if x > 0))
        if least_fit_idx == most_fit_idx:
            least_fit_idx = (least_fit_idx + 1) % 9
        fitness_values[least_fit_idx] = 0
        fitness_values[most_fit_idx] = 0
        row = randint(0, 8)
        col = edit_map[row].index(max(edit_map[row]))
        board_list[least_fit_idx][row][col] = board_list[most_fit_idx][row][col]
    return board_list


def solve_grid_using_genetic(grid):

    population_size = 10
    puzzle_board = grid
    # puzzle_board =[
    #         [7, 8, 5, 4, 3, 9, 1, 2, 0],
    #         [6, 1, 2, 8, 7, 5, 3, 0, 9],
    #         [4, 9, 3, 6, 0, 1, 5, 7, 8],
    #         [8, 5, 7, 9, 4, 3, 2, 6, 0],
    #         [0, 6, 1, 7, 5, 8, 9, 3, 4],
    #         [9, 0, 4, 1, 6, 2, 7, 8, 5],
    #         [5, 7, 0, 3, 9, 4, 6, 1, 2],
    #         [1, 2, 6, 0, 8, 7, 4, 9, 3],
    #         [3, 4, 9, 2, 1, 6, 0, 5, 7]
    #     ]
    # puzzle_board =[
    #         [7, 8, 0, 4, 0, 9, 1, 2, 0],
    #         [6, 0, 2, 8, 7, 5, 3, 0, 9],
    #         [4, 9, 0, 6, 0, 1, 5, 7, 8],
    #         [8, 5, 7, 9, 4, 3, 2, 6, 0],
    #         [0, 6, 1, 0, 5, 0, 9, 3, 0],
    #         [9, 0, 4, 1, 6, 2, 0, 0, 5],
    #         [0, 7, 0, 3, 9, 0, 6, 1, 2],
    #         [1, 2, 6, 0, 8, 7, 4, 9, 0],
    #         [0, 4, 9, 2, 1, 6, 0, 5, 7]
    #     ]

    edit_map = [[0 for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(9):
            if puzzle_board[i][j] != 0:
                edit_map[i][j] = 0
            else:
                edit_map[i][j] = 1

    time = 0
    best_fitness = -1
    num_of_generations_at_max = 20000
    puzzle_board_list = [deepcopy(puzzle_board) for _ in range(0, population_size)]
    prev = -1
    count = 0
    while best_fitness != 0 and time!=num_of_generations_at_max:
        puzzle_board_list = crossover_operator(puzzle_board_list, edit_map)
        puzzle_board_list, edit_map = mutation_operator(puzzle_board_list, edit_map)
        best_fitness = min([fitness_function(board) for board in puzzle_board_list])
        print(str(time) + ": " + str(best_fitness))
        time += 1
    fitness = [fitness_function(board) for board in puzzle_board_list]
    solution = puzzle_board_list[fitness.index(min(fitness))]
    
    return solution




# print_board(grid)
reset_grid = deepcopy(grid)
# reset_grid[1][1] = 5
screen  = pygame.display.set_mode((720,800))
screen.fill('White')
pygame.display.set_caption('Sudoku visualiser')

clock=pygame.time.Clock()
while True:
    pygame.event.pump()
    keys = pygame.key.get_pressed()
    screen.fill('White')
    if keys[pygame.K_b]:
        solve_grid(grid)
    elif keys[pygame.K_e]:
        exhaust_solve(grid)
    elif keys[pygame.K_c]:
        solve_grid_using_CSP(grid)
    elif keys[pygame.K_m]:
        solve_grid_using_CSP_modified(grid)
    elif keys[pygame.K_r]:
        grid = deepcopy(reset_grid)
    elif keys[pygame.K_g]:
        grid = deepcopy(solve_grid_using_genetic(grid))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit() 
    # highlight_cell(1,1,'Red')
    draw_grid(grid)

    pygame.display.update() 
    # clock.tick(1)



    
         







