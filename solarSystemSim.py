import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1400, 900
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Sim")

EARTH_MASS = 50
JUPITER_MASS = 200
SUN_MASS = 500
PLANET_RADIUS = 20
SUN_RADIUS = 50
FPS = 60
GRAVITY = 10
VELOCITY_SCALE = 100

WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255, 0)

class SUN:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
    
    def draw(self):
        pygame.draw.circle(win, YELLOW, (self.x, self.y), SUN_RADIUS)

class PLANET:
    def __init__(self, x, y, vel_x, vel_y, mass, color):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass
        self.color = color
    
    def move(self, sun=None):
        distance = math.sqrt((self.x - sun.x)**2 + (self.y - sun.y) ** 2)
        force = (GRAVITY * self.mass * sun.mass) / distance ** 2

        acceleration = force/self.mass
        angle = math.atan2(sun.y - self.y, sun.x - self.x)

        acceleration_x = acceleration * math.cos(angle)
        acceleration_y = acceleration * math.sin(angle)

        self.vel_x += acceleration_x
        self.vel_y += acceleration_y

        self.x += self.vel_x
        self.y += self.vel_y

    # def bounce(self, planet):
    #     pass
    
    def draw(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), PLANET_RADIUS)

# def createObj():

def movePlanet(Location, mouse, obj):
    t_x, t_y = Location
    m_x, m_y = mouse

    vel_x = (m_x - t_x) / VELOCITY_SCALE
    vel_y = (m_y - t_y) / VELOCITY_SCALE
    
    obj.vel_x += vel_x
    obj.vel_y += vel_y

    return obj



def main():
    running = True
    clock = pygame.time.Clock()

    sun = SUN(WIDTH//2, HEIGHT//2, SUN_MASS)
    earth = PLANET(450, HEIGHT//2-100, 0/VELOCITY_SCALE, 350/VELOCITY_SCALE, EARTH_MASS, BLUE)
    jupiter = PLANET(200, HEIGHT//2-100, 0/VELOCITY_SCALE, 250/VELOCITY_SCALE, JUPITER_MASS, RED)
    urrectom = PLANET(550, HEIGHT//2, 0/VELOCITY_SCALE, 600/VELOCITY_SCALE, EARTH_MASS, WHITE)

    objects = []
    temp_astroid_pos = None
    collided_earth = False
    planetClicked = False

    objects.append(earth)
    objects.append(jupiter)
    objects.append(urrectom)

    while running:
        clock.tick(FPS)

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_astroid_pos:
                    earth = movePlanet(temp_astroid_pos, mouse_pos, earth)
                    temp_astroid_pos = None
                    planetClicked = False
                else: 
                    temp_astroid_pos = mouse_pos
                    planetClicked = True
                # if math.sqrt((mouse_pos[0] - earth.x)**2 + (mouse_pos[1] - earth.y)**2) <= PLANET_RADIUS:
                #     collided_earth = True
                #     print("earth clicked")
                    
        pygame.draw.rect(win, (0,0,0), (0,0, WIDTH, HEIGHT))
        if temp_astroid_pos:
            t_x, t_y = temp_astroid_pos
            if planetClicked:
                collided_earth = math.sqrt((t_x - earth.x)**2 + (t_y - earth.y)**2) <= PLANET_RADIUS*2
                planetClicked = False

        if collided_earth:
            pygame.draw.line(win, WHITE, (earth.x, earth.y), mouse_pos, 2)
            planetClicked = False


        for obj in objects:
            obj.draw()
            obj.move(sun)
            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            collided_sun = math.sqrt((obj.x - sun.x)**2 + (obj.y - sun.y)**2) <= SUN_RADIUS
            
            if off_screen or collided_sun:
                objects.remove(obj)

        

        sun.draw()
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
