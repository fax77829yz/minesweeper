# coding=UTF-8
# 10527209 許育愷
# 10527214 郭恆嘉

import pygame
import random
import time
import sys,os

class Cell() :
  def __init__(self) :
    self.flag = False
    self.opened = False
    self.obj = '0'

class Mine() :
  game_over = False
  flag_num = 0

  def __init__(self, x, y) :
    self.mine = [[Cell() for i in range(x)] for j in range(y)]

  def print_mine( self ) :
    #x------
    print( ' ', end='')
    for x in range(len(self.mine[0])) :
      print(f' {x}', end='')
    print()
    #-------
    for i in range(len(self.mine)) :
      print(i, end = ' ')
      for j in range(len(self.mine[0])) :
        if self.mine[i][j].flag  :
          print( 'F', end = ' ')
        elif self.mine[i][j].opened :
          print( self.mine[i][j].obj, end = ' ')
        else :
          print( '~', end = ' ')
      print()
    print()

  def print_mine_ans( self ) :
    print( '  ANS: ' )
    #x------
    print( ' ', end='')
    for x in range(len(self.mine[0])) :
      print(f' {x}', end='')
    print()
    #-------
    for i in range(len(self.mine)) :
      print(i, end = ' ')
      for j in range(len(self.mine[0])) :
        print( self.mine[i][j].obj, end = ' ')
      print()

    print()
  
  def create_data( self, bomb_num ) :
    i = 0
    self.bomb_num = bomb_num
    while i < bomb_num :
      y = random.randint(0,len(self.mine)-1)
      x = random.randint(0,len(self.mine[0])-1)
      if self.is_bomb( x, y ) :
        continue

      self.mine[y][x].obj = 'B'
      self.cal_number( x, y )
      i += 1

  def is_bomb( self, x, y ) :
    if self.mine[y][x].obj is 'B' : return True
    return False

  def cal_number( self, x, y) :
    '''
      calculate eight directions besides the bomb
    '''
    if x > 0 and not self.is_bomb(x-1,y) : 
      self.mine[y][x-1].obj = str(int(self.mine[y][x-1].obj) + 1)
    if x < len(self.mine[0])-1 and not self.is_bomb(x+1,y) : 
      self.mine[y][x+1].obj = str(int(self.mine[y][x+1].obj) + 1)
    if y > 0 and not self.is_bomb(x,y-1) : 
      self.mine[y-1][x].obj = str(int(self.mine[y-1][x].obj) + 1)
    if y < len(self.mine)-1 and not self.is_bomb(x,y+1) : 
      self.mine[y+1][x].obj = str(int(self.mine[y+1][x].obj) + 1)
    if x > 0 and y > 0 and not self.is_bomb(x-1,y-1): 
      self.mine[y-1][x-1].obj = str(int(self.mine[y-1][x-1].obj) + 1)
    if x > 0 and y < len(self.mine)-1 and not self.is_bomb(x-1,y+1): 
      self.mine[y+1][x-1].obj = str(int(self.mine[y+1][x-1].obj) + 1)
    if x < len(self.mine[0])-1 and y > 0 and not self.is_bomb(x+1,y-1): 
      self.mine[y-1][x+1].obj = str(int(self.mine[y-1][x+1].obj) + 1)
    if x < len(self.mine[0])-1 and y < len(self.mine)-1 and not self.is_bomb(x+1,y+1): 
      self.mine[y+1][x+1].obj = str(int(self.mine[y+1][x+1].obj) + 1)

  def is_null(self, x, y) :
    if self.mine[y][x].obj is '0' : return True
    return False

  def open_4_direction(self, x, y) :
    
    if y-1 >= 0 : self.mine[y-1][x].opened = True
    if y+1 <= len(self.mine)-1 : self.mine[y+1][x].opened = True
    if x-1 >= 0 : self.mine[y][x-1].opened = True
    if x+1 <= len(self.mine[0])-1 : self.mine[y][x+1].opened = True

  def open_null_cell(self, x, y) :
    if self.mine[y][x].opened : return 

    self.mine[y][x].opened = True
    if y-1 >= 0 and self.is_null(x, y-1) : self.open_null_cell(x, y-1)
    if y+1 <= len(self.mine)-1 and self.is_null(x, y+1) : self.open_null_cell(x, y+1)
    if x-1 >= 0 and self.is_null(x-1, y) : self.open_null_cell(x-1, y)
    if x+1 <= len(self.mine[0])-1 and self.is_null(x+1, y) : self.open_null_cell(x+1, y)
    self.open_4_direction(x, y)
    return 

  def open_cell(self, x, y) :
    print( f'open_cell : x {x} y {y}')
    if self.mine[y][x].flag or self.mine[y][x].opened:
      return 
    elif self.is_bomb(x, y):
      self.game_over = True
      return 
    elif not self.is_null(x, y):
      self.mine[y][x].opened = True
      return 
    else :
      self.open_null_cell(x, y)

  def win_game(self) :
    if self.flag_num == self.bomb_num :
      for i in range(len(self.mine)) :
        for j in range(len(self.mine[0])) :
          if self.is_bomb(j,i) and not self.mine[i][j].flag:return False # is bomb but flag doesn't set

      return True
    return False

  def set_flag(self, x, y) :
    self.mine[y][x].flag = True
    self.flag_num += 1

  def cancel_flag(self, x, y) :
    self.mine[y][x].flag = False
    self.flag_num -= 1

  def play_game(self, x, y) :
    self.print_mine()
    self.open_cell(x, y)
    # self.set_flag(int(ans[0]), int(ans[1]))

