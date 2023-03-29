# Sabin Dheke and Hari Krishna
# CMPS 5443 
# Advance topic: 2D Games
# Assignment 2

try:
    import pygame
    import sys
    from pygame.locals import *
except ImportError:
    print("Error in loading modules")
    sys.exit(2)

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PURPLE = (255,0,255)
GREY = (169,169,169)

OVERLAP = 18

pygame.init()
screen = pygame.display.set_mode((1920, 1000))
pygame.display.set_caption("Signalling Demo")

# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))

buttons_pressed = []

class TrackSection(pygame.sprite.Sprite):
    def __init__(self, coords_length, points = False, branch = False):
        pygame.sprite.Sprite.__init__(self)
        self.coords_length = coords_length
        self.colour = WHITE
        self.occupied = False
        self.signal = None
        self.points = points
        self.branch = branch

        self.image = pygame.Surface([coords_length[2], coords_length[3]]).convert_alpha()

        self.image.fill(self.colour)

        self.rect = self.image.get_rect()
        self.rect.topleft = [coords_length[0], coords_length[1]]

        self.hitbox = pygame.Rect(coords_length[0], coords_length[1], 30, 15)
        self.hitbox.bottomright = [coords_length[0], coords_length[1] + 4]

    def occupy(self):
        self.occupied = True
        self.colour = PURPLE
        self.image = pygame.Surface([self.coords_length[2], self.coords_length[3]]).convert_alpha()
        self.image.fill(self.colour)

        if self.points:
            self.image = pygame.transform.rotate(self.image, -40)
            self.hitbox = pygame.Rect(self.coords_length[0], self.coords_length[1], 150, 80)

    def unoccupy(self):
        self.occupied = False
        self.colour = WHITE
        self.image = pygame.Surface([self.coords_length[2], self.coords_length[3]]).convert_alpha()
        self.image.fill(self.colour)

        if self.points:
            self.image = pygame.transform.rotate(self.image, -40)
            self.hitbox = pygame.Rect(self.coords_length[0], self.coords_length[1], 120, 74)

    def add_signal(self, sig):
        self.signal = sig


class Signal(pygame.sprite.Sprite):
    def __init__(self, name, track):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.track = track
        self.colour = "green"

        self.image = pygame.image.load("images/green.png").convert()

        self.rect = self.image.get_rect()
        self.rect.bottomleft = [track.coords_length[0], track.coords_length[1]]

    def set_colour(self, colour):
        self.colour = colour
        self.image = pygame.image.load("images/%s.png" % colour)

    def get_colour(self):
        return self.colour

    def add_train(self, train):
        self.trains.append(train)

    def remove_train(self, train):
        self.trains.remove(train)


class RouteButton(pygame.sprite.Sprite):
    def __init__(self, signal, points = False, branch = False):
        pygame.sprite.Sprite.__init__(self)
        self.signal = signal
        self.colour = WHITE
        self.status = False
        self.branch = branch
        self.points = points
        self.image = pygame.Surface([30, 30]).convert_alpha()

        if self.points:
            self.colour = GREEN
        self.image.fill(self.colour)

        self.rect = self.image.get_rect()
        if self.points:
            self.rect.topleft = [signal.rect[0]-80, signal.rect[1]+50]
        elif self.branch:
            self.rect.topleft = [signal.rect[0], signal.rect[1]+90]
        else:
            self.rect.topleft = [signal.rect[0], signal.rect[1]-50]

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # if the player clicked the button, the action is invoked
                if not self.status:
                    self.press()
                    return True
                else:
                    self.release()
                    return False
        return False


    def press(self):
        self.status = True
        self.colour = RED
        if self.points:
            self.colour = WHITE
            train1.route = "branch"
        self.image.fill(self.colour)

    def release(self):
        self.status = False
        self.colour = WHITE
        if self.points:
            self.colour = GREEN
            train1.route = "main"
        self.image.fill(self.colour)


