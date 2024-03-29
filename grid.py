import pygame

import os

img_X = pygame.image.load(os.path.join('file','img_X.png')) #รูป
img_O = pygame.image.load(os.path.join('file','img_O.png'))
pygame.init()

class Grid: #เส้น grid

    #------------------------- Create a grid -----------------------------------------

    def __init__(self): #ตำแหน่ง
        self.grid_lines =  [((0,200),(600,200)), # x1 line
                            ((0,400),(600,400)), # x2 line
                            ((200,0),(200,600)), # y1 line
                            ((400,0),(400,600))] # y2 line
            
        self.grid = [[0 for x in range(3)] for y in range(3)] #ขนาดของlist
        self.switch_player = True
        # search directions  N         NW        W       SW       S
        self.search_dirs = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)] #check fullrow,colum,diagonal
        self.game_over = False  

    #------------------------- Size and color of grid ---------------------------------

    def draw(self, surface): 
        for line in self.grid_lines:
            pygame.draw.line(surface, (30,30,30), line[0], line[1], 12)

        for y in range(len(self.grid)):            #ดึงรูปมาใส่ตำแหน่ง
            for x in range(len(self.grid[y])):
                if self.get_cell_value(x, y) == "X":
                    surface.blit(img_X, ((x*200)+1, (y*200)+1))
                elif self.get_cell_value(x, y) == "O":
                    surface.blit(img_O, ((x*200)+1, (y*200)+1))

    #------------------------- Check the game is still playing ---------------------------------

    def draw_status(self, surface, player):
        if not self.game_over: # If still game 
            message = player
        elif self.game_over:
            game_over_message = "Press spacebar to restart"
            font = pygame.font.Font(None, 45)
            game_over_text = font.render(game_over_message, True, (255, 255, 255))    
            surface.fill((0,0,0), (100, 275, 400, 50))
            text_rect = game_over_text.get_rect(center =(600 / 2, 300)) 
            surface.blit(game_over_text, text_rect) 
            if self.game_over and count == 3 : # Win game 
                message = player + " won !"   
            elif self.game_over and count < 3: # Draw game
                message = player + " lose !"
        
        font = pygame.font.Font(None, 70)
        text = font.render(message, True, (255, 255, 255))    
        surface.fill((0,0,0), (0, 600, 600, 100))
        text_rect = text.get_rect(center =(600 / 2, 650)) 
        surface.blit(text, text_rect) 
       
    #------------------------- Return value x , y ---------------------------------

    def get_cell_value(self, x, y): #ส่งค่ากลับ ถ้าไม่ใส่จะทำทับเลย
        return self.grid[y][x]

    #------------------------- Set value x, y ---------------------------------

    def set_cell_value(self, x, y, value):
        self.grid[y][x] = value

    #------------------------- Unable to click the same place ---------------------------------

    def get_mouse(self, x, y, player):
        if self.get_cell_value(x, y) == 0:
            self.set_cell_value(x, y, player)
            self.check_grid(x, y, player)

    #------------------------- Define bound of game ---------------------------------

    def is_within_bounds(self, x, y):
        return x >= 0 and x < 3 and y >= 0 and y < 3        

    #------------------------- Condition to check game rules ---------------------------------

    def check_grid(self, x, y, player): 
        # Global to check game draw
        global count 
        count = 1
        for index, (dirx, diry) in enumerate(self.search_dirs):
            if self.is_within_bounds(x+dirx, y+diry) and self.get_cell_value(x+dirx, y+diry) == player:
                count += 1
                xx = x + dirx
                yy = y + diry
                if self.is_within_bounds(xx+dirx, yy+diry) and self.get_cell_value(xx+dirx, yy+diry) == player:
                    count += 1
                    if count == 3:
                        break    
                if count < 3: 
                    new_dir = 0
                    # mapping the indices to opposite direction: 0-4 1-5 2-6 3-7 4-0 5-1 6-2 7-3
                    if index == 0:
                        new_dir = self.search_dirs[4] # N to S
                    elif index == 1:
                        new_dir = self.search_dirs[5] # NW to SE
                    elif index == 2:
                        new_dir = self.search_dirs[6] # W to E
                    elif index == 3:
                        new_dir = self.search_dirs[7] # SW to NE
                    elif index == 4:
                        new_dir = self.search_dirs[0] # S to N
                    elif index == 5:
                        new_dir = self.search_dirs[1] # SE to NW
                    elif index == 6:
                        new_dir = self.search_dirs[2] # E to W
                    elif index == 7:
                        new_dir = self.search_dirs[3] # NE to SW

                    if self.is_within_bounds(x + new_dir[0], y + new_dir[1]) \
                            and self.get_cell_value(x + new_dir[0], y + new_dir[1]) == player:
                        count += 1
                        if count == 3:
                            break
                    else:
                        count = 1         

        if count == 3:
            print(player, 'wins!')
            self.game_over = True
        else: #ถ้าเต็ม
            self.game_over = self.is_grid_full()

    #------------------------- Condition to check board full ---------------------------------
    
    def is_grid_full(self): 
        for row in self.grid:
            for value in row:
                if value == 0:
                    return False
        return True

    #------------------------- Reset board ---------------------------------

    def clear_grid(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.set_cell_value(x, y, 0)        


