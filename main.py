import pyxel


class Player:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

    def draw(self):
        pyxel.blt(self.x,self.y,16,16,0,120,5)      



p1 = Player(0,0)

class App:
    def __init__(self):
        pyxel.init(128, 128, title="Nuit du Code")
        self.x = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        print()

    def draw(self):
        pyxel.cls(0)
        p1.draw()

App()