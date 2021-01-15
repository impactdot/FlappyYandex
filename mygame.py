import pygame
import random
import sys
import os
import sqlite3


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))


def create_pipe(n):
    if n % 10 == 8:
        random_pipe_pos = random.randrange(400, 900)
        bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
        top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 250))
        return [bottom_pipe, top_pipe, True]
    random_pipe_pos = random.randrange(400, 900)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 350))
    return [bottom_pipe, top_pipe, False]


def move_pipes(pipes):
    for pipe in pipes:
        pipe[0].centerx -= 5
        pipe[1].centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe[2]:
            screen.blit(red_pipe_surface, pipe[0])
            red_flip_pipe = pygame.transform.flip(red_pipe_surface, False, True)
            screen.blit(red_flip_pipe, pipe[1])
        else:
            screen.blit(pipe_surface, pipe[0])
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe[1])


def remove_pipes(pipes):
    for pipe in pipes:
        if pipe[0].centerx == -600:
            pipes.remove(pipe)
    return pipes


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe[0]) or bird_rect.colliderect(pipe[1]):
            death_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 850))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


def bird_chose_display():
    champ_text = "CHAMPION:" + winner_name
    current_champion_text = norm_font.render(champ_text, True, pygame.Color('red'))
    current_champion_text_rect = current_champion_text.get_rect(center=(230, 30))
    menu_text = game_font_big.render("Choose bird", True, pygame.Color('white'))
    menu_text_rect = menu_text.get_rect(center=(288, 100))
    inst_text = game_font.render("Push the 'esc' to continue", True, pygame.Color('white'))
    inst_text_rect = inst_text.get_rect(center=(288, 870))
    # champion text
    screen.blit(current_champion_text, current_champion_text_rect)
    # слово "MENU"
    screen.blit(menu_text, menu_text_rect)
    # текст
    screen.blit(inst_text, inst_text_rect)
    screen.blit(big_bluebird, big_bluebird_rect)
    screen.blit(big_yellowbird, big_yellowbird_rect)
    screen.blit(big_blackbird, big_blackbird_rect)


# database connection
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "george.db")
con = sqlite3.connect(db_path)
cur = con.cursor()


pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((576, 1000))
pygame.display.set_caption('FlappyYandex')
clock = pygame.time.Clock()
norm_font = pygame.font.Font('data/Bullpen3D.ttf', 40)
norm_font_small = pygame.font.Font('data/Bullpen3D.ttf', 20)
game_font = pygame.font.Font('data/04B_19.ttf', 40)
game_font_big = pygame.font.Font('data/04B_19.ttf', 60)

FPS = 60
GRAVITY = 1
bird_movement = 0
# когда стукнулись, но пока не перешли в меню
game_over = False
# поле для имени
input_box = pygame.Rect(200, 380, 190, 50)
winner_name = ''
# проверить, можно ли ввести имя?
input_active = False
# если мы уже играем, то есть прыгаем и скачем
game_active = False
# открыто ли меню с птичками, регистрацией и всякой такой фигней
bird_chose = False

score = 0
high_score = 0
count = 0
letter_counter = 0

yandex_logo = pygame.image.load('data/ylogo.png').convert_alpha()
yandex_logo_rect = yandex_logo.get_rect(center=(288, 180))

scroll_surface = pygame.image.load('data/scroll.png').convert_alpha()
scroll_surface = pygame.transform.scale(scroll_surface, (40, 40))

