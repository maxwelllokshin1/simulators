import pygame
import math

pygame.init() #start the pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 900 # window to be playing on
WIDTH, HEIGHT = 1400*7, 900*7 # actual size of simulation
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # create game screen
pygame.display.set_caption("Solar System Sim") # name title


# Set mass of all planets
MERCURY_MASS = 10 
VENUS_MASS = 12
EARTH_MASS = 15
MARS_MASS = 18
JUPITER_MASS = 40
SATURN_MASS = 45
URANUS_MASS = 30
NEPTUNE_MASS = 30
SUN_MASS = 100

# Set radius
PLANET_RADIUS = 5
SUN_RADIUS = 10

# set FPS
FPS = 60

# set gravity
GRAVITY = 10

# set Velocity
VELOCITY_SCALE = 100

# all colors
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255, 0)
GREEN = (0,255,0)
ORANGE = (255,165, 0)
CYAN = (0, 255, 255)


# IMAGES FOR ALL PLANETS, SUN, AND BACKGROUND
BG = pygame.image.load("simulators/solarSystemSim/background.jpg")
sun_pic = pygame.image.load("simulators/solarSystemSim/sun.png")
mercury_pic = pygame.image.load("simulators/solarSystemSim/mercury.png")
venus_pic = pygame.image.load("simulators/solarSystemSim/venus.png")
earth_pic = pygame.image.load("simulators/solarSystemSim/earth.png")
mars_pic = pygame.image.load("simulators/solarSystemSim/mars.png")
jupiter_pic = pygame.image.load("simulators/solarSystemSim/jupiter.png")
saturn_pic = pygame.image.load("simulators/solarSystemSim/saturn.png")
urnaus_pic = pygame.image.load("simulators/solarSystemSim/uanus.png")
neptune_pic = pygame.image.load("simulators/solarSystemSim/neptune.png")


# Optimized background handling
class ScaledBackground:

    # initialize the background
    def __init__(self, img, max_zoom_level):
        self.img = img # the image
        self.max_zoom_level = max_zoom_level # zoom
        self.scaled_images = {}

    
    
    def get_scaled_image(self, zoom_level):
        if zoom_level not in self.scaled_images:
            # Scale the image only if it's not already cached
            bg_width = max(SCREEN_WIDTH, WIDTH * (zoom_level / 10))
            bg_height = max(SCREEN_HEIGHT, HEIGHT * (zoom_level / 10))

            scaled_bg = pygame.transform.scale(self.img, (int(bg_width), int(bg_height))) # the background scaled
            self.scaled_images[zoom_level] = scaled_bg # add the scaled image zoom_level to the array
        return self.scaled_images[zoom_level]

# Initialize the background cache
background_handler = ScaledBackground(BG, max_zoom_level=20)

# def hex_to_rgb(hex_code):
#     hex_code = hex_code.lstrip('#')
#     return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

# # Example hex color code
# html_color = "#3498db"  # A shade of blue

# Convert hex to RGB
# BLUE = hex_to_rgb(html_color)


# CREATED SUN CLASS
class SUN:
    # Instantiate all attributes x, y, mass, img
    def __init__(self, x, y, mass, img):
        self.x = x
        self.y = y
        self.mass = mass
        self.img = img
    
    # Draw the sun with attributes zoom_level, offset_x, offset_y
    def draw(self, zoom_level, offset_x, offset_y):
        rad = SUN_RADIUS * zoom_level   # How big the sun will be based on the zoom level
        img = pygame.transform.scale(self.img, (rad * 2, rad * 2)) # Scale the image based on zoom
        win.blit(img, (self.x - rad- offset_x, self.y - rad - offset_y)) # Draw the image at center of screen


