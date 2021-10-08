# FileName: selectSquare.py
# Author: Jishan Ye
from psychopy import event, visual, core, monitors, logging
import numpy as np
import random, sys

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
# 随机生成小方块的坐标点
# 因为小方块都是屏幕顶部运动，因为位置有一定规律，即X值变化，Y值固定
# 需要随机生成X值，再根据小方块边长，即可确定小方块四个点的坐标
# step 1.2.2: 小方块的运动
# 每次落下的数量随机，在3~5之间
# 可采取不放回抽样

# step 1.3 试次退出条件
# - 选中 0，Miss 4，C(4, 0) = 1 种可能
# - 选中 1，Miss 3，C(4, 1) = 4 种可能
# - 选中 2，Miss 2，C(4, 2) = 6 种可能
# - 选中 3，Miss 1，C(4, 3) = 4 种可能
# - 选中 4，Miss 0，C(4, 4) = 1 种可能

# step 1.4: 行为因变量
# step 1.4.1: 反应时
# 定义：如果被试选择正确，则返回被试进入第一个方块的时间-进入第二个方块的时间
# step 1.4.2: 错误率
# 定义：被试在选择第一个方块后，没有进入位置相反的方块
# 怎么样计算？？
# step 1.4.3: Miss率
# 定义：被试没有选择的小方块，掉出屏幕
# step 1.4.4: 任务时间
# 定义：一个试次中，任务开始到结束的时间

# step 1.5 Dlg信息
# 被试姓名、年龄、等等

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
rv_red = [(-960, 360), (-400, 360), (-400, -360), (-960, -360)]
rv_green = [(400, 360), (960, 360), (960, -360), (400, -360)]
rv_blue = [(-400, 540), (400, 540), (400, 360), (-400, 360)]
rv_yellow = [(-400, -360), (400, -360), (400, -540), (-400, -540)]

# speed of small rectangle
# speed_lists = np.random.randint(3, 7, 4)
speed_lists = np.random.randint(1, 4, 4)

# 小方块的左上点x坐标
s_rv_dot = []
s_rv_dot_begin = -380
for i in range(20):
    s_rv_dot.append(s_rv_dot_begin)
    s_rv_dot_begin += 35

# side length of small rectangle
s_rv_len = 30

# generate the list that contains small rect vertices
s_rv_vertices = []
for i in s_rv_dot:
    s_rv_vertices.append(
        [(i, 540), (i + s_rv_len, 540),
         (i + s_rv_len, 540 - s_rv_len), (i, 540 - s_rv_len)]
    )

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

# define a TextStim to draw text
msg = visual.TextStim(win=win, text='', color='white', units='pix')

# open a file to write data
file_name = ''
head_line = map(str, ['trial', 'rectangle', 'correct', 'wrong',
                      'miss', 'RT', 'trailTime'])
sub_data = open('test.csv', 'w')
sub_data.write(','.join(head_line) + '\n')


# show some instructions
def show_instruction():
    """
    a function for showing some instruction.
    :return:
    """
    msg = visual.TextStim(win=win, text=u'请按空格开始任务', color='white', units='pix', height=30)
    msg.draw()
    win.flip()
    key = event.waitKeys(keyList=['space'])