class Train(pygame.sprite.Sprite):
    def __init__(self, name, position, route="main"):
        super().__init__()
        self.name = name
        self.route = route
        self.current_signal = t1
        self.position = position
        self.xspeed = 0
        self.yspeed = 0
        self.i = 0
        self.j = 0

        self.image = pygame.Surface([30,15]).convert_alpha()
        self.image.fill(BLUE)

        self.hitbox = pygame.Rect(position[0],position[1],30,15)
        self.hitbox.bottomright = [position[0], position[1]+18]

        self.rect = self.image.get_rect()
        self.rect.bottomright = position

    def move(self,x_speed, y_speed=0):
        self.xspeed = x_speed
        self.yspeed = y_speed

    def update(self):
        self.rect.x += self.xspeed
        self.rect.y += self.yspeed
        if (self.rect.colliderect(b1) and self.i == 0) and self.route == "branch":
            self.rect.x += 5
            self.hitbox.x += 5
            self.image = pygame.transform.rotate(self.image,-40)
            self.i+=1
        if self.hitbox.colliderect(b2) and self.j ==0:
            self.image = pygame.transform.rotate(self.image,40)
            self.j+=1

        self.hitbox.x +=self.xspeed
        self.hitbox.y +=self.yspeed


# Create signals and track sections

t1 = TrackSection([100,500,100,10])
t2 = TrackSection([t1.coords_length[0]+t1.coords_length[2]+2,500,200,10])
t3 = TrackSection([t2.coords_length[0]+t2.coords_length[2]+2,500,200,10])
t4 = TrackSection([t3.coords_length[0]+t3.coords_length[2]+2,500,400,10])
t5 = TrackSection([t4.coords_length[0]+t4.coords_length[2]+2,500,200,10])
t6 = TrackSection([t5.coords_length[0]+t5.coords_length[2]+2,500,100,10])
t7 = TrackSection([t6.coords_length[0]+t6.coords_length[2]+2,500,100,10])
t8 = TrackSection([t7.coords_length[0]+t7.coords_length[2]+2,500,100,10])
t9 = TrackSection([t8.coords_length[0]+t8.coords_length[2]+2,500,200,10])

b1 = TrackSection([t3.coords_length[0]+t3.coords_length[2]+2,500,150,10], True, True)
b2 = TrackSection([b1.coords_length[0]+b1.coords_length[2]-36,594,150,10], False, True)
b3 = TrackSection([b2.coords_length[0]+b2.coords_length[2]+2,594,300,10], False, True)
b4 = TrackSection([b3.coords_length[0]+b3.coords_length[2]+2,594,300,10], False, True)

TRACKS = [t1,t2,t3,t4,t5,t6,t7,t8,t9]

BRANCH = [b1, b2, b3, b4]

track_group = pygame.sprite.Group()
for x in TRACKS:
    track_group.add(x)

branch_group = pygame.sprite.Group()
for x in BRANCH:
    branch_group.add(x)

#main signals
s1 = Signal("A1",t2)
s2 = Signal("A2",t3)
s3 = Signal("A3",t4)
s4 = Signal("A4",t5)
s5 = Signal("A5",t6)
s6 = Signal("A6",t7)
s7 = Signal("A7",t8)

#branch signals
s8 = Signal("B1", b2)
s9 = Signal("B2", b3)
s10 = Signal("B3", b4)

#associating signals with their track sections
t2.add_signal(s1)
t3.add_signal(s2)
t4.add_signal(s3)
t5.add_signal(s4)
t6.add_signal(s5)
t7.add_signal(s6)
t8.add_signal(s7)

b2.add_signal(s8)
b3.add_signal(s9)
b4.add_signal(s10)


SIGNALS = [s1,s2,s3,s4,s5,s6,s7,s8,s9,s10]

signal_group = pygame.sprite.Group()
for x in SIGNALS:
    signal_group.add(x)

button1 = RouteButton(s1)
button2 = RouteButton(s2)
button3 = RouteButton(s3)
button4 = RouteButton(s4)
button5 = RouteButton(s5)
button6 = RouteButton(s6)
button7 = RouteButton(s7)
button8 = RouteButton(s8, True)
button9 = RouteButton(s9, False, True)
button10 = RouteButton(s10, False, True)

BUTTONS = [button1, button2, button3, button4, button5, button6, button7, button8, button9, button10]

button_group = pygame.sprite.Group()

for x in BUTTONS:
    button_group.add(x)

# Set initial signal colors

s1.set_colour("red")
s10.set_colour("red")


# Create train sprites
train1 = Train("thomas", [150, 498], "main")
train2 = Train("mike", [1400, 498], "main")

