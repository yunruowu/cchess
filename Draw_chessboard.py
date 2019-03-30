import pygame
import pygame.font
import sys
import traceback
import copy
from math import sqrt
from pygame.locals import *

pygame.font.init()
pygame.init()

# 用于判断是取棋还是落棋
running = True
# 定义棋子半径
r = 40


# 绘制棋盘
def Draw_a_chessboard(screen):
    # 填充背景色
    screen.fill((233, 204, 138))
    # 画外框
    outer_frame_color = (60, 20, 0)
    pygame.draw.rect(screen, outer_frame_color, [80, 80, 830, 740], 5)
    # 行
    inner_frame_color = (0, 0, 0)
    for i in range(1, 10):
        pygame.draw.line(screen, inner_frame_color, (90, 90 * i), (900, 90 * i))
        # 列
    for i in range(1, 11):
        pygame.draw.line(screen, inner_frame_color, (90 * i, 90), (90 * i, 810))
    # ‘将’
    jiang_rote_color = (0, 0, 0)
    pygame.draw.lines(screen, jiang_rote_color, True, [(90, 360), (270, 360), (270, 540), (90, 540)], 3)
    pygame.draw.lines(screen, jiang_rote_color, True, [(720, 360), (900, 360), (900, 540), (720, 540)], 3)
    # ‘士’路线
    shi_rote_color = (0, 0, 0)
    pygame.draw.line(screen, shi_rote_color, (90, 360), (270, 540), 3)
    pygame.draw.line(screen, shi_rote_color, (90, 540), (270, 360), 3)
    pygame.draw.line(screen, shi_rote_color, (720, 360), (900, 540), 3)
    pygame.draw.line(screen, shi_rote_color, (720, 540), (900, 360), 3)
    # ‘象’路线
    xiang_rote_color = (0, 0, 0)
    pygame.draw.lines(screen, xiang_rote_color, True, [(270, 450), (90, 270), (270, 90), (450, 270)])
    pygame.draw.lines(screen, xiang_rote_color, True, [(270, 450), (90, 630), (270, 810), (450, 630)])
    pygame.draw.lines(screen, xiang_rote_color, True, [(720, 450), (900, 270), (720, 90), (540, 270)])
    pygame.draw.lines(screen, xiang_rote_color, True, [(720, 450), (900, 630), (720, 810), (540, 630)])
    # ‘兵’,用抗锯齿连续线段
    bing_rote_color = (255, 0, 0)
    for j in range(0, 2):
        for k in range(0, 4):
            pygame.draw.aalines(screen, bing_rote_color, False,
                                [(330 + 270 * j, 260 + 180 * k), (350 + 270 * j, 260 + 180 * k),
                                 (350 + 270 * j, 240 + 180 * k)], 3)
            pygame.draw.aalines(screen, bing_rote_color, False,
                                [(390 + 270 * j, 260 + 180 * k), (370 + 270 * j, 260 + 180 * k),
                                 (370 + 270 * j, 240 + 180 * k)], 3)
            pygame.draw.aalines(screen, bing_rote_color, False,
                                [(330 + 270 * j, 100 + 180 * k), (350 + 270 * j, 100 + 180 * k),
                                 (350 + 270 * j, 120 + 180 * k)], 3)
            pygame.draw.aalines(screen, bing_rote_color, False,
                                [(390 + 270 * j, 100 + 180 * k), (370 + 270 * j, 100 + 180 * k),
                                 (370 + 270 * j, 120 + 180 * k)], 3)
    # ‘炮’
    pao_rote_color = (255, 0, 0)
    for m in range(0, 2):
        for n in range(0, 2):
            pygame.draw.aalines(screen, pao_rote_color, False,
                                [(240 + 450 * m, 170 + 540 * n), (260 + 450 * m, 170 + 540 * n),
                                 (260 + 450 * m, 150 + 540 * n)], 3)
            pygame.draw.aalines(screen, pao_rote_color, False,
                                [(300 + 450 * m, 170 + 540 * n), (280 + 450 * m, 170 + 540 * n),
                                 (280 + 450 * m, 150 + 540 * n)], 3)
            pygame.draw.aalines(screen, pao_rote_color, False,
                                [(240 + 450 * m, 190 + 540 * n), (260 + 450 * m, 190 + 540 * n),
                                 (260 + 450 * m, 210 + 540 * n)], 3)
            pygame.draw.aalines(screen, pao_rote_color, False,
                                [(300 + 450 * m, 190 + 540 * n), (280 + 450 * m, 190 + 540 * n),
                                 (280 + 450 * m, 210 + 540 * n)], 3)

    # 绘制‘楚河汉界’
    pygame.draw.rect(screen, [233, 204, 138], [451, 91, 89, 719])
    chuhehanjie = pygame.image.load("楚河汉界.png").convert_alpha()
    screen.blit(chuhehanjie, (451, 91))
    # 画‘悔棋’，‘重新开始’和‘退出’按钮
    button_color = (163, 80, 21)
    pygame.draw.rect(screen, button_color, [980, 300, 200, 100], 5)
    pygame.draw.rect(screen, button_color, [980, 500, 200, 100], 5)
    pygame.draw.rect(screen, button_color, [980, 700, 200, 100], 5)

    s_font = pygame.font.Font('anjian_font.ttf', 45)

    text1 = s_font.render("悔    棋", True, button_color)
    text2 = s_font.render("重新开始", True, button_color)
    text3 = s_font.render("退出游戏", True, button_color)
    screen.blit(text1, (1000, 320))
    screen.blit(text2, (980, 520))
    screen.blit(text3, (980, 720))


