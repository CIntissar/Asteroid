from if3_game.engine import Sprite,Layer
from pyglet.window.key import symbol_string
from math import cos,sin,radians 
from random import randint

RESOLUTION = (800,600)  #en majuscule car c'est une constante.

class GameLayer(Layer):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        
        asteroid = Asteroid( (100,200) ) 
        self.add(asteroid)

        spaceship = Spaceship( (400,300) )        
        self.add(spaceship)


    def on_key_press(self,key,modifiers):
        if symbol_string == "ENTER":
            self.reset()
        
        super().on_key_press(key,modifiers)



class SpaceObject(Sprite):
    def __init__(self,image,position = (0,0), anchor = (0,0)): 
        super().__init__(image, position, anchor = anchor)
        self.rotation_speed = 0
        self.speed = (0,0)

    def update(self,dt): 

        self.rotation += self.rotation_speed * dt  # dégré par seconde c'est "+= degré * dt"

        new_x = self.position[0] + self.speed[0] * dt 
        new_y = self.position[1] + self.speed[1] * dt

       
        if new_x > RESOLUTION[0]:
            new_x = 0 

        # Y a une manière plus condensé pour cela
        #new x = new x % RESOLUTION[0]   ou   new_x %= RESOLUTION[0] 
                    
        elif new_x < 0:   
            new_x = RESOLUTION[0] 

        if new_y > RESOLUTION[1]: 
            new_y = 0

        elif new_y < 0:
            new_y = RESOLUTION[1] 
            
        self.position = (new_x,new_y)
        
        super().update(dt)



class Asteroid(SpaceObject):
    def __init__(self,position = (0,0),size = 3):  # on lui a donné une position de départ

        if size == 3 :
            super().__init__("assets/asteroid128.png",position,anchor = (64,64))

        elif size == 2 :
            super().__init__("assets/asteroid64.png",position,anchor = (32,32))

        elif size == 1 :
            super().__init__("assets/asteroid32.png",position,anchor = (16,16))

        self.rotation_speed = 90
        self.speed = (50,30)
        self.size = size

    def destroy(self):
        if self.size > 1:
            for i in range(2):
                baby_asteroid = Asteroid(self.position, self.size - 1)
                baby_asteroid.speed = (randint(-150,50), randint(-150,50))
                self.layer.add(baby_asteroid)
        
        super().destroy()



class Bullet(SpaceObject):
    def __init__(self,position = (0,0)):
        super().__init__("assets/bullet.png",position,anchor = (8,8))
        self.lifetime = 0.75

    def update(self,dt):
        super().update(dt)

        self.lifetime -= dt
        if self.lifetime <= 0:
            self.destroy()

    def on_collision(self,other): #other = l'autre objet en collision
        if isinstance(other,Asteroid):
            self.destroy()
            other.destroy()



class Spaceship(SpaceObject):
    def __init__(self,position = (0,0)):  # on lui a donné une position de départ
        super().__init__("assets/spaceship.png",position,anchor = (32,32))
        #self.speed = (50,30)
        self.power_on = False
        self.turn_speed = 180
        self.velocity = 0           #(force d'accélération)

    def on_key_press(self,key,modifiers):
        if symbol_string(key) == "LEFT":
            self.rotation_speed -= 90

        elif symbol_string(key) == "RIGHT":
            self.rotation_speed += 90

        elif symbol_string(key) == "UP":
            self.power_on = True

        elif symbol_string(key) == "SPACE":
            self.shoot()


    def on_key_release(self,key,modifiers):
        if symbol_string(key) == "LEFT":
            self.rotation_speed += 90

        elif symbol_string(key) == "RIGHT":
            self.rotation_speed -= 90

        elif symbol_string(key) == "UP":
            self.power_on = False
 

    def update(self,dt):
        if self.power_on == True:
            angle = - radians(self.rotation) #parce que le sens des math, est antihorlogique

            self.velocity += 500 * dt

            #self.speed = (cos(angle) * self.velocity ,sin(angle) * self.velocity)

            if self.velocity > 1000:
                self.velocity = 1000   # pour limiter la vitesse

            #Ici une autre manière de l'écrire:
            #self.velocity = min(self.velocity,100)

            new_speed_x = self.speed[0] + cos(angle) * self.velocity * dt
            new_speed_y = self.speed[1] + sin(angle) * self.velocity * dt

            self.speed = (new_speed_x, new_speed_y)

        else:
            new_speed_x = self.speed[0] * 0.99
            new_speed_y = self.speed[1] * 0.99

            self.speed = (new_speed_x, new_speed_y)

            self.velocity = 0
            

        super().update(dt)


    def shoot(self):
        #instancier Bullet
        #mais a quel position?

        bullet = Bullet(self.position)

        #donner une vitesse aux bullets
        angle = -radians(self.rotation)
        bullet.speed = (cos(angle) * 500 , sin(angle) * 500)

        #ajouter le bullet au Layer
        self.layer.add(bullet)

    def on_collision(self,other): #other = l'autre objet en collision
        if isinstance(other,Asteroid):
            self.destroy()
      

