from pygame import *
from random import randint
mixer.init()
font.init()
udar1 = mixer.Sound('удар об стену.mp3')
udar2 = mixer.Sound('удар ракеткой.mp3')
kric = mixer.Sound('ура.mp3')
window = display.set_mode((900,550))
display.set_caption("Пин-Понг")
mixer.music.load('фон.mp3')
mixer.music.play()
clock = time.Clock()
points1 = 0
points2 = 0

font15=font.SysFont("Minecraft.ttf",30)
textpoints1 = font15.render('points:'+str(points1),True,(255,255,255))
textpoints2 = font15.render('points'+str(points2),True,(255,255,255))
font14=font.SysFont("Minecraft.ttf",60)
textwin1 = font14.render('playr 1 WIN',True,(255,255,255))
textwin2 = font14.render('playr 2 WIN',True,(255,255,255))

FPS = 60
begraunt = transform.scale(image.load('begraunt.jpg'),(900,500))
game = 'play'
total = randint(1,2)
pered = False
restart = False

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,width , height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width , height))    
        self.speed_x = player_speed
        self.speed_y = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Racket(GameSprite):
    def update1(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed_y
        if keys_pressed[K_DOWN] and self.rect.y < 500 - 133:
            self.rect.y += self.speed_y
    def update2(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed_y
        if keys_pressed[K_s] and self.rect.y < 500 - 133:
            self.rect.y += self.speed_y

class Ball(GameSprite):
    def update(self):
        if pered == True:
            ball.rect.y += ball.speed_y
        if total == 1:
            self.rect.x -= self.speed_x
        else:
            self.rect.x += self.speed_x
        if self.rect.y < 0:
            udar1.play()
            self.speed_y *= -1
        if self.rect.y > 500 - 50 :
            udar1.play()
            self.speed_y *= -1

racket1 = Racket('plita.png',10,180,30,130,5)
racket2 = Racket('plita.png',860,180,30,130,5)
racket = sprite.Group()
racket.add(racket1,racket2)
ball = Ball('ball.png',425, 225,50,50,4)

wind = image.load('окно.png')
wind = transform.scale(wind,(940,50))

while True:
    if game ==  'play':
        textpoints1 = font15.render('points '+str(points1),True,(255,255,255))
        textpoints2 = font15.render('points '+str(points2),True,(255,255,255))
        window.blit(begraunt,(0,0))
        window.blit(wind,(-20,500))
        window.blit(textpoints1,(10,515))
        window.blit(textpoints2,(805,515))
        racket1.reset()
        racket1.update2()
        racket2.reset()
        racket2.update1()
        ball.reset()
        ball.update()
        display.update()
        
        if sprite.spritecollide(ball,racket,False):
            if ball.rect.colliderect(racket1):
                points1 += 1
            if ball.rect.colliderect(racket2): 
                points2 += 1
            udar2.play()
            pered = True
            ball.speed_x *= -1
        if ball.rect.x < 20:
            ball.kill()
            udar1.play()
            if total == 1:
                total = 2
            else:
                total = 1
            ball = Ball('ball.png',425, 225,50,50,4)
        if ball.rect.x > 850:
            ball.kill()
            udar1.play()
            if total == 1:
                total = 2
            else:
                total = 1
            ball = Ball('ball.png',425, 225,50,50,4)
        if points1 == 20:
            game = 'win1'
        if points2 == 20:
            game = 'win2'
    if game != 'game':
        if game == 'win1':
            window.blit(textwin1,(350,235))
            mixer.music.pause()
            # kric.play()
        if game == 'win2':
            window.blit(textwin2,(350,235))
            mixer.music.pause()
            # kric.play()
        if restart == True:
            mixer.music.play()
            points1 = 0
            points2 = 0
            game = 'play'
            ball.kill()
            ball = Ball('ball.png',425, 225,50,50,4)
            restart = False
        display.update()
    for e in event.get():
        if e.type ==QUIT:
            quit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE and game != 'play':
                restart = True
    clock.tick(FPS)