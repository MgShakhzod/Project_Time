import pygame
import os
from datetime import datetime
from json import load

class ModTime:
    def __init__(self,Mwidth: int,MHeight: int,fh: int,fm: int):
        self.Mwidth = Mwidth
        self.Mheight = MHeight
        self.fh = fh
        self.fm = fm

    def back_qty_obs(self,i: int):
        l = {
            0 : [True,True,True,False,True,True,True],
            1 : [False,False,True,False,False,True,False],
            2 : [True,False,True,True,True,False,True],
            3 : [True,False,True,True,False,True,True],
            4 : [False,True,True,True,False,True,False],
            5 : [True,True,False,True,False,True,True],
            6 : [True,True,False,True,True,True,True],
            7 : [True,False,True,False,False,True,False],
            8 : [True,True,True,True,True,True,True],
            9 : [True,True,True,True,False,True,True]
        }
        return l[i]
    
    def back_constructor(self,i: int, px: int, py: int, w: int, h: int,cl,sc):
        back_n = self.back_qty_obs(i)
        s = 0
        for obs in back_n:
            if (s == 0) and (obs == True):
                pygame.draw.rect(sc,cl,(px,py,w,h/100*12))
            if (s == 1) and (obs == True):
                pygame.draw.rect(sc,cl,(px,py+h/100*12,w/100*20,h/100*32))
            if (s == 2) and (obs == True):
                pygame.draw.rect(sc,cl,(px+w/100*80,py+h/100*12,w/100*20,h/100*32))
            if (s == 3) and (obs == True):
                pygame.draw.rect(sc,cl,(px,py+h/100*44,w,h/100*12))
            if (s == 4) and (obs == True):
                pygame.draw.rect(sc,cl,(px,py+h/100*56,w/100*20,h/100*32))
            if (s == 5) and (obs == True):
                pygame.draw.rect(sc,cl,(px+w/100*80,py+h/100*56,w/100*20,h/100*32))
            if (s == 6) and (obs == True):
                pygame.draw.rect(sc,cl,(px,py+h/100*88,w,h/100*12))
            s += 1

    def public(self,sc,cl1,cl2,qty_time):
        ost5f = (UN_WIDTH*5/100,UN_HEIGHT*5/100)
        pygame.draw.rect(sc,cl1,(ost5f[0],ost5f[1],self.Mwidth,self.Mheight),2)
        scale_num = self.Mwidth/2
        ostup = 20
        scale_num_center = (scale_num-ostup*4)/2
        if self.fh < 10:
            self.back_constructor(0,ost5f[0]+ostup,ost5f[1]+ostup,scale_num_center,UN_HEIGHT-(ost5f[1]+ostup)*2,cl2,sc)
            self.back_constructor(self.fh,ost5f[0]+scale_num/2+ostup,ost5f[1]+ostup,scale_num_center,UN_HEIGHT-(ost5f[1]+ostup)*2,cl2,sc)
        else:
            self.back_constructor(self.fh // 10,ost5f[0]+ostup,ost5f[1]+ostup,scale_num_center,UN_HEIGHT-(ost5f[1]+ostup)*2,cl2,sc)
            self.back_constructor(self.fh % 10,ost5f[0]+scale_num/2+ostup,ost5f[1]+ostup,scale_num_center,UN_HEIGHT-(ost5f[1]+ostup)*2,cl2,sc)
        if self.fm < 10:
            self.back_constructor(0,UN_WIDTH/2+ostup,ost5f[1]+ostup,scale_num_center,UN_HEIGHT-(ost5f[1]+ostup)*2,cl2,sc)
            self.back_constructor(self.fm,UN_WIDTH/2+scale_num/2+ostup,ost5f[1]+ostup,scale_num_center,UN_HEIGHT-(ost5f[1]+ostup)*2,cl2,sc)
        else:
            self.back_constructor(self.fm // 10,UN_WIDTH/2+ostup,ost5f[1]+ostup,scale_num_center,UN_HEIGHT-(ost5f[1]+ostup)*2,cl2,sc)
            self.back_constructor(self.fm % 10,UN_WIDTH/2+scale_num/2+ostup,ost5f[1]+ostup,scale_num_center,UN_HEIGHT-(ost5f[1]+ostup)*2,cl2,sc)
        if qty_time > 2:
            pygame.draw.rect(sc,cl2,(UN_WIDTH/2-10,UN_HEIGHT/2-60,20,40))
            pygame.draw.rect(sc,cl2,(UN_WIDTH/2-10,UN_HEIGHT/2+20,20,40))
        
pygame.init()

screen_info = pygame.display.Info()
MIN_SC_W = 10
MIN_SC_H = 50
UN_WIDTH = screen_info.current_w-MIN_SC_W
UN_HEIGHT = screen_info.current_h-MIN_SC_H

with open('settings.json','r',encoding='utf-8') as file:
    data_settings = load(file)

screen = pygame.display.set_mode((UN_WIDTH,UN_HEIGHT))
pygame.display.set_caption('Time')
clock = pygame.time.Clock()

os.environ['SDL_VIDEO_CENTERED'] = '1'

BACKGROUND = tuple(data_settings['BackGround_Color'])
CONTAINER_COLOR = tuple(data_settings['Border_Color'])
RED = tuple(data_settings['Numbers_Color'])
SCALE_CONTAINER = data_settings['Scale_Container']
FPS = data_settings['Max_FPS']
qty_t = 0

my_time = ModTime(UN_WIDTH*SCALE_CONTAINER/100,UN_HEIGHT*SCALE_CONTAINER/100,8,32)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    dtime = datetime.now()
    my_time.fh = int(dtime.hour)
    my_time.fm = int(dtime.minute)
    if qty_t < FPS: qty_t += 1
    else: qty_t = 0

    screen.fill(BACKGROUND)
    my_time.public(screen,CONTAINER_COLOR,RED,qty_t)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit