# FileName: selectSquare.py
# Author: Jishan Ye
from psychopy import event, visual, core, monitors, logging
from psychopy.tools.monitorunittools import posToPix
import numpy as np
import random

# 思路
# step 1：搭建界面

# step 1.1: 四个大方块；
# step 1.1.1: 大方块生成
# 注意填充色、线条颜色，位置
# 位置可以通过列表预先定义，颜色使用系统默认RGB
# step 1.1.2 大方块被选中后的效果
# 当实现落入大方块位置后，改变大方块填充颜色
# 填充为纯黑，将透明度设置为0.6，以突出眼动指示圈

# step 1.2: 小方块
# step 1.2.1: 小方块的生成
# -----------弃用------------
# 小方块可以采用图片形式，清晰度更高
# 注意颜色和大方块颜色的对应，可以先找好Psychopy中对应颜色的RGB值
# -----------弃用------------
# 随机生成小方块的坐标点
# 因为小方块都是屏幕顶部运动，因为位置有一定规律，即X值变化，Y值固定
# 需要随机生成X值，再根据小方块边长，即可确定小方块四个点的坐标
# step 1.2.2: 小方块的运动
# 每次落下的数量随机，在3~5之间
# 可采取不放回抽样


# step 2: 眼动部分
# step 2.1: 眼动位置指示
# 设置一个圆形，它的位置随眼动变化
# 以告诉被试目前视线再屏幕上的地方
# step 2.2: 计算扫视部分
# step 2.2.1: 计算规则
# 如果眼睛位置落入区域100ms，则为成功
# 两个大方块之间的扫视要在1000ms内完成
# step 2.2.2: 计算原理
#

# dummy_mode
dummy_mode = True

# full_screen or not
full_screen = False

# screen size
scn_width, scn_height = (1920, 1080)

# rect_vertices
rv_red = [(-960, 180), (-400, 180), (-400, -180), (-960, -180), ]
rv_green = [(400, 180), (960, 180), (960, -180), (400, -180)]
rv_blue = [(-400, 540), (400, 540), (400, 180), (-400, 180)]
rv_yellow = [(-400, -180), (400, -180), (400, -540), (-400, -540)]

# small rectangle vertices
# generate the ten X position
s_rv_dot = np.random.randint(-420, 420, 4)

# side length of small rectangle
s_rv_len = 30

# speed of small rectangle
# speed_lists = np.random.randint(3, 7, 4)
speed_lists = np.random.randint(1, 4, 4)

# generate the list that contains small rect vertices
s_rv_vertices = []
for i in s_rv_dot:
    s_rv_vertices.append(
        [(i, 540), (i + s_rv_len, 540),
         (i + s_rv_len, 540 - s_rv_len), (i, 540 - s_rv_len)]
    )

random.Random(12345).shuffle(s_rv_vertices)
s_rv_lists = random.sample(s_rv_vertices, k=4)  # random sample
t = s_rv_vertices[0]
print(s_rv_lists)

# print(s_rv_vertices)

# x = 0
#
#
# s_rv_red = [(x, 540), (x + s_rv_len, 540),
#             (s_rv_len, 540 - s_rv_len), (x, 540 - s_rv_len)]

# s_rv_red = [(0, 540), (30, 540), (30, 510), (0, 510)]

# create a Monitor object
my_mon = monitors.Monitor(name='mon', width=55.3, distance=60, )
my_mon.setSizePix((scn_width, scn_height))

# open a window
win = visual.Window(size=(scn_width, scn_height), fullscr=full_screen,
                    monitor=my_mon, units='pix', )

# create a mouse
mouse = event.Mouse()

win.mouseVisible = False

# define a zone just to show mouse
mouse_zone = visual.Circle(win, radius=10, edges=50, )

# set rect frame
rect_red = visual.ShapeStim(win, vertices=rv_red, fillColor='grey', lineWidth=2,
                            lineColor='red')
rect_green = visual.ShapeStim(win, vertices=rv_green, fillColor='grey', lineWidth=2,
                              lineColor='green')
rect_blue = visual.ShapeStim(win, vertices=rv_blue, fillColor='grey', lineWidth=2,
                             lineColor='blue')
rect_yellow = visual.ShapeStim(win, vertices=rv_yellow, fillColor='grey', lineWidth=2,
                               lineColor='yellow')

