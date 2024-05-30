import pyxel

# CONSTANTES APP
HEIGHT = 256
WIDTH = 256
FPS = 128

fullHeart = (0,48,216,15,15)
halfHeart = (0,51,203,10,10)
emptyHeart = (0,51,187,10,10)
lightningEmpty = (0,35,187,10,10)
lightningFull = (0,35,203,10,10)

powerup = (0,18,234,12,12)
powerupBoom = (0,34,234,12,12)

#debut de l'animation mouche qui vole faire v+16 pour passer à la suivante 
fly = (0,128,8,16,16)

#debut de l'animation d'explotion faire v+16 pour passer à la suivante 
boom = (0,128,32,16,16)



# ------------------------------------------------

class App:
    def __init__(self):
        pyxel.init(HEIGHT, WIDTH, "Nuit du Code", FPS)
        pyxel.load("3.pyxres")
        pyxel.mouse(True)
        self.x = 0
        self.player = Player(50, 50)
        self.proj = bullet(40,40)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()
        self.proj.update()

    def draw(self):
        pyxel.cls(5)
        self.player.draw()
        self.proj.draw()

# ------------------------------------------------

class Icon:
    def __init__(self, x, y, sprite : tuple) -> None:
        self.x = x
        self.y = y
        self.sp = sprite
    
    def update(self) -> None:
        if (pyxel.frame_count % (FPS/2) == 0):
            self.y += 1
        if (pyxel.frame_count % FPS == 0):
            self.y -= 2

    def draw(self) -> None:
        pyxel.blt(self.x, self.y, self.sp[0], self.sp[1], self.sp[2], self.sp[3], self.sp[4], 5)

# --------------------------------------------------

# CONSTANTES PLAYER
s1 = (0, 0, 120, 16, 16, 5)
PLAYER_SPEED = 80/FPS

#ANIMATIONS
idle = (0, 120, 2, 4)
walk = (0, 136, 4, 8)

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
            bull = bullet(self.x, self.y)
            self.bullets.append(bull)
            

        for bull in self.bullets:
            bull.update()


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
        if self.x < 0:
            self.x = 0
        elif self.x > WIDTH - 16:
            self.x = WIDTH - 16

        if self.y < 0:
            self.y = 0
        elif self.y > HEIGHT - 16:
            self.y = HEIGHT - 16

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
            self.y -= 2
        if (not self.visible) and (self.cooldown_current > 0) and (self.cooldown != 0):
            self.cooldown_current -= 1
            if self.cooldown_current == 0:
                self.visible = True

    def draw(self) -> None:
        if self.visible:
            pyxel.blt(self.x, self.y, self.sp[0], self.sp[1], self.sp[2], self.sp[3])
    
    def touched(self):
        if self.visible:
            self.cooldown_current = self.cooldown

# --------------------------------------------------

#BULLETS CONSTANTS
COOLDOWN = 0.5 #in seconds
BULLET_SPEED = 100/FPS

#SPRITES
webBall = (0,131,193,4,4,5)

class bullet:
    def __init__(self, x : float, y : float) -> None:
        self.x = x + 4
        self.y = y + 4
        self.direction = self.mouseDirection()
        print(self.mouseDirection())

    def update(self):
        self.x += BULLET_SPEED*self.direction[0]
        self.y += BULLET_SPEED*self.direction[1]

    def mouseDirection(self) -> tuple:
        x = pyxel.mouse_x - self.x
        y = pyxel.mouse_y - self.y

        return normalizeVector(x,y)
        

        
    def draw(self) -> None:
        pyxel.blt(self.x, self.y, webBall[0], webBall[1], webBall[2], webBall[3], webBall[4], webBall[5])

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
# --------------------------------------------------
App()