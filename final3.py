import pyxel
import time

class Ball: #初期設定
    def __init__(self, score = None): 
        self.x = 150
        self.y = 0
        self.radius = 15
        self.game_over = False
        self.score = score
        self.set_color()
        self.creation_time = time.time()


    def set_color(self): #500超えたら３色
        if self.score is not None and self.score > 500: 
            self.color = pyxel.rndi(0,2)
        else:
            self.color = pyxel.rndi(0,1)

        if self.color == 0 or 1 or 2:
            angle = pyxel.rndi(30, 150)
            self.vx = pyxel.cos(angle)
            self.vy = pyxel.sin(angle)
        
    def move(self):
        self.x += self.vx
        self.y += self.vy
        #跳ね返り判定
        if self.y >= 205:  # 下
            angles = pyxel.rndi(30, 150)
            self.vy = -pyxel.sin(angles)
        elif self.y < 15:  # 上
            angles = pyxel.rndi(0, 180)
            self.vy = pyxel.sin(angles)
        elif self.x < 0:  # 左
            angles = pyxel.rndi(0, 180)
            self.vy = pyxel.sin(angles)
        elif self.y > 300:  # 右
            angles = pyxel.rndi(0, 180)
            self.vy = pyxel.sin(angles)
        elif self.x < 90:  # 左の横
            angles = pyxel.rndi(30, 150)
            self.vx = pyxel.cos(angles)
            self.vy = pyxel.sin(angles)
        elif (0 < self.x < 95 and self.y < 145):  # 左の下
            angles = pyxel.rndi(30, 150)
            self.vx = pyxel.cos(angles)
            self.vy = pyxel.sin(angles)
        elif 195 < self.x:  # 右の横
            angles = pyxel.rndi(30, 150)
            self.vx = pyxel.cos(angles)
            self.vy = pyxel.sin(angles)
        elif (190 < self.x < 300 and self.y < 145):  # 右の下
            angles = pyxel.rndi(30, 150)
            self.vx = pyxel.cos(angles)
            self.vy = pyxel.sin(angles)
        #当たり判定
        if (0 < self.x < 80 and 40 < self.y < 170)or\
            (210 < self.x <300 and 40 < self.y < 170)or\
            (60 < self.x < 240 and 220 < self.y <300):
            self.vx = 0
            self.vy = 0
            self.game_over = True

        elapsed_time = time.time() - self.creation_time #5秒経ったらオレンジ

        if elapsed_time > 5 and self.color == 0 and not self.vx == 0 and not self.vy == 0:
            if pyxel.frame_count % 10 == 0:
                self.color = 3  # オレンジ色
            else:
                self.color = 0 # オリジナルの色

        if elapsed_time > 5 and self.color == 1 and not self.vx == 0 and not self.vy == 0:
            if pyxel.frame_count % 10 == 0:
                self.color = 3  # オレンジ色
            else:
                self.color = 1 # オリジナルの色

        if elapsed_time > 5 and self.color == 2 and not self.vx == 0 and not self.vy == 0:
            if pyxel.frame_count % 10 == 0:
                self.color = 3  # オレンジ色
            else:
                self.color = 2 # オリジナルの色    


    def draw(self): #爆弾の色
        if self.color == 0:
            pyxel.blt(self.x, self.y, 0, 32, 0, 16, 16, 7) #黒   
        elif self.color == 1:
            pyxel.blt(self.x, self.y, 0, 16, 0, 16, 16, 7)  #赤
        elif self.color == 2:
            pyxel.blt(self.x, self.y, 0, 48, 0, 16, 16, 7)  #青
        if self.color == 3:
            pyxel.blt(self.x, self.y, 0, 48, 16, 16, 16, 7) #オレンジ
        if self.color == 4:
            pyxel.blt(self.x, self.y, 0, 32, 16, 16, 16, 0) #爆発


