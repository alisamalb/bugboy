import pyxel
import random
import time
from textwrap import TextWrapper
import math

def drawTextBoard():
    pyxel.rect(18,198,220,54,1)
    pyxel.rectb(18,198,220,54,5)

def drawMountains():
        mountainstart=(0-pyxel.frame_count)%600-200
        pyxel.tri(-40+mountainstart,210,20+mountainstart,130,125+mountainstart,256,4)

        pyxel.tri(0+mountainstart,180,60+mountainstart,100,125+mountainstart,256,4)
        pyxel.tri(100+mountainstart,180,60+mountainstart,100,125+mountainstart,256,9)
        pyxel.tri(44+mountainstart,120,60+mountainstart,100,71+mountainstart,120,13)
        pyxel.tri(68+mountainstart,120,60+mountainstart,100,71+mountainstart,120,7)
        pyxel.rect(0,180,256,76,12)
        [pyxel.circ((0+i*16-2*(pyxel.frame_count%128))%256,185,10,12) for i in range(16)]
        [pyxel.circ((0+i*16-2*(pyxel.frame_count%128))%256,195,10,5) for i in range(16)]
        [pyxel.circ((0+i*16-2*(pyxel.frame_count%128))%256,200,10,12) for i in range(16)]
def textToScript(path):
    tw = TextWrapper()
    tw.width = 50
    characters = [["Na.", "Narrator"], ["J.", "Jenna"], ["E.", "Enemy"], [
        "Mr.", "Mr. Produce"], ["Ms.", "Ms. Producer"], ["N.", "Intern"],["Ev.","Everyone"],["Jt.","Jenna (thinking)"]]
    textFile = open(path, "r").readlines()
    script = []
    for line in textFile:
        charcterLine = False
        for c in characters:
            if c[0] in line:
                script.append([c[1], "\n".join(tw.wrap(line[len(c[0]):]))])
                charcterLine = True
        if not charcterLine:
            script.append(["", line])

    return script

class BugBoy:
    def __init__(self):
        self.life=3
        self.x=32
        self.y=64
        self.speed=2
        self.attacking=False
        self.returning=False
    
    def collisionDetection(self,scene):
        for i,bullet in enumerate(scene.bullets):
            if bullet.x < self.x+32 and bullet.x>self.x and bullet.y>self.y and bullet.y<self.y+16 and not self.attacking and not self.returning:
                self.life-=1
        for i, enemy in enumerate(scene.enemies):
            if enemy.x < self.x+32 and enemy.x>self.x-16 and enemy.y>self.y-16 and enemy.y<self.y+16:
                scene.enemies.pop(i)
        for i, choice in enumerate(scene.choices):
            if choice.x < self.x+32 and choice.x>self.x-16 and choice.y>self.y-16 and choice.y<self.y+16:
                return choice.text
        return None
    def update(self,scene):
        if pyxel.btn(pyxel.KEY_UP) and not self.attacking:
            self.y-=self.speed
            self.y=max([self.y,0])
        if pyxel.btn(pyxel.KEY_DOWN) and not self.attacking:
            self.y+=self.speed
            self.y=min([self.y,180])
        if pyxel.btn(pyxel.KEY_RIGHT) and not self.attacking:
            self.x+=self.speed
            self.x=min([self.x,80])
        if pyxel.btn(pyxel.KEY_LEFT) and not self.attacking:
            self.x-=self.speed
            self.x=max([32,self.x])
        if pyxel.btnp(pyxel.KEY_B) and not self.attacking:
            self.attacking = True
        if self.attacking:
            if self.x<240:
                self.x+=15
            else:
                self.attacking=False
                self.returning=True
        if self.returning:
            if self.x>32:
                self.x-=10
            else:
                self.returning=False
        return self.collisionDetection(scene)
        
            
    def draw(self):
        pyxel.blt(self.x, self.y-5, 0, 32, 32, 32*[-1,1][int(pyxel.frame_count/10)%2], 16, 0)
        pyxel.blt(self.x+3, self.y-5, 0, 32, 32, 32*[-1,1][int(pyxel.frame_count/10)%2], 16, 0)
        if self.attacking:
            pyxel.blt(self.x, self.y, 0, 64, 32, 32, 16, 0)
        else:   
            pyxel.blt(self.x, self.y, 0, 0, 32, 32, 16, 0)
    
