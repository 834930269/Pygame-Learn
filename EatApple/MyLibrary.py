# MyLibrary.py
from pygame import *
import sys, time, random, math, pygame

def print_text(font,x,y,text,color=(255,255,255)):
    imgText = font.render(text,True,color)
    #req'd when function moved into MyLibrary
    screen = pygame.display.get_surface()
    #移动
    screen.blit(imgText,(x,y))

class MySprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.master_image = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.row = 1
        self.direction = 0
        self.velocity = Point(0.0,0.0)

    #x property
    def _getx(self): return self.rect.x
    def _setx(self,value): self.rect.x = value
    X = property(_getx,_setx)

    #y property
    def _gety(self): return self.rect.y
    def _sety(self,value): self.rect.y = value
    Y = property(_gety,_sety)

    # position property
    def _getpos(self): return self.rect.topleft
    def _setpos(self,pos):self.rect.topleft = pos
    position = property(_getpos,_setpos)

    # filename 帧图宽度,帧图高度,帧图行,帧图列
    def load(self,filename,width,height,columns,row):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(0,0,width,height)
        self.columns = columns
        self.row = row
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width)*(rect.height // height) - 1

    def update(self,current_time,rate=30):
        if current_time > self.last_time +rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_frame = current_time

        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            #添加了row以后每次计算对row取余即可计算出当前列数
            frame_y = (self.frame // self.columns) % self.row * self.frame_height
            #如果把frame_y置为0,则表示始终都是在位图的第一行
            # 多行的话,可以通过frame_y来解决,但是要注意,y=0则返回
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame

    def __str__(self):
        return str(self.frame) + "," + str(self.first_frame) + \
            "," + str(self.last_frame) + "," + str(self.frame_width) + \
            "," + str(self.frame_height) + "," + str(self.columns) + \
            "," + str(self.rect)

#Point class
class Point(object):
    def __init__(self,x,y):
        self.__x = x
        self.__y = y
    #X property
    def getx(self): return self.__x
    def setx(self, x): self.__x = x
    x = property(getx, setx)

    #Y property
    def gety(self): return self.__y
    def sety(self, y): self.__y = y
    y = property(gety, sety)

    def __str__(self):
        return "{X:" + "{:.0f}".format(self.__x) + \
            ",Y:" + "{:.0f}".format(self.__y) + "}"