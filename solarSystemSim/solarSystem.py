import pygame
import math

pygame.init()

# WIDTH,HEIGHT = 10000, 10000
WIDTH, HEIGHT = 1400, 900
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Sim")

MERCURY_MASS = 10
VENUS_MASS = 12
EARTH_MASS = 15
MARS_MASS = 18
JUPITER_MASS = 40
SATURN_MASS = 45
URANUS_MASS = 30
NEPTUNE_MASS = 30
SUN_MASS = 100

PLANET_RADIUS = 10
SUN_RADIUS = 20
FPS = 60
GRAVITY = 10
VELOCITY_SCALE = 100

WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255, 0)
GREEN = (0,255,0)
ORANGE = (255,165, 0)
CYAN = (0, 255, 255)

BG = pygame.transform.scale(pygame.image.load("simulators/solarSystemSim/background.jpg"), (WIDTH, HEIGHT))
mercury_pic = pygame.transform.scale(pygame.image.load("simulators/solarSystemSim/mercury.png"), (PLANET_RADIUS * 2, PLANET_RADIUS * 2))
venus_pic = pygame.transform.scale(pygame.image.load("simulators/solarSystemSim/venus.png"), (PLANET_RADIUS * 2, PLANET_RADIUS * 2))
earth_pic = pygame.transform.scale(pygame.image.load("simulators/solarSystemSim/earth.png"), (PLANET_RADIUS * 2, PLANET_RADIUS * 2))
mars_pic = pygame.transform.scale(pygame.image.load("simulators/solarSystemSim/mars.png"), (PLANET_RADIUS * 2, PLANET_RADIUS * 2))
jupiter_pic = pygame.transform.scale(pygame.image.load("simulators/solarSystemSim/jupiter.png"), (PLANET_RADIUS * 2, PLANET_RADIUS * 2))
saturn_pic = pygame.transform.scale(pygame.image.load("simulators/solarSystemSim/saturn.png"), (PLANET_RADIUS * 2, PLANET_RADIUS * 2))
urnaus_pic = pygame.transform.scale(pygame.image.load("simulators/solarSystemSim/uanus.png"), (PLANET_RADIUS * 2, PLANET_RADIUS * 2))
neptune_pic = pygame.transform.scale(pygame.image.load("simulators/solarSystemSim/neptune.png"), (PLANET_RADIUS * 2, PLANET_RADIUS * 2))


# def hex_to_rgb(hex_code):
#     hex_code = hex_code.lstrip('#')
#     return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

# # Example hex color code
# html_color = "#3498db"  # A shade of blue

# Convert hex to RGB
# BLUE = hex_to_rgb(html_color)

class SUN:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
    
    def draw(self):
        pygame.draw.circle(win, YELLOW, (self.x, self.y), SUN_RADIUS)

class PLANET:
    def __init__(self, x, y, vel_x, vel_y, mass, name, img):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass
        self.name = name
        self.img = img
    
    def move(self, obj=None):
        distance = math.sqrt((self.x - obj.x)**2 + (self.y - obj.y) ** 2)
        force = (GRAVITY * self.mass * obj.mass) / distance ** 2

        acceleration = force/self.mass
        angle = math.atan2(obj.y - self.y, obj.x - self.x)

        acceleration_x = acceleration * math.cos(angle)
        acceleration_y = acceleration * math.sin(angle)

        self.vel_x += acceleration_x
        self.vel_y += acceleration_y

        self.x += self.vel_x
        self.y += self.vel_y
    
    def draw(self):
        font = pygame.font.SysFont("Comic-Sans", 16)
        text = font.render(self.name, True, WHITE)
        win.blit(text, (self.x, self.y - 20))
        # pygame.draw.circle(win, self.color, (self.x, self.y), PLANET_RADIUS)
        win.blit(self.img, (self.x - PLANET_RADIUS, self.y - PLANET_RADIUS))

# def createObj():

def movePlanet(Location, mouse, obj):
    t_x, t_y = Location
    m_x, m_y = mouse

    vel_x = (m_x - t_x) / VELOCITY_SCALE
    vel_y = (m_y - t_y) / VELOCITY_SCALE
    
    obj.vel_x += vel_x
    obj.vel_y += vel_y

    return obj

