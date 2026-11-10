import pygame
from pygame.locals import *
from pygame import mixer
import random
import mangulevelid
import sys
# ekraan: 1268 × 2756

if sys.platform == "linux" or sys.platform == "ios":
    mobile = True
else:
    mobile = False

levels = mangulevelid.levels

if mobile:
    level_num = 0
else:
    level_num = None
pygame.init()
pygame.mixer.init()
ekraan_x = 1200
ekraan_y = 700
münt = None
ekraan = pygame.display.set_mode([ekraan_x, ekraan_y])
myfont = pygame.font.SysFont("comic sans", 16)
pygame.display.flip()
clock = pygame.time.Clock()
värv = [0, 255, 0]
vajutad = False
kill_hitbox = []
collision_hitbox = []
hupe = []
'''
muusika = "TIKI TIKI - Slowed.mp3"
mixer.music.load(muusika)
mixer.music.play(-1)
'''
running = True

            

            
            
def draw_blocks():
    ekraan.blit(ree, (0, 0))
    for brick in bricks:
        ekraan.blit(brick.pilt, (brick.x, brick.y))  
    for vedur in hupe:
        ekraan.blit(vedur.pilt, (vedur.x, vedur.y))
    
class Tegelane:
    def __init__(self, x, y):
        self.pilt = pygame.image.load("blob.png")
        self.pilt = pygame.transform.smoothscale(self.pilt, (50, 50))
        self.x = x
        self.y = y
        self.liikumine_x = 0
        self.liikumine_y = 0
        self.liikumine_x_suurendaja = 0
        self.maal = None
        self.direction = None
        self.hüppamine = 50
        self.gravity = self.hüppamine
        self.gravity_suurendaja = 10
        self.kiirus = 10
    def gethitbox(self):
        self.laius = self.pilt.get_width()
        self.pikkus = self.pilt.get_height()
        return pygame.Rect(self.x, self.y, self.laius, self.pikkus)
    
    def jump(self):
        if self.maal:
            self.gravity = -self.hüppamine
            self.maal = False
            
    def dash(self):
        if self.direction == "right":
            self.liikumine_x_suurendaja = 300
        elif self.direction == "left":
            self.liikumine_x_suurendaja = -300
      
    def collide_with_hitbox(self, hitbox, x_check):
        if x_check.lower() == "x":
            self.hitbox = self.gethitbox()
            if self.hitbox.colliderect(hitbox):
                if self.liikumine_x < 0:
                    self.liikumine_x_suurendaja = 0
                    self.x = hitbox.right
                    return True
                elif self.liikumine_x > 0:
                    self.liikumine_x_suurendaja = 0
                    self.x = hitbox.left - self.hitbox.width
                    return True
                
     
        else:
            self.hitbox = self.gethitbox()
            if self.hitbox.colliderect(hitbox):
                if self.liikumine_y > 0:
                    self.y = hitbox.top - self.hitbox.height
                    self.gravity = 0
                    self.maal = True
                    return True
                elif self.liikumine_y < 0:
                    self.y = hitbox.y + hitbox.height 
                    self.gravity = 0
                    self.maal = False
                    return True
        
        
        

bob = Tegelane(0, 800)
bob.hitbox = bob.gethitbox()
class Coin:
    def __init__(self, x, y):
        self.sfx = pygame.mixer.Sound("jump.mp3")
        self.collect = pygame.mixer.Sound("it-is-i-waluigi.mp3")
        self.pilt = pygame.image.load("coin.webp").convert_alpha()
        self.pilt = pygame.transform.smoothscale(self.pilt, (50, 50))
        self.x = x
        self.y = y
        self.hitbox = None
    def gethitbox(self):
        return pygame.Rect(self.x, self.y, self.pilt.get_width(), self.pilt.get_height())
    

ree = pygame.image.load("taustapilt.png")
ree = pygame.transform.smoothscale(ree, (1200, 700))



def level_muutus(level):
    global bricks, münt, hupe, draw_blocks
    bricks = []
    münt = None
    hupe = []
    y = 0
    for row in level:
        x = 0
        for column in row:
                if column == 1:
                    bricks.append(platform(x * 50, y * 50, 50, 50, "brick.png"))
                elif column == 2:
                    münt = Coin(x * 50, y * 50)
                    münt.hitbox = münt.gethitbox()
                elif column == 3:
                    hupe.append(platform(x * 50, y * 50, 50, 50, "Spring.png"))
                x += 1
        y += 1
        
        
    ekraan.blit(ree, (0, 0))
    for brick in bricks:
        collision_hitbox.append(brick.hitbox)
    for brick in bricks:
        ekraan.blit(brick.pilt, (brick.x, brick.y))
    
    for vedur in hupe:
        ekraan.blit(vedur.pilt, (vedur.x, vedur.y))
        
        
        
        
        
