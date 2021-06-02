import pygame

import os

letterX = pygame.image.load(os.path.join('file','letterX.png')) #รูป
letterO = pygame.image.load(os.path.join('file','letterO.png'))
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

    def draw(self, surface):  #ขนาด,สีของเส้น
        for line in self.grid_lines:
            pygame.draw.line(surface, (0,0,0), line[0], line[1], 6)

        for y in range(len(self.grid)):            #ดึงรูปมาใส่ตำแหน่ง
            for x in range(len(self.grid[y])):
                if self.get_cell_value(x, y) == "X":
                    surface.blit(letterX, (x*200, y*200))
                elif self.get_cell_value(x, y) == "O":
                    surface.blit(letterO, (x*200, y*200))

    #------------------------- Check the game is still playing ---------------------------------

    def draw_status(self, surface, player):
        if not self.game_over: # If still game 
            massage = player + "'s Turn"
        elif self.game_over and count == 3 : # Win game 
            # Change show player won 
            if player == "X": 
                player = "O"
            elif player == "O":
                player = "X"
            massage = player + "'s won !"   
        elif self.game_over and count < 3 : # Draw game 
            massage = "Game Draw !"    
        font = pygame.font.Font(None, 50)
        text = font.render(massage, True, (255, 255, 255))    
        surface.fill((0,0,0), (0, 600, 600, 100))
        text_rect = text.get_rect(center =(600 / 2, 650)) 
        surface.blit(text, text_rect) 
       
    #-------------------------  ---------------------------------

    def get_cell_value(self, x, y): #ส่งค่ากลับ ถ้าไม่ใส่จะทำทับเลย
        return self.grid[y][x]

    #-------------------------  ---------------------------------

    def set_cell_value(self, x, y, value):
        self.grid[y][x] = value

    #------------------------- Unable to click the same place ---------------------------------

    def get_mouse(self, x, y, player):#ไม่ให้กดที่เดิม
        if self.get_cell_value(x, y) == 0:
            self.set_cell_value(x, y, player)
            self.check_grid(x, y, player)

    #-------------------------  ---------------------------------

    def is_within_bounds(self, x, y):
        return x >= 0 and x < 3 and y >= 0 and y < 3        

    #------------------------- Condition to check game rules ---------------------------------

    def check_grid(self, x, y, player): #ตรวจตำแหน่งรอบถ้ามีติดกันจะนำมาบวกครบ3จะชนะ
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
             
    #-------------------------  ---------------------------------
    
    def is_grid_full(self): 
        for row in self.grid:
            for value in row:
                if value == 0:
                    return False
        return True

    #-------------------------  ---------------------------------

    def clear_grid(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.set_cell_value(x, y, 0)        

    #-------------------------  ---------------------------------

    def print_grid(self): #ทำให้listออกมาเป็นแถว
        for row in self.grid:
            print(row)  
