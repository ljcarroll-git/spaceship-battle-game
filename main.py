import pygame
import os
pygame.font.init()
pygame.mixer.init()

GAME_CAPTION = "Space Battle"
WINDOW_WIDTH, WINDOW_HEIGHT = 500, 300
FPS = 60

BORDER_WIDTH = WINDOW_WIDTH//333
BORDER_X_COORDINATE = WINDOW_WIDTH//2 - BORDER_WIDTH//2
BORDER_Y_COORDINATE = 0
BORDER = pygame.Rect(BORDER_X_COORDINATE, BORDER_Y_COORDINATE, BORDER_WIDTH, WINDOW_HEIGHT)

BULLET_VELOCITY = 20
BULLET_WIDTH, BULLET_HEIGHT = 10, 5
MAX_BULLETS = 3

SHIP_VELOCITY = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 41.3

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)

HEALTH_FONT = pygame.font.SysFont("arial", 40)
WINNER_FONT = pygame.font.SysFont("arial", 100)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'laser_sound.mp3'))
SHIP_EXPLOSION_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'explosion.mp3'))

PLAYER_1_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship-1.png'))
PLAYER_1_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(PLAYER_1_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    270)
PLAYER_2_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
PLAYER_2_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(PLAYER_2_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    270)
SPACE_IMAGE = pygame.transform.scale(
    pygame.image.load(os.path.join('Assets', 'space-2.png')),
    (WINDOW_WIDTH, WINDOW_HEIGHT))

PLAYER_1_HIT = pygame.USEREVENT + 1
PLAYER_2_HIT = pygame.USEREVENT + 2

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(GAME_CAPTION)

def draw_window(player_1, player_2, player_1_bullets, player_2_bullets, player_1_health, player_2_health):
    WINDOW.blit(SPACE_IMAGE, (0,0))
    pygame.draw.rect(WINDOW, WHITE, BORDER)
    
    player_1_health_text = HEALTH_FONT.render(
        f"Health: {player_1_health}", 1, WHITE)
    player_2_health_text = HEALTH_FONT.render(
        f"Health: {player_2_health}", 1, WHITE)

    WINDOW.blit(player_1_health_text, (10, 10))
    WINDOW.blit(player_2_health_text, (WINDOW_WIDTH - player_2_health_text.get_width() - 10, 10))
    WINDOW.blit(PLAYER_1_SPACESHIP, (player_1.x, player_1.y))
    WINDOW.blit(PLAYER_2_SPACESHIP, (player_2.x, player_2.y))

    for bullet in player_1_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)
    
    for bullet in player_2_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)
    
    pygame.display.update()

def handle_player_1_movement(keys_pressed, player_1):
    if keys_pressed[pygame.K_a] and player_1.x - SHIP_VELOCITY > 0:  # LEFT
        player_1.x -= SHIP_VELOCITY
    if keys_pressed[pygame.K_d] and player_1.x + SHIP_VELOCITY + player_1.width < BORDER.x:  # RIGHT
        player_1.x += SHIP_VELOCITY
    if keys_pressed[pygame.K_w] and player_1.y - SHIP_VELOCITY > 0:  # UP
        player_1.y -= SHIP_VELOCITY
    if keys_pressed[pygame.K_s] and player_1.y + SHIP_VELOCITY + player_1.height < WINDOW_HEIGHT:  # DOWN
        player_1.y += SHIP_VELOCITY

def handle_player_2_movement(keys_pressed, player_2):
    if keys_pressed[pygame.K_LEFT] and player_2.x - SHIP_VELOCITY > BORDER.x + BORDER.width:
        player_2.x -= SHIP_VELOCITY
    if keys_pressed[pygame.K_RIGHT] and player_2.x + SHIP_VELOCITY + player_2.width < WINDOW_WIDTH:
        player_2.x += SHIP_VELOCITY
    if keys_pressed[pygame.K_UP] and player_2.y - SHIP_VELOCITY > 0:
        player_2.y -= SHIP_VELOCITY
    if keys_pressed[pygame.K_DOWN] and player_2.y + SHIP_VELOCITY + player_2.height < WINDOW_HEIGHT:
        player_2.y += SHIP_VELOCITY

def handle_bullets(player_1_bullets, player_2_bullets, player_1, player_2):
    for bullet in player_1_bullets:
        bullet.x += BULLET_VELOCITY
        if player_2.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PLAYER_2_HIT))
            player_1_bullets.remove(bullet)
        elif bullet.x > WINDOW_WIDTH:
            player_1_bullets.remove(bullet)
    
    for bullet in player_2_bullets:
        bullet.x -= BULLET_VELOCITY
        if player_1.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PLAYER_1_HIT))
            player_2_bullets.remove(bullet)
        elif bullet.x < 0:
            player_2_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WINDOW.blit(draw_text, (WINDOW_WIDTH//2 - draw_text.get_width()//2,
                        WINDOW_HEIGHT//2 - draw_text.get_height()//2))

    pygame.display.update()
    pygame.time.delay(3000)   

def main():
    pygame.event.clear()

    player_1_initial_x_coordinate = (BORDER_X_COORDINATE - 0)//3
    player_1_initial_y_coordinate = WINDOW_HEIGHT//2

    player_2_initial_x_coordinate = 2*(WINDOW_WIDTH - BORDER_X_COORDINATE)//3 + BORDER_X_COORDINATE + BORDER_WIDTH - PLAYER_2_SPACESHIP.get_width()
    player_2_initial_y_coordinate = WINDOW_HEIGHT//2

    player_1 = pygame.Rect(player_1_initial_x_coordinate, player_1_initial_y_coordinate, PLAYER_1_SPACESHIP.get_width(), PLAYER_1_SPACESHIP.get_height())
    player_2 = pygame.Rect(player_2_initial_x_coordinate, player_2_initial_y_coordinate, PLAYER_2_SPACESHIP.get_width(), PLAYER_2_SPACESHIP.get_height())
    player_1_bullets = []
    player_2_bullets = []
    starting_health = 10
    player_1_health = starting_health
    player_2_health = starting_health
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL and len(player_1_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(
                            player_1.x + player_1.width, 
                            player_1.y + player_1.height//2 - BULLET_HEIGHT//2, 
                            BULLET_WIDTH, 
                            BULLET_HEIGHT)
                        player_1_bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()
                    if event.key == pygame.K_RCTRL and len(player_2_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(
                            player_2.x, 
                            player_2.y + player_2.height//2 - BULLET_HEIGHT//2, 
                            BULLET_WIDTH, 
                            BULLET_HEIGHT)
                        player_2_bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()

                if event.type == PLAYER_2_HIT:
                    player_2_health -= 1
                    BULLET_HIT_SOUND.play()
                    
                if event.type == PLAYER_1_HIT:
                    player_1_health -= 1
                    BULLET_HIT_SOUND.play()
        
        winner_text = ""
        if player_2_health <= 0:
            winner_text = "Player 1 Wins!"
        if player_1_health <= 0:
            winner_text = "Player 2 Wins!"
        if winner_text != "":
            SHIP_EXPLOSION_SOUND.play()
            draw_window(player_1, player_2, player_1_bullets, player_2_bullets, player_1_health, player_2_health)
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        handle_player_1_movement(keys_pressed, player_1)
        handle_player_2_movement(keys_pressed, player_2)
        handle_bullets(player_1_bullets, player_2_bullets, player_1, player_2)
        draw_window(player_1, player_2, player_1_bullets, player_2_bullets, player_1_health, player_2_health)
     
    main()

if __name__ == "__main__":
    main()