class Enemy:
    def __init__(self):
        self.life=3
        self.x=200
        self.y=random.randint(60,180)
        self.vspeed=2
        self.hspeed=8
        self.image=random.randint(1,6)
        self.attacking=False
        self.timeFromLastBullet=0
    def update(self,scene):
        self.x+=round(((pyxel.frame_count+random.randint(0,2))%27-13)/6)
        self.y+=round(((pyxel.frame_count+random.randint(0,2))%27-13)/6)

        self.x=max([min([250,self.x]),160])
        self.y=max([min([180,self.y]),20])

        if self.attacking:
            self.timeFromLastBullet+=1
            if self.timeFromLastBullet>100:
                if random.randint(0,self.timeFromLastBullet)>130:
                    angle=math.atan((scene.bugboy.y-self.y)/(scene.bugboy.x-self.x))
                    scene.bullets.append(Bullet(self.x,self.y,math.sin(angle),math.cos(angle)))
                    self.timeFromLastBullet=0
    def setAttack(self,b):
        self.attacking=b
    def draw(self):
        pyxel.blt(self.x-7, self.y-5, 0, 32, 32, 32*[-1,1][int(pyxel.frame_count/10)%2], 16, 0)
        pyxel.blt(self.x-3, self.y-5, 0, 32, 32, 32*[-1,1][int(pyxel.frame_count/10)%2], 16, 0)
        pyxel.blt(self.x, self.y, 0, (self.image-1)*16, 64, 16, 16,4)      
        if self.attacking:
            pyxel.rect(self.x+8,self.y+8,5,1,0)
            pyxel.rect(self.x+10,self.y+9,3,1,0)
            pyxel.pset(self.x+13,self.y+10,0)

class Bullet:
        def __init__(self,x,y,vspeed,hspeed):
            self.x=x
            self.y=y
            self.speed=3
            self.vspeed=vspeed
            self.hspeed=hspeed
        def update(self):
            self.x-=self.hspeed*self.speed
            self.y-=self.vspeed*self.speed
        def draw(self):
            pyxel.circ(self.x,self.y,2,8)


class Cloud:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        npoints = random.randint(4, 7)
        self.balls = []
        for i in range(npoints):
            self.balls.append([random.randint(5, 25), random.randint(5, 15)])

    def draw(self):
        for b in self.balls:
            pyxel.circ(self.x+b[0], self.y+b[1], 10, 7)

    def update(self):
        self.x = (self.x-2) % 231

class ChoiceCloud:
    def __init__(self, x, y,text):
        self.x = x
        self.y = y
        self.text=text
 
    def draw(self):
        pyxel.circ(self.x+5,self.y+5,10,7)
        pyxel.circ(self.x+14,self.y+2,10,7)
        pyxel.circ(self.x+24,self.y+5,13,7)
        pyxel.text(self.x,self.y,self.text,0)
        

    def update(self):
        self.y+=((pyxel.frame_count%34)-15)//4



