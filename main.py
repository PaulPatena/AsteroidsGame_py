#Copyright of Paul Michael Patena, all rights reserved
#Email: paulmichaelpatena@gmail.com

# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
width = 800
height = 600
score = 0
lives = 3
time = 0
started = False

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
    
# Small rocks floating on background
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png - background picture
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image - Rice Rocks Startup Screen
splash_info = ImageInfo([200, 150], [399, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")
#splash_image = simplegui.load_image("https://www.dropbox.com/s/13qgwmytlqfk8ne/asteroid_splash_paul.png?dl=0")
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

ouch_sound = simplegui.load_sound("https://dl.dropbox.com/u/9374021/uughh.wav")
applause_sound = simplegui.load_sound("https://dl.dropbox.com/u/9374021/applause.wav")


THRUST_CONST = 0.3
FRICTION_CONST = 0.040
MISSILE_FACTOR = 5
ANGLE_VEL = 6

# helper functions to handle transformations
def angle_to_vector(ang):
    # conversion to unit circle, x = cosA, y = sinB
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    # sqrt( (x1-x2)^2 + (y1-y2)^2 )
    return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)


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
        
    def draw(self,canvas):
        if not self.thrust :
            source_pos = self.image_center
        else :
            source_pos =  [self.image_center[0] + self.image_size[0], self.image_center[1]]

        canvas.draw_image(self.image, source_pos, self.image_size, self.pos, self.image_size, self.angle)
        
        # This is my implementation of wrap, I did not use modulo because it takes 
        #  a lot of computing power and could cause some jumps.
        mod_pos = list(self.pos)
        x_rboundary = width - (self.image_size[0] / 2)
        x_lboundary = self.image_size[0] / 2
        
        y_bboundary = height - (self.image_size[1] / 2)
        y_tboundary = self.image_size[1] / 2
        
        if (mod_pos[0] > x_rboundary):
            mod_pos[0] = (-self.image_size[0] / 2) + mod_pos[0] - x_rboundary
        elif (mod_pos[0] < x_lboundary):
            pixels = x_lboundary - mod_pos[0]
            mod_pos[0] = width + (self.image_size[0] / 2) - pixels
            
        if (mod_pos[1] > y_bboundary):
            mod_pos[1] = (-self.image_size[1] / 2) + mod_pos[1] - y_bboundary
        elif (mod_pos[1] < y_tboundary):
            pixels = y_tboundary - mod_pos[1]
            mod_pos[1] = height + (self.image_size[1] / 2) - pixels

        canvas.draw_image(self.image, source_pos, self.image_size, mod_pos, self.image_size, self.angle)

    def get_position(self) :
        return list(self.pos)
    
    def get_radius(self) :
        return self.radius
        
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle  += self.angle_vel
        
        if self.thrust:
            forward = angle_to_vector(self.angle)
            self.vel[0] += forward[0] * THRUST_CONST
            self.vel[1] += forward[1] * THRUST_CONST
        
        self.vel[0] *= (1 - FRICTION_CONST)
        self.vel[1] *= (1 - FRICTION_CONST)

        if (self.pos[0] > width + self.image_size[0] / 2):
            self.pos[0] = self.pos[0] - width            
        elif (self.pos[0] < -self.image_size[0] / 2):
            self.pos[0] = width + self.pos[0]

        if (self.pos[1] > height + self.image_size[1] / 2):
            self.pos[1] = self.pos[1] - height
        elif (self.pos[1] < -self.image_size[1] / 2):
            self.pos[1] = height + self.pos[1]
                   
    def inc_angle_vel(self):        
        # radians = degrees * 3.1416 / 180
        self.angle_vel = ANGLE_VEL * 3.1416 / 180
        
    def dec_angle_vel(self):
        self.angle_vel = -(ANGLE_VEL * 3.1416 / 180)
        
    def reset_angle_vel(self):
        self.angle_vel = 0
        
    def set_thruster(self, boOn):
        self.thrust = boOn
        if boOn:
            ship_thrust_sound.play()
        else :
            ship_thrust_sound.pause()
            ship_thrust_sound.rewind()
    
    def shoot(self, missile_group):
        global a_missile, missile_info
        pos = list(self.pos)
        TIP_RADIUS = 38
        pos[0] += TIP_RADIUS * math.cos(self.angle)
        pos[1] += TIP_RADIUS * math.sin(self.angle)
        vel = [0, 0]
        forward = angle_to_vector(self.angle)
        vel[0] = self.vel[0] + forward[0] * MISSILE_FACTOR
        vel[1] = self.vel[1] + forward[1] * MISSILE_FACTOR
       
        a_missile = Sprite(pos, vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
    
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
   
    def get_position(self) :
        return list(self.pos)
    
    def get_radius(self) :
        return self.radius

    # returns true if self and other object collides
    def collide(self, other_obj) :
        boRet = False
        other_pos = other_obj.get_position()
        
        limit = self.radius + other_obj.get_radius()
        distance = math.sqrt( math.pow(self.pos[0] - other_pos[0], 2) + math.pow(self.pos[1] - other_pos[1], 2))
        
        if distance < limit :
            boRet = True
        
        return boRet
    
    def draw(self, canvas):
        if (self.animated) :
            self.image_center[0] = (self.age % self.lifespan) * self.image_size[0] + (self.image_size[0] / 2)
        
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
        mod_pos = list(self.pos)
        x_rboundary = width - (self.image_size[0] / 2)
        x_lboundary = self.image_size[0] / 2
        
        y_bboundary = height - (self.image_size[1] / 2)
        y_tboundary = self.image_size[1] / 2
        
        if (mod_pos[0] > x_rboundary):
            mod_pos[0] = (-self.image_size[0] / 2) + mod_pos[0] - x_rboundary
        elif (mod_pos[0] < x_lboundary):
            pixels = x_lboundary - mod_pos[0]
            mod_pos[0] = width + (self.image_size[0] / 2) - pixels
            
        if (mod_pos[1] > y_bboundary):
            mod_pos[1] = (-self.image_size[1] / 2) + mod_pos[1] - y_bboundary
        elif (mod_pos[1] < y_tboundary):
            pixels = y_tboundary - mod_pos[1]
            mod_pos[1] = height + (self.image_size[1] / 2) - pixels

        canvas.draw_image(self.image, self.image_center, self.image_size, mod_pos, self.image_size, self.angle)
        
    
    def update(self):
        boRet = False
        
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle  += self.angle_vel
        self.age += 1
        
        if (self.pos[0] > width + self.image_size[0] / 2):
            self.pos[0] = self.pos[0] - width            
        elif (self.pos[0] < -self.image_size[0] / 2):
            self.pos[0] = width + self.pos[0]

        if (self.pos[1] > height + self.image_size[1] / 2):
            self.pos[1] = self.pos[1] - height
        elif (self.pos[1] < -self.image_size[1] / 2):
            self.pos[1] = height + self.pos[1]
            
        if (self.age < self.lifespan) :
            boRet = True
        
        return boRet

def keydown(key):
    global my_ship, missile_group
    
    if (key == simplegui.KEY_MAP["right"]) :
        my_ship.inc_angle_vel()
    elif (key == simplegui.KEY_MAP["left"]) :
        my_ship.dec_angle_vel()
    elif (key == simplegui.KEY_MAP["up"]) :
        my_ship.set_thruster(True)
    elif (key == simplegui.KEY_MAP["space"]) :
        my_ship.shoot(missile_group)

def keyup(key):
    global my_ship
    
    if (key == simplegui.KEY_MAP["right"]) :
        my_ship.reset_angle_vel()
    elif (key == simplegui.KEY_MAP["left"]) :
        my_ship.reset_angle_vel()
    elif (key == simplegui.KEY_MAP["up"]) :
        my_ship.set_thruster(False)
#    elif (key == simplegui.KEY_MAP["space"]) :
#        my_ship.shoot()
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score
    center = [width / 2, height / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        score = 0
        lives = 3
        applause_sound.pause()
        applause_sound.rewind()
        soundtrack.play()

def process_sprite_group(group_obj, canvas) :
    for an_obj in list(group_obj) :
        an_obj.draw(canvas)    
        boKeep = an_obj.update()
        if not boKeep :
            group_obj.remove(an_obj)
        
        
def group_collide(group_obj, other_obj) :
    global explosion_group
    collide_count = 0
    
    for an_obj in list(group_obj) :
        if an_obj.collide(other_obj):
            explosion_group.add(Sprite(list(an_obj.get_position()), [0,0], 0, 0, explosion_image, explosion_info, explosion_sound))
            group_obj.remove(an_obj)
            collide_count += 1         

#    if (collide_count > 1):
#        print ("colide count > 1")
    return collide_count

def group_group_collide(missiles, rocks) :
    global missile_group
    
    collide_count = 0
    
    for missile in list(missiles) :    
        collide_count += group_collide(rocks, missile)
        
        if (collide_count > 0):
            #print (missile_group)
            missile_group.remove(missile)
    return collide_count

def get_distance(pos1, pos2) :
    return math.sqrt( ((pos1[0] - pos2[0])**2) + ((pos1[1] - pos2[1])**2) )

def draw(canvas):
    global time, started, rock_group, missile_group, lives, score, ROCK_COUNT
    
    # animate background
    time += 1
    
    #center = [320, 240]
    center = debris_info.get_center()
    #size = [640, 480]
    size = debris_info.get_size()
    # /8 is to slow down frame rate, * center[0] is to handle time being too high, must wrap around
    #wtime = (time / 8) % center[0]
    wtime = (time/4) % center[0]
    
    #canvas.draw_image(image, center_source, width_height_source, center_dest, width_height_dest)
    #canvss width = 800, height = 600
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [width/2, height/2], [width, height])
    canvas.draw_image(debris_image, [center[0]-wtime, center[1]], [size[0]-2*wtime, size[1]], 
                                [width/2+1.25*wtime, height/2], [width-2.5*wtime, height])
    if (wtime > 0):
        canvas.draw_image(debris_image, [size[0]-wtime, center[1]], [2*wtime, size[1]], 
                                [1.25*wtime, height/2], [2.5*wtime, height])



    # draw/update ship and sprites
    my_ship.draw(canvas)
    my_ship.update()       

    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    rock_vs_ship = group_collide(rock_group, my_ship)
    if rock_vs_ship > 0 :
        lives -= rock_vs_ship
        ROCK_COUNT -= rock_vs_ship
        ouch_sound.rewind()
        ouch_sound.play()
        #print ROCK_COUNT
    
    missile_vs_rock = group_group_collide(missile_group, rock_group)
    if missile_vs_rock > 0 :
        score += missile_vs_rock
        ROCK_COUNT -= missile_vs_rock
    
    if (lives <= 0) :
        started = False
        for obj in list(rock_group) :
            rock_group.remove(obj)
        ROCK_COUNT = 0
        soundtrack.pause()
        soundtrack.rewind()
        applause_sound.play()
    
    
    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")  

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [width/2, height/2], 
                          splash_info.get_size())

# timer handler that spawns a rock    
ROCK_COUNT = 0
def rock_spawner():
    global rock_group, ROCK_COUNT, my_ship, score
    
    ship_pos = my_ship.get_position()
    # ship radius + asteroid radius + allowance
    spawn_radius = my_ship.get_radius() + 45 + 50
    
    MAX_ROCK_VELOCITY = 7
    if (score > 5) :
        MAX_ROCK_VELOCITY = 10
    if (score > 10) :
        MAX_ROCK_VELOCITY = 14
    if (score > 15) :        
        MAX_ROCK_VELOCITY = 19
    if (score > 20) :        
        MAX_ROCK_VELOCITY = 25
    
    if (ROCK_COUNT < 12) and started :
        pos = [0, 0]
        vel = [0, 0] 
        angle = 0
        angle_vel = 0.1
        
        asteroid_x_size = (asteroid_info.get_size())[0]
        asteroid_y_size = (asteroid_info.get_size())[1]
        
        pos[0] = random.randrange(0+asteroid_x_size/2, width-asteroid_x_size/2)
        pos[1] = random.randrange(0+asteroid_y_size/2, height-asteroid_y_size/2)
        
        while ( get_distance(ship_pos, pos) < spawn_radius) :
            pos[0] = random.randrange(0+asteroid_x_size/2, width-asteroid_x_size/2)
            pos[1] = random.randrange(0+asteroid_y_size/2, height-asteroid_y_size/2)
            #print "stuck"
    
        # 0.1 to 2.5 pixel/update(60hz), 0.1 increments
        vel[0] = float(random.randint(1, MAX_ROCK_VELOCITY)) / 10.0
        vel[1] = float(random.randint(1, MAX_ROCK_VELOCITY)) / 10.0
        
        
        if (random.randrange(0, 2) == 0) :
            vel[0] *= -1
        if (random.randrange(0, 2) == 0) :
            vel[1] *= -1
        #debug print("velocity", vel)
        
        angle = random.randrange(0, 360)
        # radians = degrees * 3.1416 / 180
        angle = angle * 3.1416 / 180
        
        # range 0.01 to 0.05 radians/update(60hz), 0.001 increments
        angle_vel = random.randrange(10, 51) / 1000
        if (random.randrange(0, 2) == 0) :
            angle_vel *= -1
    
        a_rock = Sprite(pos, vel, angle, angle_vel, asteroid_image, asteroid_info)
        #print("velocity", vel)
        rock_group.add(a_rock)
        ROCK_COUNT += 1
    
#THRUST_CONST = 0.5
#FRICTION_CONST = 0.035
#MISSILE_FACTOR = 5
def inc_thrust():
    global THRUST_CONST
    THRUST_CONST += 0.1
    thrust_label.set_text("Thrust factor = "+str(THRUST_CONST/.1))

def dec_thrust():
    global THRUST_CONST
    if THRUST_CONST > 0.1 :
        THRUST_CONST -= 0.1
        thrust_label.set_text("Thrust factor = "+str(THRUST_CONST/.1))

def inc_friction():
    global FRICTION_CONST
    FRICTION_CONST += 0.005
    friction_label.set_text("Friction factor = "+str(FRICTION_CONST//.005))

def dec_friction():
    global FRICTION_CONST
    if FRICTION_CONST > 0.01 :
        FRICTION_CONST -= 0.005
        friction_label.set_text("Friction factor = "+str(FRICTION_CONST//.005))        

def inc_missile():
    global MISSILE_FACTOR
    MISSILE_FACTOR += 1
    missile_label.set_text("Missle Speed factor = "+str(MISSILE_FACTOR//1))

def dec_missile():
    global MISSILE_FACTOR
    if MISSILE_FACTOR > 1 :
        MISSILE_FACTOR -= 1
        missile_label.set_text("Missle Speed factor = "+str(MISSILE_FACTOR//1))

def inc_angleVel():
    global ANGLE_VEL
    ANGLE_VEL += 1
    angleVel_label.set_text("Angular Velocity (deg/16ms) = "+str(ANGLE_VEL))

def dec_angleVel():
    global ANGLE_VEL
    if ANGLE_VEL > 1:
        ANGLE_VEL -= 1
        angleVel_label.set_text("Angular Velocity (degrees/16ms) = "+str(ANGLE_VEL))
    
# initialize frame
frame = simplegui.create_frame("Asteroids", width, height)

thrust_label = frame.add_label("Thrust factor = "+str(THRUST_CONST/.1))
frame.add_button("Increase Thrust",  inc_thrust,  200)
frame.add_button("Decrease Thrust",  dec_thrust,  200)

friction_label = frame.add_label("Friction factor = "+str(FRICTION_CONST//.005))
frame.add_button("Increase Friction",  inc_friction,  200)
frame.add_button("Decrease Friction",  dec_friction,  200)

angleVel_label = frame.add_label("Angular Velocity (deg/16ms) = "+str(ANGLE_VEL))
frame.add_button("Increase Angular Velocity",  inc_angleVel,  200)
frame.add_button("Decrease Angular Velocity",  dec_angleVel,  200)

missile_label = frame.add_label("Missile Speed factor = "+str(MISSILE_FACTOR//1))
frame.add_button("Increase Missile Speed",  inc_missile,  200)
frame.add_button("Decrease Missile Speed",  dec_missile,  200)

frame.add_label("=======================")
frame.add_label(" C O N T R O L L E R : ")
frame.add_label("   UP     = Thruster   ")
frame.add_label("  LEFT   = Rotate Left ")
frame.add_label("  RIGHT  = Rotate Right")
frame.add_label("SPACEBAR = Fire Missle ")
frame.add_label("=======================")

# initialize ship and two sprites
my_ship = Ship([width / 2, height / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])



# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
