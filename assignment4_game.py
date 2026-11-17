import pygame

WIDTH = 800
HEIGHT = 600
FPS = 60

PLAYER_SIZE = 36
PLAYER_SPEED = 5
JUMP_SPEED = -15
GRAVITY = 0.6
MAX_FALL_SPEED = 16

COIN_RADIUS = 7
COIN_SIZE = 14
TOTAL_COINS = 5

FIREBALL_RADIUS = 12
FIREBALL_SIZE = 24

LEDGE_HEIGHT = 30
LEDGE_RISE = 95
SHAFT_LEFT = 350
SHAFT_RIGHT = 450
SHAFT_CENTER = 400

SKY_BLUE = (135, 206, 235)
SUNSET = (250, 150, 120)
NIGHT = (25, 30, 60)
BLUE = (50, 120, 255)
RED = (230, 40, 40)
GREEN = (0, 200, 0)
YELLOW = (250, 210, 60)
GOLD = (200, 150, 20)
GREY = (120, 120, 120)
BROWN = (130, 90, 60)
DARK_GREY = (65, 65, 85)
GRASS = (60, 190, 80)
SAND = (230, 180, 100)
TEAL = (80, 210, 190)
ORANGE = (255, 130, 40)
FIRE_RED = (240, 50, 20)
FIRE_ORANGE = (255, 150, 30)
FIRE_YELLOW = (255, 230, 80)
SPIKE = (230, 230, 230)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def get_world_height(level):
   
    if level == 1:
        height = 1500
    elif level == 2:
        height = 1700
    else:
        height = 1900
    return height


def get_level_name(level):
   
    if level == 1:
        name = "Meadow"
    elif level == 2:
        name = "Sunset"
    else:
        name = "Night"
    return name


def create_walls(level):
   
    world_height = get_world_height(level)
    walls = []
    y = world_height - LEDGE_HEIGHT
    side = 0

    while y > 90:
        if side == 0:
            walls.append(pygame.Rect(0, y, SHAFT_LEFT, LEDGE_HEIGHT))
            side = 1
        else:
            walls.append(
                pygame.Rect(SHAFT_RIGHT, y, WIDTH - SHAFT_RIGHT, LEDGE_HEIGHT)
            )
            side = 0
        y = y - LEDGE_RISE

    return walls


def create_coins(level):
  
    walls = create_walls(level)
    coins = []
    indexes = [1, 4, 7, 10, len(walls) - 1]

    for index in indexes:
        ledge = walls[index]
        coins.append([SHAFT_CENTER, ledge.top - 75])

    return coins


def create_exit(level):
  
    walls = create_walls(level)
    top = walls[len(walls) - 1]

    if top.left == 0:
        exit_rect = pygame.Rect(top.right - 70, top.top - 60, 40, 60)
    else:
        exit_rect = pygame.Rect(top.left + 30, top.top - 60, 40, 60)

    return exit_rect


def create_fireballs(level):
 
    if level == 1:
        fireballs = [
            [370, 1000, 900, 1100, 2],
            [430, 600, 500, 700, 2]
        ]
    elif level == 2:
        fireballs = [
            [370, 1250, 1150, 1350, 3],
            [430, 900, 800, 1000, 3],
            [370, 550, 450, 650, 3]
        ]
    else:
        fireballs = [
            [370, 1550, 1450, 1650, 3],
            [430, 1250, 1150, 1350, 3],
            [370, 950, 850, 1050, 4],
            [430, 650, 550, 750, 4]
        ]

    return fireballs


def create_spikes(level):
    
    walls = create_walls(level)
    spikes = []
    indexes = [3, 6, 9, 12]

    for index in indexes:
        if index < len(walls) - 1:
            ledge = walls[index]
            if ledge.left == 0:
                spikes.append(pygame.Rect(80, ledge.top - 16, 60, 16))
            else:
                spikes.append(pygame.Rect(660, ledge.top - 16, 60, 16))

    return spikes


def check_on_ground(player_x, player_y, walls):
   
    player = pygame.Rect(player_x, player_y + 1, PLAYER_SIZE, PLAYER_SIZE)

    for wall in walls:
        if player.colliderect(wall):
            return True

    return False


