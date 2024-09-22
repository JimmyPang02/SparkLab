import pygame
import sys
import random


# 初始化pygame
pygame.init()

# 设置游戏窗口大小
window_width = 800
window_height = 600
cell_size = 20

# 定义颜色
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# 创建游戏窗口
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('贪吃蛇游戏')

# 定义贪吃蛇和食物
snake = [(200, 200)]
snake_direction = 'RIGHT'
food = (random.randint(0, window_width//cell_size-1)*cell_size, 
        random.randint(0, window_height//cell_size-1)*cell_size)

clock = pygame.time.Clock()

# 创建得分变量
score = 0

# 游戏主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != 'DOWN':
                snake_direction = 'UP'
            elif event.key == pygame.K_DOWN and snake_direction != 'UP':
                snake_direction = 'DOWN'
            elif event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                snake_direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                snake_direction = 'RIGHT'

    # 移动贪吃蛇
    head = snake[0]
    x, y = head
    if snake_direction == 'UP':
        new_head = (x, y - cell_size)
    elif snake_direction == 'DOWN':
        new_head = (x, y + cell_size)
    elif snake_direction == 'LEFT':
        new_head = (x - cell_size, y)
    elif snake_direction == 'RIGHT':
        new_head = (x + cell_size, y)

    snake.pop() 


    # a=10
    # b=a.deepcopy()
    # b=20


    # 检查是否吃到食物
    if new_head == food:
        food = (random.randint(0, window_width//cell_size-1)*cell_size, 
                random.randint(0, window_height//cell_size-1)*cell_size)
        score += 10  # 增加得分
    else:
        pass
        
    snake.insert(0, new_head)  # 将新的头部添加到贪吃蛇

    # 渲染背景
    window.fill(black)

    # 绘制贪吃蛇
    for segment in snake:
        pygame.draw.rect(window, green, (segment[0], segment[1], cell_size, cell_size))

    # 绘制食物
    pygame.draw.rect(window, red, (food[0], food[1], cell_size, cell_size))

    # 更新窗口
    pygame.display.update()

    clock.tick(10)  # 控制帧率
