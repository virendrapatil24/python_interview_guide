# Deep Dive: Pygame

Pygame is a set of Python modules designed for writing video games. It uses the Simple DirectMedia Layer (SDL) library.

---

## 1. The Game Loop Pattern

Every game follows a standard loop:
1.  **Handle Input** (Events).
2.  **Update Game State** (Physics, Logic).
3.  **Draw** (Rendering).

```python
import pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True

while running:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # 2. Update State
    player_x += velocity_x
    
    # 3. Draw
    screen.fill((0, 0, 0)) # Clear screen
    screen.blit(player_surface, (player_x, player_y))
    pygame.display.flip() # Swap buffers (Double Buffering)
    
    clock.tick(60) # Limit to 60 FPS
```

---

## 2. Surfaces and Blitting

*   **Surface**: An object representing an image. The display is a Surface. Your character is a Surface.
*   **Blit**: Block Transfer. Copying pixels from one Surface to another.

**Optimization**: Use `convert()` or `convert_alpha()` on loaded images. This matches the pixel format of the image to the screen, making blitting much faster.
```python
img = pygame.image.load('hero.png').convert_alpha()
```

---

## 3. Sprites and Groups

Pygame provides a `Sprite` class to manage game objects.
**Groups** allow you to update and draw hundreds of objects with one command.

```python
all_sprites = pygame.sprite.Group()
all_sprites.add(hero)
all_sprites.update()
all_sprites.draw(screen)
```
