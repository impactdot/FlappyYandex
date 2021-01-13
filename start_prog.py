import pygame
import random
import sys


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


pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((576, 1024))
pygame.display.set_caption('Flappy bird')
clock = pygame.time.Clock()
game_font = pygame.font.Font('data/04B_19.ttf', 40)

FPS = 60
GRAVITY = 1
bird_movement = 0
game_active = True
score = 0
high_score = 0
count = 0

bg_surface = pygame.image.load('data/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('data/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load('data/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('data/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('data/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 512))

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
score_sound_countdown = 140


if __name__ == '__main__':
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird_movement = 0
                    bird_movement -= 9
                    flap_sound.play()
                if event.key == pygame.K_SPACE and game_active == False:
                    game_active = True
                    pipe_list.clear()
                    bird_rect.center = (100, 512)
                    bird_movement = 0
                    score = 0

            if event.type == SPAWN_PIPE:
                pipe_list.append(create_pipe(score))

            if event.type == BIRDFLAP:
                if bird_index < 2:
                    bird_index += 1
                else:
                    bird_index = 0

                bird_surface, bird_rect = bird_animation()

        screen.blit(bg_surface, (0, 0))

        if game_active:
            if count == 0:
                bird_movement += GRAVITY
            rotated_bird = rotate_bird(bird_surface)
            bird_rect.centery += bird_movement
            screen.blit(rotated_bird, bird_rect)
            game_active = check_collision(list(map(lambda x: x[0:2], pipe_list)))

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
        else:
            score_sound_countdown = 140
            screen.blit(game_over_surface, game_over_rect)
            high_score = update_score(score, high_score)
            score_display('game_over')

        floor_x_pos -= 1
        draw_floor()
        if floor_x_pos <= -576:
            floor_x_pos = 0
        count = (count + 1) % 4

        pygame.display.update()
        clock.tick(FPS)