pygame.init()
x_range, y_range = 300,300
size = 30
resize = 0
game_over_image = pygame.image.load(os.path.dirname(__file__) + '/image/gg.png') 
victory_image = pygame.image.load(os.path.dirname(__file__) + '/image/victory.jpg') 
start_image = pygame.image.load(os.path.dirname(__file__) + '/image/start.jpg') 
button_sound = pygame.mixer.Sound(os.path.dirname(__file__) + '/button.wav')
square = pygame.image.load(os.path.dirname(__file__) + '/image/square.png')
bomb = pygame.image.load(os.path.dirname(__file__) + '/image/bomb.jpg')
flag = pygame.image.load(os.path.dirname(__file__) + '/image/flag.jpg')
n1 = pygame.image.load(os.path.dirname(__file__) + '/image/number/1.jpg')
n2 = pygame.image.load(os.path.dirname(__file__) + '/image/number/2.jpg')
n3 = pygame.image.load(os.path.dirname(__file__) + '/image/number/3.jpg')
n4 = pygame.image.load(os.path.dirname(__file__) + '/image/number/4.jpg')
n5 = pygame.image.load(os.path.dirname(__file__) + '/image/number/5.jpg')
n6 = pygame.image.load(os.path.dirname(__file__) + '/image/number/6.jpg')
n7 = pygame.image.load(os.path.dirname(__file__) + '/image/number/7.jpg')
n8 = pygame.image.load(os.path.dirname(__file__) + '/image/number/8.jpg')
Is_Running = True

