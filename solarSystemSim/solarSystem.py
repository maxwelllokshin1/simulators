import pygame
import math

pygame.init()

# WIDTH,HEIGHT = 10000, 10000
SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 900
WIDTH, HEIGHT = 1400*5, 900*5
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
sun_pic = pygame.image.load("simulators/solarSystemSim/sun.png")
mercury_pic = pygame.image.load("simulators/solarSystemSim/mercury.png")
venus_pic = pygame.image.load("simulators/solarSystemSim/venus.png")
earth_pic = pygame.image.load("simulators/solarSystemSim/earth.png")
mars_pic = pygame.image.load("simulators/solarSystemSim/mars.png")
jupiter_pic = pygame.image.load("simulators/solarSystemSim/jupiter.png")
saturn_pic = pygame.image.load("simulators/solarSystemSim/saturn.png")
urnaus_pic = pygame.image.load("simulators/solarSystemSim/uanus.png")
neptune_pic = pygame.image.load("simulators/solarSystemSim/neptune.png")


# def hex_to_rgb(hex_code):
#     hex_code = hex_code.lstrip('#')
#     return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

# # Example hex color code
# html_color = "#3498db"  # A shade of blue

# Convert hex to RGB
# BLUE = hex_to_rgb(html_color)

class SUN:
    def __init__(self, x, y, mass, img):
        self.x = x
        self.y = y
        self.mass = mass
        self.img = img
    
    def draw(self, zoom_level):
        rad = SUN_RADIUS * zoom_level
        img = pygame.transform.scale(self.img, (rad * 2, rad * 2))
        win.blit(img, (self.x - rad, self.y - rad))

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
    
    def draw(self, zoom_level):
        fontSize = math.floor(16 * zoom_level)
        font = pygame.font.SysFont("Comic-Sans", fontSize)
        text = font.render(self.name, True, WHITE)
        rad = PLANET_RADIUS * zoom_level 
        img = pygame.transform.scale(self.img, (rad*2, rad*2))
        win.blit(text, text.get_rect(center=(self.x,self.y-rad-10)))
        win.blit(img, (self.x - rad, self.y - rad))

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

def zoomFeature():
    #Increase size/Decrease

    #Increase distance/Decrease
    pass

def main():
    running = True
    clock = pygame.time.Clock()

   

    mercury_distance = 57.91  
    venus_distance = 108.2   
    earth_distance = 149.6   
    mars_distance = 227.9  
    jupiter_distance = 778.3   
    saturn_distance = 1429   
    uranus_distance = 2871   
    neptune_distance = 4495  

    mercury_velocity = 478.7 
    venus_velocity = 350.2   
    earth_velocity = 297.8   
    mars_velocity = 240.77   
    jupiter_velocity = 130.7 
    saturn_velocity = 969   
    uranus_velocity = 681   
    neptune_velocity = 543   

    # Create Sun and Planets
    sun = SUN(WIDTH // 2, HEIGHT // 2, SUN_MASS, sun_pic)
    Mercury = PLANET(WIDTH // 2 - mercury_distance, HEIGHT // 2, 0, mercury_velocity/VELOCITY_SCALE, MERCURY_MASS, "Mercury", mercury_pic)
    Venus = PLANET(WIDTH // 2 - venus_distance, HEIGHT // 2, 0, venus_velocity/VELOCITY_SCALE, VENUS_MASS, "Venus", venus_pic)
    Earth = PLANET(WIDTH // 2 - earth_distance, HEIGHT // 2, 0, earth_velocity/VELOCITY_SCALE, EARTH_MASS, "Earth", earth_pic)
    Mars = PLANET(WIDTH // 2 - mars_distance, HEIGHT // 2, 0, mars_velocity/VELOCITY_SCALE, MARS_MASS, "Mars", mars_pic)
    Jupiter = PLANET(WIDTH // 2 - jupiter_distance, HEIGHT // 2, 0, jupiter_velocity/VELOCITY_SCALE, JUPITER_MASS, "Jupiter", jupiter_pic)
    Saturn = PLANET(WIDTH // 2 - saturn_distance, HEIGHT // 2, 0, saturn_velocity/VELOCITY_SCALE, SATURN_MASS, "Saturn", saturn_pic)
    Uranus = PLANET(WIDTH // 2 - uranus_distance, HEIGHT // 2, 0, uranus_velocity/VELOCITY_SCALE, URANUS_MASS, "Uranus", urnaus_pic)
    Neptune = PLANET(WIDTH // 2 - neptune_distance, HEIGHT // 2, 0, neptune_velocity/VELOCITY_SCALE, NEPTUNE_MASS, "Neptune", neptune_pic)


    objects = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune]

    sliderWidth = 300
    sliderHeight = 5
    sliderX = (SCREEN_WIDTH) - sliderWidth - 75


    sunMassSliderPos = 30  
    sunMassSliderY = 50

    zoomSliderPos = 30
    zoomSliderY = sunMassSliderY + 75

    selected_planet = None
    planetClicked = False

    sunSlider = False
    zoomSlider = False

    zoom_level = 1.0


    while running:
        clock.tick(FPS)

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                sunSlider = False
                zoomSlider = False

            if event.type == pygame.MOUSEMOTION:
                if sunSlider:
                    sunMassSliderPos = max(0, min(sliderWidth, mouse_pos[0] - sliderX))
                    sun.mass = (sunMassSliderPos / sliderWidth) * 1000  
                if zoomSlider:
                    zoomSliderPos = max(0, min(sliderWidth, mouse_pos[0] - sliderX))
                    zoom_level = (zoomSliderPos / sliderWidth) * 20  

            if event.type == pygame.MOUSEBUTTONDOWN:
                if math.sqrt((mouse_pos[0] - (sliderX + sunMassSliderPos))**2 + (mouse_pos[1] - sunMassSliderY)**2) <= 50:
                    sunSlider = True
                if math.sqrt((mouse_pos[0] - (sliderX + zoomSliderPos))**2 + (mouse_pos[1] - zoomSliderY)**2) <= 50:
                    zoomSlider = True

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
                    

        win.blit(BG, (0,0))

        if selected_planet and planetClicked:
            pygame.draw.line(win, WHITE, (selected_planet.x, selected_planet.y), mouse_pos, 2)

        # draws slider for changing suns mass feature
        draw_slider(sliderX, sunMassSliderY, sliderWidth, sliderHeight, sunMassSliderPos)

        font = pygame.font.SysFont("Comic-Sans", 20)
        mass_text = font.render(f"Sun's Mass: {int(sun.mass)}", True, WHITE)
        win.blit(mass_text, (sliderX , sunMassSliderY-35))


        # Draws slided for zoom in/out feature
        draw_slider(sliderX, zoomSliderY, sliderWidth, sliderHeight, zoomSliderPos)

        font = pygame.font.SysFont("Comic-Sans", 20)
        mass_text = font.render(f"ZOOM IN/OUT: {int(zoom_level)}", True, WHITE)
        win.blit(mass_text, (sliderX , zoomSliderY-35))

        for obj in objects:
            obj.draw(zoom_level)
            obj.move(sun)

            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            collided_sun = math.sqrt((obj.x - sun.x)**2 + (obj.y - sun.y)**2) <= SUN_RADIUS
            
            if off_screen or collided_sun:
                objects.remove(obj)

        

        sun.draw(zoom_level)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
