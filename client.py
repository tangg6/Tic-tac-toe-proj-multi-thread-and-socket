import pygame
from grid import Grid

pygame.init()

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '850,100'

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
server.connect((HOST,PORT)) #เชื่อมต่อ

#------------------------- Recieve data from server --------------------------------

def recieve_data():
    while True:
        data = server.recv(1024).decode()
        print(data)

create_thread(recieve_data)

#------------------------- Create a display of game ---------------------------------

surface = pygame.display.set_mode((600,700))
pygame.display.set_caption("Tic tac toe") #caption
icon = pygame.image.load ('games.png')
pygame.display.set_icon (icon)

#------------------------- Import sound into game -----------------------------------

pygame.mixer.music.load('s10.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.0)
# Declare grid
grid = Grid()

#------------------------- Playing game --------------------------------------------

running = True
player = "X"        # First play always be X
winner = None

running = True      # Loop check that still on game
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over:                 #ถ้าเกมจบจะกดไม่ได้
            if pygame.mouse.get_pressed()[0]:                                   #คลิกได้แค่คลิกซ้าย
                pos = pygame.mouse.get_pos() 
                cellX, cellY = pos[0] // 200, pos[1] // 200
                if pos[0]<=600 and pos[1]<=600: 
                    grid.get_mouse(cellX, cellY, player)
                    send_data = '{}-{}'.format(cellX, cellY).encode()       # Use format string to enable encode function
                    server.send(send_data)                              # send to server
       
                    if grid.switch_player:
                        if player == "X":
                            click_sound = pygame.mixer.Sound('nsj.wav')
                            click_sound.set_volume(0.4)
                            click_sound.play()
                            player = "O"
                        else:
                            click_sound = pygame.mixer.Sound('nsj2.wav')
                            click_sound.set_volume(0.4)
                            click_sound.play()
                            player = "X"
                    
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