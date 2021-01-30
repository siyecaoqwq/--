# 任务：删除碰撞元素

from loadImg import *
from initData import *
import sys
import pygame
import time

pygame.init()
# 设置窗口
screen = pygame.display.set_mode([480, 670])
# 设置窗口标题
pygame.display.set_caption('飞机大战1.0')
gameState = 'GAMEing'
# 病毒列表
virusList = []
# 子弹列表
bulletList = []

# 自定义生成病毒事件
ADDVIRUS = 30
# 开启生成病毒事件定时器
pygame.time.set_timer(ADDVIRUS, 80000)

music = pygame.mixer.Sound('12465.wav')
music.play(-1, 0)



分数 = 1000
# 绘制函数
def draw():
    # 绘制背景
    screen.blit(bgImg, [0, 0])
    # 绘制病毒
    for virus in virusList:
        screen.blit(virus['img'], [virus['x'], virus['y']])
    # 绘制飞机
    screen.blit(plane['img'], [plane['x'], plane['y']])
    # 绘制子弹
    for bullet in bulletList:
        screen.blit(bullet['img'], [bullet['x'], bullet['y']])


# 移动函数
def move():
    # 病毒移动
    for virus in virusList:
        virus['y'] += 1
    # 子弹移动
    for bullet in bulletList:
        bullet['y'] -= 2


# 检测碰撞函数
def checkHit(v, p):
    # 碰撞范围上下左右边缘
    top = p['y'] - v['height']
    bottom = p['y'] + p['height']
    left = p['x'] - v['width']
    right = p['x'] + p['width']
    # 碰撞条件，如果发生碰撞返回True
    if v['x'] >= left and v['x'] <= right:
        if v['y'] >= top and v['y'] <= bottom:
            return True


# 碰撞响应函数
def check():
    global 分数
    # 检测病毒与飞机碰撞
    for virus in virusList:
        if checkHit(virus, plane):
            pygame.time.set_timer(ADDVIRUS, 0)
            分数 -= 1
            print('-1')
            if 分数 == 0:
                print('GameOver')
                time.sleep(1)
                exit(0)
    # 检测病毒与子弹碰撞
    for virus in virusList:
        for bullet in bulletList:
            if checkHit(virus, bullet):
                virus['state'] = False
                bullet['state'] = False
                break


# 删除元素函数
def delete():
    # 声明使用的是全局变量
    global virusList, bulletList
    # 删除移出屏幕的病毒
    new_virusList = []
    for virus in virusList:
        # 判断病毒在屏幕内并且状态为True -----------------
        if virus['y'] < 670 and virus['state']:
            new_virusList.append(virus)
    virusList = new_virusList
    # 删除移出屏幕的子弹
    new_bulletList = []
    for bullet in bulletList:
        # 判断子弹在屏幕内并且状态为True -----------------
        if bullet['y'] > -bullet['height'] and bullet['state']:
            new_bulletList.append(bullet)
    bulletList = new_bulletList


# 事件判断函数
def eventListen():
    for event in pygame.event.get():
        # 退出事件
        if event.type == pygame.QUIT:
            sys.exit()
        # 生成病毒事件，添加病毒
        elif event.type == ADDVIRUS:
            virusList.append(getVirus())
        # 键盘按下事件
        elif event.type == pygame.KEYDOWN:
            # 按下左键
            if event.key == pygame.K_LEFT:
                plane['x'] -= 20
                # 飞机超出左边界后，固定x坐标
                if plane['x'] < 0:
                    plane['x'] = 0
            # 按下右键
            elif event.key == pygame.K_RIGHT:
                plane['x'] += 20
                # 飞机超出右边界后，固定x坐标
                if plane['x'] > 480 - plane['width']:
                    plane['x'] = 480 - plane['width']
            # 按下空格按键
            elif event.key == pygame.K_SPACE:
                bulletList.append(getBullet())
                virusList.append(getVirus())


# 主循环
while True:
    # 使用事件判断函数
    eventListen()
    # 使用绘制函数
    draw()
    if gameState == 'GAMEing':
        # 使用移动函数
        move()
        # 使用删除函数
        delete()
        # 使用碰撞响应函数
        check()
        # 更新窗口
    pygame.display.update()
