# examplemazes.py
import pygame
import numpy as np
import sys

# Initialize Pygame
pygame.init()
pygame.display.set_caption('Maze Game')

# Load mazes
maze0 = np.zeros((25, 25))
maze1 = np.load("maze1.npy")
maze2 = np.load("maze2.npy")
maze3 = np.load("maze3.npy")

# Colors
WHITE = (240, 240, 240)
BLACK = (20, 20, 20)
RED = (200, 30, 30)
HOVER = (255, 200, 200)
BUTTON = (255, 255, 255)
BORDER = (150, 150, 150)

# Fonts
FONT = pygame.font.SysFont("Arial", 22, bold=True)

# Screen setup
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def draw_button(surface, rect, text, font, hover, base_color, hover_color, border_color, text_color):
    color = hover_color if hover else base_color
    pygame.draw.rect(surface, color, rect, border_radius=8)
    pygame.draw.rect(surface, border_color, rect, width=2, border_radius=8)
    draw_text_center(surface, text, font, rect, text_color)


def draw_text_center(surface, text, font, rect, color):
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)


def draw_title(surface, text, font, y):
    title_surf = font.render(text, True, BLACK)
    title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, y))
    surface.blit(title_surf, title_rect)


def start_menu():
    start_button = pygame.Rect(125, 100, 150, 50)
    quit_button = pygame.Rect(125, 170, 150, 50)

    while True:
        screen.fill(WHITE)
        draw_title(screen, "Welcome to Frieren Maze Game", FONT, 50)

        mouse_pos = pygame.mouse.get_pos()
        draw_button(screen, start_button, "Start", FONT, start_button.collidepoint(mouse_pos),
                    BUTTON, HOVER, BORDER, RED)
        draw_button(screen, quit_button, "Quit", FONT, quit_button.collidepoint(mouse_pos),
                    BUTTON, HOVER, BORDER, RED)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(mouse_pos):
                    return  # Go to maze selection
                elif quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()


def maze_selection_menu():
    button_size = (150, 60)
    spacing = 30
    top_margin = 60

    buttons = [
        {"label": "Custom", "maze": maze0},
        {"label": "Maze 1", "maze": maze1},
        {"label": "Maze 2", "maze": maze2},
        {"label": "Maze 3", "maze": maze3},
    ]

    button_rects = []
    for i in range(2):
        for j in range(2):
            x = spacing + j * (button_size[0] + spacing)
            y = top_margin + i * (button_size[1] + spacing)
            button_rects.append(pygame.Rect(x, y, *button_size))

    while True:
        screen.fill(WHITE)
        draw_title(screen, "Select a Maze", FONT, 30)

        mouse_pos = pygame.mouse.get_pos()
        for idx, rect in enumerate(button_rects):
            draw_button(screen, rect, buttons[idx]["label"], FONT,
                        rect.collidepoint(mouse_pos), BUTTON, HOVER, BORDER, RED)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for idx, rect in enumerate(button_rects):
                    if rect.collidepoint(mouse_pos):
                        return buttons[idx]["maze"]


def get_user_input():
    start_menu()
    return maze_selection_menu()