# 绘制棋子
def Draw_a_chessman(screen, color, qizi, x, y):
    red_color = (255, 0, 0)
    black_color = (0, 0, 0)

    pygame.draw.circle(screen, (0, 0, 0), (x, y), 46)
    pygame.draw.circle(screen, (247, 157, 12), (x, y), 45)
    pygame.draw.circle(screen, (0, 0, 0), (x, y), 40, 3)
    pygame.draw.circle(screen, (181, 131, 16), (x, y), 35)

    q_font = pygame.font.Font('qizi_font.ttf', 60)

    if color == 'red':
        q_color = red_color
    elif color == 'black':
        q_color = black_color

    screen.blit(q_font.render(qizi[0], True, q_color), (x - 30, y - 40))


# 绘制带有棋盘的棋子
def Draw_a_chessboard_with_chessman(map, screen):
    Draw_a_chessboard(screen)
    for each_qizi in hongqi.keys():
        Draw_a_chessman(screen, hongqi[each_qizi]['color'], each_qizi, hongqi[each_qizi]['now_weizhi'][0],
                        hongqi[each_qizi]['now_weizhi'][1])
    for each_qizi in heiqi.keys():
        Draw_a_chessman(screen, heiqi[each_qizi]['color'], each_qizi, heiqi[each_qizi]['now_weizhi'][0],
                        heiqi[each_qizi]['now_weizhi'][1])


# 通过位置寻找棋子
def find(x, y):
    for key in hongqi.keys():
        if sqrt((hongqi[key]['now_weizhi'][0] - x) ** 2 + (hongqi[key]['now_weizhi'][1] - y) ** 2) < r:
            return [key, hongqi[key]]
    for key in heiqi.keys():
        if sqrt((heiqi[key]['now_weizhi'][0] - x) ** 2 + (heiqi[key]['now_weizhi'][1] - y) ** 2) < r:
            return [key, heiqi[key]]


# 判断该位置有无棋子
def weizhi_panduan(x, y):
    for key in hongqi.keys():
        if [x, y] == hongqi[key]['now_weizhi']:
            return True
    for key in heiqi.keys():
        if [x, y] == heiqi[key]['now_weizhi']:
            return True
    return False


