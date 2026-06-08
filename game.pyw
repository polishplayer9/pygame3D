import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((280*4,244*4))
pygame.display.set_caption("game")
clock = pygame.time.Clock()
running = True

difficultySpeed = 3

gameover = False

camX = 0
camY = 0
camZ = 0

groundLevel = 25

#instances list
instances = []

#instance drawing list
instancesToDraw = []

gravity = 0.25

c_black = (0,0,0)
c_white = (255,255,255)

c_red = (255,0,0)
c_darkRed = (155,0,0)

c_green = (0,255,0)
c_blue = (0,0,255)

c_yellow = (255,255,0)
c_orange = (255,155,0)

c_cyan = (0,255,255)
c_pink = (255,0,255)

width, height = screen.get_size()
perspCenterX = width/2
perspCenterY = height/2

enemyTimer = 0
enemyTimergoal = 10

def lerp(a,b,t):
    return a + (b-a)*t

def normalize(val,minval,maxval):
    return (val - minval) / (maxval - minval)

def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))

def project3D(x,y,z):
    x -= camX
    y -= camY
    z -= camZ
    z = max(z,0.0001)
    return (
        perspCenterX+(((x)*200)/z),
        perspCenterY+(((y)*200)/z)
        )
def drawCube(color,x,y,xs,ys,rotx,roty):
    pass

def drawShadow(self):
    rect43d(
             #left up
             self.x,
             groundLevel+self.yscale,
             self.z,
             #right up
             self.x+self.xscale,
             groundLevel+self.yscale,
             self.z,
             #right down
             self.x+self.xscale,
             groundLevel+self.yscale,
             self.z-self.yscale/2,
             #left down
             self.x,
             groundLevel+self.yscale,
             self.z-self.yscale/2,
             c_darkRed
    )

def destroy(ins):
    instances.remove(ins)
    instancesToDraw.remove(ins)

def drawGUI():
    #drawText(50,50,str(player.hp)+" / "+str(player.maxhp),None,60,c_white)
    rectangle(350,50,500,20,c_red)
    rectangle(350,50,(player.hp/player.maxhp)*500,20,c_green)

def drawInstances():
    rectangle(0,perspCenterY+10,width,height/2,c_red)
    instancesToDraw.sort(key=lambda p: p.z, reverse=True)
    for instance in instancesToDraw[:]:
        drawShadow(instance)
        instance.draw()
        
def stepInstances():
    for instance in instances[:]:
        instance.step()
    
    
def rectangle(x,y,xs,ys,color):
    rect = pygame.Rect(x,y,xs,ys)
    pygame.draw.rect(screen,color,rect)
      
def rect43d(x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4,color):
    if(z1 <= 0 or z2 <= 0 or z3 <= 0 or z4 <= 0):return
    proj1 = project3D(x1,y1,z1)
    proj2 = project3D(x2,y2,z2)
    proj3 = project3D(x3,y3,z3)
    proj4 = project3D(x4,y4,z4)
    pygame.draw.polygon(screen,color,[proj1,proj2,proj3,proj4])
  
def rectangleObj(self,x,y,xs,ys,color):
    rect = pygame.Rect(x+self.drawX,y+self.drawY,xs,ys)
    pygame.draw.rect(screen,color,rect)
    
def rectangle3D(self,x,y,z,xs,ys,color):
    if(z <= 0):return
    x3d, y3d = project3D(x,y,z)
    xs3d = xs/((z-camZ)/200)
    ys3d = ys/((z-camZ)/200)
        
    rect = pygame.Rect(x3d,y3d,xs3d,ys3d)
    pygame.draw.rect(screen,color,rect)
    
def drawText(x,y,text,font,size,color):
    f = pygame.font.SysFont(font,size)
    text = f.render(text,True,color)
    screen.blit(text,(x,y))
    

#if player collides with a object of class also made from scratch but that doesn't matter anymore i guess
def isColliding(obj,clas5):
    for ins in instances:
        if not isinstance(ins,clas5):continue
        if(obj.x < ins.x+ins.xscale and
           obj.x+obj.xscale > ins.x and
           obj.y < ins.y+ins.yscale and
           obj.y+obj.yscale > ins.y):
            return True
    return False

def isColliding3D(obj,clas5):
    for ins in instances:
        if not isinstance(ins,clas5):continue
        if(obj.x < ins.x+ins.xscale and
           obj.x+obj.xscale > ins.x and
           obj.y < ins.y+ins.yscale and
           obj.y+obj.yscale > ins.y and
           obj.z < ins.z+ins.zscale and
           obj.z+obj.zscale > ins.z):
            return True
    return False
        
    
def place_meeting(self,offsetx,offsety,clas5):
    class fakeBox:
        pass
    f = fakeBox()
    f.xscale = self.xscale
    f.yscale = self.yscale
    f.x = self.x+offsetx
    f.y = self.y+offsety
    return isColliding(f,clas5)

