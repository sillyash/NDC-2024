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