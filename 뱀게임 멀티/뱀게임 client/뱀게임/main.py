import pygame
from pygame.locals import *
import time
import random
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from os import startfile
import sys
from socket import *

class data_socket_client:
    clientSock = socket(AF_INET, SOCK_STREAM)
    clientSock.connect(('25.29.175.241', 8080))
    print('연결에 성공했습니다.')

    def output(self, q):
        a = q
        
        b = ''
        data = []
        for i in range(len(a)):
            data.append(','.join(list(map(str, a[i]))) + ':') 
        for i in range(len(data)):
                b += data[i]
                      
        self.clientSock.send(b.encode('utf-8'))
        
    def input(self):
        data = self.clientSock.recv(1024)
        data = data.decode('utf-8')
        data = data.split("-")
        a,b = data[0].split(":"),data[1].split(":")
        a_list, b_list = [], []
        
        for i in range(len(a) -1 ):
            a_list.append(list(map(int, a[i].split(','))))
        for i in range(len(b) -1 ):
            b_list.append(list(map(int, b[i].split(','))))
        
        return a_list,b_list

client = data_socket_client()

def score_update(N):
   M = list(map(int, open("./score.txt", 'r').readlines() + [f'{N}\n']))
   M.sort()
   M.reverse()
   M = list(map(str, M))
   open('./score.txt','w').write('\n'.join(M[:-1]))
    
#뱀게임
SCREEN_WIDTH = 800       # 게임 화면의 너비
SCREEN_HEIGHT = 800
# 게임 화면의 높이
BLOCK_SIZE = 40
SNAKE_SIZE = 20

pygame.init()              # 파이게임을 사용하기 전에 초기화한다.

RED = 250,0,0
GREEN = 0,250,0
WHITE = 255,255,255
BLUE = 0,250,0
GRAY = 250,0,0
BLACK = 100,150,255
TEXTCOLOR = 255, 255, 255
ORANGE = 255, 140, 0

# 지정한 크기의 게임 화면 창을 연다.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_background(screen):
   """게임의 배경을 그린다."""
   #background = pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT))
   background_image = pygame.image.load('game_background.png')
   #pygame.draw.rect(screen, WHITE, background_image)
   screen.blit(background_image, (0, 0))

def draw_block(screen, color, position):
   """position 위치에 color 색깔의 블록을 그린다."""
   block = pygame.Rect((position[1] * BLOCK_SIZE, position[0] * BLOCK_SIZE),
                       (BLOCK_SIZE, BLOCK_SIZE))
   pygame.draw.rect(screen, color, block)

def draw_apple(screen, color, position):
   """position 위치에 color 색깔의 블록을 그린다."""
   block = pygame.Rect((position[0][1] * BLOCK_SIZE, position[0][0] * BLOCK_SIZE),
                       (BLOCK_SIZE, BLOCK_SIZE))
   pygame.draw.rect(screen, color, block)

def draw_snake(screen, color, position):
   """position 위치에 color 색깔의 블록을 그린다."""
   block = pygame.Rect((position[1] * SNAKE_SIZE, position[0] * SNAKE_SIZE),
                       (SNAKE_SIZE, SNAKE_SIZE))
   pygame.draw.rect(screen, color, block)

def draw_snake2p(screen, color, position):
   """position 위치에 color 색깔의 블록을 그린다."""
   block = pygame.Rect((position[1] * SNAKE_SIZE, position[0] * SNAKE_SIZE),
                       (SNAKE_SIZE, SNAKE_SIZE))
   pygame.draw.rect(screen, color, block)

draw_background(screen)
draw_block(screen, RED, [1, 1])
draw_block(screen, RED, [3, 1])
draw_block(screen, RED, [5, 1])
draw_block(screen, RED, [7, 1])
draw_snake(screen, BLUE, [12, 10])
draw_snake(screen, BLUE, [12, 11])
draw_snake(screen, BLUE, [12, 12])
draw_snake(screen, BLUE, [12, 13])
draw_snake2p(screen, TEXTCOLOR, [24, 22])
draw_snake2p(screen, TEXTCOLOR, [24, 23])
draw_snake2p(screen, TEXTCOLOR, [24, 25])
draw_snake2p(screen, TEXTCOLOR, [24, 26])


block_position = [0, 0]  # 블록의 위치 [y, x]


last_moved_time = datetime.now()  # 마지막으로 블록을 움직인 때

# 방향키 입력에 따라 바꿀 블록의 방향
DIRECTION_ON_KEY = {
   pygame.K_UP: 'north',
   pygame.K_DOWN: 'south',
   pygame.K_LEFT: 'west',
   pygame.K_RIGHT: 'east',
}
dicSnakeDirection = {'north':'south','south':'north','west':'east','east':'west'}


