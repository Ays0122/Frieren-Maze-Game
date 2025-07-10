def moverock(maze,r,c, move:str):
    
    match move:
        case "left":
            if (c-2)<0:
                return maze
            
            elif maze[r][c-2] ==0:
                maze[r][c-1] = 0
                maze[r][c-2] = 4
                return maze
        case "right":
            if (c+2)>24:
                return maze
            elif maze[r][c+2] ==0:
                maze[r][c+1] = 0
                maze[r][c+2] = 4
                return maze
        case "up":
            if (r-2)<0:
                return maze
            
            elif maze[r-2][c] ==0:
                maze[r-1][c] = 0
                maze[r-2][c] = 4
                return maze
            return maze
        case "down":
            if (r+2)<0:
                return maze
            
            elif maze[r+2][c] ==0:
                maze[r+1][c] = 0
                maze[r+2][c] = 4
            return maze