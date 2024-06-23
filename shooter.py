#Create your own shooter
from pygame import *
from random import randint

Yellow = (255, 255, 0)
White = (255, 255, 255)
Red = (139, 0, 0)

font.init()
font_name = font.Font(None, 36)

font_win = font.Font(None, 36)
font_lose = font.Font(None, 36)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed,):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys [K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys [K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global missed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint (80, win_width - 80)
            missed += 1
            
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500

score = 0
missed = 0
goal = 16
max_missed = 3


clock = time.Clock()
window = display.set_mode((win_width, win_height))
display.set_caption("Space")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

rocket = Player("rocket.png", win_width/2, win_height - 100, 80, 100, 15)

ufos = sprite.Group()
for i in range(1, 6):
    ufo = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 2))
    ufos.add(ufo)

bullets = sprite.Group()

mixer.init()
#mixer.music.load("space.wav")
#mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')


font.init()
font_name = font.Font(None, 36)

win_text = font_name.render("YOU WIN!!!", True, Yellow)
lose_text = font_name.render("YOU LOSE!!!", True, Red)





run = True
finish = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #fire_sound.play()
                rocket.fire()

    if finish != True:
        window.blit(background, (0, 0))
        rocket.reset()
        ufos.draw(window)
        bullets.draw(window)

        text_counter = font_name.render("Score: " + str(score), True, White)
        window.blit(text_counter, (10, 10))

        text_missed = font_name.render("Missed: " + str(missed), True, White)
        window.blit(text_missed, (10, 35))

        collides = sprite.groupcollide(ufos, bullets, True, True)
        for c in collides:
            score += 1
            ufo = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
            ufos.add(ufo)
        
        if score >= goal:
            finish = True
            window.blit(win_text, (250, 250))

        if sprite.spritecollide(rocket, ufos, False):
            finish = True
            window.blit(lose_text, (250, 250))

        if missed >= max_missed:
            finish = True
            window.blit(lose_text, (250, 250))
        
           

        rocket.update()
        bullets.update()
        ufos.update()


        fps = 60
        clock.tick(fps)
        display.update()

    else:
        finish = False
        score = 0
        missed = 0

        for b in bullets:
            b.kill()
        
        for m in ufos:
            m.kill()
        
        time.delay(5000)
        for i in range(5):
            ufo = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
            ufos.add(ufo)