bg_surface = pygame.image.load('data/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)
bg_surface_night = pygame.image.load('data/background-night.png').convert()
bg_surface_night = pygame.transform.scale2x(bg_surface_night)

floor_surface = pygame.image.load('data/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

# нужно это как то красиво сделать, как в уроках показывали
bluebird_downflap = pygame.transform.scale2x(pygame.image.load('data/bluebird-downflap.png').convert_alpha())
bluebird_midflap = pygame.transform.scale2x(pygame.image.load('data/bluebird-midflap.png').convert_alpha())
bluebird_upflap = pygame.transform.scale2x(pygame.image.load('data/bluebird-upflap.png').convert_alpha())
bird_frames = [bluebird_downflap, bluebird_midflap, bluebird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 512))

bird_icon = pygame.image.load('data/bluebird-midflap.png').convert_alpha()
bird_icon_rect = bird_icon.get_rect(topleft=(10, 10))

yellowbird_downflap = pygame.transform.scale2x(pygame.image.load('data/yellowbird-downflap.png').convert_alpha())
yellowbird_midflap = pygame.transform.scale2x(pygame.image.load('data/yellowbird-midflap.png').convert_alpha())
yellowbird_upflap = pygame.transform.scale2x(pygame.image.load('data/yellowbird-upflap.png').convert_alpha())

blackbird_downflap = pygame.transform.scale2x(pygame.image.load('data/blackbird-downflap.png').convert_alpha())
blackbird_midflap = pygame.transform.scale2x(pygame.image.load('data/blackbird-midflap.png').convert_alpha())
blackbird_upflap = pygame.transform.scale2x(pygame.image.load('data/blackbird-upflap.png').convert_alpha())

big_bluebird = pygame.transform.scale2x(bluebird_midflap)
big_bluebird_rect = big_bluebird.get_rect(center=(screen.get_width() // 2, 250))
big_yellowbird = pygame.transform.scale2x(yellowbird_midflap)
big_yellowbird_rect = big_yellowbird.get_rect(center=(screen.get_width() // 2, 450))
big_blackbird = pygame.transform.scale2x(blackbird_midflap)
big_blackbird_rect = big_blackbird.get_rect(center=(screen.get_width() // 2, 650))


BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

red_pipe_surface = pygame.image.load('data/pipe-red.png')
red_pipe_surface = pygame.transform.scale2x(red_pipe_surface)
pipe_surface = pygame.image.load('data/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWN_PIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE, 1200)

game_over_surface = pygame.transform.scale2x(pygame.image.load('data/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(288, 512))

flap_sound = pygame.mixer.Sound('data/sfx_wing.wav')
death_sound = pygame.mixer.Sound('data/sfx_hit.wav')
score_sound = pygame.mixer.Sound('data/sfx_point.wav')
peacock_sound = pygame.mixer.Sound('data/peacock.wav')
score_sound_countdown = 140


if __name__ == '__main__':
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f and game_active:
                    peacock_sound.play()

                if event.key == pygame.K_SPACE and game_active:
                    bird_movement = 0
                    bird_movement -= 9
                    flap_sound.play()

                if event.key == pygame.K_ESCAPE and bird_chose:
                    bird_chose = False
                    game_active = False

                if event.key == pygame.K_SPACE and not game_active:
                    game_active = True
                    pipe_list.clear()
                    bird_rect.center = (100, 512)
                    bird_movement = 0
                    score = 0
            # not bird_chose_display - т.к. это мы не делаем в меню
            if event.type == pygame.KEYDOWN and game_over:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        letter_counter = 0
                        game_over = False
                        # обновил вверху account
                    elif event.key == pygame.K_BACKSPACE:
                        winner_name = winner_name[:-1]
                        if letter_counter >= 1:
                            letter_counter -= 1
                        else:
                            letter_counter = 0
                    else:
                        if letter_counter <= 6:
                            winner_name += event.unicode
                            letter_counter += 1

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not game_over:
                    if game_active:
                        bird_movement = 0
                        bird_movement -= 9
                        flap_sound.play()
                    else:
                        if bird_chose:
                            pass
                        else:
                            if event.pos[0] <= 44 and event.pos[1] <= 34:
                                bird_chose = True
                            else:
                                game_active = True
                                pipe_list.clear()
                                bird_rect.center = (100, 512)
                                bird_movement = 0
                                score = 0
                                score_sound_countdown = 140
                elif event.button == 1 and game_over:
                    # If the user clicked on the input_box rect.
                    if input_box.collidepoint(event.pos):
                        # Toggle the active variable.
                        input_active = not input_active
                    else:
                        input_active = False

            if event.type == SPAWN_PIPE:
                pipe_list.append(create_pipe(score))

            if event.type == BIRDFLAP:
                if bird_index < 2:
                    bird_index += 1
                else:
                    bird_index = 0

                bird_surface, bird_rect = bird_animation()

        if score % 60 < 30:
            screen.blit(bg_surface, (0, 0))
        else:
            screen.blit(bg_surface_night, (0, 0))

        if bird_chose:
            bird_chose_display()
        else:
            if game_active:
                if count == 0:
                    bird_movement += GRAVITY
                rotated_bird = rotate_bird(bird_surface)
                bird_rect.centery += bird_movement
                screen.blit(rotated_bird, bird_rect)
                game_active = check_collision(list(map(lambda x: x[0:2], pipe_list)))
                if not game_active:
                    game_over = True
                pipe_list = move_pipes(pipe_list)
                pipe_list = remove_pipes(pipe_list)
                draw_pipes(pipe_list)
                score_display('main_game')
                score_sound_countdown -= 1
                if score_sound_countdown <= 0:
                    score += 1
                    if score % 5 == 0:
                        score_sound.play()
                    score_sound_countdown = 70
            elif not game_active and game_over:
                if score > high_score:
                    screen.blit(bg_surface, (0, 0))
                    winner_text1 = norm_font.render("ENTER YOUR NAME,", True, pygame.Color('blue'))
                    winner_text1_rect = winner_text1.get_rect(center=(288, 300))
                    screen.blit(winner_text1, winner_text1_rect)
                    winner_text2 = norm_font.render("NEW CHAMPION", True, pygame.Color('blue'))
                    winner_text2_rect = winner_text2.get_rect(center=(288, 350))
                    screen.blit(winner_text2, winner_text2_rect)
                    txt_surface = norm_font.render(winner_name, True, pygame.Color('blue'))
                    screen.blit(txt_surface, (input_box.x, input_box.y))
                    # Blit the input_box rect.
                    pygame.draw.rect(screen, pygame.Color('green'), input_box, 2)
                else:
                    game_over = False
            else:
                score_sound_countdown = 140
                # запуск меню
                screen.blit(bird_icon, bird_icon_rect)
                screen.blit(game_over_surface, game_over_rect)
                screen.blit(yandex_logo, yandex_logo_rect)
                # eto figna
                high_score = update_score(score, high_score)
                score_display('game_over')

        floor_x_pos -= 1
        draw_floor()
        if floor_x_pos <= -576:
            floor_x_pos = 0
        count = (count + 1) % 4
        pygame.display.update()
        clock.tick(FPS)