def place_meeting3D(self,offsetx,offsety,offsetz,clas5):
    class fakeBox:
        pass
    f = fakeBox()
    f.xscale = self.xscale
    f.yscale = self.yscale
    f.zscale = self.zscale
    f.x = self.x+offsetx
    f.y = self.y+offsety
    f.z = self.z+offsetz
    return isColliding3D(f,clas5)
    

class Player:
    def __init__(self,xp,yp,zp):
        instances.append(self)
        instancesToDraw.append(self)
        self.invincibleTimer = 0
        self.blinkTimer = 0
        
        self.visible = True
        
        self.maxhp = 100
        self.hp = self.maxhp
        
        
        self.color = c_yellow
        self.brightness = 1
        
        self.x = xp
        self.y = yp
        self.z = zp
        
        self.xspd = 0
        self.yspd = 0
        self.zspd = 0
        
        self.drawX = 0
        self.drawY = 0
        self.drawZ = 0
        self.xscale = 50
        self.yscale = 50
        self.zscale = 50
        self.onground = False
        self.walkSpeed = 2
        
    def hurt(self,amount):
        global difficultySpeed
        if(self.invincibleTimer <= 0):
            self.invincibleTimer = 120
            self.hp -= amount
            
    def controls(self):
        rl = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
        du = (keys[pygame.K_UP] - keys[pygame.K_DOWN])
        if(keys[pygame.K_SPACE] and self.onground):
            self.yspd = -7
        self.xspd = lerp(self.xspd,rl * self.walkSpeed,0.05)
        self.zspd = lerp(self.zspd,du * self.walkSpeed,0.05)
        print("X : "+str(self.x)+", Y : "+str(self.y)+", Z : "+str(self.z))
        
    def physics(self):
        self.yspd += gravity
        self.x += self.xspd
        self.y += self.yspd
        self.z += self.zspd
        if self.y >= groundLevel:
            self.y = groundLevel
            self.onground = True
        else:
            self.onground = False
        
    def step(self):
        global camX
        global camY
        global camZ
        camX = self.x+self.xscale/2
        camY = self.y-self.yscale/2
        camZ = self.z-self.zscale
        global gameover
        self.invincibleTimer -= 1
        if(self.invincibleTimer > 0):
            self.color = c_orange
            self.blinkTimer += 1
            if(self.blinkTimer > 1):
                self.blinkTimer = 0
                self.visible = not self.visible
        else:
            self.visible = True
            self.color = c_yellow
        if(not gameover):
            self.controls()
        self.physics()
        self.brightness = clamp(normalize(self.z-camZ,1000,0),0.3,1)
        if(place_meeting3D(self,0,0,0,Enemy)):
            self.hurt(10)
        if(self.hp <= 0):
            gameover = True
        
    def draw(self):
      if(self.visible):
        rectangle3D(self,self.x,self.y,self.z,self.xscale,self.yscale,tuple(x*self.brightness for x in self.color))
        
class Enemy:
    def __init__(self,xp,yp,zp):
        instances.append(self)
        instancesToDraw.append(self)
        self.x = xp
        self.y = yp
        self.z = zp
        
        self.xspd = 0
        self.yspd = 0
        self.zspd = 0
        
        self.color = c_cyan
        self.brightness = 1
        
        self.drawX = 0
        self.drawY = 0
        self.drawZ = 0
        self.xscale = 50
        self.yscale = 50
        self.zscale = 1
        self.walkSpeed = 0
        
    def physics(self):
        self.x += self.xspd
        self.y += self.yspd
        self.z += self.zspd
        
    def step(self):
        self.physics()
        self.walkSpeed = difficultySpeed
        self.zspd = 0
        self.brightness = clamp(normalize(self.z-camZ,1000,0),0.3,1)
        
    def draw(self):
        self.drawX = 0
        self.drawY = 0
        self.drawZ = 0
        rectangle3D(self,self.x,self.y,self.z,self.xscale,self.yscale,tuple(x*self.brightness for x in self.color))        

class Collision:
    def __init__(self,xp,yp,xs,ys):
        instances.append(self)
        self.x = xp
        self.y = yp
        self.drawX = 0
        self.drawY = 0
        self.drawZ = 0
        self.xscale = xs
        self.yscale = ys
        self.zscale = 50
    def step(self):
        pass
    def draw(self):
        self.drawX = self.x
        self.drawY = self.y
        rectangleObj(self,0,0,self.xscale,self.yscale,c_pink)

player = Player(-25,25,50)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    screen.fill(c_blue)
    if(not gameover):
        enemyTimer += 1
        if(enemyTimer > enemyTimergoal):
            enemyTimer = 0
            Enemy(random.randint(-500,500),random.randint(-100,25),1000)
        difficultySpeed += 0.0001
    else:
        difficultySpeed = lerp(difficultySpeed,0,0.05)
        player.zspd = lerp(player.zspd,0,0.01)
        player.xspd = lerp(player.xspd,0,0.01)
    stepInstances()
    drawInstances()
    drawGUI()
    pygame.display.flip()
    clock.tick(120)