def draw_slider(slider_x, slider_y, slider_width, slider_height, slider_pos):
    pygame.draw.rect(win, WHITE, (slider_x, slider_y, slider_width, slider_height))
    pygame.draw.circle(win, (150,150,150), (slider_x + slider_pos, slider_y + slider_height // 2), 10)

def main():
    running = True
    clock = pygame.time.Clock()

    sun = SUN(WIDTH//2, HEIGHT//2, SUN_MASS)
    Mercury = PLANET(WIDTH//2 - 50, HEIGHT//2, 0/VELOCITY_SCALE, 500/VELOCITY_SCALE, MERCURY_MASS, "Mercury", mercury_pic)
    Venus = PLANET(WIDTH//2 - 100, HEIGHT//2, 0/VELOCITY_SCALE, 350/VELOCITY_SCALE, VENUS_MASS, "Venus", venus_pic)
    Earth = PLANET(WIDTH//2 - 125, HEIGHT//2, 0/VELOCITY_SCALE, 300/VELOCITY_SCALE, EARTH_MASS, "Earth", earth_pic)
    Mars = PLANET(WIDTH//2 - 200, HEIGHT//2, 0/VELOCITY_SCALE, 250/VELOCITY_SCALE, MARS_MASS, "Mars", mars_pic)
    Jupiter = PLANET(WIDTH//2 - 300, HEIGHT//2, 0/VELOCITY_SCALE, 150/VELOCITY_SCALE, JUPITER_MASS, "Jupiter", jupiter_pic)
    Saturn = PLANET(WIDTH//2 - 400, HEIGHT//2, 0/VELOCITY_SCALE, 120/VELOCITY_SCALE, SATURN_MASS, "Saturn", saturn_pic)
    Uranus = PLANET(WIDTH//2 - 500, HEIGHT//2, 0/VELOCITY_SCALE, 90/VELOCITY_SCALE, URANUS_MASS, "Uranus", urnaus_pic)
    Neptune = PLANET(WIDTH//2 - 600, HEIGHT//2, 0/VELOCITY_SCALE, 80/VELOCITY_SCALE, NEPTUNE_MASS, "Neptune", neptune_pic)

    objects = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune]
    # collided_earth = False

    # Slider values
    slider_width = 300
    slider_height = 5
    slider_pos = 150  # Initial position of the slider (scaled mass of Sun)
    slider_x = (WIDTH) - slider_width - 100
    slider_y = 50

    selected_planet = None
    planetClicked = False

    sunClicked = False

    
    # objects.append(Mercury)
    # objects.append(Venus)
    # objects.append(Earth)
    # objects.append(Mars)
    # objects.append(Jupiter)
    # objects.append(Saturn)
    # objects.append(Uranus)
    # objects.append(Neptune)

    while running:
        clock.tick(FPS)

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle slider dragging
            if event.type == pygame.MOUSEBUTTONDOWN:
                if slider_x <= mouse_pos[0] <= slider_x + slider_width and slider_y <= mouse_pos[1] <= slider_y + slider_height:
                    # If mouse click is on the slider
                    sunClicked = True

            if event.type == pygame.MOUSEBUTTONUP:
                sunClicked = False

            if event.type == pygame.MOUSEMOTION:
                if sunClicked:
                    # Update slider position based on mouse movement
                    slider_pos = max(0, min(slider_width, mouse_pos[0] - slider_x))
                    # Update Sun's mass based on slider position (scale the value)
                    sun.mass = 50 + (slider_pos / slider_width) * 200  # Mass range from 50 to 250

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not selected_planet:
                    for obj in objects:
                        if math.sqrt((mouse_pos[0] - obj.x)**2 + (mouse_pos[1] - obj.y)**2) <= PLANET_RADIUS*2:
                            selected_planet = obj
                            planetClicked = True
                            break
                        
                elif selected_planet and planetClicked:
                    planetClicked = False

                
                if selected_planet and not planetClicked:
                    selected_planet = movePlanet((selected_planet.x, selected_planet.y), mouse_pos, selected_planet)
                    selected_planet = None
                    
        # pygame.draw.rect(win, (0,0,0), (0,0, WIDTH, HEIGHT))

        win.blit(BG, (0,0))

        if selected_planet and planetClicked:
            pygame.draw.line(win, WHITE, (selected_planet.x, selected_planet.y), mouse_pos, 2)

        # Draw the Sun's mass slider
        draw_slider(slider_x, slider_y, slider_width, slider_height, slider_pos)

        # Display current Sun's mass
        font = pygame.font.SysFont("Comic-Sans", 20)
        mass_text = font.render(f"Sun's Mass: {int(sun.mass)}", True, WHITE)
        win.blit(mass_text, (slider_x , slider_y-35))

        for obj in objects:
            obj.draw()
            obj.move(sun)
            # for obj2 in objects:
            #     if obj2 == obj:
            #         break
            #     else:
            #         obj.move(obj2)
            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            collided_sun = math.sqrt((obj.x - sun.x)**2 + (obj.y - sun.y)**2) <= SUN_RADIUS
            
            if off_screen or collided_sun:
                objects.remove(obj)

        

        sun.draw()
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()