class ammo:
    def __init__(self, pilt, a, b):
        self.x = 0
        self.y = 0
        self.liikumine_x = 50
        self.pilt = pygame.image.load(pilt)
        self.pilt = pygame.transform.smoothscale(self.pilt, (a, b))
        self.width = a
        self.height = b
        self.hitbox = pygame.Rect(a, b, self.x, self.y)
    def get_hitbox():
        return pygame.Rect(self.x, self.y, self.width, self.height)
        
        
beam = ammo("beam.png", 50, 10)

class platform():
    def __init__(self, x, y, laius, pikkus, pilt):
        self.pilt = pygame.image.load(pilt)
        self.pilt = pygame.transform.scale(self.pilt, (laius, pikkus))
        self.x, self.y = x, y
        self.hitbox = pygame.Rect(self.x, self.y, self.pilt.get_width(), self.pilt.get_height())
    def boost(self):
        return -80
      
bricks = []
t = 0
x = 0
y = 0



if mobile:
    level = levels[level_num]
    level_muutus(level[0])
    bob.x = level[1][0]
    bob.y = level[1][1]
    
for brick in bricks:
    collision_hitbox.append(brick.hitbox)

for vedru in hupe: 
    collision_hitbox.append(vedru.hitbox)

def arrows(suund):
    pilt = pygame.image.load("Arrow.jpg")
    pilt = pygame.transform.smoothscale(pilt, (300, 300))
    pilt = pygame.transform.rotate(pilt, suund)
    return pilt




up_arrow = arrows(0)
up_arrow_rect = pygame.Rect(900, 2000, 300, 300)
left_arrow = arrows(90)
left_arrow_rect = pygame.Rect(0, 2000, 300, 300)
right_arrow = arrows(-90)
right_arrow_rect = pygame.Rect(400, 2000, 300, 300)
pygame.draw.rect(ekraan, [0,0,0], up_arrow_rect)
pygame.draw.rect(ekraan, [0,0,0], left_arrow_rect)
pygame.draw.rect(ekraan, [0,0,0], right_arrow_rect)
    
ekraan.blit(up_arrow, (900, 2000))
ekraan.blit(left_arrow, (0, 2000))
ekraan.blit(right_arrow, (400, 2000))

sõrmele_lisa = []
right_key = False
nimi = []
sõrmed = {}

vajutad_pos = []
jooks = 0
ekraan.blit(ree, (0, 0))
if mobile:
    level_muutus(level[0])
