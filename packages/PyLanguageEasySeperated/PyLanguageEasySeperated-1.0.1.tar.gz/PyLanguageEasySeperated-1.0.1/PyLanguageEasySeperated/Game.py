import pygame
from pygame.locals import *
from pygame import mixer
import sys
import keyboard

clock = pygame.time.Clock()


def text_font(text_type, size):
    my_font = pygame.font.SysFont(text_type, size)
    return my_font


class Game:
    pygame.init()

    def __init__(self, width, height, caption):
        self.image = None
        self.color = None
        self.width = width
        self.height = height
        self.Player = None
        self.obstacles = {}
        self.names = []
        self.Buttons = {}
        self.buttonNames = []
        self.scrollX = 0
        self.scrollY = 0
        self.myMouse = False
        self.windowX = 0
        self.windowY = 0
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(caption)

    def backgroundColor(self, color=(255, 255, 255)):
        self.color = color
        self.display.fill(color)

    def backgroundImage(self, image=""):
        self.image = image
        img = pygame.image.load(self.image)
        self.display.blit(img, (0, 0))

    def Image(self, image="", pos_x=0, pos_y=0):
        img = pygame.image.load(image)
        self.display.blit(img, (pos_x - self.windowX, pos_y - self.windowY))

    def Text(self, text="Game2D", text_type="freesansbold.ttf", size=32, pos_x=0, pos_y=0, color=(255, 255, 255)):
        my_font = text_font(text_type, size)
        text_surface = my_font.render(text, True, color)
        self.display.blit(text_surface, (pos_x, pos_y))

    def obstacle(self, image, name="", pos_x=0, pos_y=0):
        img = pygame.image.load(image)
        pos_x = pos_x - self.windowX
        pos_y = pos_y - self.windowY
        obstacle = img.get_rect(topleft=(pos_x, pos_y))
        if name not in self.names:
            self.names.append(name)
        self.obstacles[name] = obstacle
        self.display.blit(img, (pos_x, pos_y))

    def player(self, image, pos_x=0, pos_y=0):
        img = pygame.image.load(image)
        obstacle2 = img.get_rect(topleft=(pos_x, pos_y))
        self.Player = obstacle2
        self.display.blit(img, (pos_x, pos_y))

    def collided(self):
        for obstacle in self.names:
            nowObstacle = self.obstacles[obstacle]
            if self.Player.colliderect(nowObstacle):
                place = [obstacle]
                PlayerLeft = self.Player[0]
                PlayerTop = self.Player[1]
                PlayerRight = self.Player[0] + self.Player[2]
                PlayerBottom = self.Player[1] + self.Player[3]
                ObsLeft = nowObstacle[0]
                ObsTop = nowObstacle[1]
                ObsRight = nowObstacle[0] + nowObstacle[2]
                ObsBottom = nowObstacle[1] + nowObstacle[3]
                if ObsTop < PlayerTop <= ObsBottom < PlayerBottom and (PlayerTop - ObsBottom) >= -8:
                    place.append("bottom")
                elif ObsBottom > PlayerBottom >= ObsTop > PlayerTop and (PlayerBottom - ObsTop) <= 8:
                    place.append("top")
                elif ObsRight > PlayerRight >= ObsLeft > PlayerLeft and (PlayerRight - ObsLeft) <= 8:
                    place.append("left")
                elif PlayerRight > ObsRight >= PlayerLeft > ObsLeft and (ObsRight - PlayerLeft) <= 8:
                    place.append("right")
                else:
                    place.append("center")
                return place

    def getScroller(self):
        scroller = [self.scrollX, self.scrollY]
        return scroller

    def addButton(self, image, name="", pos_x=0, pos_y=0):
        img = pygame.image.load(image)
        obstacle2 = img.get_rect(topleft=(pos_x, pos_y))
        self.Buttons[name] = obstacle2
        self.display.blit(img, (pos_x, pos_y))

    def buttonPressed(self, button):
        nowObstacle = self.Buttons[button]
        if self.myMouse:
            mouse = pygame.mouse.get_pos()
            mouseX = mouse[0]
            mouseY = mouse[1]
            obsL = nowObstacle[0]
            obsT = nowObstacle[1]
            obsR = nowObstacle[2] + nowObstacle[0]
            obsB = nowObstacle[3] + nowObstacle[1]
            if obsL < mouseX < obsR and obsT < mouseY < obsB:
                return True

    @staticmethod
    def music(music):
        mixer.music.load(music)
        mixer.music.play(-1)

    @staticmethod
    def sound(sound):
        sound_play = mixer.Sound(sound)
        sound_play.play()

    def moveScroller(self, SetX=0, SetY=0):
        self.scrollX += SetX
        self.scrollY += SetY

    def setScroller(self, SetX=0, SetY=0):
        self.scrollX = SetX
        self.scrollY = SetY

    def ScrollX(self, position=0):
        return position + self.scrollX

    def ScrollY(self, position=0):
        return position + self.scrollY

    @staticmethod
    def getMousePosition():
        return pygame.mouse.get_pos()

    def addQuitter(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.myMouse = True
            else:
                self.myMouse = False

    def moveScreen(self, x=0, y=0):
        self.windowX = x
        self.windowY = y

    def createMap(self, Map, objects, imageForObjects, startX=0, startY=0, differenceX=10, differenceY=10):
        done = False
        count = 0
        count2 = 0
        letCount = 0
        name = 0
        for positions in Map:
            count2 = 0
            for letter in positions:
                letCount = 0
                for letter2 in objects:
                    if letter2 == letter:
                        img = pygame.image.load(imageForObjects[letCount])
                        pos_x = startX + (count2 * differenceX) - self.windowX
                        pos_y = startY + (count * differenceY) - self.windowY
                        obstacle = img.get_rect(topleft=(pos_x, pos_y))
                        nowName = str(name)
                        if nowName not in self.names:
                            self.names.append(nowName)
                        self.obstacles[nowName] = obstacle
                        self.display.blit(img, (pos_x, pos_y))
                        name += 1
                    letCount += 1
                count2 += 1
            count += 1

    @staticmethod
    def keyPressed(key):
        if keyboard.is_pressed(key):
            return True
        else:
            return False

    @staticmethod
    def keyReleased(key):
        if not keyboard.is_pressed(key):
            return True
        else:
            return False

    @staticmethod
    def setFrame(framePerSec=60):
        clock.tick(framePerSec)

    @staticmethod
    def update():
        pygame.display.update()
