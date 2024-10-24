import pygame
import socket


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "127.0.0.1" # ip4 address for host
        self.port = 5555
        self.addr = (self.host, self.port)
        self.id = int(self.connect())

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(2048).decode() # get connect id

    def send(self, data): # input data(send) return data(reply)
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        
        except socket.error as e:
            return str(e)


class Player():
    width = height = 50
    
    def __init__(self, startx, starty, color=(255,0,0)):
        self.x = startx
        self.y = starty
        self.velocity = 2
        self.color = color

    def draw(self, images, g):

        g.blit(images, (self.x, self.y))

    def move(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """

        if dirn == 0:
            self.x += self.velocity
        elif dirn == 1:
            self.x -= self.velocity
        elif dirn == 2:
            self.y -= self.velocity
        else:
            self.y += self.velocity


class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.players = [Player(0,0) for i in range(10)]
        self.canvas = Canvas(self.width, self.height, "Testing...")
        self.image =  pygame.image.load('dd.png').convert_alpha()
    def run(self):
        clock = pygame.time.Clock()
        run = True
        id = self.net.id
        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                if self.players[id].x <= self.width - self.players[id].velocity:
                    self.players[id].move(0)

            if keys[pygame.K_LEFT]:
                if self.players[id].x >= self.players[id].velocity:
                    self.players[id].move(1)

            if keys[pygame.K_UP]:
                if self.players[id].y >= self.players[id].velocity:
                    self.players[id].move(2)

            if keys[pygame.K_DOWN]:
                if self.players[id].y <= self.height - self.players[id].velocity:
                    self.players[id].move(3)

            # Send Network Stuff

            p = self.parse_data(self, self.send_data())
            for i in range(10):
                self.players[i].x = int(p[i].split(":")[1].split(",")[0])
                self.players[i].y = int(p[i].split(":")[1].split(",")[1])
            # Update Canvas
            self.canvas.draw_background()

            for i in range(10):
                self.players[i].draw(self.image, self.canvas.get_canvas())
            self.canvas.update()

        pygame.quit()

    def send_data(self):
        """
        Send position to server
        :return: None
        """
        try:
            data = str(self.net.id) + ":" + str(self.players[self.net.id].x) + "," + str(self.players[self.net.id].y)
            reply = self.net.send(data)
            return reply
        except Exception as e:
            print("senddata:",e)
            return 0

    @staticmethod
    def parse_data(self,data):
        try:
            d = data.split("|")
            return d
        except Exception as e:
            print("parsedata:",e)
            return 0


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
        self.screen.fill((255,255,255))
