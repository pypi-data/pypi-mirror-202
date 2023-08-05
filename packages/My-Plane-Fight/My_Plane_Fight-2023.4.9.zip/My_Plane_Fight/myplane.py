import pygame


class MyPlane(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image1=pygame.image.load("images/me1.png").convert_alpha()
        self.image2=pygame.image.load("images/me2.png").convert_alpha()
        self.image_life=pygame.image.load("images/life.png").convert_alpha()
        self.image_life_rect=self.image_life.get_rect
        self.destroy_images=[]
        self.destroy_images.extend([\
            pygame.image.load("images/me_destroy_1.png").convert_alpha(),\
            pygame.image.load("images/me_destroy_2.png").convert_alpha(),\
            pygame.image.load("images/me_destroy_3.png").convert_alpha(),\
            pygame.image.load("images/me_destroy_4.png").convert_alpha(),\
            ])
        self.rect=self.image1.get_rect()
        self.width,self.height=bg_size[0],bg_size[1]
        self.rect.left,self.rect.top=(self.width-self.rect.width)//2,\
                                      self.height-self.rect.height-60
        self.speed=10
        self.active=True
        self.mask=pygame.mask.from_surface(self.image1)
        self.ming=5
    def reset(self):
        self.rect.left,self.rect.top=(self.width-self.rect.width)//2,\
                                      self.height-self.rect.height-60
        self.active=True
    def moveUp(self):
        if self.rect.top>0:
            self.rect.top-=self.speed
        else:
            self.rect.top=0
    def moveDown(self):
        if self.rect.bottom<self.height-60:
            self.rect.bottom+=self.speed
        else:
            self.rect.bottom=self.height-60
    def moveLeft(self):
        if self.rect.left>0:
            self.rect.left-=self.speed
        else:
            self.rect.left=0
    def moveRight(self):
        if self.rect.right<self.width:
            self.rect.right+=self.speed
        else:
            self.rect.right=self.width
#me=MyPlane([800,600])
#print('width=',me.width,'height=',me.height)#,me.rect.top,me.rect.bottom
