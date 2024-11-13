import pygame
import random


pygame.init()



WIDTH, HEIGHT = 800, 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Sierpiski Triangle")



BLACK = (0, 0, 0)

WHITE = (255, 255, 255)



vertices = [(WIDTH // 2, 50), (50, HEIGHT - 50), (WIDTH - 50, HEIGHT - 50)]

zoom_factor = 1.0

center_x, center_y = WIDTH // 2, HEIGHT // 2



ZOOM_STEP = 0.1

PAN_STEP = 10



font = pygame.font.Font(None, 30)



def sierpinski_points(iterations, zoom, center_x, center_y):

    points = []

    x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)

    

    for _ in range(iterations):

        vx, vy = random.choice(vertices)

        x = (x + vx) // 2

        y = (y + vy) // 2

        zoomed_x = (x - center_x) * zoom + WIDTH // 2

        zoomed_y = (y - center_y) * zoom + HEIGHT // 2

        

        if 0 <= zoomed_x < WIDTH and 0 <= zoomed_y < HEIGHT:

            points.append((int(zoomed_x), int(zoomed_y)))

    

    return points


def draw_sierpinski(zoom, center_x, center_y):

    """Draw the Sierpiski triangle with specified zoom and center."""
    
    base_iterations = 50000
    
    iterations = int(base_iterations * zoom)
    
    
    
    points = sierpinski_points(iterations, zoom, center_x, center_y)
    
    for point in points:
        
        screen.set_at(point, WHITE)
        


def render_text(text, position, color=WHITE):
    
    """Render text on the screen."""
    
    text_surface = font.render(text, True, color)
    
    screen.blit(text_surface, position)
    


def main():
    
    """Main loop for the Sierpiski triangle zoom with dynamic detail."""
    
    global zoom_factor, center_x, center_y


    clock = pygame.time.Clock()
    
    running = True


    while running:
        
        screen.fill(BLACK)
        
        
        
        draw_sierpinski(zoom_factor, center_x, center_y)
        


        render_text(f"Zoom: {zoom_factor:.2f}", (10, 10))
        


        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                
                running = False


            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                if event.button == 4:
                    
                    zoom_factor *= (1 + ZOOM_STEP)
                    
                elif event.button == 5:
                    
                    zoom_factor *= (1 - ZOOM_STEP)
                    


            elif event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    
                    zoom_factor *= (1 + ZOOM_STEP)
                    
                elif event.key == pygame.K_MINUS:
                    
                    zoom_factor *= (1 - ZOOM_STEP)
                    
                
                
                elif event.key == pygame.K_LEFT:
                    
                    center_x -= PAN_STEP / zoom_factor
                elif event.key == pygame.K_RIGHT:
                    
                    center_x += PAN_STEP / zoom_factor
                elif event.key == pygame.K_UP:
                    
                    center_y -= PAN_STEP / zoom_factor
                elif event.key == pygame.K_DOWN:
                    
                    center_y += PAN_STEP / zoom_factor


        pygame.display.flip()
        
        clock.tick(30)
        


    pygame.quit()
    


if __name__ == "__main__":
    
    main()
    