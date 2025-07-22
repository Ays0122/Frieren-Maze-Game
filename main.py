import sys
import math
import pygame # type: ignore
import numpy as np # type: ignore
from collections import deque
from rocklogic import moverock
from my_menu import get_user_input

pygame.init()

# Maze (0 = open path, 1 = wall)

maze = get_user_input()

print("Game Started ")

if maze is None:
    print("No maze was selected. Exiting...")
    sys.exit()
    
start = (0, 0)  # Top-left corner
end = (24, 24)    # Bottom-right corner


def start_position(r,c):
    global start
    start = (r,c)
    return start
def end_position(r,c):
    global end
    end = (r,c)
    return end

def print_maze(maze):
    for row in maze:
        print(" ".join(map(str, row)))

def draw_text(text, font, text_col):
    img = font.render(text, True, text_col)
    screen.blit(img, (int(width/2)-110, int(height/2)-50))
    pygame.display.update()
    pygame.time.delay(1500)

def maze_solver(maze, start, end):
    rows = len(maze)
    cols = len(maze[0])
    moves = [(0,1), (1,0), (0,-1), (-1,0)] #Valid move set
    queue = deque([ ( start[0], start[1], [] ) ]) #(row, col, path taken)
    visited = set([start])

    while queue:
        r, c, path = queue.popleft()
        path = path + [(r,c)] #Store path

        if (r,c) == end:
            return path #Gives the path after reaching end

        # Moving in available direction(up down left right)
        for dr, dc in moves:
            nr = r + dr
            nc = c + dc
            # Check for valid moves
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0 and (nr, nc) not in visited:
                queue.append((nr, nc, path))
                visited.add((nr, nc))

    return 0

    
#Graphical stuffs
RED = (255, 0, 0)
GREEN = (0, 255, 0)
text_font = pygame.font.SysFont("Arial", 30, bold=True)
CELL_SIZE = 30
width = height = CELL_SIZE*len(maze)
size = (width, height)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# Textures
image_block = pygame.image.load('textures/wood_block.png')
image_block = pygame.transform.scale(image_block, (CELL_SIZE, CELL_SIZE))

image_rock = pygame.image.load('textures/rock.png')
image_rock = pygame.transform.scale(image_rock, (CELL_SIZE, CELL_SIZE))

image_patch = pygame.image.load('textures/wood_texture.png')
image_patch = pygame.transform.scale(image_patch, (CELL_SIZE, CELL_SIZE))

image_final_path = pygame.image.load('textures/wood_texture_green.png')
image_final_path = pygame.transform.scale(image_final_path, (CELL_SIZE, CELL_SIZE))

image_chest = pygame.image.load('textures/image_chest.png')
image_chest = pygame.transform.scale(image_chest, (CELL_SIZE,CELL_SIZE))

image_frieren_down = pygame.image.load('textures/frieren_sprite.png')
image_frieren_down = pygame.transform.scale(image_frieren_down, (CELL_SIZE,CELL_SIZE))

image_frieren_side = pygame.image.load('textures/frieren_side.png')
image_frieren_side = pygame.transform.scale(image_frieren_side, (CELL_SIZE,CELL_SIZE))

image_frieren_back = pygame.image.load('textures/frieren_back.png')
image_frieren_back = pygame.transform.scale(image_frieren_back, (CELL_SIZE,CELL_SIZE))

image_win = pygame.image.load('textures/image_win.png')
image_win = pygame.transform.scale(image_win, size)
def draw_maze(maze):
    rows = len(maze)
    cols = len(maze[0])

    for r in range(rows):
        for c in range(cols):

            if maze[r][c] == 1:
                screen.blit(image_block, (c*CELL_SIZE,r*CELL_SIZE))

            elif maze[r][c]==0:
                screen.blit(image_patch, (c * CELL_SIZE, r * CELL_SIZE))
            
            elif maze[r][c]==4:
                screen.blit(image_patch, (c * CELL_SIZE, r * CELL_SIZE))
                screen.blit(image_rock, (c * CELL_SIZE, r * CELL_SIZE))



def draw_shortest_path(maze):
    reset=False
    preserve_character = True
    path=maze_solver(maze, start, end)
    if path == 0:
        draw_text("NO VALID PATH", text_font, RED)

    else:
        for r,c in path:

            if preserve_character:
                screen.blit(image_frieren, (c * CELL_SIZE, r * CELL_SIZE))
                preserve_character=False
            else:
                screen.blit(image_final_path, (c * CELL_SIZE, r * CELL_SIZE))
            pygame.display.update()
            clock.tick(120)
        screen.blit(image_chest, (c * CELL_SIZE, r * CELL_SIZE))
        pygame.display.update()
        while not reset:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return