def mine_game(level) : 
  if level == 'entry' :
    m = Mine( 10,10 )
    m.create_data( 10 )
  elif level == 'medium' :
    m = Mine( 14,14 )
    m.create_data( 35 )
  elif level == 'hard' :
    m = Mine( 20,20 )
    m.create_data( 80 )
  else : return

  m.print_mine_ans()
  while not m.game_over and not m.win_game():
    draw_map(m)
    pygame.display.update()
    for e in pygame.event.get():
      if e.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      elif e.type == pygame.MOUSEBUTTONUP and e.button == 1: # left click
        pos = pygame.mouse.get_pos()
        m.open_cell(int(pos[0]/size),int(pos[1]/size))
        m.print_mine()
      elif e.type == pygame.MOUSEBUTTONUP and e.button == 3: # right click
        pos = pygame.mouse.get_pos()
        if m.mine[int(pos[1]/size)][int(pos[0]/size)].flag :
          m.cancel_flag(int(pos[0]/size),int(pos[1]/size))
        else :
           m.set_flag(int(pos[0]/size),int(pos[1]/size))
        m.print_mine()

  if m.game_over:
    draw_map(m)
    pygame.display.update()
    time.sleep(3)
    base_surf.blit(pygame.transform.scale(game_over_image, (x_range+resize,y_range+resize)),(0,0))
  else :
    base_surf.blit(pygame.transform.scale(victory_image, (x_range+resize,y_range+resize)),(0,0))

  pygame.display.update()
  time.sleep(3)
  return 

def draw_map(m):   
  x,y = 0,0
  base_surf.fill((0,0,0))
  for i in range(len(m.mine)) :
    for j in range(len(m.mine[0])) :
      if m.mine[i][j].opened :
        if not m.is_null(j,i) :
          if m.mine[i][j].obj == '1':
            base_surf.blit(pygame.transform.scale(n1, (30, 30)),(j*size,i*size))
          if m.mine[i][j].obj == '2':
            base_surf.blit(pygame.transform.scale(n2, (30, 30)),(j*size,i*size))
          if m.mine[i][j].obj == '3':
            base_surf.blit(pygame.transform.scale(n3, (30, 30)),(j*size,i*size))
          if m.mine[i][j].obj == '4':
            base_surf.blit(pygame.transform.scale(n4, (30, 30)),(j*size,i*size))
          if m.mine[i][j].obj == '5':
            base_surf.blit(pygame.transform.scale(n5, (30, 30)),(j*size,i*size))
          if m.mine[i][j].obj == '6':
            base_surf.blit(pygame.transform.scale(n6, (30, 30)),(j*size,i*size))
          if m.mine[i][j].obj == '7':
            base_surf.blit(pygame.transform.scale(n7, (30, 30)),(j*size,i*size))
          if m.mine[i][j].obj == '8':
            base_surf.blit(pygame.transform.scale(n8, (30, 30)),(j*size,i*size))
        else :
          rec = pygame.Rect(j*size, i*size, size, size)
          pygame.draw.rect(base_surf,(125,125,125),rec,0 )
      elif m.mine[i][j].flag :
        base_surf.blit(pygame.transform.scale(flag, (30, 30)),(j*size,i*size))
      elif m.is_bomb(j,i) and m.game_over:
        base_surf.blit(pygame.transform.scale(bomb, (30, 30)),(j*size,i*size))
      else :
        base_surf.blit(pygame.transform.scale(square, (30, 30)),(j*size,i*size))

  while x < x_range:
      pygame.draw.line(base_surf, (255,255,255), (x,0), (x,y_range))
      x += size
  while y < y_range:
      pygame.draw.line(base_surf, (255,255,255), (0,y), (x_range,y))
      y += size

def get_level(pos) :
  if 99 <= pos[0] and pos[0] <=180 and 124 <= pos[1] and pos[1] <= 156 :
    return 'entry', 0
  elif 99 <= pos[0] and pos[0] <=180 and 177 <= pos[1] and pos[1] <= 210 :
    return 'medium', 120
  elif 99 <= pos[0] and pos[0] <=180 and 234 <= pos[1] and pos[1] <= 269 :
    return 'hard', 300
  else : return 'none', 0

if __name__ == '__main__' : 
  while Is_Running :
    resize = 0
    base_surf = pygame.display.set_mode((x_range+resize,y_range+resize))
    base_surf.blit(start_image,(0,0))
    pygame.display.update()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif e.type == pygame.MOUSEBUTTONUP:           
            level, resize = get_level(pygame.mouse.get_pos())
            #button_sound.play()
            base_surf = pygame.display.set_mode((x_range+resize,y_range+resize))    
            mine_game(level)
