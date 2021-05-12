from if3_game.engine import init, Game, Sprite, Layer
from asteroid import Asteroid,GameLayer, RESOLUTION


init(RESOLUTION,"Asteroid")

game = Game()
game.debug = True #affiche les informations de debug comme la forme de la collision

#on peut mettre le background ici
#bg = Sprite("le nom du fichier")

#bg_layer = 
game_layer = GameLayer()

#et ajouter le add background ici!
#bg_layer.add(bg)

#game.dd(bg_layer)
game.add(game_layer)

game.run()        