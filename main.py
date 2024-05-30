import pyxel

# CONSTANTES APP
HEIGHT = 256
WIDTH = 256
FPS = 60
NEST_W = 58

# icones
fullHeart = (0,48,216,15,15)
halfHeart = (0,51,203,10,10)
emptyHeart = (0,51,187,10,10)
lightningEmpty = (0,35,187,10,10)
lightningFull = (0,35,203,10,10)

# ...
powerupHeal = (0,2,234,12,12)
powerup = (0,18,234,12,12)
powerupBoom = (0,34,234,12,12)

#debut de l'animation mouche qui vole faire v+16 pour passer à la suivante 
fly = (0,128,8,-16,16)

#debut de l'animation d'explosion faire v+16 pour passer à la suivante 
boom = (0,128,32,16,16)

# nectar
nectar = (0,2,234,12,12)

# diver
spriteDiver = (0,0,8,16,16)

# ---------- FONCTIONS GLOBALES ----------

def normalizeVector(x : int, y : int) -> tuple:
    if abs(x) > abs(y):
        if x != 0:
            return(x/abs(x), y/abs(x))
    elif abs(y) > abs(x):
        if y != 0:
            return(x/abs(y), y/abs(y))
    else:
        return(x/abs(x),x/abs(x))

def abs(x):
    return x*pyxel.sgn(x)

def collision(r1 : tuple, r2 : tuple) -> bool:
    # (x, y, w, h)
    x1 = abs(r1[0])
    y1 = abs(r1[1])
    w1 = abs(r1[2])
    h1 = abs(r1[3])
    x2 = abs(r2[0])
    y2 = abs(r2[1])
    w2 = abs(r2[2])
    h2 = abs(r2[3])

    if (x2 < x1 < (x2+w2)) or (x2 < (x1+w1) < (x2+w2)):
        if y2 < y1 < (y2+h2):
            return True
        elif y2 < (y1+h1) < (y2+h2):
            return True
    return False

# ----------------- CLASSES -------------------

class App:
    def __init__(self):
        pyxel.init(HEIGHT, WIDTH, "Nuit du Code", FPS)
        pyxel.load("3.pyxres")
        pyxel.mouse(True)
        self.x = 0
        self.player = Player(50, 50)
        self.flies = []
        self.nest = Nest()
        self.score = 0
        self.nectar = PowerUp(60,80,powerupHeal, 10)
        pyxel.playm(0, 0, True)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()
        self.nectar.update()
        if collision(self.nectar.rect(), self.player.rect()) and self.nectar.visible == True:
            self.nest.addLife(4)
            self.nectar.used()
        #self.nest.update()
        self.spawnFlies()
        
        # updates projectiles
        # joueur
        for bullet in self.player.bullets:
            """for diver in self.divers:
                if collision(bullet, diver):
                    self.joueur.removeLife(1)
                    self.player.bullets.remove(bullet)"""
            
            for fly in self.flies:
                if collision(bullet.rect(), fly.rect()):
                    if (fly.removeLife(1)):
                        self.flies.remove(fly)
                        self.score += 1
                    self.player.bullets.remove(bullet)
            
            if bullet != None:
                bullet.update()

        # update mouches
        for fly in self.flies:
            fly.update()
            if collision(fly.rect(), self.nest.rect()):
                self.flies.remove(fly)
                self.nest.removeLife(2)


    def draw(self):
        pyxel.cls(5)
        pyxel.bltm(0, 0, 1, 0, 0, 255, 255)
        self.player.draw()
        self.nectar.draw()
        #self.nest.draw()

        # draw mouches
        for fly in self.flies:
            fly.draw()
        
        pyxel.text(WIDTH-50, 4, "Score : " + str(self.score), 0)
        pyxel.text(WIDTH-180, 4, "Nest life : " + str(self.nest.life), 0)

    def spawnFlies(self):
        if (pyxel.frame_count % 45 == 0):
            self.flies.append(Fly(WIDTH,pyxel.rndi(10,HEIGHT-15)))

# ------------------------------------------------

