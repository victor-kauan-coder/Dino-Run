# -----------------------------------------------------------------------------
# Dino Game
#
# A Chrome Dino-style game created with Pygame.
# This version includes fixes for sprite positioning, clearer variable names,
# and English comments for better readability.
# -----------------------------------------------------------------------------

import pygame
from pygame.locals import *
from sys import exit
import os
from random import randrange, choice

# --- Initialization ---
pygame.init()
pygame.mixer.init()

# --- Constants ---

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 25)

# Screen Dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# --- Asset Loading ---

# Get the absolute path for the game's directories
main_dir = os.path.dirname(__file__)
image_dir = os.path.join(main_dir, 'images')
sound_dir = os.path.join(main_dir, 'songs')

# Load Sounds
jump_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'jump_sound.wav'))
death_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'death_sound.wav'))
score_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'score_sound.wav'))
score_sound.set_volume(0.6)

# Load Spritesheet
sprite_sheet = pygame.image.load(os.path.join(image_dir, 'dinoSpritesheet.png'))

# --- Game Window Setup ---
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dino Game')

# --- Game Variables ---
game_speed = 10
score = 0
is_game_over = False
# Obstacle type: 0 for Cactus, 1 for Pterodactyl
obstacle_type = choice([0, 1])

# Game clock for controlling the frame rate
clock = pygame.time.Clock()

# --- Classes ---

class Dino(pygame.sprite.Sprite):
    """Represents the player-controlled dinosaur."""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.walking_sprites = []
        self.sprite_index = 0
        # Extract walking animation frames from the spritesheet
        for i in range(3):
            img = sprite_sheet.subsurface((32 * i, 0), (32, 32))
            img = pygame.transform.scale(img, (32 * 3, 32 * 3))
            self.walking_sprites.append(img)
        
        self.image = self.walking_sprites[self.sprite_index]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        
        # --- POSITION CORRECTION ---
        # Position the dino so its feet are on the ground line (SCREEN_HEIGHT - 64)
        self.rect.bottom = SCREEN_HEIGHT - 14
        # Store the correct initial Y position for jumping logic
        self.initial_y = self.rect.y
        # Set the starting X position
        self.rect.centerx = 100
        
        self.is_jumping = False

    def jump(self):
        # Allow jumping only if the dino is on the ground
        if not self.is_jumping and self.rect.y == self.initial_y:
            self.is_jumping = True
            jump_sound.play()

    def update(self):
        # Handle the jump mechanics
        if self.is_jumping:
            # Move up until it reaches the jump height limit
            if self.rect.y <= self.initial_y - 150:
                self.is_jumping = False
            self.rect.y -= 20  # Move up
        else:
            # Apply gravity until it's back on the ground
            if self.rect.y < self.initial_y:
                self.rect.y += 20  # Move down (gravity)
            else:
                self.rect.y = self.initial_y # Snap to ground

        # Update walking animation
        self.sprite_index += 0.25
        if self.sprite_index >= 3:
            self.sprite_index = 0
        self.image = self.walking_sprites[int(self.sprite_index)]

