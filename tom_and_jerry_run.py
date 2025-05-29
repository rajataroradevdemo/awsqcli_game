import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
GROUND_Y = 300
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tom and Jerry Run")
clock = pygame.time.Clock()

# Create directories for assets if they don't exist
os.makedirs("images", exist_ok=True)
os.makedirs("sounds", exist_ok=True)

# Function to load and scale images
def load_image(name, scale=1):
    try:
        image = pygame.image.load(os.path.join("images", name))
        if scale != 1:
            new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
            image = pygame.transform.scale(image, new_size)
        return image
    except pygame.error:
        print(f"Cannot load image: {name}")
        # Create a placeholder colored rectangle
        surf = pygame.Surface((50, 50))
        surf.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        return surf

# Function to load sounds
def load_sound(name):
    try:
        sound_path = os.path.join("sounds", name)
        if os.path.exists(sound_path):
            return pygame.mixer.Sound(sound_path)
        else:
            print(f"Sound file missing: {sound_path}")
            return None
    except pygame.error:
        print(f"Cannot load sound: {name}")
        return None

class Tom(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load Tom animations
        self.running_frames = [
            load_image("tom_run1.png", 0.2),
            load_image("tom_run2.png", 0.2),
            load_image("tom_run3.png", 0.2),
            load_image("tom_run4.png", 0.2)
        ]
        self.jumping_image = load_image("tom_jump.png", 0.2)
        self.crash_image = load_image("tom_crash.png", 0.2)
        
        # Animation variables
        self.current_frame = 0
        self.animation_speed = 0.2
        self.animation_time = 0
        
        self.image = self.running_frames[0]
        self.rect = self.image.get_rect()
        self.rect.bottom = GROUND_Y
        self.rect.x = 50
        self.velocity = 0
        self.jumping = False
        self.crashed = False

    def jump(self):
        if not self.jumping and not self.crashed:
            self.velocity = -15
            self.jumping = True

    def crash(self):
        self.crashed = True
        self.image = self.crash_image

    def update(self):
        if not self.crashed:
            # Apply gravity
            self.velocity += 0.8
            self.rect.y += self.velocity

            # Check ground collision
            if self.rect.bottom > GROUND_Y:
                self.rect.bottom = GROUND_Y
                self.velocity = 0
                self.jumping = False

            # Update animation
            if self.jumping:
                self.image = self.jumping_image
            else:
                self.animation_time += 1
                if self.animation_time >= FPS * self.animation_speed:
                    self.animation_time = 0
                    self.current_frame = (self.current_frame + 1) % len(self.running_frames)
                    self.image = self.running_frames[self.current_frame]

class Jerry(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load Jerry animations
        self.frames = [
            load_image("jerry1.png", 0.15),
            load_image("jerry2.png", 0.15)
        ]
        self.current_frame = 0
        self.animation_speed = 0.3
        self.animation_time = 0
        
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.bottom = GROUND_Y - 150  # Jerry runs on a platform above
        self.rect.x = WINDOW_WIDTH - 100

    def update(self):
        # Update animation
        self.animation_time += 1
        if self.animation_time >= FPS * self.animation_speed:
            self.animation_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type_id):
        super().__init__()
        # Different obstacles
        self.types = {
            0: ("Water", load_image("water.png", 0.15)),
            1: ("Iron", load_image("iron.png", 0.15)),
            2: ("Sofa", load_image("sofa.png", 0.15)),
            3: ("Bat", load_image("bat.png", 0.15)),
            4: ("Cloth", load_image("cloth.png", 0.15))
        }
        
        self.type = type_id
        self.image = self.types[type_id][1]
        self.rect = self.image.get_rect()
        self.rect.bottom = GROUND_Y
        self.rect.x = WINDOW_WIDTH
        self.speed = 5

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("cloud.png", 0.2)
        self.rect = self.image.get_rect()
        self.rect.y = random.randint(50, 150)
        self.rect.x = WINDOW_WIDTH
        self.speed = random.uniform(0.5, 1.5)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

class Game:
    def __init__(self):
        # Create sprites
        self.tom = Tom()
        self.jerry = Jerry()
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.all_sprites.add(self.tom)
        self.all_sprites.add(self.jerry)
        
        # Load background
        self.background = load_image("background.png")
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Load sounds
        self.jump_sound = load_sound("jump.wav")
        self.collision_sound = load_sound("collision.wav")
        self.point_sound = load_sound("point.wav")
        
        # Load background music
        try:
            pygame.mixer.music.load(os.path.join("sounds", "background_music.wav"))
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)  # Loop indefinitely
        except pygame.error:
            print("Cannot load background music")
        
        self.score = 0
        self.game_over = False
        self.obstacle_timer = 0
        self.cloud_timer = 0
        self.game_speed = 1.0
        self.obstacles_passed = 0

    def spawn_obstacle(self):
        self.obstacle_timer += 1
        if self.obstacle_timer >= 60 / self.game_speed:
            if random.randint(1, 100) < 30:
                obstacle = Obstacle(random.randint(0, 4))
                self.obstacles.add(obstacle)
                self.all_sprites.add(obstacle)
                self.obstacle_timer = 0

    def spawn_cloud(self):
        self.cloud_timer += 1
        if self.cloud_timer >= 120:
            if random.randint(1, 100) < 20:
                cloud = Cloud()
                self.clouds.add(cloud)
                self.all_sprites.add(cloud)
                self.cloud_timer = 0

    def run(self):
        while not self.game_over:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.tom.jump()
                        if self.jump_sound:
                            self.jump_sound.play()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            # Update
            self.all_sprites.update()
            self.spawn_obstacle()
            self.spawn_cloud()

            # Check collisions
            if pygame.sprite.spritecollide(self.tom, self.obstacles, False):
                if not self.game_over:
                    self.tom.crash()
                    if self.collision_sound:
                        self.collision_sound.play()
                    pygame.mixer.music.stop()
                    self.game_over = True

            # Remove off-screen obstacles and update score
            for obstacle in list(self.obstacles):
                if obstacle.rect.right < self.tom.rect.left and obstacle in self.obstacles:
                    self.obstacles_passed += 1
                    self.score += 1
                    if self.point_sound:
                        self.point_sound.play()
                    obstacle.kill()
                    
                    # Increase game speed every 10 obstacles
                    if self.obstacles_passed % 10 == 0:
                        self.game_speed += 0.1
                        for obs in self.obstacles:
                            obs.speed = 5 * self.game_speed

            # Draw
            screen.blit(self.background, (0, 0))
            
            # Draw ground
            pygame.draw.line(screen, BLACK, (0, GROUND_Y), (WINDOW_WIDTH, GROUND_Y), 2)
            
            # Draw platform for Jerry
            pygame.draw.line(screen, BLACK, (0, GROUND_Y - 150), (WINDOW_WIDTH, GROUND_Y - 150), 2)
            
            self.all_sprites.draw(screen)
            
            # Draw score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f'Score: {self.score}', True, BLACK)
            screen.blit(score_text, (10, 10))

            if self.game_over:
                game_over_font = pygame.font.Font(None, 72)
                game_over_text = game_over_font.render('Game Over!', True, (255, 0, 0))
                restart_text = font.render('Press any key to restart', True, BLACK)
                screen.blit(game_over_text, (WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2 - 50))
                screen.blit(restart_text, (WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2 + 20))
                
                # Wait for key press to restart
                pygame.display.flip()
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            waiting = False
                            return  # Return to main loop to restart game

            pygame.display.flip()
            clock.tick(FPS)

# Main game loop
def main():
    # Create placeholder images if they don't exist
    placeholder_images = [
        "tom_run1.png", "tom_run2.png", "tom_run3.png", "tom_run4.png",
        "tom_jump.png", "tom_crash.png", "jerry1.png", "jerry2.png",
        "water.png", "iron.png", "sofa.png", "bat.png", "cloth.png",
        "cloud.png", "background.png"
    ]
    
    for img in placeholder_images:
        img_path = os.path.join("images", img)
        if not os.path.exists(img_path):
            # Create a placeholder colored image
            surf = pygame.Surface((100, 100))
            surf.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            pygame.image.save(surf, img_path)
            print(f"Created placeholder for {img}")
    
    # Create placeholder sounds if they don't exist
    placeholder_sounds = ["jump.wav", "collision.wav", "point.wav", "background_music.mp3"]
    
    # We can't create placeholder sounds easily, so we'll just print a message
    for snd in placeholder_sounds:
        snd_path = os.path.join("sounds", snd)
        if not os.path.exists(snd_path):
            print(f"Sound file missing: {snd_path}")
    
    # Game loop
    while True:
        game = Game()
        game.run()

if __name__ == "__main__":
    main()