# define a function to run trials
def run_trial(pos_lists, speed_lists, trial_index):
    """
    a function to run trials.
    :param pos_lists: 小方块的初始位置
    :param speed_lists: 小方块的速度
    :param trial_index: 试次数
    :return:
    """
    # set small rect
    s_rect_red = visual.ShapeStim(win, vertices=pos_lists[0], fillColor='red',
                                  lineColor=None)
    s_rect_green = visual.ShapeStim(win, vertices=pos_lists[1], fillColor='green',
                                    lineColor=None)
    s_rect_blue = visual.ShapeStim(win, vertices=pos_lists[2], fillColor='blue',
                                   lineColor=None)
    s_rect_yellow = visual.ShapeStim(win, vertices=pos_lists[3], fillColor='yellow',
                                     lineColor=None)

    # define the select state of square as False
    red_selected = False
    green_selected = False
    blue_selected = False
    yellow_selected = False

    # define the select state of small rect as False
    s_red_selected = False
    s_green_selected = False
    s_blue_selected = False
    s_yellow_selected = False

    # define the small rect out the screen as False
    s_red_out = False
    s_green_out = False
    s_blue_out = False
    s_yellow_out = False

    # define wrong select counts
    red_wrong = 0
    green_wrong = 0
    blue_wrong = 0
    yellow_wrong = 0

    # set a timer
    t = core.getTime()

    # draw a cross FIXATION
    while core.getTime() - t <= 0.5:
        msg.setText('+')
        msg.height = 50
        msg.draw()
        win.flip()

    # draw rect
    while not mouse.isPressedIn(rect_red):

        mouse_zone.pos = mouse.getPos()

        # if the mouse fall in the big rect
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

        if not (s_red_selected and s_green_selected):
            # if do a right select
            if red_selected and green_selected:
                # print(abs(red_time - green_time))
                if red_time - green_time < 0:
                    s_rect_red.opacity = 0
                    s_red_selected = True
                    RT_red = abs(red_time - green_time)
                    print('r: ' + str(RT_red))
                else:
                    s_rect_green.opacity = 0
                    s_green_selected = True
                    RT_green = abs(red_time - green_time)
                    print('g: ' + str(RT_green))
                green_selected = False
                red_selected = False
        if not (s_blue_selected and s_yellow_selected):
            # if do a right select
            if blue_selected and yellow_selected:
                if blue_time - yellow_time < 0:
                    s_rect_blue.opacity = 0
                    s_blue_selected = True
                    RT_blue = abs(blue_time - yellow_time)
                    print('b: ' + str(RT_blue))
                else:
                    s_rect_yellow.opacity = 0
                    s_yellow_selected = True
                    RT_yellow = abs(blue_time - yellow_time)
                    print('y: ' + str(RT_yellow))
                yellow_selected = False
                blue_selected = False

        # if do a WRONG selected from red rect
        if red_selected:
            if blue_selected:  # red --> blue --> green
                red_wrong += 1
                print('r: ' + str(red_wrong))
                blue_selected = False
                red_selected = False
            if yellow_selected:  # red --> yellow --> green
                red_wrong += 1
                print('r: ' + str(red_wrong))
                yellow_selected = False
                red_selected = False

        # if do a WRONG selected from blue rect
        if blue_selected:
            if red_selected:  # blue --> red --> yellow
                blue_wrong += 1
                print('b: ' + str(blue_wrong))
                red_selected = False
                blue_selected = False
            if green_selected:  # blue --> green --> yellow
                blue_wrong += 1
                print('b: ' + str(blue_wrong))
                green_selected = False
                blue_selected = False

        # if do a WRONG selected from green rect
        if green_selected:
            if blue_selected:  # green --> blue --> red
                green_wrong += 1
                print('g: ' + str(green_wrong))
                blue_selected = False
                green_selected = False
            if yellow_selected:  # green --> yellow --> red
                green_wrong += 1
                print('g: ' + str(green_wrong))
                yellow_selected = False
                green_selected = False

        # if do a WRONG selected from yellow rect
        if yellow_selected:
            if red_selected:  # yellow --> red --> blue
                yellow_wrong += 1
                print('y: ' + str(yellow_wrong))
                red_selected = False
                yellow_selected = False
            if green_selected:  # yellow --> green --> blue
                yellow_wrong += 1
                print('y: ' + str(yellow_wrong))
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

        # print('red pos: ' + str(s_rect_red.pos[1]))

        if s_rect_red.pos[1] < -1080 and not s_red_selected:
            s_red_out = True
            RT_red = 'NA'
        if s_rect_green.pos[1] < -1080 and not s_green_selected:
            s_green_out = True
            RT_green = 'NA'
        if s_rect_blue.pos[1] < -1080 and not s_blue_selected:
            s_blue_out = True
            RT_blue = 'NA'
        if s_rect_yellow.pos[1] < -1080 and not s_yellow_selected:
            s_yellow_out = True
            RT_yellow = 'NA'

        # define some rules to exit trail
        # 选中0，错过1，C(4, 0) = 1种可能
        if s_red_out and s_green_out and s_blue_out and s_yellow_out:  # 0 selected, miss 4
            break

        # 选中4，错过0，C(4, 4) = 1种可能
        elif s_red_selected and s_green_selected and s_blue_selected and s_yellow_selected:  # 4 selected, miss 0
            break

        # 选中1，错过3，C(4, 1) = 4种可能
        elif s_red_selected and s_green_out and s_blue_out and s_yellow_out:  # 1 red selected, miss 3
            break
        elif s_green_selected and s_red_out and s_blue_out and s_yellow_out:  # 1 green selected, miss 3
            break
        elif s_blue_selected and s_red_out and s_green_out and s_yellow_out:  # 1 blue selected, miss 3
            break
        elif s_yellow_selected and s_red_out and s_green_out and s_blue_out:  # 1 yellow selected, miss 3
            break

        # 选中2，错过2，C(4, 2) = 6种可能
        elif s_red_selected and s_green_selected and s_blue_out and s_yellow_out:  # 2 red, green selected, miss 2
            break
        elif s_red_selected and s_blue_selected and s_green_out and s_yellow_out:  # 2 red, blue selected, miss 2
            break
        elif s_red_selected and s_yellow_selected and s_green_out and s_blue_out:  # 2 red, yellow selected, miss 2
            break
        elif s_green_selected and s_blue_selected and s_red_out and s_yellow_out:  # 2 green, blue selected, miss 2
            break
        elif s_green_selected and s_yellow_selected and s_red_out and s_blue_out:  # 2 green, yellow selected, miss 2
            break
        elif s_blue_selected and s_yellow_selected and s_red_out and s_green_out:  # 2 blue, yellow selected, miss 2
            break

        # 选中3，错过1，C(4, 3) = 4种可能
        elif s_red_selected and s_green_selected and s_blue_selected and s_yellow_out:  # 3 r, g, b selected, miss 1
            break
        elif s_red_selected and s_green_selected and s_yellow_selected and s_blue_out:  # 3 r, g, y selected, miss 1
            break
        elif s_red_selected and s_blue_selected and s_yellow_selected and s_green_out:  # 3 r, b, y selected, miss 1
            break
        elif s_green_selected and s_blue_selected and s_yellow_selected and s_red_out:  # 3 g, b, y selected, miss 1
            break

    # get trail time
    trial_time = core.getTime() - t

    # write trial info to CSV
    red_data = [trial_index, 'red', s_red_selected, red_wrong, s_red_out, RT_red, trial_time]
    sub_data.write(','.join(map(str, red_data)) + '\n')
    green_data = [trial_index, 'green', s_green_selected, green_wrong, s_green_out, RT_green, trial_time]
    sub_data.write(','.join(map(str, green_data)) + '\n')
    blue_data = [trial_index, 'blue', s_blue_selected, blue_wrong, s_blue_out, RT_blue, trial_time]
    sub_data.write(','.join(map(str, blue_data)) + '\n')
    yellow_data = [trial_index, 'yellow', s_yellow_selected, yellow_wrong, s_yellow_out, RT_yellow, trial_time]
    sub_data.write(','.join(map(str, yellow_data)) + '\n')


show_instruction()

random.Random(12345).shuffle(s_rv_vertices)
trial_index = 1
for i in range(10):
    s_rv_lists = random.sample(s_rv_vertices, k=4)  # random sample
    print(s_rv_lists)
    run_trial(s_rv_lists, speed_lists, trial_index)
    trial_index += 1

sub_data.close()

win.close()
core.quit()