run = True
start_selection = True
pygame.display.set_caption('Frieren Maze Game')
#initialize r and c for keyboard inputs
r = c = 0 #As start = (0, 0)
image_frieren = image_frieren_down
blockMode = True

#Game starts
while run:
    for event in pygame.event.get():
        draw_maze(maze)
        #draw start and end point
        (s_r, s_c) = start
        (e_r, e_c) = end

        screen.blit(image_frieren, (s_c * CELL_SIZE, s_r * CELL_SIZE)) # Start Icon
        screen.blit(image_chest, (e_c * CELL_SIZE, e_r * CELL_SIZE)) # End Icon

        pygame.display.update()
        if event.type == pygame.QUIT:
            np.save("maze.npy", maze)
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            temp_r = r
            temp_c = c
            posx = event.pos[0]
            posy = event.pos[1]
            r = int(math.floor(posy / CELL_SIZE))
            c = int(math.floor(posx / CELL_SIZE))
            print(f"start={start} end={end}")
            print(f"r={r} c={c}")
            if event.button==2: #middle click

                draw_shortest_path(maze)
                pygame.display.update()
            if event.button==1: #left click
                if start!=(r,c) and end != (r,c) and maze[r][c]==0 and blockMode==True and maze[r][c]!=4:
                    maze[r][c]=1
                    screen.blit(image_block, (c * CELL_SIZE, r * CELL_SIZE))
                    pygame.display.update()
                    print("WOOD")
                elif start!=(r,c) and end != (r,c) and maze[r][c]==0 and blockMode==False and maze[r][c]!=1:
                    maze[r][c]=4
                    screen.blit(image_rock, (c * CELL_SIZE, r * CELL_SIZE))
                    pygame.display.update()
                    print("ROCK")
                elif maze[r][c]==1 or maze[r][c]==4:
                    maze[r][c]=0
                    screen.blit(image_patch, (c * CELL_SIZE, r * CELL_SIZE))
                    pygame.display.update()
                    print("PATCH")

            if event.button==3:  #right click
                if start_selection:
                    start_position(r,c)
                    start_selection=False
                    temp_r = r
                    temp_c = c
                else:
                    end_position(r,c)
                    start_selection=True
                pygame.display.update()
            r = temp_r
            c = temp_c

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                image_frieren = image_frieren_side
                if (c-1)<0 or maze[r][c-1] == 1 or (maze[r][c-1] == 4 and (maze[r][c-2] == 1 or maze[r][c-2] == 4)):
                    break
                elif (not (c-2)<0) and maze[r][c-1] == 4:
                    maze = moverock(maze,r,c, "left")
                 
                if maze[r][c-1]!=4:
                    c = c - 1
                start_position(r, c)
                print(f"r={r} c={c}")
            if event.key == pygame.K_RIGHT:
                image_frieren = pygame.transform.flip(image_frieren_side, True, False)
                if (c+1)>24 or maze[r][c+1] == 1 or (maze[r][c+1] == 4 and ((c+2)>24 or maze[r][c+2] == 1 or maze[r][c+2] == 4)):
                    break
                elif (not (c+2)>24) and maze[r][c+1] == 4:
                    maze = moverock(maze,r,c, "right")
                
                if maze[r][c+1]!=4:
                    c = c + 1
                start_position(r, c)
                print(f"r={r} c={c}")
            if event.key == pygame.K_UP:
                image_frieren = image_frieren_back
                if (r-1)<0 or maze[r-1][c] == 1:
                    break
                elif (not (r-2)<0) and maze[r-1][c] == 4:
                    maze = moverock(maze,r,c, "up")
                
                if maze[r-1][c]!=4:
                    r = r - 1
                start_position(r, c)
                print(f"r={r} c={c}")
            if event.key == pygame.K_DOWN:
                image_frieren = image_frieren_down
                if (r+1)>24 or maze[r+1][c] == 1:
                    break
                elif (not (r+2)>24) and maze[r+1][c] == 4:
                    maze = moverock(maze,r,c, "down")
                
                if maze[r+1][c]!=4:
                    r = r + 1
                start_position(r, c)
                print(f"r={r} c={c}")
            if event.key == pygame.K_RSHIFT:
                blockMode = not blockMode
            if event.key == pygame.K_r:
                pass
            pygame.display.update()

        if start == end:
            screen.blit(image_win, (0,0))
            pygame.display.update()
            draw_text("CONGRATS!!!!!", text_font, GREEN)
            run = False