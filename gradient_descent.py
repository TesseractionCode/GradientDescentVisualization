from re import X
import pygame
from eq_visualizer import *
from math import cos, sin

resolution = (800, 600)
screen = pygame.display.set_mode(resolution)


def plottingFunction(x, y):
    return sin(x**2 + y**2)


viewFrame = ViewFrame(0, 0, resolution[0], resolution[1])

visualizer = EqVisualizer(viewFrame, plottingFunction)
visualizer.maxViewHeight = 1
visualizer.minViewHeight = -1
visualizer.viewPosX, visualizer.viewPosY = (0, 0)
visualizer.unitPerPixel = 0.01

visualizer.genImage()

ball_pos = [.8, .7]
descent_rate = 0.04


def descend():
    x = ball_pos[0]
    y = ball_pos[1]
    partial_x = cos(x**2 + y**2) * 2*x
    partial_y = cos(x**2 + y**2) * 2*y
    ball_pos[0] -= partial_x * descent_rate
    ball_pos[1] -= partial_y * descent_rate


def render():
    visualizer.draw(screen)
    screen_x, screen_y = visualizer.cartesianPosToScreenPos(
        ball_pos[0], ball_pos[1])
    pygame.draw.circle(screen, (255, 255, 255), (screen_x, screen_y), 10)
    
    pygame.display.flip()

render()
running = True
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                descend()
                render()
