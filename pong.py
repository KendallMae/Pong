import pygame
import random
from network import Network

class Ball():
    def __init__(self, startx, starty, color=(255,0,0)):
        self.r = pygame.Rect(startx, starty, 30, 30)
        self.width = 20
        self.height = 20
        self.x_velocity = 4
        self.y_velocity = 4
        self.color = color
        

    def draw(self, g):
        pygame.draw.ellipse(g, self.color ,(self.r.x, self.r.y, self.width, self.height), 0)
    
    def move(self, player, player2):
        screen_width = 500
        screen_height = 500

        self.r.x += self.x_velocity
        self.r.y += self.y_velocity

        # Goal
        if self.r.right <= -75 or self.r.left >= screen_width + 75:
            self.r.x = screen_width/2 - self.width/2
            self.r.y = screen_height/2 - self.height/2
            self.x_velocity *= -1

        # Boucing off top and bottom
        if self.r.top <= 0 or self.r.bottom >=screen_height:
            self.y_velocity *= -1
        
        if self.r.colliderect(player) or self.r.colliderect(player2):
            self.x_velocity *= -1

class Player():
    def __init__(self, startx, starty, color=(0,0,255)):
        self.r = pygame.Rect(startx, starty, 20, 100)
        self.width = 20
        self.height = 100
        self.velocity = 10
        self.color = color

    def draw(self, g):
        pygame.draw.rect(g, self.color ,(self.r.x, self.r.y, self.width, self.height), 0)

    def move(self):
        screen_width = 500
        screen_height = 500

        if self.r.top <= 0:
            self.r.top = 0

        if self.r.bottom >= screen_height:
            self.r.bottom = screen_height

class Game:

    def __init__(self, w, h):
        screen_width = 500
        screen_height = 500

        self.net = Network()
        self.width = w
        self.height = h
        self.ball = Ball(screen_width/2 - 10, screen_height/2 - 10)
        self.player = Player(screen_width - 30, screen_height/2 - 70)
        self.player2 = Player(10, screen_height/2 - 70, (0,255,0))
        self.canvas = Canvas(self.width, self.height, "PONG")

    def run(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                self.player.r.y -= self.player.velocity

            if keys[pygame.K_DOWN]:
                self.player.r.y += self.player.velocity

            self.player.move()

            # Send Network Stuff
            hello, self.player2.r.y = self.parse_data(self.send_data())

            if hello == 470:
                self.ball.move(self.player.r, self.player2.r)

            # Update Canvas
            self.canvas.draw_background()
            self.ball.draw(self.canvas.get_canvas())
            self.player.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
            self.canvas.update()

        pygame.quit()

    def send_data(self):
        data = str(self.net.id) + ":" + str(self.player.r.x) + "," + str(self.player.r.y)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0,0


class Canvas:

    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w,h))
        pygame.display.set_caption(name)

    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (0,0,0))

        self.screen.draw(render, (x,y))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((0,0,0))
