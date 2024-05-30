import pyxel

# CONSTANTES APP

HEIGHT = 128
WIDTH = 128
FPS = 128

class App:
    def __init__(self):
        pyxel.init(HEIGHT, WIDTH, "Nuit du Code", FPS)
        pyxel.load("3.pyxres")
        self.x = 0
        self.player = Player(50,50)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update()PLAYER_SPEED

    def draw(self):
        pyxel.cls(5)
        self.player.draw()


# CONSTANTES PLAYER
#SPRITES
s1 = (0, 0, 120, 16, 16, 5)

PLAYER_SPEED = 55/FPS

class Player:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y
        self.life = 5
        self.cSprite = s1

    def update(self):
        self.move()
        
    def move(self):
        if pyxel.btn(pyxel.KEY_Z):
            self.y -= PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_S):
            self.y += PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_Q):
            self.x -= PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_D):
            self.x += PLAYER_SPEED
        

    def draw(self):
        pyxel.blt(self.x, self.y, self.cSprite[0], self.cSprite[1], self.cSprite[2], self.cSprite[3], self.cSprite[4], self.cSprite[5])      




App()