rect = bob.gethitbox()
while running:
    clock.tick(60)
    
    
    
    
    
    bob.liikumine_x_suurendaja = 0
    jooks += 1
    if jooks == 48000:
        jooks = 1
    bob.liikumine_y = 0
    

    bob.hitbox = bob.gethitbox()
    if vajutad == False:
        vajutad_pos = [15000, 15000]
    
    ekraan.blit(ree, rect, rect)
    ekraan.blit(bob.pilt, [bob.x, bob.y])
    
    if münt != None:
        münt.hitbox = münt.gethitbox()
        ekraan.blit(münt.pilt, [münt.x, münt.y])
    
        
    
    
    
    
    events = []
    for event in pygame.event.get():
        events.append(event)
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bob.jump()
        if event.type == pygame.FINGERDOWN:
            vajutad_pos = [event.x * 1268, event.y *2450]
            sõrmed[event.finger_id] = vajutad_pos
            finger_hitbox = pygame.Rect(vajutad_pos[0], vajutad_pos[1], 50, 50)
            vajutad = True
        if event.type == pygame.FINGERMOTION:
            xy = [event.x * 1268, event.y * 2450]
            sõrmed[event.finger_id] = (xy[0],xy[1]) 
            vajutad = True
            
        if event.type == pygame.FINGERUP:
            if len(sõrmed) == 0:
                 vajutad = False
            del sõrmed[event.finger_id]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r or event.key == pygame.K_UP:
                if bob.direction == "right":
                    bob.dash()
                elif bob.direction == "left":
                    bob.dash()
        if level_num == None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level_num = 0
                    right_key = True
                elif event.key == pygame.K_2:
                    level_num = 1
                    right_key = True
                elif event.key == pygame.K_3:
                    level_num = 2
                    right_key = True
                elif event.key == pygame.K_4:
                    level_num = 3
                    right_key = True
                elif event.key == pygame.K_5:
                    level_num = 4
                    right_key = True
                    
                if right_key == True:
                    level = levels[level_num]
                    level_muutus(level[0])
                    bob.x = level[1][0]
                    bob.y = level[1][1]
                    
                    
                    
         # ekraan 1268 × 2450              
    nupp = pygame.key.get_pressed()
    #vajutad = pygame.mouse.get_pressed()[0]
    
    if münt != None and bob.gethitbox().colliderect(münt.gethitbox()):
        collision_hitbox = []  
        bricks = []
        try:
            level = levels[levels.index(level) + 1]
        except IndexError:
            running = False
            #level = levels[0]
        level_muutus(level[0])
        level_num += 1
        bob.x, bob.y = level[1][0], level[1][1]
        for brick in bricks:
            collision_hitbox.append(brick.hitbox)
              
        
        
    if nupp[K_SPACE]:
        bob.jump()
        
    if nupp[K_a]:
        bob.liikumine_x_suurendaja -= 20
        bob.direction = "left"
    if nupp[K_d]:
        bob.liikumine_x_suurendaja += 20
        bob.direction = "right"
    if vajutad:  
        for sõrm in sõrmed.values():      
            if vajutad and left_arrow_rect.x < sõrm[0] < left_arrow_rect.x + left_arrow_rect.width and left_arrow_rect.y < sõrm[1] < left_arrow_rect.y + left_arrow_rect.height:
                bob.liikumine_x -= 10
        
            if vajutad and right_arrow_rect.x < sõrm[0] < right_arrow_rect.x + right_arrow_rect.width and right_arrow_rect.y < sõrm[1] < right_arrow_rect.y + right_arrow_rect.height:
                bob.liikumine_x += 10
                
            if vajutad and up_arrow_rect.x < sõrm[0] < up_arrow_rect.x + up_arrow_rect.width and up_arrow_rect.y < sõrm[1] < up_arrow_rect.y + up_arrow_rect.height:
                bob.jump()
    
    if jooks % 2 == 0:     
        bob.liikumine_y += bob.gravity
        if bob.gravity < bob.hüppamine:
            bob.gravity += bob.gravity_suurendaja
    
        
    '''
    bob.liikumine_y += bob.gravity
    if bob.gravity < bob.hüppamine:
        bob.gravity += bob.gravity_suurendaja
    '''
            
    rect = bob.gethitbox()
    bob.maal = False
    bob.liikumine_x += bob.liikumine_x_suurendaja
    bob.x += bob.liikumine_x / 10
    bob.liikumine_x -= bob.liikumine_x / 10
    for vedru in hupe:
        bob.collide_with_hitbox(vedru.hitbox, "x")
        if bob.collide_with_hitbox(vedru.hitbox, "y"):
            bob.gravity = vedru.boost()
        
            
    for hitbox in collision_hitbox:
        bob.collide_with_hitbox(hitbox, "x")
        
    bob.y += bob.liikumine_y
    bob.maal = False
    for vedru in hupe:
        if bob.collide_with_hitbox(vedru.hitbox, "y"):
            bob.gravity = vedru.boost()
    for hitbox in collision_hitbox:
        bob.collide_with_hitbox(hitbox, "y")
    
    
    
    
    
    
    if bob.y < 0:
        bob.y = 0
        bob.gravity = bob.hüppamine
        bob.maal = False
    if bob.y > ekraan_y - bob.pilt.get_height():
        bob.y = ekraan_y - bob.pilt.get_height()
        bob.maal = True
    if bob.x < 0:
        bob.x = 0
    if bob.x > ekraan_x - bob.pilt.get_width():
        bob.x = ekraan_x - bob.pilt.get_width()
    if level_num == None:
        text = myfont.render(f"level; {level_num}", True, (0,255,0))
    else:
        text = myfont.render(f"level; {level_num + 1}", True, (0,255,0))
    ekraan.blit(text,(0, 0))
    pygame.display.flip()





bob.x = 200
bob.y = 200 
        
for i in range(50):
    clock.tick(5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    width_goal_1 = random.randint(50, 500)
    width_goal = width_goal_1
    height_goal_1 = random.randint(50, 500)
    height_goal = height_goal_1
    for _ in range(20):
        width_goal -= width_goal_1 / 20
        height_goal -= height_goal_1 / 20
        bob.pilt_uus = pygame.transform.smoothscale(bob.pilt, (-(width_goal - width_goal_1), -(height_goal - height_goal_1) ))
        bob.hitbox = bob.gethitbox()
        ekraan.blit(bob.pilt_uus, (bob.x, bob.y))
        
        pygame.display.flip()
        ekraan.blit(ree, (0, 0))
        ekraan.fill(värv)
        
pygame.quit()
