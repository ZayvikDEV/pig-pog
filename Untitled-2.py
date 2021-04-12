from pygame import *
from random import randint

mixer.init()
mixer.music.load('')

img_back = "galaxy.jpg"

font.init()
font = font.SysFont('Arial', 80)

score = -99
lost = 0 
max_lost = 3
goal = 10
life = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -13)
        bullets.add(bullet)

win_width = 2000
win_height = 2000
display.set_caption("Shish")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

finish = False
run = True 
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

    if not finish:
        window.blit(background,(0,0))
        
        text_goal = font2.render("Goal: " + str(goal), 1, (255, 255, 255))
        window.blit(text_goal,(10, 10))

        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text,(10,40))

        text_lose = font2.render("Lost: " + str(lost) + " of 3", 1, (255, 255, 255))
        window.blit(text_lose,(10,70))

        ship.update()
        monsters.update()
        bullets.update()
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 180), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
        
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        display.update()
    time.delay(50)
