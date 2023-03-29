# Sabin Dheke and Hari Krishna
# CMPS 5443 
# Advance topic: 2D Games
# Assignment 2

import pygame
from MyGame import MyGame
from Engine.Drawer import drawer

game = MyGame()

while True:
    drawer.screen.fill((11, 111, 199), (0, 0, drawer.width, drawer.height))

    # Initialize delta time for smoother animations
    drawer.initDeltaTime()

    # Process all events in the event queue
    for event in pygame.event.get():
        # Handle the Quit event (e.g. when user closes the window)
        if event.type == pygame.QUIT:
            exit(0)
        # Handle keydown event
        if event.type == pygame.KEYDOWN:
            game.onKeyDown(event.key)
        # Handle keyup event
        if event.type == pygame.KEYUP:
            game.onKeyUp(event.key)
        # Handle mouse button down event
        if event.type == pygame.MOUSEBUTTONDOWN:
            game.onMouseDown(event)
        # Handle mouse button up event
        if event.type == pygame.MOUSEBUTTONUP:
            game.onMouseUp(event)

    # Update game state
    game.update()

    # Draw game objects on the screen
    game.draw()

    # Update the screen display
    pygame.display.flip()