def move_player(player_x, player_y, x_change, y_change, walls):

    player_x = player_x + x_change
    player = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)

    for wall in walls:
        if player.colliderect(wall):
            player_x = player_x - x_change
            player = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)

    player_y = player_y + y_change
    player = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
    landed = False

    for wall in walls:
        if player.colliderect(wall):
            if y_change > 0:
                player_y = wall.top - PLAYER_SIZE
                landed = True
            elif y_change < 0:
                player_y = wall.bottom
            player = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)

    return player_x, player_y, landed


def move_fireballs(fireballs):
 
    for fireball in fireballs:
        fireball[1] = fireball[1] + fireball[4]

        if fireball[1] < fireball[2]:
            fireball[1] = fireball[2]
            fireball[4] = -fireball[4]
        if fireball[1] > fireball[3]:
            fireball[1] = fireball[3]
            fireball[4] = -fireball[4]


def hit_fireball(player, fireballs):

    for fireball in fireballs:
        rect = pygame.Rect(
            fireball[0] - FIREBALL_RADIUS,
            fireball[1] - FIREBALL_RADIUS,
            FIREBALL_SIZE,
            FIREBALL_SIZE
        )
        if player.colliderect(rect):
            return True

    return False


def hit_spikes(player, spikes):
 
    for spike in spikes:
        if player.colliderect(spike):
            return True

    return False


def collect_coins(player, coins):
   
    coins_left = []

    for coin in coins:
        coin_rect = pygame.Rect(
            coin[0] - COIN_RADIUS,
            coin[1] - COIN_RADIUS,
            COIN_SIZE,
            COIN_SIZE
        )
        if not player.colliderect(coin_rect):
            coins_left.append(coin)

    return coins_left


def draw_cloud(screen, x, y, colour):
 
    pygame.draw.circle(screen, colour, (x, y), 25)
    pygame.draw.circle(screen, colour, (x - 30, y + 8), 20)
    pygame.draw.circle(screen, colour, (x + 30, y + 8), 20)


def draw_background(screen, level):
   
    if level == 1:
        screen.fill(SKY_BLUE)
        pygame.draw.circle(screen, YELLOW, (700, 80), 45)
        draw_cloud(screen, 120, 100, WHITE)
        draw_cloud(screen, 400, 70, WHITE)
        draw_cloud(screen, 610, 160, WHITE)
    elif level == 2:
        screen.fill(SUNSET)
        pygame.draw.circle(screen, ORANGE, (680, 150), 55)
        draw_cloud(screen, 130, 90, (255, 215, 200))
        draw_cloud(screen, 420, 120, (255, 215, 200))
    else:
        screen.fill(NIGHT)
        pygame.draw.circle(screen, (240, 240, 200), (680, 90), 42)
        pygame.draw.circle(screen, NIGHT, (700, 75), 40)
        stars = [
            [90, 80], [180, 150], [300, 70], [390, 130],
            [520, 60], [600, 150], [760, 140]
        ]
        for star in stars:
            pygame.draw.circle(screen, WHITE, (star[0], star[1]), 2)


def draw_walls(screen, walls, level, camera_y):
 
    if level == 1:
        body = GREY
        top = GRASS
    elif level == 2:
        body = BROWN
        top = SAND
    else:
        body = DARK_GREY
        top = TEAL

    for wall in walls:
        rect = pygame.Rect(
            wall.left, wall.top - camera_y, wall.width, wall.height
        )
        if rect.bottom > 0 and rect.top < HEIGHT:
            pygame.draw.rect(screen, body, rect)
            pygame.draw.rect(
                screen, top, (rect.left, rect.top, rect.width, 8)
            )
            pygame.draw.rect(screen, BLACK, rect, 2)


def draw_spikes(screen, spikes, camera_y):
   
    for spike in spikes:
        top = spike.top - camera_y
        if top < HEIGHT and top + spike.height > 0:
            number = spike.width // 12
            for index in range(number):
                x = spike.left + index * 12
                points = [
                    (x, top + spike.height),
                    (x + 6, top),
                    (x + 12, top + spike.height)
                ]
                pygame.draw.polygon(screen, SPIKE, points)
                pygame.draw.polygon(screen, BLACK, points, 1)


