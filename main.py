import pyxel

# CONSTANTES APP

HEIGHT = 128
WIDTH = 128
FPS = 128

class App:
    def __init__(self):
        pyxel.init(HEIGHT, WIDTH, "Nuit du Code", FPS)
        self.x = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        print()

    def draw(self):
        pyxel.cls(0)
        p1.draw()


# CONSTANTES PLAYER
sprite1 = (0, 120, 16, 16)

class Player:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

    def draw(self):
        pyxel.blt(self.x,self.y,16,16,0,120,5)      


p1 = Player(0,0)

App()