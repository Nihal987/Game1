import random
import pygame
pygame.init()

win = pygame.display.set_mode((500,500))
pygame.display.set_caption("Enemies")

clock = pygame.time.Clock()

walkRight = [pygame.image.load('Resources/R1.png'), pygame.image.load('Resources/R2.png'), pygame.image.load('Resources/R3.png'), pygame.image.load('Resources/R4.png'), pygame.image.load('Resources/R5.png'), pygame.image.load('Resources/R6.png'), pygame.image.load('Resources/R7.png'), pygame.image.load('Resources/R8.png'), pygame.image.load('Resources/R9.png')]
walkLeft = [pygame.image.load('Resources/L1.png'), pygame.image.load('Resources/L2.png'), pygame.image.load('Resources/L3.png'), pygame.image.load('Resources/L4.png'), pygame.image.load('Resources/L5.png'), pygame.image.load('Resources/L6.png'), pygame.image.load('Resources/L7.png'), pygame.image.load('Resources/L8.png'), pygame.image.load('Resources/L9.png')]
bg = pygame.image.load('Resources/mario.jpg')
bg = pygame.transform.scale(bg, (500, 500))
char = pygame.image.load('Resources/standing.png')
BL = pygame.image.load('Resources/bulletLeft.png')
BL = pygame.transform.scale(BL, (30, 30))
BR = pygame.transform.flip(BL,True,False)

class Player:
    def __init__(self,x,y,width,height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.left = False
        self.right = False
        self.standing = True
        self.isJump = False
        self.jumpCount = 10
        self.walkCount = 0
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self,win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.left:
                win.blit(walkLeft[0], (self.x, self.y))
            else:
                win.blit(walkRight[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        # pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

class Projectile:
    def __init__(self,x,y,color,radius,facing) -> None:
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,win):
        if self.facing == -1:
            win.blit(BL,(self.x,self.y))
        else:
            win.blit(BR,(self.x,self.y))
        # pygame.draw.circle(win,(0,0,0),(self.x,self.y),self.radius)
        
class Enemy:

    walkRight = [pygame.image.load('Resources/R1E.png'), pygame.image.load('Resources/R2E.png'), pygame.image.load('Resources/R3E.png'), pygame.image.load('Resources/R4E.png'), pygame.image.load('Resources/R5E.png'), pygame.image.load('Resources/R6E.png'), pygame.image.load('Resources/R7E.png'), pygame.image.load('Resources/R8E.png'), pygame.image.load('Resources/R9E.png'), pygame.image.load('Resources/R10E.png'), pygame.image.load('Resources/R11E.png')]
    walkLeft = [pygame.image.load('Resources/L1E.png'), pygame.image.load('Resources/L2E.png'), pygame.image.load('Resources/L3E.png'), pygame.image.load('Resources/L4E.png'), pygame.image.load('Resources/L5E.png'), pygame.image.load('Resources/L6E.png'), pygame.image.load('Resources/L7E.png'), pygame.image.load('Resources/L8E.png'), pygame.image.load('Resources/L9E.png'), pygame.image.load('Resources/L10E.png'), pygame.image.load('Resources/L11E.png')]

    def __init__(self,x,y,width,height,start,end) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.start = start
        self.end = end
        self.isEnter = True
        self.path = [self.start,self.end]
        self.isLeft = True if self.x==0 else False
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)

    def draw(self,win):
        self.move()
        if self.walkCount + 1 >= 33:
            self.walkCount = 0
        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        # pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

    def move(self):
        if self.isEnter:
            if self.isLeft:
                if self.x <= self.path[0]:
                    self.x += self.vel
                else:
                    self.isEnter = False 
            else:
                self.vel = -3
                if self.x >= self.path[1]:
                    self.x += self.vel
                else:
                    self.isEnter = False
        else:
            if self.vel > 0:
                if self.x + self.vel < self.path[1]:
                    self.x += self.vel
                else:
                    self.vel *= -1
                    self.walkCount = 0
            else:
                if self.x - self.vel > self.path[0]:
                    self.x += self.vel
                else:
                    self.vel *= -1
                    self.walkCount = 0

    def hit(self):
        print("Goblin: Ouch!")

def redrawGameWindow():
    win.blit(bg,(0,0))
    man.draw(win)
    for goblin in goblins:
        goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

man = Player(200,345,64,64)
goblins = []
shootLoop = 0
goblinLoop = 0
bullets = []
level = 27
run = True
while run:
    clock.tick(27)

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 9:
        shootLoop = 0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # print(goblinLoop)
    if goblinLoop > 0:
        goblinLoop += 1
    if goblinLoop > 5 * level:
        goblinLoop = 0
    
    if goblinLoop == 0 and len(goblins)<10:
        temp_x = random.choice([0,500]) #pick which side of the screen to start from
        goblins.append(Enemy(temp_x,350,64,64,100,400))
        goblinLoop = 1
    
    # Bullet Goblin Collision
    for bullet in bullets:
        for goblin in goblins:
            if bullet.y + BL.get_height() > goblin.hitbox[1] and  bullet.y < goblin.hitbox[1] + goblin.hitbox[3]:
                if bullet.x + BL.get_width() > goblin.hitbox[0] and bullet.x < goblin.hitbox[0] + goblin.hitbox[2]:
                    # goblin.hit()
                    goblins.pop(goblins.index(goblin))
                    bullets.pop(bullets.index(bullet))
                    if(level>5):
                        level -= 1

        if bullet.x > 0 and bullet.x < 500:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) <10:
            bullets.append(Projectile(round(man.x + man.width//2), round(man.y + man.height//3), (255,0,0), 6, facing))
    
        shootLoop = 1
    
    if keys[pygame.K_LEFT] and man.x > 0:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width:
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    else:
        man.standing = True
    
    if not(man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
    else:
        if man.jumpCount >= -10:
            neg = 0.5
            if man.jumpCount <0:
                neg = -0.5
            man.y -= int(man.jumpCount**2 * neg)
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()

pygame.quit()