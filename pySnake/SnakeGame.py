import datetime
import sys
import random

import pygame


def play():
    pygame.mixer.init(44100, -16, 2, 2048)
    music = pygame.mixer.Sound('499fe33297885e4.mp3')
    scors = open('highscore.txt', 'r+')

    snake_speed = 10
    speed = 0

    window_x = 720
    window_y = 480

    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)

    pygame.init()

    pygame.display.set_caption('Snake Game')
    game_window = pygame.display.set_mode((window_x, window_y))

    fps = pygame.time.Clock()

    snake_position = [100, 50]

    snake_body = [[100, 50],
                  [90, 50],
                  [80, 50],
                  [70, 50]
                  ]
    fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                      random.randrange(1, (window_y // 10)) * 10]

    fruit_spawn = True

    direction = 'RIGHT'
    change_to = direction

    score = 0

    def show_score(color, font, size):

        score_font = pygame.font.SysFont(font, size)

        score_surface = score_font.render('Score : ' + str(score), True, color)

        score_rect = score_surface.get_rect()

        game_window.blit(score_surface, score_rect)

    def save_score(score_to_save):
        scors.write(f'{str(score_to_save)}\n')

    def game_over():
        save_score(score)
        my_font = pygame.font.SysFont('times new roman', 50)

        max_score = 0
        for line in scors.readlines():
            if int(line) > max_score:
                max_score = int(line)

        game_over_surface = my_font.render(
            f'Your Score is : {str(score)} Best: {max_score}', True, red)

        game_over_rect = game_over_surface.get_rect()

        game_over_rect.midtop = (window_x / 2, window_y / 4)

        game_window.blit(game_over_surface, game_over_rect)
        pygame.display.flip()

        scors.close()

        start = datetime.datetime.now()

        while start + datetime.timedelta(seconds=5) > datetime.datetime.now():
            for close_event in pygame.event.get():
                if close_event.type == pygame.QUIT:
                    sys.exit()

        play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                if event.key == pygame.K_RSHIFT:
                    change_to = 'SPACE'
                if event.key == pygame.K_ESCAPE:
                    change_to = 'ESCAPE'

        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'
        if change_to == 'SPACE':
            direction = 'SPACE'
        if change_to == 'ESCAPE':
            direction = 'ESCAPE'

        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10
        if direction == 'SPACE':
            if snake_speed > 0:
                speed = snake_speed
                snake_speed = 0
            if snake_speed == 0:
                snake_speed = speed
        if direction == 'ESCAPE':
            pygame.quit()

        snake_body.insert(0, list(snake_position))
        if snake_position[0] == fruit_position[0] and snake_position[1] == \
                fruit_position[1]:
            music.play()
            score += 10
            snake_speed += 1
            fruit_spawn = False
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                              random.randrange(1, (window_y // 10)) * 10]

        fruit_spawn = True
        game_window.fill(black)

        for pos in snake_body:
            pygame.draw.rect(game_window, green,
                             pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(game_window, white, pygame.Rect(
            fruit_position[0], fruit_position[1], 10, 10))

        if snake_position[0] < 0 or snake_position[0] > window_x - 10:
            game_over()
        if snake_position[1] < 0 or snake_position[1] > window_y - 10:
            game_over()

        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                game_over()

        show_score(white, 'times new roman', 20)

        pygame.display.update()

        fps.tick(snake_speed)


play()
