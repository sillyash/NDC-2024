import pyxel

class App:
    def __init__(self):
        pyxel.init(128, 128, title="Nuit du Code")
        self.x = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        print()

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(self.x, 0, 8, 8, 9)

App()