class Snake:
   """뱀 클래스"""
   color = GREEN  # 뱀의 색


   def __init__(self):
       self.positions = [[27, 9], [28, 9], [29, 9], [30, 9]]  # 뱀의 위치
       self.direction = 'north'  # 뱀의 방향
   def draw(self, screen):
       """뱀을 화면에 그린다."""
       randomR = random.randint(0,255)
       randomG = random.randint(0,255)
       randomB = random.randint(0,255)
            
       color = randomR, randomG, randomB
       for position in self.positions:  # 뱀의 몸 블록들을 순회하며
           
            draw_snake2p(screen, (0,0,255), position)  # 각 블록을 그린다
            draw_snake2p(screen, ORANGE, self.positions[0])
                      
   def crawl(self, add):
       """뱀이 현재 방향으로 한 칸 기어간다."""
       self.positions = add
       y,x = self.positions[0]
       
            
       if self.direction == 'north':
           self.positions = [[y - 1, x]] + self.positions[:-1]
       elif self.direction == 'south':
           self.positions = [[y + 1, x]] + self.positions[:-1]
       elif self.direction == 'west':
           self.positions = [[y, x - 1]] + self.positions[:-1]
       elif self.direction == 'east':
           self.positions = [[y, x + 1]] + self.positions[:-1]
        
   def turn(self, direction):
       """뱀의 방향을 바꾼다."""
       if self.direction != dicSnakeDirection[DIRECTION_ON_KEY[event.key]]:
           self.direction = direction
        
   def grow(self):
       """뱀이 한 칸 자라나게 한다."""
       tail_position = self.positions[-1]
       x, y = -1, -1
       self.positions.append([x, y]) 
        
   def ungrow(self):#뱀이 한 칸 줄어들게 한다.
       if len(self.positions) >= 2:
           del self.positions[-1]

   def growClear(self):#뱀을 한 칸만 남겨둔다.
       if len(self.positions) >= 2:
           del self.positions[0:-1]

class Snake2p:
   """뱀 클래스"""
   color = GREEN  # 뱀의 색

   def __init__(self):
       self.positions = [[27, 27], [28, 27], [29, 27], [30, 27]]  # 뱀의 위치
       self.direction = 'north'  # 뱀의 방향
   def draw(self, screen):
       """뱀을 화면에 그린다."""
       randomR = random.randint(0,255)
       randomG = random.randint(0,255)
       randomB = random.randint(0,255)
       color = randomR, randomG, randomB
       for position in self.positions:  # 뱀의 몸 블록들을 순회하며
            draw_snake2p(screen, TEXTCOLOR, position)  # 각 블록을 그린다
            draw_snake2p(screen, ORANGE, self.positions[0])
   def crawl(self):
       """뱀이 현재 방향으로 한 칸 기어간다."""
       head_position = self.positions[0]
       y, x = head_position
            
       if self.direction == 'north':
           self.positions = [[y - 1, x]] + self.positions[:-1]
       elif self.direction == 'south':
           self.positions = [[y + 1, x]] + self.positions[:-1]
       elif self.direction == 'west':
           self.positions = [[y, x - 1]] + self.positions[:-1]
       elif self.direction == 'east':
           self.positions = [[y, x + 1]] + self.positions[:-1]
        
   def turn(self, direction):
       """뱀의 방향을 바꾼다."""
       if self.direction != dicSnakeDirection[DIRECTION_ON_KEY[event.key]]:
           self.direction = direction
        
   def grow(self):
       """뱀이 한 칸 자라나게 한다."""
       tail_position = self.positions[-1]
       x, y = 100, 100
       self.positions.append([x, y]) 

   def growClear(self):#뱀을 한 칸만 남겨둔다.
       if len(self.positions) >= 2:
           del self.positions[0:-1]

class Apple:
   """사과 클래스"""
   color = RED  # 사과의 색
   
   def __init__(self, position = [[9,9]]):
       self.position = position #사과의 위치
       
   def draw(self, screen):
       """사과를 화면에 그린다."""
       draw_apple(screen, GRAY, self.position)

class SnakeCollisionException(Exception):
   """뱀 충돌 예외"""
   pass

