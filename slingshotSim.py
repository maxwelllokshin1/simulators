import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grav Slingshot Effect")

PLANET_MASS = 100
OBJ_MASS = 5
GRAVITY = 5
FPS = 60
PLANET_RADIUS = 50
OBJ_RADIUS = 5
VEL_SCALE = 100

BG = pygame.transform.scale(pygame.image.load("simulators/background.jpg"), (WIDTH, HEIGHT))#black background or pygame.image.load("backgorund.jpg")
PLANET = pygame.transform.scale(pygame.image.load("simulators/jupiter.png"), (PLANET_RADIUS * 2, PLANET_RADIUS * 2))#PLANET COLOR

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass

    def draw(self):
        win.blit(PLANET, (self.x - PLANET_RADIUS, self.y - PLANET_RADIUS))


class SpaceObject:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass

    def move(self, planet=None):
        distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)
        force = (GRAVITY * self.mass * planet.mass) / distance ** 2

        acceleration = force/self.mass
        angle = math.atan2(planet.y - self.y, planet.x - self.x)

        acceleration_x = acceleration * math.cos(angle)
        acceleration_y = acceleration * math.sin(angle)

        self.vel_x += acceleration_x
        self.vel_y += acceleration_y

        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self):
        pygame.draw.circle(win, RED, (int(self.x), int(self.y)), OBJ_RADIUS)

def create_obj(Location, mouse):
    t_x, t_y = Location
    m_x, m_y = mouse

    vel_x = (t_x - m_x) / VEL_SCALE
    vel_y = (t_y - m_y) / VEL_SCALE

    obj = SpaceObject(t_x, t_y, vel_x, vel_y, OBJ_MASS)
    return obj

def main():
    running = True
    clock = pygame.time.Clock()

    planet = Planet(WIDTH // 2, HEIGHT // 2, PLANET_MASS)

    objects = []
    temp_obj_pos = None

    while running:
        clock.tick(FPS)

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_obj_pos:
                    # t_x, t_y = temp_obj_pos
                    obj = create_obj(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None
                else:
                    temp_obj_pos = mouse_pos

        win.blit(BG, (0,0))

        if temp_obj_pos:
            pygame.draw.line(win, WHITE, temp_obj_pos, mouse_pos, 2)
            pygame.draw.circle(win, RED, temp_obj_pos, OBJ_RADIUS)

        for obj in objects:
            obj.draw()
            obj.move(planet)
            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            collided = math.sqrt((obj.x - planet.x)**2 + (obj.y - planet.y)**2) <= PLANET_RADIUS
            if off_screen or collided:
                objects.remove(obj)

        planet.draw()

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
