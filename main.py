import pygame
import sys
from os import path
from map import list
from pygame import mixer
import math
pygame.init()
screen = pygame.display.set_mode((560, 560), 0, 0)
pygame.display.set_caption('推木箱小游戏')
boxList = []
ballList = []
wallList = []
peopleDir = {'x': 0, 'y': 0}
clock = pygame.time.Clock()
def initData(level):
  boxList.clear()
  ballList.clear()
  wallList.clear()
  data = list[level]
  index = -1
  for i in range(0, 16):
    for j in range(0, 16):
      index += 1
      item = data[index]
      if item == 1:
        wallList.append(1)
      else:
        wallList.append(0)
  
      if item == 2:
        ballList.append(2)
      else:
        ballList.append(0)
  
      if item == 3:
        boxList.append(3)
      else:
        boxList.append(0)

      if item == 4:
        peopleDir['x'] = j
        peopleDir['y'] = i


class GameApp:
  level = 0 # 第一关
  map = None
  background = None
  wall = None
  ball = None
  box = None
  down_people = None
  left_people = None
  right_people = None
  up_people = None
  direction = 'down'
  levelFont = None
  ballNum = 0
  def __init__(self):
    self.loadFile()
    icon = pygame.image.load(self.resolve('img/down.png'))
    pygame.display.set_icon(icon)
    mixer.music.load(self.resolve('img/background.wav'))
    self.levelFont = pygame.font.Font(self.resolve('img/msyh.ttc'), 20)
    

    mixer.music.play(-1)
    self.runGame()
    
  def loadFile(self):
    self.background = pygame.image.load(self.resolve('img/bg.jpg'))
    self.wall = pygame.image.load(self.resolve('img/wall.png'))
    self.ball = pygame.image.load(self.resolve('img/ball.png'))
    self.box = pygame.image.load(self.resolve('img/box.png'))
    self.down_people = pygame.image.load(self.resolve('img/down.png'))
    self.left_people = pygame.image.load(self.resolve('img/left.png'))
    self.right_people = pygame.image.load(self.resolve('img/right.png'))
    self.up_people = pygame.image.load(self.resolve('img/up.png'))

  def resolve(self, filename):
    dirName = path.dirname(__file__)
    return dirName + '/' + filename
  
  def renderLevel(self):
    levelText = self.levelFont.render('第'+str(self.level+1)+'关', True, (0, 0, 0))
    screen.blit(levelText, (490, 5))

  def renderPeople(self, i, j):
    if self.direction == 'down':
      screen.blit(self.down_people, (j*35-7, i*35-27))
    if self.direction == 'left':
      screen.blit(self.left_people, (j*35-7, i*35-27))
    if self.direction == 'right':
      screen.blit(self.right_people, (j*35-7, i*35-27))
    if self.direction == 'up':
      screen.blit(self.up_people, (j*35-7, i*35-27))

  def renderData(self):
    index = -1
    for i in range(0, 16):
      for j in range(0, 16):
        index+=1
        if wallList[index] == 1:
          screen.blit(self.wall, (j*35, i*35 - 13))
        if ballList[index] == 2:
          self.ballNum+=1
          screen.blit(self.ball, (j*35 + 2, i*35 + 2))
        if boxList[index] == 3:
          screen.blit(self.box, (j*35, i*35 - 11))
        if peopleDir['x'] == j and peopleDir['y'] == i:
          self.renderPeople(i, j)

  def hasGo(self, preItem, nextItem, preIndex, nextIndex, x, y):
    if preItem == 0 or preItem == 2:
      peopleDir['x'] = x
      peopleDir['y'] = y
      return True
    if preItem == 3: # 推箱子走路
      if nextItem == 0 or nextItem == 2:
        boxList[preIndex] = 0
        boxList[nextIndex] = 3
        peopleDir['x'] = x
        peopleDir['y'] = y
        self.checkGameover(nextIndex)
        self.checkWin()
        return True
    return False
  def checkGameover(self, nextIndex):
    y = math.floor(nextIndex/16)
    x = nextIndex%16
    preItem = 0
    if ballList[nextIndex] != 2:
      checkList = [
        wallList[(y-1)*16 + x],
        wallList[y*16 + x-1],
        wallList[(y+1)*16 + x],
        wallList[y*16 + x+1],
        wallList[(y-1)*16 + x]
      ]
      for item in checkList:
        if item == 0:
          preItem = 0
        elif item == 1 and preItem == 0:
          preItem = 1
        elif item == 1 and preItem == 1: # 如果相邻是两面墙及失败了
          self.level = 0
          initData(self.level)
          break


  def checkWin(self):
    index = -1
    winNum = 0
    self.ballNum = 0
    for i in range(0, 16):
      for j in range(0, 16):
        index+=1
        if ballList[index] == 2:
          self.ballNum+=1
          if (boxList[index] == 3):
            winNum+=1
    if self.ballNum == winNum:
      self.level+=1
      initData(self.level)

  def pushData(self, type):
    x = peopleDir['x']
    y = peopleDir['y']
    curIndex = y*16+x
    if type == 'left':
      preIndex = y*16+x-1
      nextIndex = y*16+x-2
      preItem = max([boxList[preIndex], ballList[preIndex], wallList[preIndex]])
      nextItem = max([boxList[nextIndex], ballList[nextIndex], wallList[nextIndex]])
      if self.hasGo(preItem, nextItem, preIndex, nextIndex, x-1, y):
        self.direction = 'left'
    if type == 'right':
      preIndex = y*16+x+1
      nextIndex = y*16+x+2
      preItem = max([boxList[preIndex], ballList[preIndex], wallList[preIndex]])
      nextItem = max([boxList[nextIndex], ballList[nextIndex], wallList[nextIndex]])
      if self.hasGo(preItem, nextItem, preIndex, nextIndex, x+1, y):
        self.direction = 'right'
    if type == 'up':
      preIndex = (y-1)*16+x
      nextIndex = (y-2)*16+x
      preItem = max([boxList[preIndex], ballList[preIndex], wallList[preIndex]])
      nextItem = max([boxList[nextIndex], ballList[nextIndex], wallList[nextIndex]])
      if self.hasGo(preItem, nextItem, preIndex, nextIndex, x, y-1):
        self.direction = 'up'
    if type == 'down':
      preIndex = (y+1)*16+x
      nextIndex = (y+2)*16+x
      preItem = max([boxList[preIndex], ballList[preIndex], wallList[preIndex]])
      nextItem = max([boxList[nextIndex], ballList[nextIndex], wallList[nextIndex]])
      if self.hasGo(preItem, nextItem, preIndex, nextIndex, x, y+1):
        self.direction = 'down'
    
  def runGame(self):    
    while True:
      clock.tick(300)
      screen.fill((0, 0, 0))
      screen.blit(self.background, (0, 0))
      self.renderData()
      self.renderLevel()
      for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
          pygame.quit()  # 退出pygame
          sys.exit() # 退出系统
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.pushData('left')
          if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.pushData('right')
          if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.pushData('down')
          if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.pushData('up')
      pygame.display.update()
      
if __name__ == '__main__':
  initData(0)
  GameApp()