class Menu:
    def __init__(self):
        self.optionSelected = 0
        self.clouds = [Cloud(random.randint(10, 245),
                             random.randint(10, 245)) for x in range(10)]

    def draw(self):
        pyxel.cls(5)
        [cloud.draw()
         for cloud in self.clouds]
        pyxel.rect(0, 20, 256, 40, 0)
        pyxel.blt(73, 22+pyxel.frame_count % 16 // 4, 0, 16, 0, 128, 32, 0)
        pyxel.rect(90, 74, 90, 70, 2)
        pyxel.rectb(91, 75, 88, 68, 7)
        pyxel.rect(110, 82+16*self.optionSelected, 50, 10, 0)
        pyxel.text(116, 84+16*self.optionSelected, '>', pyxel.frame_count % 16)
        pyxel.text(120, 84, "PLAY!", 7)
        pyxel.text(120, 100, "Credits", 7)
        pyxel.text(120, 116, "Quit", 7)

    def update(self, app):
        [cloud.update() for cloud in self.clouds]
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.optionSelected = (self.optionSelected+1) % 3
        if pyxel.btnp(pyxel.KEY_UP):
            self.optionSelected = (self.optionSelected-1) % 3
        if pyxel.btn(pyxel.KEY_ENTER):
            if self.optionSelected == 0:
                app.state = 4

            if self.optionSelected == 1:
                app.state = 3

            if self.optionSelected == 2:
                pyxel.quit()


class Credits:
    def __init__(self):
        self.read = 1

    def draw(self):
        pyxel.rect(16, 16, 118, 118, 9)
        pyxel.text(
            20, 32, "This game was created for \n GAME OFF 2021", 0)
        pyxel.text(
            20, 52, "By\nDiana Croce and\n Simone Albani".upper(), 0)
        pyxel.text(
            20, 72, "Using Pyxel\ngithub.com/kitao/pyxel", 0)
        pyxel.rect(58, 110, 70, 20, 0)
        pyxel.text(62, 115, "OK (press ENTER)", 9)

    def update(self, app):
        if pyxel.btnr(pyxel.KEY_ENTER):
            self.read = 1
        if pyxel.btnp(pyxel.KEY_ENTER) and self.read:
            self.read = 0
            time.sleep(0.5)
            app.state = 0


class Incipit:
    def __init__(self):
        self.read = 1

    def draw(self):

        pyxel.text(
            20, 32, "zzZ"*round(pyxel.frame_count/50%5), 7)

        pyxel.text(
            20, 52, ">", pyxel.frame_count % 5)
        pyxel.text(24, 52, "Wake Jenna up", 7)

    def update(self, app):
        if pyxel.btnr(pyxel.KEY_ENTER):
            self.read = 1
        if pyxel.btnp(pyxel.KEY_ENTER) and self.read:
            self.read = 0
            app.state = 1


class Scene0:
    def __init__(self):
        self.script = textToScript("scripts/scene0.txt")
        self.line = 0
        self.cursor = 1

    def update(self, app):
        self.cursor += 1
        if pyxel.btnr(pyxel.KEY_ENTER):
            self.line += 1
            self.cursor = 1
        if self.line==len(self.script):
            app.state+=1

    def draw(self):
        drawTextBoard()

        if self.line<=len(self.script)-1:
            pyxel.text(25, 205, self.script[self.line][0], 7)
            pyxel.text(25, 215, self.script[self.line][1][:self.cursor], 7)

class Scene1:
    def __init__(self):
        pyxel.image(0).load(0, 32, "images/bugboy.png")
        pyxel.image(0).load(32, 32, "images/wing.png")
        pyxel.image(0).load(64,32,"images/bugboy_attacking.png")
        [pyxel.image(0).load(i*16, 64, "images/enemy"+str(i+1)+".png") for i in range(6)]
        self.script = textToScript("scripts/scene1.txt")
        self.line = 0
        self.cursor = 1
        self.bugboy=BugBoy()
        self.enemies=[Enemy() for i in range(4)]
        self.clouds = [Cloud(random.randint(10, 245),
                             random.randint(10, 245)) for x in range(10)]
        self.proceed=True
        self.choices=[]
        self.bullets=[]
        #check arrows
        self.up=False
        self.down=False
        self.right=False
        self.left=False
        self.choiceMade =False

    def update(self, app):
        self.cursor += 1
        if self.line==len(self.script)-1 and not self.choiceMade:
            self.proceed=False
            if self.choices==[]:
                self.choices=[ChoiceCloud(100,64,"Inspiring"),ChoiceCloud(110,144,"Relatable")]
                print(self.script[-1])
        if self.line==len(self.script)-1 and self.choiceMade:
            app.state+=1
        if pyxel.btnr(pyxel.KEY_ENTER) and self.proceed:
            self.line += 1
            self.cursor = 1
        #if self.line==len(self.script) and self.proceed:
        #    app.state+=1
        
        if self.line ==50:
            [enemy.setAttack(True) for enemy in self.enemies]
        
        [cloud.update() for cloud in self.clouds]
        [cloud.update() for cloud in self.choices]
        action= self.bugboy.update(self)
        if action:
            if action=="Inspiring":
                self.script+=textToScript("scripts/scene1a.txt")
                self.proceed=1
                self.choices=[]
                self.choiceMade=True
                self.line+=1
            if action=="Relatable":
                self.script+=textToScript("scripts/scene1b.txt")
                self.proceed=1
                self.choices=[]
                self.choiceMade=True
                self.line+=1

        if len(self.enemies)<2:
            self.enemies+=[Enemy() for i in range(3)]
            [enemy.setAttack(True) for enemy in self.enemies]
        [enemy.update(self) for enemy in self.enemies]
        [bullet.update() for bullet in self.bullets]

    def draw(self):
        if self.line>15:
            pyxel.cls(6)
            pyxel.text(3,3,"Lives: "+str(self.bugboy.life),0)

        if self.line<=15:
            pyxel.rect(32,32,192,150,15)
        if self.line>15:
            [cloud.draw() for cloud in self.clouds]
        if self.line>15:
            drawMountains()
        if self.line>13:
            self.bugboy.draw()
        if self.line>45:
            [enemy.draw() for enemy in self.enemies]
            [bullet.draw() for bullet in self.bullets]
        [cloud.draw() for cloud in self.choices]


        
        drawTextBoard()
        if self.line<=len(self.script)-1:
            pyxel.text(25, 205, self.script[self.line][0], 7)
            pyxel.text(25, 215, self.script[self.line][1][:self.cursor], 7)

class Thanks:
    def draw(self):
        pyxel.text(50,50,"Thank you for playing the Intro of\nJenna and Bug Boy\n in the big break :)",7)


        
class App:
    def __init__(self):
        pyxel.init(256, 256, caption="Jenna and bugboy", fps=60)
        self.loadImage()
        self.incipit = Incipit()
        self.scene0 = Scene0()
        self.menu = Menu()
        self.credits = Credits()
        self.scene1= Scene1()
        self.thanks=Thanks()
        self.state = 0 # [incipit,scene0,menu,credits,scene1]
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if self.state == 0:
            self.incipit.update(self)
        if self.state == 1:
            self.scene0.update(self)
        if self.state ==2:
            self.menu.update(self)
        if self.state==3:
            self.credits.update(self)
        if self.state==4:
            self.scene1.update(self)

    def draw(self):
        pyxel.cls(0)
        if self.state == 0:
            self.incipit.draw()
        if self.state == 1:
            self.scene0.draw()
        if self.state ==2:
            self.menu.draw()
        if self.state==3:
            self.credits.draw()
        if self.state == 4:
            self.scene1.draw()
        if self.state ==5:
            self.thanks.draw()

    def loadImage(self):
        pyxel.image(0).load(16, 0, f"logo.png")


App()