# Create PLANET class
class PLANET:
    # Define all attributes x, y, vel_x, vel_y, mass, name, img
    def __init__(self, x, y, vel_x, vel_y, mass, name, img, adjusted_x, adjusted_y):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass
        self.name = name
        self.img = img
    
    # Move this object
    def move(self, obj=None):

        # move based on how much gravity will pull the planets using suns mass
        distance = math.sqrt((self.x - obj.x)**2 + (self.y - obj.y) ** 2) # Calculates distance from the sun
        force = (GRAVITY * self.mass * obj.mass) / distance ** 2 # Force Equation from PHYSICS

        acceleration = force/self.mass  # Calculate acceleration using force / mass
        angle = math.atan2(obj.y - self.y, obj.x - self.x) # now find the angle using opp/adj

        acceleration_x = acceleration * math.cos(angle) # find the component for x using Ax forumla
        acceleration_y = acceleration * math.sin(angle) # find component for y using Ay formula

        # change the velocities based on acceleration
        self.vel_x += acceleration_x  
        self.vel_y += acceleration_y

        # change positions based off velocities
        self.x += self.vel_x
        self.y += self.vel_y
    

    # Draw the planet 
    def draw(self, zoom_level, offset_x, offset_y):
        # change the position based on the zoom
        self.adjusted_x = (self.x - WIDTH//2) * (zoom_level/10) + WIDTH // 2 
        self.adjusted_y = (self.y - HEIGHT//2) * (zoom_level/10) + HEIGHT // 2

        # change the radius based on zoom
        rad = PLANET_RADIUS * zoom_level 

        # all text stuff
        fontSize = math.floor(16 * zoom_level) # font size based on zoom level
        font = pygame.font.SysFont("Comic-Sans", fontSize) # font style
        text = font.render(self.name, True, WHITE)  # how the text should look
        win.blit(text, text.get_rect(center=(self.adjusted_x - offset_x,self.adjusted_y - rad - 10 - offset_y)))  # pasting the text on the planets

        # create the planet image based on radius
        img = pygame.transform.scale(self.img, (rad*2, rad*2)) 
        win.blit(img, (self.adjusted_x - rad - offset_x, self.adjusted_y - rad - offset_y)) # draw planet image

def movePlanet(Location, mouse, obj):
    t_x, t_y = Location # Second location when clicked  
    m_x, m_y = mouse # Initial clicked point

    vel_x = ((m_x - t_x)*2) / VELOCITY_SCALE
    vel_y = ((m_y - t_y)*2) / VELOCITY_SCALE
    
    obj.vel_x += vel_x
    obj.vel_y += vel_y

    return obj

def draw_slider(slider_x, slider_y, slider_width, slider_height, slider_pos):
    pygame.draw.rect(win, WHITE, (slider_x, slider_y, slider_width, slider_height))
    pygame.draw.circle(win, (150,150,150), (slider_x + slider_pos, slider_y + slider_height // 2), 10)

def main():
    running = True
    clock = pygame.time.Clock()

   
    # All planets distances relative to the sun
    mercury_distance = 57.91  
    venus_distance = 108.2   
    earth_distance = 149.6   
    mars_distance = 227.9  
    jupiter_distance = 778.3   
    saturn_distance = 1429   
    uranus_distance = 2871   
    neptune_distance = 4495  

    # All Planets Velocities
    mercury_velocity = 478.7 
    venus_velocity = 350.2   
    earth_velocity = 297.8   
    mars_velocity = 240.77   
    jupiter_velocity = 130.7 
    saturn_velocity = 150 # 969   
    uranus_velocity = 130 # 681   
    neptune_velocity = 110 # 543   

    # Create Sun and Planets
    sun = SUN(WIDTH // 2, HEIGHT // 2, SUN_MASS, sun_pic)
    Mercury = PLANET(WIDTH // 2 - mercury_distance, HEIGHT // 2, 0, mercury_velocity/VELOCITY_SCALE, MERCURY_MASS, "Mercury", mercury_pic, 0, 0)
    Venus = PLANET(WIDTH // 2 - venus_distance, HEIGHT // 2, 0, venus_velocity/VELOCITY_SCALE, VENUS_MASS, "Venus", venus_pic, 0, 0)
    Earth = PLANET(WIDTH // 2 - earth_distance, HEIGHT // 2, 0, earth_velocity/VELOCITY_SCALE, EARTH_MASS, "Earth", earth_pic, 0, 0)
    Mars = PLANET(WIDTH // 2 - mars_distance, HEIGHT // 2, 0, mars_velocity/VELOCITY_SCALE, MARS_MASS, "Mars", mars_pic, 0, 0)
    Jupiter = PLANET(WIDTH // 2 - jupiter_distance, HEIGHT // 2, 0, jupiter_velocity/VELOCITY_SCALE, JUPITER_MASS, "Jupiter", jupiter_pic, 0, 0)
    Saturn = PLANET(WIDTH // 2 - saturn_distance, HEIGHT // 2, 0, saturn_velocity/VELOCITY_SCALE, SATURN_MASS, "Saturn", saturn_pic, 0 ,0 )
    Uranus = PLANET(WIDTH // 2 - uranus_distance, HEIGHT // 2, 0, uranus_velocity/VELOCITY_SCALE, URANUS_MASS, "Uranus", urnaus_pic, 0 ,0 )
    Neptune = PLANET(WIDTH // 2 - neptune_distance, HEIGHT // 2, 0, neptune_velocity/VELOCITY_SCALE, NEPTUNE_MASS, "Neptune", neptune_pic, 0, 0)


    # Add all planets to array
    objects = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune]

    # Initialize the sliders properties
    sliderWidth = 300
    sliderHeight = 5
    sliderX = (SCREEN_WIDTH) - sliderWidth - 75

    # Sun slider pos and Y
    sunMassSliderPos = sliderWidth / 10 
    sunMassSliderY = 50

    # Zoom slider pos and Y
    zoomSliderPos = sliderWidth/2
    zoomSliderY = sunMassSliderY + 75

    # Spped slider pos and Y
    speedUpSliderPos = sliderWidth / 5
    speedUpSliderY = zoomSliderY + 75

    selected_planet = None # Current planet selected
    planetClicked = False # Is the planet cilcked?

    # Certain selected slider
    sunSlider = False
    zoomSlider = False
    speedUpSlider = False

    # Moving screen?
    moveScreen = False

    # The zoom
    zoom_level = 10.0

    # Since all planets will be located at top left of screen, adjust their offset according to the WIDTH, HEIGHT, and screen
    offset_x = (WIDTH - SCREEN_WIDTH) //2
    offset_y = (HEIGHT - SCREEN_HEIGHT) //2

    # Last mouse position
    last_mouse_pos = None

    # IN PROCESS
    fps_multiplier = 1


    # Run program
    while running:
        clock.tick(FPS) # Run based on FPS

        mouse_pos = pygame.mouse.get_pos()  # get the mouse position

        # Current backgorund information
        scaled_bg = background_handler.get_scaled_image(zoom_level)
        width_bg = (scaled_bg.get_width() - SCREEN_WIDTH) //2
        height_bg = (scaled_bg.get_height() - SCREEN_HEIGHT) //2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                sunSlider = False
                zoomSlider = False
                speedUpSlider = False
                moveScreen = False
                last_mouse_pos = None

            if event.type == pygame.MOUSEMOTION:
                if sunSlider:
                    sunMassSliderPos = max(0, min(sliderWidth, mouse_pos[0] - sliderX))
                    sun.mass = (sunMassSliderPos / sliderWidth) * 1000  
                if zoomSlider:
                    zoomSliderPos = max(0, min(sliderWidth, mouse_pos[0] - sliderX))
                    zoom_level = (zoomSliderPos / sliderWidth) * 20
                if speedUpSlider:
                    speedUpSliderPos = max(0, min(sliderWidth, mouse_pos[0] - sliderX))
                    fps_multiplier = (speedUpSliderPos / sliderWidth) * 1000
                    # adjusted_fps = int(FPS * fps_multiplier)  # Adjust FPS based on multiplier
                    # clock.tick(adjusted_fps)
                    # sun.mass = SUN_MASS * speed_multiplier

                    
                    
                if moveScreen and last_mouse_pos:
                    dx = (mouse_pos[0] - last_mouse_pos[0]) / 10
                    dy = (mouse_pos[1] - last_mouse_pos[1]) / 10
                    offset_x -= dx  
                    offset_y -= dy
                    # if offset_x + SCREEN_WIDTH >= WIDTH and offset_x <= 0 and offset_y + SCREEN_HEIGHT >= HEIGHT and offset_y <= 0:

                offset_x = max(0, min(offset_x, WIDTH - SCREEN_WIDTH))
                offset_y = max(0, min(offset_y, HEIGHT - SCREEN_HEIGHT))


            if event.type == pygame.MOUSEBUTTONDOWN:
                # print(sun.x, " ", sun.y)
                # print(offset_x, " ", offset_y)
                # print(0-width_bg, " ", 0-height_bg)
                # print(Earth.x, " ", Earth.y)
                if 0 <= mouse_pos[0] <= SCREEN_WIDTH and 0 <= mouse_pos[0] <= SCREEN_HEIGHT:
                    moveScreen = True
                    last_mouse_pos = mouse_pos

                # Sun mass slider
                if math.sqrt((mouse_pos[0] - (sliderX + sunMassSliderPos))**2 + (mouse_pos[1] - sunMassSliderY)**2) <= 50:
                    sunSlider = True
                # Zoom slider
                if math.sqrt((mouse_pos[0] - (sliderX + zoomSliderPos))**2 + (mouse_pos[1] - zoomSliderY)**2) <= 50:
                    zoomSlider = True
                # SPeed up slider
                if math.sqrt((mouse_pos[0] - (sliderX + speedUpSliderPos))**2 + (mouse_pos[1] - speedUpSliderY)**2) <= 50:
                    speedUpSlider = True

                if not selected_planet:
                    for obj in objects:
                        if math.sqrt((mouse_pos[0] + offset_x - obj.adjusted_x)**2 + ((mouse_pos[1] + offset_y) - obj.adjusted_y)**2) <= PLANET_RADIUS*(2*zoom_level):
                            print("CLICKED ", obj.name, " ", ((mouse_pos[0] + offset_x) - obj.x))
                            selected_planet = obj
                            planetClicked = True
                            break
                        
                elif selected_planet and planetClicked:
                    planetClicked = False

                print("OFFSET: ", offset_x * (zoom_level/10), " ", offset_y * (zoom_level/10))
                if selected_planet and not planetClicked:
                    selected_planet = movePlanet((selected_planet.x, selected_planet.y), (mouse_pos[0] + offset_x, mouse_pos[1] + offset_y), selected_planet)
                    selected_planet = None

        # Draw the scaled background (no need to scale every time)
        win.blit(scaled_bg, (0-width_bg, 0-height_bg))


        if selected_planet and planetClicked:
            pygame.draw.line(win, WHITE, (selected_planet.adjusted_x - offset_x, selected_planet.adjusted_y - offset_y), mouse_pos, 2)

        # draws slider for changing suns mass feature
        draw_slider(sliderX, sunMassSliderY, sliderWidth, sliderHeight, sunMassSliderPos)

        font = pygame.font.SysFont("Comic-Sans", 20)
        mass_text = font.render(f"Sun's Mass: {int(sun.mass)}", True, WHITE)
        win.blit(mass_text, (sliderX , sunMassSliderY-35))


        # Draws slider for zoom in/out feature
        draw_slider(sliderX, zoomSliderY, sliderWidth, sliderHeight, zoomSliderPos)

        font = pygame.font.SysFont("Comic-Sans", 20)
        zoom_text = font.render(f"ZOOM IN/OUT: {int(zoom_level)}", True, WHITE)
        win.blit(zoom_text, (sliderX , zoomSliderY-35))

        # Draws slider for speed up feature
        draw_slider(sliderX, speedUpSliderY, sliderWidth, sliderHeight, speedUpSliderPos)

        font = pygame.font.SysFont("Comic-Sans", 20)
        speed_text = font.render(f"SPEED UP/ SLOW DOWN: {int(fps_multiplier)}", True, WHITE)
        win.blit(speed_text, (sliderX , speedUpSliderY-35))

        for obj in objects:
            obj.draw(zoom_level, offset_x, offset_y)
            obj.move(sun)

            # obj.x += obj.vel_x * speed_multiplier  # Apply speed multiplier to velocity
            # obj.y += obj.vel_y * speed_multiplier

            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            collided_sun = math.sqrt((obj.x - sun.x)**2 + (obj.y - sun.y)**2) <= SUN_RADIUS
            
            if off_screen or collided_sun:
                objects.remove(obj)

        sun.draw(zoom_level, offset_x, offset_y)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()