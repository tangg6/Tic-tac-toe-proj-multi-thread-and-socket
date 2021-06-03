import pygame
from grid import Grid

pygame.init()

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '850,200'

import threading

def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True # Use deamon thread
    thread.start()

import socket
HOST = '127.0.0.1'
PORT = 62107
connection_established = False

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((HOST,PORT)) # เชื่อมต่อ

#------------------------- Recieve data from server --------------------------------

def recieve_data():
    global turn
    while True:
        data = server.recv(1024).decode()
        data = data.split('-')
        x,y= int(data[0]), int(data[1])
        if data[2] == 'yourturn':
            turn = True
        if data[3] == 'False':
            grid.game_over = True
        if grid.get_cell_value(x, y) == 0:
            grid.set_cell_value(x, y, "X")

create_thread(recieve_data)

#------------------------- Create a display of game ---------------------------------

surface = pygame.display.set_mode((600,700))
pygame.display.set_caption("Tic tac toe") #caption
icon = pygame.image.load(os.path.join('file','games.png'))
pygame.display.set_icon (icon)

#------------------------- Import sound into game -----------------------------------

pygame.mixer.music.load(os.path.join('file','s10.wav'))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)
# Declare grid
grid = Grid()

#------------------------- Playing game --------------------------------------------

player = "O"        
turn = False 
playing = 'True'

running = True      # Loop check that still on game
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over:                 #ถ้าเกมจบจะกดไม่ได้
            if pygame.mouse.get_pressed()[0]:                                   #คลิกได้แค่คลิกซ้าย
                if turn and not grid.game_over:                                   
                    pos = pygame.mouse.get_pos() 
                    cellX, cellY = pos[0] // 200, pos[1] // 200
                    if pos[0]<=600 and pos[1]<=600: 
                        grid.get_mouse(cellX, cellY, player)
                        click_sound = pygame.mixer.Sound(os.path.join('file','nsj2.wav'))
                        click_sound.set_volume(0.4)
                        click_sound.play()
                        if grid.game_over:
                            playing = 'False'
                        send_data = '{}-{}-{}-{}'.format(cellX, cellY, 'yourturn', playing).encode()       # Use format string to enable encode function
                        server.send(send_data)                              # send to server
                        turn = False
       
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.game_over:
                grid.clear_grid()
                grid.game_over = False
                playing = 'True'
            elif event.key == pygame.K_ESCAPE:
                running = False                    
                
    surface.fill((255,255,255))

    # Put grid line in surface
    grid.draw(surface)
    grid.draw_status(surface,player)

    pygame.display.flip()