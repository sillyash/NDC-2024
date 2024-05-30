import pyxel

# CONSTANTES APP
HEIGHT = 128
WIDTH = 128
FPS = 128

fullHeart = (48,216,15,15)
halfHeart = (51,203,10,10)
emptyHeart = (51,187,10,10)
lightningEmpty = (35,187,10,10)
lightningFull = (35,203,10,10)

powerup = (18,234,12,12)
powerupBoom = (34,234,12,12)

#debut de l'animation mouche qui vole faire v+16 pour passer à la suivante 
fly = (128,8,16,16)

#debut de l'animation d'explotion faire v+16 pour passer à la suivante 
boom = (128,32,16,16)



# ------------------------------------------------

class App:
    def __init__(self):
        pyxel.init(HEIGHT, WIDTH, "Nuit du Code", FPS)
        self.x = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()

    def draw(self):
        pyxel.cls(0)
        p1.draw()

# ------------------------------------------------

class Icon:
    def __init__(self, x, y, sprite : tuple) -> None:
        self.x = x
        self.y = y
        self.sp = sprite
    
    def update(self) -> None:
        if (pyxel.frame_count % (FPS/2) == 0):
            self.y += 1
        elif (pyxel.frame_count % FPS == 0):
            self.y -= 2

    def draw(self) -> None:
        pyxel.blt(self.x, self.y, self.sp[0], self.sp[1], self.sp[2], self.sp[3])

# --------------------------------------------------

# CONSTANTES PLAYER
s1 = (0, 0, 120, 16, 16, 5)
PLAYER_SPEED = 55/FPS

class Player:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y
        self.cSprite = s1
        self.direction = 1
        self.cursor = 0
        self.lives = 6
        self.hearts = []
        self.lightnings = []
        self.Initialize_Icons()
        self.icons = [self.hearts, self.lightnings]

    def update(self):
        self.move()
        for i in range(len(self.icons)):
            for icon in range(self.icons[i]):
                icon.update()

    def draw(self):
        pyxel.blt(self.x, self.y, self.cSprite[0], self.cSprite[1], self.cSprite[2], self.cSprite[3], self.cSprite[4], self.cSprite[5])  
        # draw icons
        for i in range(len(self.icons)):
            for icon in range(self.icons[i]):
                icon.draw()

    def Initialize_Icons(self) -> None:
        heart1 = Icon(3, 3, fullHeart)
        heart2 = Icon(10, 3, fullHeart)
        heart3 = Icon(17, 3, fullHeart)
        self.hearts.append(heart1, heart2, heart3)
        light1 = Icon(125, 125, lightningEmpty)
        light2 = Icon(118, 125, lightningEmpty)
        self.lightnings.append(light1, light2) 

    def move(self):
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

        if pyxel.frame_count % (FPS/8) == 0 and isMoving:
            self.cSprite = (0, self.cursor, 136, self.direction*16, 16, 5)
            
            if(self.cursor < 48):
                self.cursor += 16
            else:
                self.cursor = 0   


# ------------------------------------------------
    
class PowerUp:
    def __init__(self, x, y, sprite : tuple, cooldown = 0) -> None:
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

App()