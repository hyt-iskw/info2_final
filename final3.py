import pyxel
import time


class Ball:
    def __init__(self):
        self.x = 150
        self.y = 0
        self.radius = 10
        self.color = pyxel.rndi(0, 1)
        angle = pyxel.rndi(30, 150)
        self.vx = pyxel.cos(angle)
        self.vy = pyxel.sin(angle)

    def move(self):
        self.x += self.vx
        self.y += self.vy

        if self.y >= 240:  # 下
            angles = pyxel.rndi(30, 150)
            self.vy = -pyxel.sin(angles)
        elif self.y < 0:  # 上
            angles = pyxel.rndi(0, 180)
            self.vy = pyxel.sin(angles)
        elif self.x < 100:  # 左の横
            angles = pyxel.rndi(30, 150)
            self.vx = pyxel.cos(angles)
            self.vy = pyxel.sin(angles)
        elif (0 < self.x < 100 and self.y < 150):  # 左の下
            angles = pyxel.rndi(30, 150)
            self.vx = pyxel.cos(angles)
            self.vy = pyxel.sin(angles)
        elif 200 < self.x:  # 右の横
            angles = pyxel.rndi(30, 150)
            self.vx = pyxel.cos(angles)
            self.vy = pyxel.sin(angles)
        elif (200 < self.x < 300 and self.y < 150):  # 右の下
            angles = pyxel.rndi(30, 150)
            self.vx = pyxel.cos(angles)
            self.vy = pyxel.sin(angles)



    def draw(self):
        if self.color == 0:
            pyxel.circ(self.x, self.y, self.radius, 0)  # 0→黒(10）
        elif self.color == 1:
            pyxel.circ(self.x, self.y, self.radius, 8)  # 1→赤（８）


class App:
    def __init__(self):
        pyxel.init(300, 250)
        self.balls = [Ball()]
        self.last_ball_time = time.time()
        self.selected_ball = None  # Variable to store the selected ball
        pyxel.run(self.update, self.draw)

    def update(self):
        current_time = time.time()
        if current_time - self.last_ball_time > 3:
            self.balls.append(Ball())
            self.last_ball_time = current_time


        for ball in self.balls:
            ball.move()

    
    def draw(self):
        pyxel.cls(7)

        pyxel.rect(0, 50, 90, 150, 14)
        pyxel.rect(210, 50, 300, 150, 13)

        pyxel.line(130, 0, 130, 10, 0)
        pyxel.line(130, 10, 170, 10, 0)
        pyxel.line(170, 10, 170, 0, 0)

        pyxel.mouse(True)

        
        

        for ball in self.balls:
            ball.draw()

App()
