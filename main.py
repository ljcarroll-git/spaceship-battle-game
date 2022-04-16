import pygame
import os
pygame.font.init()
pygame.mixer.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 600
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
FPS = 60
VELOCITY = 5
BULLET_VELOCITY = 20
BULLET_WIDTH, BULLET_HEIGHT = 10, 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 41.3
MAX_BULLETS = 4
BORDER_WIDTH = 10
GAME_CAPTION = "Space Battle"
BORDER = pygame.Rect(WINDOW_WIDTH//2 - BORDER_WIDTH//2, 0, BORDER_WIDTH, WINDOW_HEIGHT)

HEALTH_FONT = pygame.font.SysFont("arial", 40)
WINNER_FONT = pygame.font.SysFont("arial", 100)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    90)
    
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    270)

SPACE_IMAGE = pygame.transform.scale(
    pygame.image.load(os.path.join('Assets', 'space_2.jpg')),
    (WINDOW_WIDTH, WINDOW_HEIGHT))

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(GAME_CAPTION)

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WINDOW.blit(SPACE_IMAGE, (0,0))
    pygame.draw.rect(WINDOW, BLACK, BORDER)
    
    red_health_text = HEALTH_FONT.render(
        f"Health: {red_health}", 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        f"Health: {yellow_health}", 1, WHITE)

    WINDOW.blit(red_health_text, (WINDOW_WIDTH - red_health_text.get_width() - 10, 10))
    WINDOW.blit(yellow_health_text, (10, 10))
    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WINDOW.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)
    
    pygame.display.update()

def handle_yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0:  # LEFT
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x + VELOCITY + yellow.height < BORDER.x:  # RIGHT
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0:  # UP
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.width < WINDOW_HEIGHT:  # DOWN
        yellow.y += VELOCITY

def handle_red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width:
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + VELOCITY + red.height < WINDOW_WIDTH:
        red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0:
        red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.width < WINDOW_HEIGHT:
        red.y += VELOCITY

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WINDOW_WIDTH:
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WINDOW.blit(draw_text, (WINDOW_WIDTH//2 - draw_text.get_width()//2,
                        WINDOW_HEIGHT//2 - draw_text.get_height()//2))

    pygame.display.update()
    pygame.time.delay(5000)   

def main():
    pygame.event.clear()
    yellow = pygame.Rect(300, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow_bullets = []
    red_bullets = []
    starting_health = 10
    yellow_health = starting_health
    red_health = starting_health
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL and len(yellow_bullets) <= MAX_BULLETS:
                        bullet = pygame.Rect(
                            yellow.x + yellow.width, 
                            yellow.y + yellow.height//2 - BULLET_HEIGHT//2, 
                            BULLET_WIDTH, 
                            BULLET_HEIGHT)
                        yellow_bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()
                    if event.key == pygame.K_RCTRL and len(red_bullets) <= MAX_BULLETS:
                        bullet = pygame.Rect(
                            red.x, 
                            red.y + red.height//2 - BULLET_HEIGHT//2, 
                            BULLET_WIDTH, 
                            BULLET_HEIGHT)
                        red_bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()

                if event.type == RED_HIT:
                    red_health -= 1
                    BULLET_HIT_SOUND.play()
                    
                if event.type == YELLOW_HIT:
                    yellow_health -= 1
                    BULLET_HIT_SOUND.play()
        
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        if winner_text != "":
            draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        handle_yellow_movement(keys_pressed, yellow)
        handle_red_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
     
    main()

if __name__ == "__main__":
    main()