class Nest:
    def __init__(self) -> None:
        self.life = 50
        self.width = NEST_W
    
    def addLife(self, i):
        self.life += i

    def removeLife(self, dmg) -> bool:
        if self.life-dmg > 1:
            self.life -= dmg
            return False
        else:
            return True
    
    def rect(self):
        return (0,0,self.width+2,HEIGHT)


# ------------------------------------------------

class Icon:
    def __init__(self, x, y, sprite : tuple) -> None:
        self.x = x
        self.y = y
        self.sp = sprite
    
    def update(self) -> None:
        if (pyxel.frame_count % (FPS/2) == 0):
            self.y += 1
        if ((pyxel.frame_count % FPS) == 0):
            self.y -= 2

    def draw(self) -> None:
        pyxel.blt(self.x, self.y, self.sp[0], self.sp[1], self.sp[2], self.sp[3], self.sp[4], 5)

# --------------------------------------------------

# CONSTANTES PLAYER
s1 = (0, 0, 120, 16, 16, 5)
PLAYER_SPEED = 80/FPS

#ANIMATIONS
idle = (0, 120, 2, 2.5)
walk = (0, 136, 4, 6)

class Player:
    def __init__(self, x : float, y : float) -> None:
        self.x = x
        self.y = y
        self.cSprite = s1
        self.direction = 1
        self.cursor = 0
        self.lives = 6

        #bullets
        self.timer = 0
        self.bullets = []

        #HUD
        self.hearts = []
        self.lightnings = []
        self.Initialize_Icons()
        self.icons = [self.hearts, self.lightnings]

    def update(self):
        self.move()
        for i in range(len(self.icons)):
            for icon in self.icons[i]:
                icon.update()

        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and pyxel.frame_count - self.timer > COOLDOWN*FPS:
            self.timer = pyxel.frame_count
            bull = Bullet(self.x, self.y, webBall)
            self.bullets.append(bull)
            

        for bull in self.bullets:
            bull.update()
            if bull.touchBorder():
                self.bullets.remove(bull)

    def removeLife(self, dmg):
        if self.life > 0:
            self.life -= dmg
        else:
            self.die()

    def draw(self):
        for bullet in self.bullets:
            bullet.draw()
        pyxel.blt(self.x, self.y, self.cSprite[0], self.cSprite[1], self.cSprite[2], self.cSprite[3], self.cSprite[4], self.cSprite[5])
        # draw icons
        for i in range(len(self.icons)):
            for icon in self.icons[i]:
                icon.draw()

    def Initialize_Icons(self) -> None:
        heart1 = Icon(3, 3, fullHeart)
        heart2 = Icon(10, 3, fullHeart)
        heart3 = Icon(17, 3, fullHeart)
        self.hearts.append(heart1)
        self.hearts.append(heart2)
        self.hearts.append(heart3)
        light1 = Icon(WIDTH - 15, HEIGHT - 15, lightningEmpty)
        light2 = Icon(WIDTH - 15*2, HEIGHT - 15, lightningEmpty)
        self.lightnings.append(light1)
        self.lightnings.append(light2) 

    def move(self) -> None:
        isMoving = False
    
        if pyxel.btn(pyxel.KEY_Z):
            self.y -= PLAYER_SPEED
            isMoving = True
        if pyxel.btn(pyxel.KEY_S):
            self.y += PLAYER_SPEED
            isMoving = True
        if pyxel.btn(pyxel.KEY_Q):
            self.x -= PLAYER_SPEED
            isMoving = True
            self.direction = -1
        if pyxel.btn(pyxel.KEY_D):
            self.x += PLAYER_SPEED
            isMoving = True
            self.direction = 1

        self.touchBorder()

        if isMoving:
            self.anim(walk[0],walk[1],walk[2],walk[3])
        else:
            self.anim(idle[0],idle[1],idle[2],idle[3])

    def touchBorder(self) -> None:
        if self.x < NEST_W:
            self.x = NEST_W
        elif self.x > WIDTH - 16:
            self.x = WIDTH - 16

        if self.y < 0:
            self.y = 0
        elif self.y > HEIGHT - 16:
            self.y = HEIGHT - 16
    
    def rect(self) -> tuple:
        return (self.x, self.y, 16, 16)

    def anim(self, first_x : int, first_y : int, nbFrame : int, speed : int):
        if pyxel.frame_count % (FPS/speed) == 0:
            self.cSprite = (0, first_x + self.cursor, first_y, self.direction*16, 16, 5)
            
            if(self.cursor < (nbFrame-1)*16):
                self.cursor += 16
            else:
                self.cursor = 0