def main():
    # 将'hongqi','heiqi','running','order',设置为可改
    global hongqi, heiqi, running, order

    # 棋子初始位置
    hongqi = {'将': {'color': 'red', 'now_weizhi': [90, 450]}, '士1': {'color': 'red', 'now_weizhi': [90, 360]},
              '士2': {'color': 'red', 'now_weizhi': [90, 540]}, '相1': {'color': 'red', 'now_weizhi': [90, 270]},
              '相2': {'color': 'red', 'now_weizhi': [90, 630]}, '马1': {'color': 'red', 'now_weizhi': [90, 180]},
              '马2': {'color': 'red', 'now_weizhi': [90, 720]}, '车1': {'color': 'red', 'now_weizhi': [90, 90]},
              '车2': {'color': 'red', 'now_weizhi': [90, 810]}, '炮1': {'color': 'red', 'now_weizhi': [270, 180]},
              '炮2': {'color': 'red', 'now_weizhi': [270, 720]}, '兵1': {'color': 'red', 'now_weizhi': [360, 90]},
              '兵2': {'color': 'red', 'now_weizhi': [360, 270]}, '兵3': {'color': 'red', 'now_weizhi': [360, 450]},
              '兵4': {'color': 'red', 'now_weizhi': [360, 630]}, '兵5': {'color': 'red', 'now_weizhi': [360, 810]}
              }
    heiqi = {'将': {'color': 'black', 'now_weizhi': [900, 450]}, '士1': {'color': 'black', 'now_weizhi': [900, 360]},
             '士2': {'color': 'black', 'now_weizhi': [900, 540]}, '相1': {'color': 'black', 'now_weizhi': [900, 270]},
             '相2': {'color': 'black', 'now_weizhi': [900, 630]}, '马1': {'color': 'black', 'now_weizhi': [900, 180]},
             '马2': {'color': 'black', 'now_weizhi': [900, 720]}, '车1': {'color': 'black', 'now_weizhi': [900, 90]},
             '车2': {'color': 'black', 'now_weizhi': [900, 810]}, '炮1': {'color': 'black', 'now_weizhi': [720, 180]},
             '炮2': {'color': 'black', 'now_weizhi': [720, 720]}, '兵1': {'color': 'black', 'now_weizhi': [630, 90]},
             '兵2': {'color': 'black', 'now_weizhi': [630, 270]}, '兵3': {'color': 'black', 'now_weizhi': [630, 450]},
             '兵4': {'color': 'black', 'now_weizhi': [630, 630]}, '兵5': {'color': 'black', 'now_weizhi': [630, 810]}
             }

    # 定义棋子半径
    r = 40

    # 定义两个存储棋子现在的状态
    backups1 = []
    backups2 = []

    # 创建一个窗口
    screen = pygame.display.set_mode([1200, 900])
    # 设置窗口标题
    pygame.display.set_caption("中国象棋")
    # 在窗口画出棋盘以及按钮
    Draw_a_chessboard(screen)
    clock = pygame.time.Clock()

    while True:
        Draw_a_chessboard_with_chessman(map, screen)
        pygame.display.flip()
        # 监听所有事件
        for event in pygame.event.get():
            # 点击x则关闭窗口
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    # 鼠标第一次按下选择棋子
                    if running:
                        x, y = event.pos[0], event.pos[1]
                        for key in hongqi.keys():
                            if sqrt((hongqi[key]['now_weizhi'][0] - x) ** 2 + (
                                    hongqi[key]['now_weizhi'][1] - y) ** 2) < r:
                                backups1 = [key, hongqi[key]]
                        for key in heiqi.keys():
                            if sqrt((heiqi[key]['now_weizhi'][0] - x) ** 2 + (
                                    heiqi[key]['now_weizhi'][1] - y) ** 2) < r:
                                backups2 = [key, heiqi[key]]
                        if backups1:
                            # 用于暂存棋子状态
                            backups3 = copy.deepcopy(backups1)
                            hongqi.pop(backups1[0])
                            running = not running
                        elif backups2:
                            # 用于暂存棋子状态
                            backups4 = copy.deepcopy(backups2)
                            heiqi.pop(backups2[0])
                            running = not running
                    # 鼠标再次按下，落下棋子
                    else:
                        if r < event.pos[0] < 900 + r and r < event.pos[1] < 810 + r:
                            x = (event.pos[0] + r) // 90 * 90
                            y = (event.pos[1] + r) // 90 * 90

                            if backups1:  # 红棋
                                # 判断所走位置是否有棋子
                                if weizhi_panduan(x, y):
                                    hongqi[backups3[0]] = backups3[1]
                                else:
                                    hongqi[backups1[0]] = backups1[1]
                                    hongqi[backups1[0]]['now_weizhi'] = [x, y]

                                backups1 = []
                                running = not running
                            elif backups2:  # 黑棋
                                if weizhi_panduan(x, y):
                                    heiqi[backups4[0]] = backups4[1]
                                else:
                                    heiqi[backups2[0]] = backups2[1]
                                    heiqi[backups2[0]]['now_weizhi'] = [x, y]
                                backups2 = []
                                running = not running
                        else:
                            if backups1:
                                hongqi[backups1[0]] = backups3[1]
                                backups1 = []
                                running = not running
                            elif backups2:
                                heiqi[backups2[0]] = backups4[1]
                                backups2 = []
                                running = not running


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()