class App:
    def __init__(self):
        pyxel.init(300, 300)
        pyxel.load("sample-6.pyxres")
        pyxel.play(0,1,loop=True)
        self.score = 0
        self.moving_balls_count = 0
        self.reset_game()
        self.show_start_screen = True
        self.start_time = True
        
        pyxel.run(self.update, self.draw)

    def start_game(self): #スタート
        self.show_start_screen = False
        self.reset_game()

    def reset_game(self): #リセット
        self.balls = [Ball(self.score)]
        self.last_ball_time = time.time()
        self.current_ball = None
        self.dragging = False
        self.game_over = False
        self.score = 0
        pyxel.play(0,1,loop=True)

    def update(self): #時間計測
        current_time = time.time() 

        if self.show_start_screen:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.start_game()
            return


        if pyxel.btnp(pyxel.KEY_SPACE) and self.game_over: #リセット
            self.reset_game()
        if self.game_over:
            return
        
        self.score += 1 #スコア
        self.moving_balls_count = sum(1 for ball in self.balls if ball.vx or ball.vy)

        if current_time - self.last_ball_time > 0.7: #新しいボール
            self.balls.append(Ball(self.score))
            self.last_ball_time = current_time

        mx, my = pyxel.mouse_x, pyxel.mouse_y #ドラッグ&ドロップ
        
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.select_ball(mx, my)
        elif pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            self.release_ball()
        if self.dragging and self.current_ball:
            self.current_ball.x = mx
            self.current_ball.y = my

        for ball in self.balls: #爆弾動く
            ball.move()
            
        for ball in self.balls: #ゲームオーバー判定
            if (
                (0 < ball.x < 80 and 40 < ball.y < 170 and ball.color != 1 ) or
                (220 < ball.x < 300 and 40 < ball.y < 170 and ball.color != 0 ) or
                (60 < ball.x < 240 and 220 < ball.y < 300 and ball.color != 2 )
            ):
                self.game_over = True

                for ball in self.balls:
                    ball.vx = 0
                    ball.vy = 0
                    if not  (mx >= ball.x - ball.radius and
                            mx <= ball.x + ball.radius and 
                            my >= ball.y - ball.radius and 
                            my <= ball.y + ball.radius):
                        ball.color = 4                        
                        pyxel.play(0,0)
                break

        # 動いているボールが30個を超えたらゲームオーバー
        moving_balls_count = sum(1 for ball in self.balls if abs(ball.vx) > 0 or abs(ball.vy) > 0)
        if moving_balls_count > 30:
            for ball in self.balls:
                if abs(ball.vx) > 0 or abs(ball.vy) > 0:
                    ball.color = 4  # オレンジ(9)に変更
                    pyxel.play(0,0)
                    self.game_over = True



    def draw(self):
        if self.show_start_screen:
            # スタート画面を描画
            pyxel.cls(0)
            pyxel.blt(40,35,0,16,0,16,16,7)
            pyxel.blt(60,25,0,16,0,16,16,7)
            pyxel.blt(90,35,0,48,0,16,16,7)
            pyxel.blt(120,35,0,48,16,16,16,7)
            pyxel.blt(160,30,0,16,16,16,16,7)
            pyxel.blt(170,50,0,16,16,16,16,7)
            pyxel.text(177,40,"3333",13)
            pyxel.text(187,60,"3333",13)
            pyxel.text(60, 80, "THE  B O M B S  E M E R G E N C Y", 9)
            pyxel.text(60, 100, "-- HOW TO PLAY THIS GAME -- ", 7)
            pyxel.text(60, 120, "1. PUT BOMBS INTO THE SAME COLOR ZONE.", 7)
            pyxel.text(60, 140, "2. AFTER A SPECIFIC TIME, EACH BOMB TURNS ORANGE, ", 7)
            pyxel.text(60, 160, "   AND YOU CAN'T PUT ORANGE BOMBS INTO ANY ZONE.", 7)
            pyxel.text(60, 180, "3. IF THERE ARE 30 BOMBS ON THE FLOOR,", 7)
            pyxel.text(60, 200, "   OR IF YOU PUT ONE BOMB INTO A DIFFERENT COLOR ZONE,", 7)
            pyxel.text(60, 220, "   THE GAME IS OVER!!", 7)
            pyxel.text(80, 250, "    PRESS SPACE TO START    ", 7)
            return
        #背景
        for xi in range(0, 300, 16): 
            for yi in range(0, 300, 16):
                pyxel.blt(xi,yi,0,0,0,16,16,)


        pyxel.rect(70,120, 50,80, 13)
        pyxel.text(115,122,"o",0)
        pyxel.text(115,192,"o",0)
        pyxel.text(72,192,"o",0)
        pyxel.line(70,120, 120,120, 7)
        pyxel.line(120,120, 120,200, 7)

        pyxel.rect(140,60, 65,20, 13)
        pyxel.text(142,62,"+",0)
        pyxel.text(142,75,"+",0)
        pyxel.text(199,62,"+",0)
        pyxel.text(199,75,"+",0)
        pyxel.line(140,60, 205,60, 7)
        pyxel.line(205,60, 205,80, 7)

        pyxel.rect(0,240, 40,50, 13)
        pyxel.text(35,242,"+",0)
        pyxel.text(35,284,"+",0)
        pyxel.line(0,240, 40,240, 7)
        pyxel.line(40,240, 40,290, 7)

        pyxel.rect(220,200, 75,40, 13)
        pyxel.text(222,202,"o",0)
        pyxel.text(290,202,"o",0)
        pyxel.text(290,234,"o",0)
        pyxel.line(220,200, 295,200, 7)
        pyxel.line(295,200, 295,240, 7)

        #赤のエリア
        for xi in range(0, 90, 15):
            for yi in range(20, 170, 15):
                pyxel.blt(xi,yi,0, 0,32, 15,15)
        #赤のエリアの枠線
        pyxel.rect(0,20, 10,150, 10)
        pyxel.rect(0,20, 90,10, 10)
        pyxel.rect(80,20, 10,150, 10)
        pyxel.rect(0,170, 90,10, 10)

        #黒のエリア
        for xi in range(210, 300, 15):
            for yi in range(20, 170, 15):
                pyxel.blt(xi,yi,0, 16,32, 15,15)
        #黒のエリアの枠線
        pyxel.rect(290,20, 10,150, 10)
        pyxel.rect(210,20, 90,10, 10)
        pyxel.rect(210,20, 10,150, 10)
        pyxel.rect(210,170, 90,10, 10)

        #青のエリアの下書き
        pyxel.rect(60,230, 180,60, 6)
        pyxel.line(60,230,240,230,7)
        pyxel.line(240,230,240,290,7)
        pyxel.text(63,233,"@",0)
        pyxel.text(63,283,"@",0)
        pyxel.text(233,233,"@",0)
        pyxel.text(233,283,"@",0)
        #爆弾の入り口
        for xi in range(120,170,15):
            for yi in range(0,15,15):
                pyxel.blt(xi,yi, 0,48,32,15,15)
        pyxel.rect(185,0,120,15,11)
        pyxel.blt(120,0,0,0,48,16,16,7)
        pyxel.blt(170,0,0,16,48,16,16,7)
        pyxel.text(190,5,"<<<",0)
        pyxel.text(285,5,"<<<",0)
        pyxel.blt(205,0,0,16,0,15,15,7)
        pyxel.blt(225,0,0,32,0,15,15,7)
        pyxel.blt(245,0,0,16,0,15,15,7)
        pyxel.blt(265,0,0,32,0,15,15,7)
        pyxel.rect(186,13,120,2,0)
        pyxel.line(186,15,300,15,3)
        pyxel.rect(40,0,80,15,11)
        pyxel.line(45,15,120,15,3)
        pyxel.text(85,5,">>     >",0)
        for xi in range(65,120,30):
            for yi in range(0,14,14):
                pyxel.blt(xi,yi, 0,48,48,16,16,7)
        
        if self.score > 500:
            #青のエリア
            pyxel.rect(50, 220, 200, 180, 6)
            for xi in range(50, 240, 15):
                for yi in range(220, 300, 15):
                    pyxel.blt(xi,yi,0, 32,32, 15,15)
            #青のエリアの枠線
            pyxel.rect(50,220, 200,10, 10)
            pyxel.rect(50,220, 10,80, 10)
            pyxel.rect(240,220, 10,100, 10 )
            pyxel.rect(50,290, 200,10,10)

        pyxel.blt(pyxel.mouse_x,pyxel.mouse_y, 0,16,16,16,16,7)
        
        pyxel.rect(0,0, 45,10,0)
        pyxel.text(2, 2, "SCORE:"+str(self.score), 7)
        pyxel.rect(0,10, 63,10,0)
        pyxel.text(2, 12, "MOVING BOMBS:"+str(self.moving_balls_count), 7)


        for ball in self.balls:
            ball.draw()
        if self.game_over:
            pyxel.rect(108,118,91,19,0)
            pyxel.text(110, 120, "  G A M E  O V E R !  ", 7)
            pyxel.text(110, 130, "PRESS SPACE TO RESTART", 7)
        
        

        

    def select_ball(self, mx, my):
        for ball in self.balls: #ドラッグ
            if (
                mx >= ball.x - ball.radius
                and mx <= ball.x + ball.radius
                and my >= ball.y - ball.radius
                and my <= ball.y + ball.radius
            ):
                self.current_ball = ball
                self.dragging = True
                break

    def release_ball(self): #ドロップ
        self.dragging = False
        self.current_ball = None

    
App()