class GameBoard:
   """게임판 클래스"""
   width = 20   # 게임판의 너비
   height = 20  # 게임판의 높이
   
   def __init__(self):
       self.snake = Snake()  # 게임판 위의 뱀
       self.snake2p = Snake2p()
       self.apple = Apple()
       self.check = 0
       pygame.display.set_caption('뱀게임 client')
        
   def draw_text(self, text, font, surface, x,y,main_color):
       text_obj = font.render(text, True, main_color)
       text_rect = text_obj.get_rect()
       text_rect.centerx = x
       text_rect.centery = y
       surface.blit(text_obj, text_rect)
        
   def draw(self, screen):
       """화면에 게임판의 구성요소를 그린다."""
       self.apple.draw(screen)  # 게임판 위의 사과를 그린다
       self.snake.draw(screen)  # 게임판 위의 뱀을 그린다
       self.snake2p.draw(screen)
       self.draw_text(f'점수: {len(self.snake.positions)-4}',pygame.font.Font('NanumGothic.ttf', 20),screen,50,30,TEXTCOLOR)
       self.draw_text(f'점수: {len(self.snake2p.positions)-4}',pygame.font.Font('NanumGothic.ttf', 20),screen,750,30,TEXTCOLOR)
       
        
   def process_turn(self):
       """게임을 한 차례 진행한다."""
       scorelog = []
       applelog = []
       self.snake.positions, applelog = client.input()
       if (self.apple.position != applelog):
           self.apple.position = applelog
           self.check = 0
       client.output(self.snake2p.positions)
       #self.snake.crawl(snakelog)
       self.snake2p.crawl()
       
       
       if (self.snake.positions[0][0] < 0 or self.snake.positions[0][1] < 0) or (self.snake.positions[0][0] > 39 or self.snake.positions[0][1] > 39) or (self.snake2p.positions[0][0] < 0 or self.snake2p.positions[0][1] < 0) or (self.snake2p.positions[0][0] > 39 or self.snake2p.positions[0][1] > 39):
           
           raise SnakeCollisionException()
       
       # 뱀의 머리가 뱀의 몸과 부딛혔으면
       if self.snake.positions[0] in self.snake.positions[1:] or self.snake2p.positions[0] in self.snake2p.positions[1:]:
           
           pass  # 뱀 충돌 예외를 일으킨다
       for i in range(1,len(self.snake.positions)):
          if self.snake2p.positions[0] == self.snake.positions[i]:
             
             raise SnakeCollisionException()
       for i in range(1, len(self.snake2p.positions)):
          if self.snake.positions[0] == self.snake2p.positions[i]:
             
             raise SnakeCollisionException()
       for i in range(0,41):
          if self.snake.positions[0] == (i,40) or self.snake2p.positions[0] == (i,40):
             
             raise SnakeCollisionException()  # 뱀 충돌 예외를 일으킨다
          if self.snake.positions[0] == (40,i) or self.snake2p.positions[0] == (40,i):
             
             raise SnakeCollisionException()  
          if self.snake.positions[0] == (i,-40) or self.snake2p.positions[0] == (i,-40):
             
             raise SnakeCollisionException()
             
          if self.snake.positions[0] == (-40,i) or self.snake2p.positions[0] == (-40,i):
             
             raise SnakeCollisionException()
          
       # 뱀의 머리와 사과가 닿았으면
       if (self.snake.positions[0][0] == self.apple.position[0][0]*2 or self.snake.positions[0][0] == self.apple.position[0][0]*2+1) and (self.snake.positions[0][1] == self.apple.position[0][1]*2 or self.snake.positions[0][1] == self.apple.position[0][1]*2+1):
           self.snake.grow()     # 뱀을 한 칸 자라게 한다

       elif (self.snake2p.positions[0][0] == self.apple.position[0][0]*2 or self.snake2p.positions[0][0] == self.apple.position[0][0]*2+1) and (self.snake2p.positions[0][1] == self.apple.position[0][1]*2 or self.snake2p.positions[0][1] == self.apple.position[0][1]*2+1):
           if (self.check == 0):
               self.snake2p.grow()
               self.check = 1
           
           
timeChange = 0.1
TURN_INTERVAL = timedelta(seconds=0.1)  # 게임 진행 간격을 정의한다
last_turn_time = datetime.now()
game_board = GameBoard()
while True:
   events = pygame.event.get()
   for event in events:
      if event.type == pygame.QUIT:
         pygame.quit()
      if event.type == pygame.KEYDOWN:  # 화살표 키가 입력되면 뱀의 방향을 바꾼다
         if event.key in DIRECTION_ON_KEY:
            game_board.snake2p.turn(DIRECTION_ON_KEY[event.key])
         
         
               
   # 시간이 TURN_INTERVAL만큼 지날 때마다 게임을 한 차례씩 진행한다
   if TURN_INTERVAL < datetime.now() - last_turn_time:
       try:
           game_board.process_turn()
       except SnakeCollisionException:
          score_update(len(game_board.snake.positions)-4)
          startfile('read_leaderboard_pyqt.py')
          pygame.quit()
          sys.exit()
       last_turn_time = datetime.now()
   draw_background(screen)
   game_board.draw(screen)
   pygame.display.update()