# ------------------------------------------------
    
class PowerUp:
    def __init__(self, x : int, y : int, sprite : tuple, cooldown = 0) -> None:
        self.x = x
        self.y = y
        self.sp = sprite
        self.visible = True
        self.cooldown = cooldown
        self.cooldown_current = 0
    
    def update(self) -> None:
        if (pyxel.frame_count % (FPS/2) == 0):
            self.y += 1
        elif (pyxel.frame_count % FPS == 0):
            self.y -= 1
        if (pyxel.frame_count % 60 == 0):
            if (not self.visible) and (self.cooldown_current > 0) and (self.cooldown != 0):
                self.cooldown_current -= 1
                if self.cooldown_current == 0:
                    self.visible = True
    
    def rect(self) -> tuple:
        return (self.x, self.y, 12, 12)

    def used(self):
        self.cooldown_current = self.cooldown
        self.visible = False

    def draw(self) -> None:
        if self.visible:
            pyxel.blt(self.x, self.y, self.sp[0], self.sp[1], self.sp[2], self.sp[3], self.sp[4], 5)
    
    def touched(self):
        if self.visible:
            self.cooldown_current = self.cooldown

# --------------------------------------------------

#BULLETS CONSTANTS
COOLDOWN = 0.28 #in seconds
BULLET_SPEED = 125/FPS

#SPRITES
webBall = (0,131,193,4,4,5)

class Bullet:
    def __init__(self, x : float, y : float, sprite) -> None:
        self.x = x + 4
        self.y = y + 4
        self.sprite = sprite
        self.direction = self.mouseDirection()

    def update(self):
        self.x += BULLET_SPEED*self.direction[0]
        self.y += BULLET_SPEED*self.direction[1]

    def mouseDirection(self) -> tuple:
        x = pyxel.mouse_x - self.x
        y = pyxel.mouse_y - self.y

        return normalizeVector(x,y)
    
    def touchBorder(self) -> bool:
        if self.x < 0:
            return True
        elif self.x > WIDTH:
            return True

        if self.y < 0:
            return True
        elif self.y > HEIGHT:
            return True
        return False
    
    def rect(self) -> tuple:
        return (self.x, self.y, 4, 4)
        
    def draw(self) -> None:
        pyxel.blt(self.x, self.y, self.sprite[0], webBall[1], self.sprite[2], self.sprite[3], self.sprite[4], self.sprite[5])
    
# --------------------------------------------------

class Fly :
    def __init__(self, x:int,y:int):
        self.x = x
        self.y = y
        self.life = 2
        self.cursor = 0
        self.cSprite = fly # constante glob
        
    def draw (self):
        pyxel.blt(self.x, self.y, self.cSprite[0], self.cSprite[1], self.cSprite[2], self.cSprite[3], self.cSprite[4], 5)

    def touchBorder(self):
        if self.x < 0:
            self.x = 0
        elif self.x > WIDTH - 16:
            self.x = WIDTH - 16
        if self.y < 0:
            self.y = 0
        elif self.y > HEIGHT - 16:
            self.y = HEIGHT - 16
    
    def removeLife(self, dmg) -> bool:
        if self.life > 1:
            self.life -= dmg
            return False
        else:
            return True

    def update(self):
        self.move()
    
    def move(self):
        if (pyxel.frame_count % 5 == 0):
            if (self.x > NEST_W):
                self.x -= 1
                self.anim(128,8,8,2)

    def anim(self, first_x : int, first_y : int, nbFrame : int, speed : int):
        if (pyxel.frame_count % 30) == 0:
            self.cSprite = (0, first_x + self.cursor, first_y, 16, 16, 5)
            
            if(self.cursor < (nbFrame-1)*16):
                self.cursor += 16
            else:
                self.cursor = 0
        # REMOVE
        self.cSprite = fly
    
    def rect(self) -> tuple:
        return (self.x, self.y, 16, 16)





App()

