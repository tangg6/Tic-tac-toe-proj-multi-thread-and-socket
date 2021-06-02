import pygame
from grid import Grid

pygame.init()

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '200,100'

import threading

def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True # Use deamon thread
    thread.start()

#------------------------ Open server ------------------------------

import socket

HOST = '127.0.0.1'
PORT = 62107
connection_established = False
conn, addr = None, None # Define connection and address

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print("waiting for connection...")

#------------------------- Recieve data from client --------------------------------

def recieve_data():
    global turn
    while True:
        data = conn.recv(1024).decode()
        data = data.split('-')
        x,y= int(data[0]), int(data[1])
        if data[2] == 'yourturn':
            turn = True
        if data[3] == 'False':
            grid.game_over = True
        if grid.get_cell_value(x, y) == 0:
            grid.set_cell_value(x, y, "O")
        print(data)

#------------------------ Another thread doing about server ------------------------------

def waiting_for_connection():
    global connection_established, conn, addr
    conn, addr = server.accept() # wait for connection 
    print('Connection address:', str(addr)) # show detail of client that connected
    connection_established = True
    recieve_data()

create_thread(waiting_for_connection)

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

player = "X"        # First play always be X turn 
turn = True         # Server is first play
playing = 'True'

running = True      # Loop check that still on game
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and connection_established:                 #ถ้าเกมจบจะกดไม่ได้
            if pygame.mouse.get_pressed()[0]:                                   #คลิกได้แค่คลิกซ้าย
                if turn and not grid.game_over:                                   
                    pos = pygame.mouse.get_pos() 
                    cellX, cellY = pos[0] // 200, pos[1] // 200
                    if pos[0]<=600 and pos[1]<=600:             # Condition to check player click the right posotion
                        grid.get_mouse(cellX, cellY, player)
                        click_sound = pygame.mixer.Sound('nsj.wav')
                        click_sound.set_volume(0.4)
                        click_sound.play()
                        if grid.game_over:
                            playing = 'False'
                        send_data = '{}-{}-{}-{}'.format(cellX, cellY, 'yourturn', playing).encode()       # Use format string to enable encode function
                        conn.send(send_data)                        # send to client
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