def draw_coins(screen, coins, frames, camera_y):
  
    radius = COIN_RADIUS + (frames // 15) % 2

    for coin in coins:
        y = coin[1] - camera_y
        if y > -20 and y < HEIGHT + 20:
            pygame.draw.circle(screen, GOLD, (coin[0], y), radius + 2)
            pygame.draw.circle(screen, YELLOW, (coin[0], y), radius)
            pygame.draw.circle(screen, WHITE, (coin[0] - 2, y - 2), 2)


def draw_exit(screen, exit_rect, open_door, camera_y):
   
    if open_door:
        colour = GREEN
    else:
        colour = RED

    rect = pygame.Rect(
        exit_rect.left, exit_rect.top - camera_y,
        exit_rect.width, exit_rect.height
    )
    pygame.draw.rect(screen, colour, rect)
    pygame.draw.rect(screen, BLACK, rect, 3)
    pygame.draw.circle(
        screen, YELLOW, (rect.right - 10, rect.top + 30), 3
    )


def draw_fireballs(screen, fireballs, frames, camera_y):
  
    radius = FIREBALL_RADIUS + (frames // 6) % 2

    for fireball in fireballs:
        y = fireball[1] - camera_y
        if y > -30 and y < HEIGHT + 30:
            pygame.draw.circle(screen, FIRE_RED, (fireball[0], y), radius)
            pygame.draw.circle(
                screen, FIRE_ORANGE, (fireball[0], y), radius - 4
            )
            pygame.draw.circle(
                screen, FIRE_YELLOW, (fireball[0], y), radius - 8
            )
            pygame.draw.circle(
                screen, BLACK, (fireball[0], y), radius, 2
            )


def draw_player(screen, player, camera_y):
    """Draw the player with eyes.

    Args:
        screen: The pygame surface to draw on.
        player: The player's pygame.Rect.
        camera_y: How far the world has scrolled up.

    Returns:
        None.
    """
    rect = pygame.Rect(
        player.left, player.top - camera_y, PLAYER_SIZE, PLAYER_SIZE
    )
    pygame.draw.rect(screen, BLUE, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    pygame.draw.circle(screen, WHITE, (rect.left + 11, rect.top + 12), 5)
    pygame.draw.circle(screen, WHITE, (rect.left + 25, rect.top + 12), 5)
    pygame.draw.circle(screen, BLACK, (rect.left + 12, rect.top + 12), 2)
    pygame.draw.circle(screen, BLACK, (rect.left + 26, rect.top + 12), 2)


def draw_text(screen, text, size, x, y, colour):
    """Draw one line of text on the screen.

    Args:
        screen: The pygame surface to draw on.
        text: The words to show.
        size: The font size in pixels.
        x: The left edge of the text.
        y: The top edge of the text.
        colour: The colour of the text.

    Returns:
        None.
    """
    font = pygame.font.SysFont(None, size)
    message = font.render(text, True, colour)
    screen.blit(message, (x, y))


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Assignment 4 - Platformer")

pygame.mixer.music.load("background_music.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()
level = 1
world_height = get_world_height(level)
walls = create_walls(level)
coins = create_coins(level)
exit_rect = create_exit(level)
fireballs = create_fireballs(level)
spikes = create_spikes(level)

player_x = 150
player_y = world_height - LEDGE_HEIGHT - PLAYER_SIZE
start_y = player_y
camera_y = world_height - HEIGHT + 40
player_y_speed = 0
level_frames = 0
game_state = "playing"
lose_message = "YOU FELL!"

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        running = False

    if game_state == "playing":
        x_change = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            x_change = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x_change = PLAYER_SPEED

        on_ground = check_on_ground(player_x, player_y, walls)

        if on_ground and (
            keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]
        ):
            player_y_speed = JUMP_SPEED

        player_y_speed = player_y_speed + GRAVITY
        if player_y_speed > MAX_FALL_SPEED:
            player_y_speed = MAX_FALL_SPEED

        player_x, player_y, landed = move_player(
            player_x, player_y, x_change, player_y_speed, walls
        )

        if landed:
            player_y_speed = 0

        if player_x < 0:
            player_x = 0
        if player_x > WIDTH - PLAYER_SIZE:
            player_x = WIDTH - PLAYER_SIZE

        move_fireballs(fireballs)

        player = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
        coins = collect_coins(player, coins)
        level_frames = level_frames + 1

        camera_y = int(player_y) - 390
        if camera_y < 0:
            camera_y = 0
        if camera_y > world_height - HEIGHT + 40:
            camera_y = world_height - HEIGHT + 40

        if player_y > world_height:
            game_state = "lost"
            lose_message = "YOU FELL!"
        elif hit_spikes(player, spikes):
            game_state = "lost"
            lose_message = "OUCH!"
        elif hit_fireball(player, fireballs):
            game_state = "lost"
            lose_message = "BURNED!"

        if game_state == "playing":
            if len(coins) == 0 and player.colliderect(exit_rect):
                if level == 3:
                    game_state = "won"
                else:
                    game_state = "next"

    else:
        if keys[pygame.K_r]:
            if game_state == "next":
                level = level + 1
            elif game_state == "won":
                level = 1

            world_height = get_world_height(level)
            walls = create_walls(level)
            coins = create_coins(level)
            exit_rect = create_exit(level)
            fireballs = create_fireballs(level)
            spikes = create_spikes(level)
            player_x = 150
            player_y = world_height - LEDGE_HEIGHT - PLAYER_SIZE
            start_y = player_y
            camera_y = world_height - HEIGHT + 40
            player_y_speed = 0
            level_frames = 0
            game_state = "playing"

    draw_background(screen, level)
    draw_walls(screen, walls, level, camera_y)
    draw_spikes(screen, spikes, camera_y)
    draw_coins(screen, coins, level_frames, camera_y)
    draw_exit(screen, exit_rect, len(coins) == 0, camera_y)
    draw_fireballs(screen, fireballs, level_frames, camera_y)

    player = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
    draw_player(screen, player, camera_y)

    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 44))
    draw_text(
        screen,
        "Level " + str(level) + " - " + get_level_name(level),
        24, 20, 10, WHITE
    )
    draw_text(
        screen,
        "Coins: " + str(TOTAL_COINS - len(coins)) + " / " + str(TOTAL_COINS),
        24, 300, 10, WHITE
    )

    height = int(start_y - player_y) // 10
    if height < 0:
        height = 0
    draw_text(screen, "Height: " + str(height) + "m", 24, 500, 10, WHITE)
    draw_text(
        screen, "Time: " + str(level_frames // FPS) + "s", 24, 660, 10, WHITE
    )

    pygame.draw.rect(screen, BLACK, (0, HEIGHT - 44, WIDTH, 44))
    if game_state == "playing":
        if len(coins) == 0:
            draw_text(
                screen, "The door is open! Climb to the top!",
                22, 20, HEIGHT - 34, WHITE
            )
        else:
            draw_text(
                screen, "Climb up, grab the coins, and dodge the fireballs!",
                22, 20, HEIGHT - 34, WHITE
            )

    if game_state == "next":
        panel = pygame.Rect(170, 195, 460, 210)
        pygame.draw.rect(screen, BLACK, panel)
        pygame.draw.rect(screen, WHITE, panel, 3)
        draw_text(screen, "LEVEL COMPLETE!", 44, 205, 215, GREEN)
        draw_text(
            screen, "Time: " + str(level_frames // FPS) + "s",
            28, 350, 280, WHITE
        )
        draw_text(
            screen, "Press R for level " + str(level + 1),
            26, 240, 335, WHITE
        )

    if game_state == "won":
        panel = pygame.Rect(170, 195, 460, 210)
        pygame.draw.rect(screen, BLACK, panel)
        pygame.draw.rect(screen, WHITE, panel, 3)
        draw_text(screen, "YOU WIN!", 56, 285, 215, GREEN)
        draw_text(
            screen, "Time: " + str(level_frames // FPS) + "s",
            28, 350, 285, WHITE
        )
        draw_text(screen, "Press R to play again", 26, 265, 335, WHITE)

    if game_state == "lost":
        panel = pygame.Rect(170, 195, 460, 210)
        pygame.draw.rect(screen, BLACK, panel)
        pygame.draw.rect(screen, WHITE, panel, 3)
        lose_x = 400 - len(lose_message) * 15
        draw_text(screen, lose_message, 56, lose_x, 215, RED)
        draw_text(
            screen, "Time: " + str(level_frames // FPS) + "s",
            28, 350, 280, WHITE
        )
        draw_text(screen, "Press R to try again", 26, 265, 335, WHITE)

    pygame.display.flip()

pygame.quit()
