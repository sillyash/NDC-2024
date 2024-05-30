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
        pyxel.rect(self.x, 0, 8, 8, 9)


# CONSTANTES PLAYER
sprite1 = (0, 120, 16, 16)

class player:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

    def draw(self):
        print()


App()