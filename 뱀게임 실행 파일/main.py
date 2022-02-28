import pygame
from pygame.locals import *
import time
import random
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from os import startfile
import sys

def score_update(N):
   print(N)
   M = list(map(int, open("./score.txt", 'r').readlines() + [f'{N}\n']))
   M.sort()
   M.reverse()
   print(M)
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

def draw_snake(screen, color, position):
   """position 위치에 color 색깔의 블록을 그린다."""
   block = pygame.Rect((position[1] * SNAKE_SIZE, position[0] * SNAKE_SIZE),
                       (SNAKE_SIZE, SNAKE_SIZE))
   pygame.draw.rect(screen, color, block)


draw_background(screen)
draw_block(screen, RED, (1, 1))
draw_block(screen, RED, (3, 1))
draw_block(screen, RED, (5, 1))
draw_block(screen, RED, (7, 1))
draw_snake(screen, BLUE, (12, 10))
draw_snake(screen, BLUE, (12, 11))
draw_snake(screen, BLUE, (12, 12))
draw_snake(screen, BLUE, (12, 13))


block_position = [0, 0]  # 블록의 위치 [y, x]


block_position = [0, 0]
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
       self.positions = [(16, 20), (17, 20), (18, 20), (19, 20)]  # 뱀의 위치
       self.direction = 'north'  # 뱀의 방향
   def draw(self, screen):
       """뱀을 화면에 그린다."""
       for position in self.positions:  # 뱀의 몸 블록들을 순회하며
           draw_snake(screen, (0, 0, 250), position)  # 각 블록을 그린다
           draw_snake(screen, ORANGE, self.positions[0])
   def crawl(self):
       """뱀이 현재 방향으로 한 칸 기어간다."""
       head_position = self.positions[0]
       y, x = head_position
            
       if self.direction == 'north':
           self.positions = [(y - 1, x)] + self.positions[:-1]
       elif self.direction == 'south':
           self.positions = [(y + 1, x)] + self.positions[:-1]
       elif self.direction == 'west':
           self.positions = [(y, x - 1)] + self.positions[:-1]
       elif self.direction == 'east':
           self.positions = [(y, x + 1)] + self.positions[:-1]
        
   def turn(self, direction):
       """뱀의 방향을 바꾼다."""
       if self.direction != dicSnakeDirection[DIRECTION_ON_KEY[event.key]]:
           self.direction = direction
        
   def grow(self):
       """뱀이 한 칸 자라나게 한다."""
       tail_position = self.positions[-1]
       y, x = tail_position
       self.positions.append((x, y)) 
        
   def ungrow(self):#뱀이 한 칸 줄어들게 한다.
       if len(self.positions) >= 2:
           del self.positions[-1]

   def growClear(self):#뱀을 한 칸만 남겨둔다.
       if len(self.positions) >= 2:
           del self.positions[0:-1]

class Apple:
   """사과 클래스"""
   color = RED  # 사과의 색
   def __init__(self, position=(13, 15)):
       self.position = position  # 사과의 위치
   def draw(self, screen):
       """사과를 화면에 그린다."""
       draw_block(screen, GRAY, self.position)

class SnakeCollisionException(Exception):
   """뱀 충돌 예외"""
   pass

class GameBoard:
   """게임판 클래스"""
   width = 20   # 게임판의 너비
   height = 20  # 게임판의 높이

   def __init__(self):
       self.snake = Snake()  # 게임판 위의 뱀
       self.apple = Apple((random.randint(0, 29)/2, random.randint(0, 29)/2))  # 게임판 위의 사과
       pygame.display.set_caption('뱀게임')
       game_icon = pygame.image.load("snack.png")
       pygame.display.set_icon(game_icon)
        
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
       self.draw_text(f'점수: {len(self.snake.positions)-4}',pygame.font.Font('NanumGothic.ttf', 20),screen,50,30,TEXTCOLOR)
       #self.draw_text('난이도 올리기: f키',pygame.font.Font('NanumGothic.ttf', 20),screen,83,785,TEXTCOLOR)
        
   def process_turn(self):
       """게임을 한 차례 진행한다."""
       self.snake.crawl()

       for i in range(len(self.snake.positions)):
         if (self.snake.positions[i][0] < 0 or self.snake.positions[i][1] < 0) or (self.snake.positions[i][0] > 39 or self.snake.positions[i][1] > 39):
            raise SnakeCollisionException()
       
       # 뱀의 머리가 뱀의 몸과 부딛혔으면
       if self.snake.positions[0] in self.snake.positions[1:]:
           raise SnakeCollisionException()  # 뱀 충돌 예외를 일으킨다
      
       for i in range(0,41):
          if self.snake.positions[0] == (i,40):
             raise SnakeCollisionException()  # 뱀 충돌 예외를 일으킨다
          if self.snake.positions[0] == (40,i):
             raise SnakeCollisionException()  
          if self.snake.positions[0] == (i,-40):
             raise SnakeCollisionException()  
          if self.snake.positions[0] == (-40,i):
             raise SnakeCollisionException()
         
       # 뱀의 머리와 사과가 닿았으면
       if (self.snake.positions[0][0] == self.apple.position[0]*2 or self.snake.positions[0][0] == self.apple.position[0]*2+1) and (self.snake.positions[0][1] == self.apple.position[1]*2 or self.snake.positions[0][1] == self.apple.position[1]*2+1):
           self.snake.grow()     # 뱀을 한 칸 자라게 한다
           self.put_new_apple()  # 사과를 새로 놓는다
   def put_new_apple(self):
       """게임판에 새 사과를 놓는다."""
       self.apple = Apple((random.randint(0, 29)/2, random.randint(0, 29)/2))
       for position in self.snake.positions:    # 뱀 블록을 순회하면서
           if ((self.apple.position[0]*2,  self.apple.position[1]*2) == position) or ((self.apple.position[0]*2+1,  self.apple.position[1]*2+1) == position) or ((self.apple.position[0]*2+1,  self.apple.position[1]*2) == position) or ((self.apple.position[0]*2,  self.apple.position[1]*2+1) == position):  # 사과가 뱀 위치에 놓인 경우를 확인해
               self.put_new_apple()             # 사과를 새로 놓는다
               break



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
            game_board.snake.turn(DIRECTION_ON_KEY[event.key])
               
   # 시간이 TURN_INTERVAL만큼 지날 때마다 게임을 한 차례씩 진행한다
   if TURN_INTERVAL < datetime.now() - last_turn_time:
       try:
           game_board.process_turn()
       except SnakeCollisionException:
          score_update(len(game_board.snake.positions)-4)
          startfile('read_leaderboard_pyqt.exe')
          pygame.quit()
          sys.exit()
       last_turn_time = datetime.now()
   draw_background(screen)
   game_board.draw(screen)
   pygame.display.update()

