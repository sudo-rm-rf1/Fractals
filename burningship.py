import pygame
import numpy as np

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Burning Ship Fractal")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

MAX_ITER = 256
zoom_factor = 1.0
center_x, center_y = -1, -0.5

ZOOM_STEP = 0.1
PAN_STEP = 0.1

TILE_SIZE = 50
cache = {}

font = pygame.font.Font(None, 30)

def burning_ship(c, max_iter):
    """Compute the Burning Ship sequence to determine if a point is in the fractal."""
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = complex(abs(z.real), abs(z.imag)) ** 2 + c
    return max_iter

def get_tile_key(x, y, zoom):
    """Create a unique key for each tile based on position and zoom level."""
    return (int(x / TILE_SIZE), int(y / TILE_SIZE), round(zoom, 2))

def draw_fractal(zoom, center_x, center_y):
    """Draw the Burning Ship fractal, using a cache to store tiles."""
    for x in range(0, WIDTH, TILE_SIZE):
        for y in range(0, HEIGHT, TILE_SIZE):
            tile_key = get_tile_key(x, y, zoom)
            
            if tile_key in cache:
                screen.blit(cache[tile_key], (x, y))
            else:
                tile_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
                for tx in range(TILE_SIZE):
                    for ty in range(TILE_SIZE):
                        px = x + tx
                        py = y + ty
                        real = center_x + (px - WIDTH / 2) / (0.5 * zoom * WIDTH)
                        imag = center_y + (py - HEIGHT / 2) / (0.5 * zoom * HEIGHT)
                        c = complex(real, imag)
                        color = burning_ship(c, MAX_ITER)
                        r = (color % 8) * 32
                        g = (color % 16) * 16
                        b = (color % 32) * 8
                        tile_surface.set_at((tx, ty), (r, g, b))
                
                screen.blit(tile_surface, (x, y))
                cache[tile_key] = tile_surface.copy()

def render_text(text, position, color=WHITE):
    """Render text on the screen."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def main():
    """Main loop for the fractal zoom."""
    global zoom_factor, center_x, center_y

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)

        draw_fractal(zoom_factor, center_x, center_y)

        render_text(f"Zoom: {zoom_factor:.2f}", (10, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    zoom_factor *= (1 + ZOOM_STEP)
                    cache.clear()
                elif event.button == 5:
                    zoom_factor *= (1 - ZOOM_STEP)
                    cache.clear()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    zoom_factor *= (1 + ZOOM_STEP)
                    cache.clear()
                elif event.key == pygame.K_MINUS:
                    zoom_factor *= (1 - ZOOM_STEP)
                    cache.clear()
                elif event.key == pygame.K_LEFT:
                    center_x -= PAN_STEP / zoom_factor
                    cache.clear()
                elif event.key == pygame.K_RIGHT:
                    center_x += PAN_STEP / zoom_factor
                    cache.clear()
                elif event.key == pygame.K_UP:
                    center_y -= PAN_STEP / zoom_factor
                    cache.clear()
                elif event.key == pygame.K_DOWN:
                    center_y += PAN_STEP / zoom_factor
                    cache.clear()

        clock.tick(30)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
