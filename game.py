import pygame
import random

# Initialize the game
pygame.init()

# Create display surface
GAME_FOLDER = 'C:\\Users\\nimra\\Desktop\\game\\escape_and_catch\\'
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Set caption and background
pygame.display.set_caption("Escape & Catch")
background_image = pygame.transform.scale(pygame.image.load(GAME_FOLDER + 'background.jpg'), (WINDOW_WIDTH, WINDOW_HEIGHT))

# Game actors (make the car bigger)
uncle = pygame.transform.scale(pygame.image.load(GAME_FOLDER + 'actor1.png'), (120, 160))
uncle_rect = uncle.get_rect()
uncle_rect.centerx = WINDOW_WIDTH // 2
uncle_rect.centery = WINDOW_HEIGHT - 180
uncle_velocity = 5

# Background scroll settings
background_y = 0  # Start background position
background_speed = 5  # Initial speed of background movement

# Coin actor and movement speed
coin = pygame.transform.scale(pygame.image.load(GAME_FOLDER + 'coin.png'), (32, 32))
coin_rect = coin.get_rect()
coin_rect.left = random.randint(100, WINDOW_WIDTH - coin_rect.width)
coin_rect.top = -50  # Start above the screen
coin_velocity = 5  # Initial speed of coin falling

# Obstacles
obstacle1 = pygame.transform.scale(pygame.image.load(GAME_FOLDER + 'obstacle1.png'), (100, 100))
obstacle2 = pygame.transform.scale(pygame.image.load(GAME_FOLDER + 'obstacle2.png'), (100, 100))
obstacle = random.choice([obstacle1, obstacle2])
obstacle_rect = obstacle.get_rect()
obstacle_rect.left = random.randint(100, WINDOW_WIDTH - obstacle_rect.width)
obstacle_rect.top = -50  # Start above the screen
obstacle_velocity = 5  # Initial speed of obstacles falling

# Game Sounds
loss = pygame.mixer.Sound(GAME_FOLDER + 'loss.wav')
loss.set_volume(0.5)
pick = pygame.mixer.Sound(GAME_FOLDER + 'pickup.wav')
pick.set_volume(0.5)
pygame.mixer.music.load(GAME_FOLDER + 'background_music.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Game HUD
big_game_font = pygame.font.Font(GAME_FOLDER + 'font1.ttf', 60)
small_game_font = pygame.font.Font(GAME_FOLDER + 'font1.ttf', 30)
black_color = pygame.Color(0, 0, 0)
white_color = pygame.Color(255, 255, 255)

game_title = big_game_font.render('Escape & Catch', True, black_color)
game_title_rect = game_title.get_rect()
game_title_rect.centerx = WINDOW_WIDTH // 2
game_title_rect.top = 10

player_score = 0
player_lives = 3
score = small_game_font.render('Score: ' + str(player_score), True, white_color)
score_rect = score.get_rect()
score_rect.left = 50
score_rect.top = 10

# Timer for coin delay
coin_timer = 0
coin_delay = 1000  # 1 second delay (1000 milliseconds)

# Timer for obstacle delay
obstacle_timer = 0
obstacle_delay = 1000  # 1 second delay for obstacle

# Game loop
FPS = 60
clock = pygame.time.Clock()
running = True
game_over = False

while running:
    # Handle events
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_q:
                running = False

    if not game_over:
        # Key input for uncle's movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and uncle_rect.left > 0:
            uncle_rect.left -= uncle_velocity
        if keys[pygame.K_RIGHT] and uncle_rect.right < WINDOW_WIDTH:
            uncle_rect.right += uncle_velocity

        # Scroll the background
        background_y += background_speed
        if background_y >= WINDOW_HEIGHT:
            background_y = 0  # Reset background when fully scrolled

        # Apply the background (scrolling)
        display_surface.blit(background_image, (0, background_y - WINDOW_HEIGHT))
        display_surface.blit(background_image, (0, background_y))

        # Move the coin down if enough time has passed (1 second delay)
        current_time = pygame.time.get_ticks()
        if current_time - coin_timer > coin_delay:
            coin_rect.top += coin_velocity

        # Move the obstacle down if enough time has passed
        if current_time - obstacle_timer > obstacle_delay:
            obstacle_rect.top += obstacle_velocity

        # Check if coin is caught by the uncle (car)
        if coin_rect.colliderect(uncle_rect):
            pick.play()
            player_score += 1
            score = small_game_font.render('Score: ' + str(player_score), True, white_color)
            # Respawn the coin after 1 second delay
            coin_timer = pygame.time.get_ticks()
            coin_rect.left = random.randint(100, WINDOW_WIDTH - coin_rect.width)
            coin_rect.top = -50  # Start above the screen again

        # Check if coin goes out of the screen (missed coin)
        if coin_rect.top > WINDOW_HEIGHT:
            # Respawn the coin after 1 second delay
            coin_timer = pygame.time.get_ticks()
            coin_rect.left = random.randint(100, WINDOW_WIDTH - coin_rect.width)
            coin_rect.top = -50  # Start above the screen again

        # Check if obstacle goes out of the screen
        if obstacle_rect.top > WINDOW_HEIGHT:
            obstacle = random.choice([obstacle1, obstacle2])  # Randomly choose the next obstacle
            obstacle_rect = obstacle.get_rect()
            obstacle_rect.left = random.randint(100, WINDOW_WIDTH - obstacle_rect.width)
            obstacle_rect.top = -50  # Start above the screen again
            obstacle_timer = pygame.time.get_ticks()  # Reset obstacle timer

        # Check for collision with the obstacle
        if obstacle_rect.colliderect(uncle_rect):
            loss.play()
            game_over = True  # Set game over flag

        # Gradually increase game speed
        if player_score > 0 and player_score % 5 == 0:  # Increase speed every 5 coins
            background_speed += 0.001
            coin_velocity += 0.001
            uncle_velocity += 0.001
            obstacle_velocity += 0.001  # Increase obstacle speed

        # Draw the car
        display_surface.blit(uncle, uncle_rect)

        # Draw the coin
        display_surface.blit(coin, coin_rect)

        # Draw the obstacle
        display_surface.blit(obstacle, obstacle_rect)

        # Draw HUD elements
        display_surface.blit(game_title, game_title_rect)
        display_surface.blit(score, score_rect)

    else:
        # Game Over screen
        game_over_message = big_game_font.render('Game Over!', True, black_color)
        game_over_rect = game_over_message.get_rect()
        game_over_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30)
        display_surface.blit(game_over_message, game_over_rect)

        restart_message = small_game_font.render('Press R to Restart or Q to Quit', True, white_color)
        restart_rect = restart_message.get_rect()
        restart_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30)
        display_surface.blit(restart_message, restart_rect)

        # Handle restart or quit
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:  # Restart the game
            player_score = 0
            player_lives = 3
            coin_rect.left = random.randint(100, WINDOW_WIDTH - coin_rect.width)
            coin_rect.top = -50
            obstacle_rect.left = random.randint(100, WINDOW_WIDTH - obstacle_rect.width)
            obstacle_rect.top = -50
            game_over = False
            coin_timer = 0
            obstacle_timer = 0
            background_speed = 5
            coin_velocity = 5
            uncle_velocity = 5
            obstacle_velocity = 5

    # Refresh window
    pygame.display.update()
    clock.tick(FPS)

# Quit the game
pygame.quit()