# set small rect
s_rect_red = visual.ShapeStim(win, vertices=s_rv_lists[0], fillColor='red',
                              lineColor=None)
s_rect_green = visual.ShapeStim(win, vertices=s_rv_lists[1], fillColor='green',
                                lineColor=None)
s_rect_blue = visual.ShapeStim(win, vertices=s_rv_lists[2], fillColor='blue',
                               lineColor=None)
s_rect_yellow = visual.ShapeStim(win, vertices=s_rv_lists[3], fillColor='yellow',
                                 lineColor=None)

# define some lists that contains rect mark
# test_lists = {'first_select': '', 'secdond_select': ''}
# test_lists = []

# define the select state of square as False
red_selected = False
green_selected = False
blue_selected = False
yellow_selected = False

# set a timer
t = core.getTime()

# draw rect
while not mouse.isPressedIn(rect_red):

    mouse_zone.pos = mouse.getPos()

    if rect_red.contains(mouse):
        rect_red.fillColor = 'black'
        rect_red.opacity = 0.6
        red_selected = True
        red_time = core.getTime() - t
    else:
        rect_red.fillColor = 'grey'
        rect_red.opacity = 1

    if rect_green.contains(mouse):
        rect_green.fillColor = 'black'
        rect_green.opacity = 0.6
        green_selected = True
        green_time = core.getTime() - t
    else:
        rect_green.fillColor = 'grey'
        rect_green.opacity = 1

    if rect_blue.contains(mouse):
        rect_blue.fillColor = 'black'
        rect_blue.opacity = 0.6
        blue_selected = True
        blue_time = core.getTime() - t
    else:
        rect_blue.fillColor = 'grey'
        rect_blue.opacity = 1

    if rect_yellow.contains(mouse):
        rect_yellow.fillColor = 'black'
        rect_yellow.opacity = 0.6
        yellow_selected = True
        yellow_time = core.getTime() - t
    else:
        rect_yellow.fillColor = 'grey'
        rect_yellow.opacity = 1

    # if do a right select
    if red_selected and green_selected:
        print('red: ' + str(red_time))
        print('green: ' + str(green_time))
        if red_time - green_time < 0:
            s_rect_red.fillColor = 'grey'
        else:
            s_rect_green.fillColor = 'grey'

        green_selected = False
        red_selected = False
    elif blue_selected and yellow_selected:
        print('blue: ' + str(blue_time))
        print('yellow: ' + str(yellow_time))
        if blue_time - yellow_time < 0:
            s_rect_blue.fillColor = 'grey'
        else:
            s_rect_yellow.fillColor = 'grey'

        yellow_selected = False
        blue_selected = False

    # if do a WRONG selected
    if red_selected:
        if blue_selected:  # red --> blue --> green
            blue_selected = False
            red_selected = False
        if yellow_selected:  # red --> yellow --> green
            yellow_selected = False
            red_selected = False

    # if do a WRONG selected
    if blue_selected:
        if red_selected:  # blue --> red --> yellow
            red_selected = False
            blue_selected = False
        if green_selected:  # blue --> green --> yellow
            green_selected = False
            blue_selected = False

    # if do a WRONG selected
    if green_selected:
        if blue_selected:  # green --> blue --> red
            blue_selected = False
            green_selected = False
        if yellow_selected:  # green --> yellow --> red
            yellow_selected = False
            green_selected = False

    # if do a WRONG selected
    if yellow_selected:
        if red_selected:  # yellow --> red --> blue
            red_selected = False
            yellow_selected = False
        if green_selected:  # yellow --> green --> blue
            green_selected = False
            yellow_selected = False

    # draw mouse zone
    mouse_zone.draw()

    # draw rect frame
    rect_red.draw()
    rect_green.draw()
    rect_blue.draw()
    rect_yellow.draw()

    # draw small rect
    s_rect_red.draw()
    s_rect_green.draw()
    s_rect_blue.draw()
    s_rect_yellow.draw()

    # set the speed of small rect
    s_rect_red.pos -= (0, speed_lists[0])
    s_rect_green.pos -= (0, speed_lists[1])
    s_rect_blue.pos -= (0, speed_lists[2])
    s_rect_yellow.pos -= (0, speed_lists[3])

    win.flip()

    # if s_rect_red.pos[-1] < -1080:
    #     break
    # define some rules to abort trial


win.close()
core.quit()
