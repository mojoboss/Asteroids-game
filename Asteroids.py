import simplegui
import math
import random

# globals for user interface
started = False
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
acc_const = 1
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.acc = [0,0]
        ############
        
    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos
    
    def shoot(self):
        global missile_group
        fwd_vector = angle_to_vector(self.angle)
        missile_pos=[self.pos[0]+ 42*fwd_vector[0], self.pos[1]+ 42*fwd_vector[1] ]
        missile_vel = [self.vel[0] + 15*fwd_vector[0], self.vel[1] + 15*fwd_vector[1]]
        a_missile = Sprite(missile_pos, missile_vel, 0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
                                  
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size,self.pos, self.image_size, self.angle )
    
    def set_angular_vel(self, key):         
        if key == simplegui.KEY_MAP['right']:
            self.angle_vel= 0.07
        elif key == simplegui.KEY_MAP['left']:
            self.angle_vel= -0.07
            
    def acclerate(self, key):
        if key == simplegui.KEY_MAP['up']:
            self.thrust = True
    
    def shooting_missile(self, key):
        if key == simplegui.KEY_MAP['space']:
            self.shoot()
            
    def set_key_up(self, key):         
        if key == simplegui.KEY_MAP['right']:
            self.angle_vel= 0
        elif key == simplegui.KEY_MAP['left']:
            self.angle_vel= 0
        elif key == simplegui.KEY_MAP['up']:
            self.thrust = False    

    def update(self):
        if self.thrust == True:
            self.acc = acc_const*angle_to_vector(self.angle)
            self.acc[0] /= 5
            self.acc[1] /= 5
            self.image_center[0] = 130
            ship_thrust_sound.play()
            
        if self.thrust == False:
            self.acc = [0, 0]
            self.image_center[0] = 45
            ship_thrust_sound.pause()
            
        self.angle+= self.angle_vel
        self.vel[0] += self.acc[0] - 0.009*self.vel[0]   #this is the net force/accleration on the spaceship including friction
        self.vel[1] += self.acc[1] - 0.009*self.vel[1]   #multiplying 0.009 by self.vel ensures friction which applies only when  
        self.pos[0] += self.vel[0]                 #ship is moving i.e. when vel != 0
        self.pos[1] += self.vel[1]
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
    
    def get_age(self):
        return self.age
    
    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos
    
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle )
    
    def update(self):
        self.angle+= self.angle_vel
        self.pos[0] += self.vel[0]        
        self.pos[1] += self.vel[1]
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        self.age += 1
        if self.age > 30 :
            return True
        else :
            return False
        
    def collide(self, object):
        global lives, started
        sum = self.get_radius() + object.get_radius()
        if sum > dist(self.get_position(), object.get_position()):
            if type(object) == Ship:
                lives -= 1
                if lives <= 0:
                    started = False
            return True
        else:
            return False

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score, my_ship, rock_group, missile_group
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        lives = 3
        score = 0
        my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
        rock_group = set([])
        missile_group = set([])
        started = True
        
        
           
def draw(canvas):
    global time
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    # draw lives and score
    
    canvas.draw_text("LIVES = "+str(lives), [10, 30], 30, "White")
    canvas.draw_text("SCORE = "+str(score), [610, 30], 30, "White")
    
    if started:
        #update & draw sprites
        process_sprite_group(canvas)
        
        # draw ship 
        my_ship.draw(canvas)
        
        # update ship 
        my_ship.update()
        
        group_collide(rock_group, my_ship)
        group_group_collide()
        
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())

    
    
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
    if started:
        temp = random.randrange(-5, 5)
        ang_vel = temp*random.random()
        ang_vel /= 10
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        rock_vel = [random.randrange(-1, 1), random.randrange(-1, 1)]
        a_rock = Sprite(rock_pos, rock_vel, 0, ang_vel, asteroid_image, asteroid_info)
        if len(rock_group)<13:
            rock_group.add(a_rock)
        
#function to draw and update rock group
def process_sprite_group(canvas):
    for x in rock_group:
        x.draw(canvas)
        x.update()
    
    global missile_group
    for x in missile_group:
        x.draw(canvas)
        if x.update():
            remove_set = set([])
            remove_set.add(x)
            missile_group = set(missile_group.difference(remove_set))
        
    
    
#function  to detect collisions b/w a group and an object
def group_collide(sprite_group, obj):
    global rock_group
    flag = 0
    remove_set = set([])
    for x in sprite_group:
        if x.collide(obj):
            flag = 1
            remove_set.add(x)
    rock_group = set(rock_group.difference(remove_set))
    if flag == 1:
        return True
    
#function  to detect collisions b/w two group
def group_group_collide():
    global rock_group, missile_group, score
    remove_missile_set = set([])
    for x in missile_group:
        if group_collide(rock_group, x):
            score += 10
            remove_missile_set.add(x)
    missile_group = set(missile_group.difference(remove_missile_set))	
    


    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])

#########################
#key handlers
def keydown(key):
     my_ship.set_angular_vel(key)
     my_ship.acclerate(key) 
     my_ship.shooting_missile(key)   
######        
def keyup(key):
     my_ship.set_key_up(key)
##########################

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)
# get things rolling
timer.start()
frame.start()