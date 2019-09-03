#Game of Pong, has 4 options, either easy or hard mode, and either curved paddles or flat paddles
#Uses graphics modules by Zelle, slightly modified to better suit this program
#By Jack Heinzel and Alvin Bierley

from modifiedgraphics import *
from time import sleep
import random


#defines a class Paddle
class Paddle:
    def __init__(self, position, size, side, window):
        """Initiates the class, which is a rectangle that can be controlled by the user or by AI"""
        self.position = position
        self.side = side
        self.size = size
        self.paddle = Rectangle(Point(945*side + 30, position - size), Point(945*side + 25, position + size))
        self.paddle.setFill("white")
        self.paddle.draw(window)
        self.window = window
    def getSize(self):
        """returns the size of the paddle"""
        return self.size
    def getPosition(self):
        """returns the upper and lower bounds of the paddle in a list"""
        return [self.position + self.size, self.position - self.size]
    def getCenter(self):
        """returns the center location for the paddle"""
        return self.position
    def reset(self, position):
        """resets the paddles to their original positions"""
        self.paddle.undraw()
        self.position = position
        self.paddle = Rectangle(Point(945*self.side + 30, position - self.size), Point(945*self.side + 25, position + self.size))
        self.paddle.setFill("white")
        self.paddle.draw(self.window)
    def control(self, up, down):
        """controls the paddle, moving it at a speed of +/- 15"""
        #moves the paddle down
        if self.window.checkKey() == up and self.getPosition()[1] > -15:
            self.paddle.move(0,-15)
            self.position += -15
        #moves the paddle up
        elif self.window.checkKey() == down and self.getPosition()[0] < 815:
            self.paddle.move(0,15)
            self.position += 15

        #Moves the paddle always, because moving is computationally slow, and without it, the program would run at inconsistent speeds
        else:
            self.paddle.move(0,0)
    def HardAI(self, ball, speedYInit):
        """an AI that has a smaller error"""
        ballSpeed = ball.getSpeed()[1]
        ballY = ball.getY()
        #defines an error that will make the AI possible to beat, and scales with the vertical speed of the ball
        if abs(ballSpeed) <= abs(speedYInit):
            Error = 0
        else:
            Error = random.randint(-abs(ballSpeed)//20 + 1,abs(ballSpeed)//20)
        self.paddle.move(0, ballSpeed+3*Error)
        self.position += ballSpeed+3*Error
        #resets the paddle if a point has been scored
        if ball.check():
            self.position = 400
            self.paddle.undraw()
            self.paddle = Rectangle(Point(975, self.position - self.size), Point(970, self.position + self.size))
            self.paddle.setFill("white")
            self.paddle.draw(self.window)
    def EasyAI(self, ball, speedYInit):
        """an AI with a larger error"""
        ballSpeed = ball.getSpeed()[1]
        ballY = ball.getY()
        #defines an error that makes the AI possible to beat, and one that scales with the speed of the ball
        if abs(ballSpeed) <= abs(speedYInit):
            Error = 0
        else:
            Error = random.randint(-(ballSpeed**2)//(30) + 1,(ballSpeed**2)//(30))
        self.paddle.move(0, ballSpeed+2*Error)
        self.position += ballSpeed+2*Error
        #resets the paddle if a point has been scored
        if ball.check():
            self.position = 400
            self.paddle.undraw()
            self.paddle = Rectangle(Point(975, self.position - self.size), Point(970, self.position + self.size))
            self.paddle.setFill("white")
            self.paddle.draw(self.window)
    def UnDraw(self):
        """undraws the paddle"""
        self.paddle.undraw()
class ball:
    def __init__(self, speed, window):
        """initiates a sphere with a speed and a location, which can be rebounded if it hits a paddle. Also in this class are the scores of both players"""
        self.location = [500,400]
        self.speed = speed
        self.ball = Circle(Point(self.location[0],self.location[1]), 5)
        self.ball.setFill("white")
        self.ball.draw(window)
        self.window = window
        self.checker = False
        self.score_0 = 0
        self.score_1 = 0
        self.score_0_Text = Text(Point(150, 50), "Player 1 score: " + str(self.score_0))
        self.score_0_Text.setSize(25)
        self.score_0_Text.draw(window)
        self.score_1_Text = Text(Point(850, 50), "Player 2 score: " + str(self.score_1))
        self.score_1_Text.setSize(25)
        self.score_1_Text.draw(window)
        self.rallyCount = 1
    def getSpeed(self):
        """returns the speed"""
        return self.speed
    def speedUp(self):
        """speeds up the ball by 1.5"""
        self.speed[0] *= 1.5
        self.speed[1] *= 1.5
    def rallyCurved(self, Paddle1, Paddle2):
        """describes the movement of the ball if the player selected to use curved paddles"""
        self.ball.move(self.speed[0],self.speed[1])
        self.location[0] += self.speed[0]
        self.location[1] += self.speed[1]
        #Rebounds the ball, changing the speed based on where the ball hits the paddle
        if self.location[0] <= 30 - self.speed[0]:
            if self.location[1] >= Paddle1.getPosition()[1]+self.speed[1] and self.location[1] <= Paddle1.getPosition()[0]+self.speed[1]:
                theta = (self.location[1] - Paddle1.getCenter())/(3*Paddle1.getSize())
                cosTheta = 1 - (theta**2)/2
                sinTheta = theta
                self.speed = [-1*(2*self.speed[0]*cosTheta**2 + 2*self.speed[1]*cosTheta*sinTheta - self.speed[0]),-1*(2*self.speed[0]*cosTheta*sinTheta + 2*self.speed[1]*sinTheta**2 - self.speed[1])]
                self.rallyCount += 1
                #speed up the ball if it has rebounded 3 times
                if self.rallyCount%4 == 0:
                    self.speedUp()
                    self.rallyCount = 1
        #Rebounds the ball, changing the speed based on where the ball hits the paddle
        if self.location[0] >= 970 - self.speed[0]:
            if self.location[1] >= Paddle2.getPosition()[1]+self.speed[1] and self.location[1] <= Paddle2.getPosition()[0]+self.speed[1]:
                theta = (self.location[1] - Paddle2.getCenter())/(3*Paddle2.getSize())
                cosTheta = 1 - (theta**2)/2
                sinTheta = theta
                self.speed = [-1*(2*self.speed[0]*cosTheta**2 + 2*self.speed[1]*cosTheta*sinTheta - self.speed[0]),-1*(2*self.speed[0]*cosTheta*sinTheta + 2*self.speed[1]*sinTheta**2 - self.speed[1])]
                self.rallyCount += 1
                #speeds up the ball if it has rebounded 3 times
                if self.rallyCount%4 == 0:
                    self.speedUp()
                    self.rallyCount = 1
        #bounces the ball if it hits the top or bottom of the screen
        if self.location[1] > 800 or self.location[1] < 0:
            self.speed[1] *= -1
    def rallyFlat(self, Paddle1, Paddle2):
        """defines the motion of a ball if the player selected to use flat paddles"""
        self.ball.move(self.speed[0],self.speed[1])
        self.location[0] += self.speed[0]
        self.location[1] += self.speed[1]
        #rebounds off the paddle
        if self.location[0] <= 30 - self.speed[0]:
            if self.location[1] >= Paddle1.getPosition()[1] and self.location[1] <= Paddle1.getPosition()[0]:
                self.speed[0] *= -1
                self.rallyCount += 1
                #speeds up the ball if it has rebounded 3 times
                if self.rallyCount%4 == 0:
                    self.speedUp()
                    self.rallyCount = 1
        #rebounds off the paddle
        if self.location[0] >= 970 - self.speed[0]:
            if self.location[1] >= Paddle2.getPosition()[1] and self.location[1] <= Paddle2.getPosition()[0]:
                self.speed[0] *= -1
                self.rallyCount += 1
                #speeds up the ball if it has rebounded 3 times
                if self.rallyCount%4 == 0:
                    self.speedUp()
                    self.rallyCount = 1
        #bounces the ball off the top or bottom
        if self.location[1] > 800 or self.location[1] < 0:
            self.speed[1] *= -1
    def getX(self):
        """returns the x position"""
        return self.location[0]
    def getY(self):
        """returns the y position"""
        return self.location[1]
    def boardReset(self, speedX, speedY):
        """resets the board, resets the speed to speeds input"""
        self.location = [500,400]
        self.ball.undraw()
        self.ball = Circle(Point(self.location[0],self.location[1]), 5)
        self.ball.setFill("white")
        self.ball.draw(self.window)
        self.speed[0] = speedX
        self.speed[1] = speedY
    def check(self):
        """checks if the ball has gone off either end of the board, if it has, it updates the scores, and returns True"""
        #checks if it runs off either end
        if self.location[0] > 970:
            self.score_0_Text.undraw()
            self.score_0 += 1
            self.score_0_Text = Text(Point(150, 50), "Player 1 score: " + str(self.score_0))
            self.score_0_Text.setSize(25)
            self.score_0_Text.draw(self.window)
            self.checker = True
        if self.location[0] < 30:
            self.score_1_Text.undraw()
            self.score_1 += 1
            self.score_1_Text = Text(Point(850, 50), "Player 2 score: " + str(self.score_1))
            self.score_1_Text.setSize(25)
            self.score_1_Text.draw(self.window)
            self.checker = True
        #if it has, it creates a message for the user to continue once they click, and resets the rally count
        if self.checker:
            for i in range(10):
                self.ball.move(self.speed[0],self.speed[1])
                sleep(.04)
            clickMessage = Text(Point(500,400),"Click to continue")
            clickMessage.setSize(50)
            clickMessage.draw(self.window)
            self.window.getMouse()
            clickMessage.undraw()
            self.checker = False
            self.rallyCount = 1
            return True
    def getScores(self):
        """returns the scores"""
        return self.score_0, self.score_1
    def UnDraw(self):
        """undraws all the drawn items in the class"""
        self.ball.undraw()
        self.score_0_Text.undraw()
        self.score_1_Text.undraw()
def infoScreen(window):
    """a function to describe how the game works"""
    pong = Text(Point(500,120),"PONG")
    pong.setSize(70)
    pong.draw(window)
    flat = Text(Point(250, 300), "Flat Paddle:")
    flat.setSize(40)
    flat.draw(window)
    curve = Text(Point(750, 300), "Curved Paddle:")
    curve.setSize(40)
    curve.draw(window)
    flatDesc = Text(Point(250, 375), "Reflects off at a straight angle")
    curveDesc = Text(Point(750,375), "Reflects off at a changing angle")
    flatDesc.setSize(20)
    curveDesc.setSize(20)
    flatDesc.draw(window)
    curveDesc.draw(window)
    speedDesc = Text(Point(500, 220), "Ball speeds up every 3 rebounds")
    speedDesc.setSize(30)
    speedDesc.draw(window)
    flatPaddle = Rectangle(Point(150, 450), Point(200, 700))
    flatPaddle.draw(window)
    curvePaddle = Rectangle(Point(650, 450), Point(700, 700))
    curvePaddle.draw(window)
    x = -1
    #creates an animation of sorts to show how balls of certain incident angles reflect off the paddles in either mode
    while x == -1:
        for i in range(6):
            LineI = Line(Point(200,650-30*i), Point(350, 700-30*i))
            LineI.draw(window)
            LineCI = Line(Point(700,650-30*i),Point(850, 650-30*i))
            LineCI.draw(window)
            sleep(1)
            LineF = Line(Point(200,650-30*i), Point(350, 600-30*i))
            LineF.draw(window)
            LineCF = Line(Point(700,650-30*i),Point(850, 700-50*i))
            LineCF.draw(window)
            sleep(1)
            LineI.undraw()
            LineF.undraw()
            LineCI.undraw()
            LineCF.undraw()
            y = window.checkMouse()
            try:
                x = y.getX()
                break
            except:
                pass
    #undraws everything
    pong.undraw()
    flat.undraw()
    curve.undraw()
    speedDesc.undraw()
    flatPaddle.undraw()
    curvePaddle.undraw()
    flatDesc.undraw()
    curveDesc.undraw()
def startScreen(window):
    """creates a selection screen for easy or hard"""
    easy = Rectangle(Point(200,50),Point(800,350))
    hard = Rectangle(Point(200,450),Point(800,750))
    easy.draw(window)
    hard.draw(window)
    easyText = Text(Point(500,200), "EASY MODE")
    easyText.setSize(50)
    hardText = Text(Point(500,600), "HARD MODE")
    hardText.setSize(50)
    easyText.draw(window)
    hardText.draw(window)
    pX = 0
    pY = 0
    while not (200 < pX < 800 and (50 < pY < 350 or 450 < pY < 750)):
        p = window.getMouse()
        pX = p.getX()
        pY = p.getY()
    easy.undraw()
    hard.undraw()
    easyText.undraw()
    hardText.undraw()
    return pY

def curveOrFlatScreen(window):
    """creates a selection screen to select curved or flat paddles"""
    flat = Rectangle(Point(200,50),Point(800,350))
    curve = Rectangle(Point(200,450),Point(800,750))
    flat.draw(window)
    curve.draw(window)
    flatText = Text(Point(500,200), "FLAT PADDLES")
    flatText.setSize(50)
    curveText = Text(Point(500,600), "CURVED PADDLES")
    curveText.setSize(50)
    flatText.draw(window)
    curveText.draw(window)
    p2X = 0
    p2Y = 0
    while not (200 < p2X < 800 and (50 < p2Y < 350 or 450 < p2Y < 750)):
        p2 = window.getMouse()
        p2X = p2.getX()
        p2Y = p2.getY()
    flat.undraw()
    curve.undraw()
    flatText.undraw()
    curveText.undraw()
    return p2Y
def controls(window):
    """creates a screen displaying the controls"""
    arrowkeys = Text(Point(500,150), "Controls: Arrow Keys")
    arrowkeys.setSize(50)
    up = Rectangle(Point(470,300), Point(530,360))
    down = Rectangle(Point(470,370),Point(530,430))
    arrowkeys.draw(window)
    up.draw(window)
    down.draw(window)
    sideArrow = Rectangle(Point(540,370),Point(600,430))
    sideArrow.draw(window)
    upText = Text(Point(500,330), "UP")
    downText = Text(Point(500,400), "DOWN")
    sideText = Text(Point(570,400), "RIGHT")
    upText.setSize(15)
    downText.setSize(15)
    sideText.setSize(15)
    upText.draw(window)
    downText.draw(window)
    sideText.draw(window)
    upControl = Text(Point(500, 500), "UP: moves paddle up")
    downControl = Text(Point(500, 540), "DOWN: moves paddle down")
    sideControl = Text(Point(500, 580), "SIDE: stops paddle motion")
    upControl.setSize(15)
    downControl.setSize(15)
    sideControl.setSize(15)
    upControl.draw(window)
    downControl.draw(window)
    sideControl.draw(window)
    #waits for click
    window.getMouse()
    arrowkeys.undraw()
    up.undraw()
    down.undraw()
    sideArrow.undraw()
    upText.undraw()
    downText.undraw()
    sideText.undraw()
    upControl.undraw()
    downControl.undraw()
    sideControl.undraw()
def main():
    #creates a loop for continuous play, if desired
    play = True
    while play:
        winOrig = GraphWin("Pong",1000,800)
        #creates a background with a random color
        winOrig.setBackground(color_rgb(10*random.randint(8,16),10*random.randint(8,16),10*random.randint(8,16)))
        controls(winOrig)
        infoScreen(winOrig)
        pY = startScreen(winOrig)
        p2Y = curveOrFlatScreen(winOrig)
        #draws a dividing line
        divide = Line(Point(500,0),Point(500,800))
        divide.draw(winOrig)
        #creates an initial speed for the ball, which is more or less random
        if random.randint(0,1) == 0:
            speedInitX = -1*random.randint(12,16)
        else:
            speedInitX = random.randint(12,16)
        if random.randint(0,1) == 0:
            speedInitY = -1*random.randint(10,15)
        else:
            speedInitY = random.randint(10,15)
        pongBall = ball([speedInitX,speedInitY],winOrig)
        paddle1 = Paddle(400, 80, 0, winOrig)
        paddle2 = Paddle(400, 80, 1, winOrig)
        score0 = 0
        score1 = 0
        #defines a number that will end the game if either player reaches it
        end = 2
        #creates a loop based on what the player chose to play as
        if p2Y < 400:
            if pY < 400:
                while score0 != end and score1 != end:
                    paddle1.control("Up", "Down")
                    paddle2.EasyAI(pongBall,speedInitY)
                    pongBall.rallyFlat(paddle1, paddle2)
                    X = pongBall.check()
                    if pongBall.getX() < 30 or pongBall.getX() > 970:
                        paddle2.reset(400)
                        paddle1.reset(400)
                        if X:
                            pongBall.boardReset(speedInitX, speedInitY)
                        sleep(3)
                        score0, score1 = pongBall.getScores()
            else:
                while score0 != end and score1 != end:
                    paddle1.control("Up", "Down")
                    paddle2.HardAI(pongBall,speedInitY)
                    pongBall.rallyFlat(paddle1, paddle2)
                    X = pongBall.check()
                    if pongBall.getX() < 30 or pongBall.getX() > 970:
                        paddle2.reset(400)
                        paddle1.reset(400)
                    if X:
                        pongBall.boardReset(speedInitX, speedInitY)
                        sleep(3)
                        score0, score1 = pongBall.getScores()
        else:
            if pY < 400:
                while score0 != end and score1 != end:
                    paddle1.control("Up", "Down")
                    paddle2.EasyAI(pongBall,speedInitY)
                    pongBall.rallyCurved(paddle1, paddle2)
                    X = pongBall.check()
                    if pongBall.getX() < 30 or pongBall.getX() > 970:
                        paddle2.reset(400)
                        paddle1.reset(400)
                    if X:
                        pongBall.boardReset(speedInitX, speedInitY)
                        sleep(3)
                        score0, score1 = pongBall.getScores()
            else:
                while score0 != end and score1 != end:
                    paddle1.control("Up", "Down")
                    paddle2.HardAI(pongBall,speedInitY)
                    pongBall.rallyCurved(paddle1, paddle2)
                    X = pongBall.check()
                    if pongBall.getX() < 30 or pongBall.getX() > 970:
                        paddle2.reset(400)
                        paddle1.reset(400)
                    if X:
                        pongBall.boardReset(speedInitX, speedInitY)
                        sleep(3)
                        score0, score1 = pongBall.getScores()
        #undraws everything, after the game is over
        paddle1.UnDraw()
        paddle2.UnDraw()
        pongBall.UnDraw()
        divide.undraw()
        #builds a screen telling the player congrats if they won, or condolences if they lost
        if score0 == end:
            congrats = Text(Point(500,300),"CONGRATULATIONS!")
        else:
            congrats = Text(Point(500,300),"Better luck next time...")
        congrats.setSize(80)
        congrats.draw(winOrig)
        #builds a screen asking if they want to play again
        playagain = Text(Point(500, 500), "Play again?")
        playagain.setSize(40)
        playagain.draw(winOrig)
        yes = Text(Point(250, 650), "Yes!")
        yes.setSize(30)
        no = Text(Point(750, 650), "No")
        no.setSize(30)
        yes.draw(winOrig)
        no.draw(winOrig)
        yesRect = Rectangle(Point(200,600),Point(300,700))
        noRect = Rectangle(Point(700,600),Point(800,700))
        yesRect.draw(winOrig)
        noRect.draw(winOrig)
        x = -1
        y = -1
        #if they select they want to play again, then the window closes, and the program runs again. If not, the window closes and the program completes.
        while not ((200 < x < 300 or 700 < x < 800) and 600 < y < 700):
            p = winOrig.getMouse()
            x = p.getX()
            y = p.getY()
        if x > 500:
            play = False
        winOrig.close()

if __name__ == "__main__":
    main()