class Cloud(pygame.sprite.Sprite):
    """Represents the clouds moving in the background."""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((7 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (96, 96))
        self.rect = self.image.get_rect()
        # Position clouds randomly
        self.rect.y = randrange(50, 200, 50)
        self.rect.x = SCREEN_WIDTH - randrange(30, 300, 90)

    def update(self):
        # Move the cloud to the left
        self.rect.x -= game_speed
        # If cloud goes off-screen, reposition it to the right
        if self.rect.topright[0] < 0:
            self.rect.x = SCREEN_WIDTH
            self.rect.y = randrange(50, 200, 50)

class Ground(pygame.sprite.Sprite):
    """Represents a single tile of the scrolling ground."""
    def __init__(self, x_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((6 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        # The top of the ground is at this Y coordinate
        self.rect.y = SCREEN_HEIGHT - 64
        self.rect.x = x_pos * 64

    def update(self):
        # Move the ground tile to the left
        self.rect.x -= game_speed
        # If tile goes off-screen, reposition it to the right end
        if self.rect.topright[0] < 0:
            self.rect.x = SCREEN_WIDTH

class Pterodactyl(pygame.sprite.Sprite):
    """Represents the flying Pterodactyl obstacle."""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.flying_sprites = []
        self.sprite_index = 0
        self.obstacle_id = 1 # This obstacle corresponds to type 1
        # Extract flying animation frames
        for i in range(3, 5):
            img = sprite_sheet.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (64, 64))
            self.flying_sprites.append(img)

        self.image = self.flying_sprites[self.sprite_index]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        # Its position is intentionally high, as it's a flying obstacle
        self.rect.center = (SCREEN_WIDTH, SCREEN_HEIGHT - 250)
        self.rect.x = SCREEN_WIDTH

    def update(self):
        # Only move if this obstacle type is chosen
        if obstacle_type == self.obstacle_id:
            self.rect.x -= game_speed
            # Update flying animation
            self.sprite_index += 0.25
            if self.sprite_index > 1:
                self.sprite_index = 0
            self.image = self.flying_sprites[int(self.sprite_index)]

class Cactus(pygame.sprite.Sprite):
    """Represents the cactus obstacle."""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((5 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.obstacle_id = 0 # This obstacle corresponds to type 0
        
        # --- POSITION CORRECTION ---
        # Position the cactus so its base is on the ground line
        self.rect.bottom = SCREEN_HEIGHT - 24
        self.rect.x = SCREEN_WIDTH

    def update(self):
        # Only move if this obstacle type is chosen
        if obstacle_type == self.obstacle_id:
            self.rect.x -= game_speed

# --- Helper Functions ---

def render_text(text, font_size, font_color):
    """Renders text to a surface."""
    font = pygame.font.SysFont('comicsansms', font_size, True, False)
    text_surface = font.render(str(text), True, font_color)
    return text_surface

def restart_game():
    """Resets all game variables to their initial state."""
    global score, game_speed, is_game_over, obstacle_type
    score = 0
    game_speed = 10
    is_game_over = False
    
    # Reset dino's position and state
    dino.rect.y = dino.initial_y
    dino.is_jumping = False
    
    # Reset obstacle positions and choose a new one
    cactus.rect.x = SCREEN_WIDTH
    pterodactyl.rect.x = SCREEN_WIDTH
    obstacle_type = choice([0, 1])

# --- Object and Sprite Group Creation ---
all_sprites = pygame.sprite.Group()

dino = Dino()
all_sprites.add(dino)

cactus = Cactus()
all_sprites.add(cactus)

pterodactyl = Pterodactyl()
all_sprites.add(pterodactyl)

for _ in range(4):
    cloud = Cloud()
    all_sprites.add(cloud)

# Create enough ground tiles to cover the screen plus one extra
for i in range(SCREEN_WIDTH // 64 + 2):
    ground_tile = Ground(i)
    all_sprites.add(ground_tile)

# Group for collision detection
obstacle_group = pygame.sprite.Group()
obstacle_group.add(cactus, pterodactyl)


# --- Main Game Loop ---
while True:
    clock.tick(30)
    window.fill(WHITE)

    # --- 1. Event Handling ---
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if not is_game_over:
                    dino.jump()
            if event.key == K_r and is_game_over:
                restart_game()

    # --- 2. Game Logic ---

    # Check for collisions between dino and obstacles
    collisions = pygame.sprite.spritecollide(dino, obstacle_group, False, pygame.sprite.collide_mask)

    if collisions and not is_game_over:
        death_sound.play()
        is_game_over = True
        
    # If the game is not over, update sprites and score
    if not is_game_over:
        score += 1
        all_sprites.update()

        # Check if the current obstacle is off-screen to choose a new one
        if (obstacle_type == 0 and cactus.rect.topright[0] < 0) or \
           (obstacle_type == 1 and pterodactyl.rect.topright[0] < 0):
            
            obstacle_type = choice([0, 1])
            # Reposition both obstacles to the right, ready for the next run
            cactus.rect.x = SCREEN_WIDTH
            pterodactyl.rect.x = SCREEN_WIDTH

        # Increase speed and play sound every 100 points
        if score % 100 == 0 and score > 0:
            score_sound.play()
            if game_speed < 23:
                game_speed += 1

    # --- 3. Drawing / Rendering ---
    all_sprites.draw(window)

    # Render the score
    score_text = render_text(score, 40, BLACK)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH - 100, 40))
    window.blit(score_text, score_rect)
    
    # If game is over, display the game over message
    if is_game_over:
        game_over_text = render_text('GAME OVER', 40, RED)
        restart_text = render_text('Press R to restart', 30, BLACK)
        
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))

        window.blit(game_over_text, game_over_rect)
        window.blit(restart_text, restart_rect)

    # Update the full display surface to the screen
    pygame.display.flip()