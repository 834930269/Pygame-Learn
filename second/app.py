import pygame
from pygame import *

class MySprite(pygame.sprite.Sprite):
    def __init__(self,target):
        pygame.sprite.Sprite.__init__(self)
        self.target_surface = target
        self.image = None
        self.master_image = None
        self.rect = None
        self.topleft = 0,0
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.row = 1

    # filename 帧图宽度,帧图高度,帧图行,帧图列
    def load(self,filename,width,height,columns,row):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = 0,0,width,height
        self.columns = columns
        self.row = row
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width)*(rect.height // height) - 1

    def update(self,current_time,rate=60):
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
            rect = (frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame

pygame.init()
screen = pygame.display.set_mode((800,600),0,32)
pygame.display.set_caption("精灵测试")
font = pygame.font.Font(None,18)
framerate = pygame.time.Clock()

cat = MySprite(screen)
cat.load("mdm.png",100,100,4,1)
group = pygame.sprite.Group()
group.add(cat)

while True:
    framerate.tick(100)
    ticks = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
        exit()

    screen.fill((0,0,100))

    group.update(ticks)
    group.draw(screen)
    pygame.display.update()