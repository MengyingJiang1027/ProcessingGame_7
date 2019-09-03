from random import choice

class Fish():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.facing = UP
        self.moving = UP
        self.vx = 0
        self.vy = -2
        self.img = img

    def display(self):
        image(self.img, self.x, self.y, self.img.width * 0.2, self.img.height * 0.2)

    def update(self):
        if self.moving == UP:
            self.vx = 0
            self.vy = -2
        if self.moving == DOWN:
            self.vx = 0
            self.vy = 2
        if self.moving == LEFT:
            self.vx = -2
            self.vy = 0
        if self.moving == RIGHT:
            self.vx = 2
            self.vy = 0
            
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        
        if self.x > 950:
            self.x = 0
        if self.x < 0:
            self.x = 950
        if self.y > 640:
            self.y = 150
        if self.y < 150:
            self.y = 640

    def run(self):
        self.display()
        self.update()

    # 设置鱼的朝向
    def setFacing(self, facing):
        self.facing = facing

    # 设置鱼的移动方向
    def setMoving(self, moving):
        self.moving = moving

class FishSystem():
    def __init__(self):
        self.row = 6
        self.col = 6
        
        self.upImages = []
        self.downImages = []
        self.leftImages = []
        self.rightImages = []
        for i in range(1, 7):
            upImage = loadImage("fish" + str(i) + "up.png")
            downImage = loadImage("fish" + str(i) + "down.png")
            leftImage = loadImage("fish" + str(i) + "left.png")
            rightImage = loadImage("fish" + str(i) + "right.png")
            self.upImages.append(upImage)
            self.downImages.append(downImage)
            self.leftImages.append(leftImage)
            self.rightImages.append(rightImage)
        
        self.fishes = []

        for row in range(1, self.row + 1):
            rowFish = []
            for col in range(1, self.col + 1):
                fish = Fish((col - 1) * 60, (row - 1) * 60 + 150, choice(self.upImages))                
                rowFish.append(fish)
            self.fishes.append(rowFish)


    def run(self):
        for rowFish in self.fishes:
            for fish in rowFish:
                fish.run()

    def setFacing(self, facing):
        for rowFish in self.fishes:
            for fish in rowFish:
                fish.setFacing(facing)
                
                if fish.facing == UP:
                    fish.img = choice(self.upImages)
                if fish.facing == DOWN:
                    fish.img = choice(self.downImages)
                if fish.facing == LEFT:
                    fish.img = choice(self.leftImages)
                if fish.facing == RIGHT:
                    fish.img = choice(self.rightImages)
   
    def setMoving(self, moving):
        for rowFish in self.fishes:
            for fish in rowFish:
                fish.setMoving(moving)

class Game():
    def __init__(self):
        self.bg = loadImage("background.png")
        self.directions = [UP, DOWN, LEFT, RIGHT]
        self.facing = choice(self.directions)
        self.moving = choice(self.directions)
        self.tips = ["facing","moving"]
        self.gameTip = choice(self.tips)
        self.score = 0
        
        self.images = []
        self.images.append(loadImage("preparing.png"))
        self.images.append(loadImage("playing.png"))
        self.images.append(loadImage("failed.png"))
        self.images.append(loadImage("levelup.png"))
        self.images.append(loadImage("success.png"))
        self.images.append(loadImage("score_alpha.png"))
        self.images.append(loadImage("score.png"))
        
        self.level = 1
        self.startTime = 0
        self.state = "preparing"
        self.fishes = FishSystem()
        self.fishes.setFacing(self.facing)
        self.fishes.setMoving(self.moving)
        
    def check(self):
        if self.gameTip == "facing":
            if self.facing == keyCode:
                self.score = self.score + 1
            else:
                self.score = self.score - 1
                if self.score < 0:
                    self.score = 0
        if self.gameTip == "moving":
            if self.moving == keyCode:
                self.score = self.score + 1
            else:
                self.score = self.score - 1
                if self.score < 0:
                    self.score = 0
                
    def update(self):
        self.gameTip = choice(self.tips)
        self.facing = choice(self.directions)
        self.moving = choice(self.directions)
        
    def display(self):
        if self.state == "preparing":
            bg = self.images[0]
            image(bg, 0, 0)
            
        if self.state == "playing":
            bg = self.images[1]
            image(bg, 0, 0)
            

            for i in range(3 + self.level):
                image(self.images[5], 800 - self.images[5].width * i, 50)
                
    
            for i in range(self.score):
                image(self.images[6], 800 - self.images[6].width * i, 50)
                
          
            noStroke()

            fill(50, 210, 252)
            ellipse(880, 80, 60, 60)
            
        
            fill(255, 95, 160)
            angle = map((21 - self.level) * 1000 -  (millis() - self.startTime), (21 - self.level) * 1000, 0, 0, 360)
            arc(880, 80, 60, 60, radians(-90), radians(-90 + angle))
            
     
            if (21 - self.level) * 1000 -  (millis() - self.startTime) >= 0:
                if self.score >= (3 + self.level):
                    if self.level == 8:
                        self.state = "success"
                    else:
                        self.state = "levelup" 
                        self.startTime = millis()
            else:
                self.state = "failed"                    
        
        # image(self.bg, 0, 0, self.bg.width * 0.5, self.bg.height * 0.5)
    
            self.fishes.run()
            
            fill(0)
            text(self.gameTip, 50, 50)
            # text(self.score, 900, 50)
            
        if self.state == "failed":
            bg = self.images[2]
            image(bg, 0, 0)
            
        if self.state == "levelup":
            if millis() - self.startTime < 3000:
                bg = self.images[3]
                image(bg, 0, 0)

            else:
                self.state = "playing"
                self.score = 0
                self.level += 1
                self.startTime = millis()
            
        if self.state == "success":
            bg = self.images[4]
            image(bg, 0, 0)
            
    def onkeypress(self):
        if self.state == "preparing":
            if key == "s":
                self.state = "playing"
                self.startTime = millis()
                
        if self.state == "playing":
        
            if keyCode in [UP, DOWN, LEFT, RIGHT]:
        
                self.check()
                        
            
                self.update()
                self.fishes.setFacing(self.facing)
                self.fishes.setMoving(self.moving)
                
        if self.state == "failed":
            if key == "s":
                self.state = "playing"
                self.startTime = millis()
                self.score = 0
                
        if self.state == "success":
            if key == "s":
                self.state = "preparing"
                self.score = 0
                self.level = 1

    
def setup():
    global game
    
    game = Game()
    
    textFont(createFont("kaiti", 30))
    
    size(950, 640)

def draw():
    global game
    game.display()

def keyPressed():
    global game
    game.onkeypress()