train_group = pygame.sprite.Group()
train_group.add(train1)
train_group.add(train2)

clock = pygame.time.Clock()

screen.blit(background, (0, 0))

pygame.display.flip()
GameExit = False

while not GameExit:
    clock.tick(20)
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            GameExit = True

        if event.type == KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if b1.hitbox.colliderect(train1.hitbox) and train1.route == "branch":
                    train1.move(10,8)
                else:
                    train1.move(25)
                train1.update()

        for x in BUTTONS:
            if not len(buttons_pressed) ==2:
                if x.is_clicked(event):
                    buttons_pressed.append(x)


    occupied_tracks = []

    #track circuit detection logic

    for x in TRACKS:
        if x.rect.colliderect(train1.hitbox):
            occupied_tracks.append(x)
            train1.current_signal = x
            x.occupy()

        elif x.rect.colliderect(train2.hitbox):
            occupied_tracks.append(x)
            train2.current_signal = x
            x.occupy()

        else:
            if x.occupied == True:
                x.unoccupy()
                if x.signal is not None:
                    x.signal.set_colour("yellow")

    for x in BRANCH:
        if (((x.rect.colliderect(train1.hitbox) and (train1.route == "branch")) or (x.rect.colliderect(train2.hitbox)
                and (train2.route == "branch")))) and x != b1:
            occupied_tracks.append(x)
            x.occupy()
        elif x.hitbox.colliderect(train1.hitbox) and x == b1:
            occupied_tracks.append(x)
            x.occupy()
        else:
            if x.occupied == True:
                if x.signal is not None:
                    x.signal.set_colour("yellow")
            x.unoccupy()

    if len(buttons_pressed) == 2:
        if buttons_pressed[0].signal.get_colour() == "red" and not buttons_pressed[0].points:
            buttons_pressed[0].signal.set_colour("green")
        if buttons_pressed[1].signal.get_colour() == "green" or buttons_pressed[1].signal.get_colour() == "yellow"\
                and not buttons_pressed[1].points:
            buttons_pressed[1].signal.set_colour("red")
        buttons_pressed[0].release()
        buttons_pressed[1].release()
        buttons_pressed = []

    #signal logic
    for x in occupied_tracks:
        if not x.branch:
            whichtrack = TRACKS.index(x)
            if x.signal is not None:
                x.signal.set_colour("red")

        else:
            whichtrack = BRANCH.index(x)
            if whichtrack == 1:
                TRACKS[2].signal.set_colour("green")
                TRACKS[3].signal.set_colour("yellow")
            elif whichtrack == 2:
                TRACKS[3].signal.set_colour("green")
            if x.signal is not None:
                x.signal.set_colour("red")

    for x in SIGNALS:
        if x.get_colour() == "red" and SIGNALS[SIGNALS.index(x)-1].get_colour() != "red":
            SIGNALS[SIGNALS.index(x) - 1].set_colour("yellow")
        if x.get_colour() == "yellow" and SIGNALS[SIGNALS.index(x)-1].get_colour() != "red":
            SIGNALS[SIGNALS.index(x) - 1].set_colour("green")

    #handle the train movement
    next_signal = TRACKS[TRACKS.index(train1.current_signal)+1].signal

    if train1.current_signal.signal == s3 and train1.route == "branch":
        next_signal = BRANCH[1].signal


    if next_signal.colour == "red":
        if train1.rect.x+30 < next_signal.rect.x - 10:
            if b1.hitbox.colliderect(train1.hitbox) and train1.route == "branch":
                train1.move(4, 3)
            else:
                train1.move(1,0)
            train1.update()

    elif next_signal.colour == "green":
        if b1.hitbox.colliderect(train1.hitbox) and train1.route == "branch":
            train1.move(4, 3)
        else:
            train1.move(5,0)
        train1.update()

    elif next_signal.colour == "yellow":
        if b1.hitbox.colliderect(train1.hitbox) and train1.route == "branch":
            train1.move(4, 3)
        else:
            train1.move(3,0)
        train1.update()


    branch_group.draw(screen)
    track_group.draw(screen)
    signal_group.draw(screen)
    train_group.draw(screen)
    button_group.draw(screen)
    pygame.display.flip()

pygame.quit()
quit()