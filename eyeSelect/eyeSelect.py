# FileName: selectSquare.py
# Author: Jishan Ye
from psychopy import event, visual, core, monitors, gui
from string import digits, ascii_letters
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
import numpy as np
import random, sys, logging, os, time, pylink
from pylink import *


# 配置log信息
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

# dummy_mode
dummy_mode = False

# full_screen or not
full_screen = True

# 停留在大方块多长秒才能选中
stay_time = 0.1

# screen size
scn_width, scn_height = (1920, 1080)

# 在1 - 4 之间随机生成4个整数，为小方块下落的速度
# speed_lists = np.random.randint(3, 7, 4)
speed_lists = np.random.randint(1, 4, 4)

# 小方块的左上点x坐标
s_rv_dot = []
s_rv_dot_begin = -380
for i in range(20):
    s_rv_dot.append(s_rv_dot_begin)
    s_rv_dot_begin += 35

# 小方块的边长
s_rv_len = 30

# 根据小方块左上点x坐标和边长，生成小方块其他点的坐标
s_rv_vertices = []
for i in s_rv_dot:
    s_rv_vertices.append(
        [(i, 540), (i + s_rv_len, 540),
         (i + s_rv_len, 540 - s_rv_len), (i, 540 - s_rv_len)]
    )

# 输入被试信息
while True:
    dlg = gui.Dlg(title=r'输入被试信息')
    dlg.addField(u'编号：')
    dlg.addField(u'姓名：', )
    dlg.addField(u'性别（1-男；2-女）：')
    ok_data = dlg.show()
    if dlg.OK:
        # print(ok_data)
        print('EDF data filename: {} - {} - {}'.format(ok_data[0],
                                                       ok_data[1], ok_data[2]))
    else:
        print(u'取消')
        core.quit()
        sys.exit()

    edf_name = dlg.data[0] + dlg.data[1] + dlg.data[2]
    allowed_char = ascii_letters + digits + '_'
    if not all([c in allowed_char for c in allowed_char]):
        print('ERROR: Invalid EDF filename.')
    elif len(edf_name) > 8:
        print('ERROR: EDF filename should not exceed 8 characters.')
    else:
        break

# set up a folder to store the EDF data files and the associated resources
# e.g., files defining the interest areas used in each trial
results_folder = os.path.join(os.path.dirname(__file__), 'results/expSelect/eyeData')
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

# We download EDF data file from the EyeLink Host PC to the local hard
# drive at the end of each testing session, here we rename the EDF to
# include session start date/time
time_str = time.strftime("_%Y_%m_%d_%H_%M", time.localtime())
session_identifier = edf_name + time_str

# create a folder for the current testing session in the "results" folder
session_folder = os.path.join(results_folder, session_identifier)
if not os.path.exists(session_folder):
    os.makedirs(session_folder)

# create a 'aoi' folder to save the VFRAME commands for each trial
aoi_folder = os.path.join(session_folder, 'aoi')
if not os.path.exists(aoi_folder):
    os.makedirs(aoi_folder)

# Step 1: Connect to the EyeLink Host PC
#
# The Host IP address, by default, is "100.1.1.1".
# the "el_tracker" objected created here can be accessed through the Pylink
# Set the Host PC address to "None" (without quotes) to run the script
# in "Dummy Mode"
if dummy_mode:
    el_tracker = pylink.EyeLink(None)
else:
    try:
        el_tracker = pylink.EyeLink("100.1.1.1")
    except RuntimeError as error:
        print('ERROR:', error)
        core.quit()
        sys.exit()

# Step 2: Open an EDF data file on the Host PC
edf_file = edf_name + ".EDF"
try:
    el_tracker.openDataFile(edf_file)
except RuntimeError as err:
    print('ERROR:', err)
    # close the link if we have one open
    if el_tracker.isConnected():
        el_tracker.close()
    core.quit()
    sys.exit()

# Add a header text to the EDF file to identify the current experiment name
# This is OPTIONAL. If your text starts with "RECORDED BY " it will be
# available in DataViewer's Inspector window by clicking
# the EDF session node in the top panel and looking for the "Recorded By:"
# field in the bottom panel of the Inspector.
preamble_text = 'RECORDED BY %s' % os.path.basename(__file__)
el_tracker.sendCommand("add_file_preamble_text '%s'" % preamble_text)

# Step 3: Configure the tracker
#
# Put the tracker in offline mode before we change tracking parameters
el_tracker.setOfflineMode()

# Get the software version:  1-EyeLink I, 2-EyeLink II, 3/4-EyeLink 1000,
# 5-EyeLink 1000 Plus, 6-Portable DUO
eyelink_ver = 0  # set version to 0, in case running in Dummy mode
if not dummy_mode:
    vstr = el_tracker.getTrackerVersionString()
    eyelink_ver = int(vstr.split()[-1].split('.')[0])
    # print out some version info in the shell
    print('Running experiment on %s, version %d' % (vstr, eyelink_ver))

# File and Link data control
# what eye events to to save in the EDF file, include everything by default
file_event_flags = 'LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT'
# what eye events to make available over the link, include everything by default
link_event_flags = 'LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON,FIXUPDATE,INPUT'
# what sample data to save in the EDF data file and to make available
# over the link, include the 'HTARGET' flag to save head target sticker
# data for supported eye trackers
if eyelink_ver > 3:
    file_sample_flags = 'LEFT,RIGHT,GAZE,HREF,RAW,AREA,HTARGET,GAZERES,BUTTON,STATUS,INPUT'
    link_sample_flags = 'LEFT,RIGHT,GAZE,GAZERES,AREA,HTARGET,STATUS,INPUT'
else:
    file_sample_flags = 'LEFT,RIGHT,GAZE,HREF,RAW,AREA,GAZERES,BUTTON,STATUS,INPUT'
    link_sample_flags = 'LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,INPUT'
el_tracker.sendCommand("file_event_filter = %s" % file_event_flags)
el_tracker.sendCommand("file_sample_data = %s" % file_sample_flags)
el_tracker.sendCommand("link_event_filter = %s" % link_event_flags)
el_tracker.sendCommand("link_sample_data = %s" % link_sample_flags)

# Optional tracking parameters
# Sample rate, 250, 500, 1000, or 2000, check your tracker specification
# if eyelink_ver > 2:
#     el_tracker.sendCommand("sample_rate 1000")
# Choose a calibration type, H3, HV3, HV5, HV13 (HV = horizontal/vertical),
el_tracker.sendCommand("calibration_type = HV5")
# Set a gamepad button to accept calibration/drift check target
# You need a supported gamepad/button box that is connected to the Host PC
el_tracker.sendCommand("button_function 5 'accept_target_fixation'")

# 大方块的坐标
rv_red = [(-960, 360), (-400, 360), (-400, -360), (-960, -360)]
rv_green = [(400, 360), (960, 360), (960, -360), (400, -360)]
rv_blue = [(-400, 540), (400, 540), (400, 360), (-400, 360)]
rv_yellow = [(-400, -360), (400, -360), (400, -540), (-400, -540)]

# create a Monitor object
my_mon = monitors.Monitor(name='mon', width=55.3, distance=60, )
my_mon.setSizePix((scn_width, scn_height))

# open a window
win = visual.Window(size=(scn_width, scn_height), fullscr=full_screen,
                    monitor=my_mon, units='pix', )

# Pass the display pixel coordinates (left, top, right, bottom) to the tracker
# see the Eyelink Installation Guide, "Customizing Screen Settings"
el_coords = "screen_pixel_coords = 0 0 %d %d" % (scn_width - 1, scn_height - 1)
el_tracker.sendCommand(el_coords)

# Write a DISPLAY_COORDS message to the EDF file
# Data Viewer needs this piece of info for proper visualization, see Data
# Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"
dv_coords = "DISPLAY_COORDS  0 0 %d %d" % (scn_width - 1, scn_height - 1)
el_tracker.sendMessage(dv_coords)

# Configure a graphics environment (genv) for tracker calibration
genv = EyeLinkCoreGraphicsPsychoPy(el_tracker, win)
print(genv)  # print out the version number of the CoreGraphics library

# Set background and foreground colors for the calibration target
# in PsychoPy, (-1, -1, -1)=black, (1, 1, 1)=white, (0, 0, 0)=mid-gray
foreground_color = (-1, -1, -1)
background_color = win.color
genv.setCalibrationColors(foreground_color, background_color)

# Set up the calibration target
#
# The target could be a "circle" (default), a "picture", a "movie" clip,
# or a rotating "spiral". To configure the type of calibration target, set
# genv.setTargetType to "circle", "picture", "movie", or "spiral", e.g.,
# genv.setTargetType('picture')
#
# Use gen.setPictureTarget() to set a "picture" target
# genv.setPictureTarget(os.path.join('images', 'calibration_target.png'))
#
# Use genv.setMovieTarget() to set a "movie" target
# genv.setMovieTarget(os.path.join('videos', 'calibVid.mov'))

# Use the default calibration target ('circle')
genv.setTargetType('circle')

# Configure the size of the calibration target (in pixels)
# this option applies only to "circle" and "spiral" targets
genv.setTargetSize(25)

# Beeps to play during calibration, validation and drift correction
# parameters: target, good, error
#     target -- sound to play when target moves
#     good -- sound to play on successful operation
#     error -- sound to play on failure or interruption
# Each parameter could be ''--default sound, 'off'--no sound, or a wav file
genv.setCalibrationSounds('', '', '')

# Request Pylink to use the PsychoPy window we opened above for calibration
pylink.openGraphicsEx(genv)

# 创建Mouse类，用来初始化鼠标
mouse = event.Mouse()
win.mouseVisible = False

# 设置一个Circle，用来显示鼠标或眼动所在位置
mouse_zone = visual.Circle(win, radius=10, edges=50, )

# 设置大方块的相关属性
rect_red = visual.ShapeStim(win, vertices=rv_red, fillColor='grey', lineWidth=2,
                            lineColor='red')
rect_green = visual.ShapeStim(win, vertices=rv_green, fillColor='grey', lineWidth=2,
                              lineColor='green')
rect_blue = visual.ShapeStim(win, vertices=rv_blue, fillColor='grey', lineWidth=2,
                             lineColor='blue')
rect_yellow = visual.ShapeStim(win, vertices=rv_yellow, fillColor='grey', lineWidth=2,
                               lineColor='yellow')

# 定义TextStim，用来呈现文字
msg = visual.TextStim(win=win, text='', color='white', units='pix')

# 打开一个CSV文件，用来写行为数据
file_name = ''
head_line = map(str, ['trial', 'rectangle', 'correct', 'wrong',
                      'miss', 'RT', 'trailTime'])
sub_data = open('test.csv', 'w')
# 写入headline
sub_data.write(','.join(head_line) + '\n')


def clear_screen(win):
    """
    clear up the PsychoPy window
    :param win:
    :return:
    """
    win.fillColor = genv.getBackgroundColor()
    win.flip()


def show_msg(win, text, wait_for_keypress=True, any_key_to_terminate=True):
    """
    Show task instructions on screen
    :param win:
    :param text:
    :param wait_for_keypress:
    :param any_key_to_terminate:
    :return:
    """
    msg = visual.TextStim(win, text,
                          color=genv.getForegroundColor(),
                          wrapWidth=scn_width / 2,
                          height=30)
    clear_screen(win)
    msg.draw()
    win.flip()

    # wait indifinitely, terminates upon any key press
    if any_key_to_terminate and wait_for_keypress:
        event.waitKeys()
        clear_screen(win)


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


def show_break():
    """
    a function for taking break during trials.
    :return:
    """
    msg = visual.TextStim(win=win, height=40, color='white', bold=True)
    text_pre = u'现在请休息 '
    text_suf = u' 秒'
    for i in range(15, 0, -1):
        text = text_pre + str(i) + text_suf
        msg.setText(text)
        msg.draw()
        win.flip()
        core.wait(1)


def abort_trial():
    """Ends recording """

    el_tracker = pylink.getEYELINK()

    # Stop recording
    if el_tracker.isRecording():
        # add 100 ms to catch final trial events
        pylink.pumpDelay(100)
        el_tracker.stopRecording()

    # clear the screen
    clear_screen(win)
    # Send a message to clear the Data Viewer screen
    bgcolor_RGB = (116, 116, 116)
    el_tracker.sendMessage('!V CLEAR %d %d %d' % bgcolor_RGB)

    # send a message to mark trial end
    el_tracker.sendMessage('TRIAL_RESULT %d' % pylink.TRIAL_ERROR)

    return pylink.TRIAL_ERROR


def terminate_task():
    """ Terminate the task gracefully and retrieve the EDF data file

    file_to_retrieve: The EDF on the Host that we would like to download
    win: the current window used by the experimental script
    """

    el_tracker = pylink.getEYELINK()

    if el_tracker.isConnected():
        # Terminate the current trial first if the task terminated prematurely
        error = el_tracker.isRecording()
        if error == pylink.TRIAL_OK:
            abort_trial()

        # Put tracker in Offline mode
        el_tracker.setOfflineMode()

        # Clear the Host PC screen and wait for 500 ms
        el_tracker.sendCommand('clear_screen 0')
        pylink.msecDelay(500)

        # Close the edf data file on the Host
        el_tracker.closeDataFile()

        # Show a file transfer message on the screen
        msg = 'EDF data is transferring from EyeLink Host PC...'
        show_msg(win, msg, wait_for_keypress=False)

        # Download the EDF data file from the Host PC to a local data folder
        # parameters: source_file_on_the_host, destination_file_on_local_drive
        local_edf = os.path.join(session_folder, session_identifier + '.EDF')
        try:
            el_tracker.receiveDataFile(edf_file, local_edf)
        except RuntimeError as error:
            print('ERROR:', error)

        # Close the link to the tracker.
        el_tracker.close()

    # close the PsychoPy window
    win.close()

    # quit PsychoPy
    core.quit()
    sys.exit()


def get_mouse_eye_pos():
    """
    获取鼠标或眼睛实时位置
    :return:
    """
    if dummy_mode:
        mouse_zone.pos = mouse.getPos()
    else:
        eye_used = el_tracker.eyeAvailable()
        # logging.info('eye_used: ' + str(eye_used))
        if eye_used == 2:
            eye_used = 0

        ldata = el_tracker.getNewestSample()
        # logging.info('ldata: ' + str(ldata))
        if ldata is not None:
            if eye_used == 1 and ldata.isRightSample():
                # print('right' + str(ldata.getRightEye().getGaze()))
                gaze_pos = ldata.getRightEye().getGaze()
                current_eye_pos = (gaze_pos[0] - scn_width / 2, scn_height / 2 - gaze_pos[1])
            elif eye_used == 0 and ldata.isLeftSample():
                # print('left' + str(ldata.getLeftEye().getGaze()))
                gaze_pos = ldata.getLeftEye().getGaze()
                current_eye_pos = (gaze_pos[0] - scn_width / 2, scn_height / 2 - gaze_pos[1])

            mouse_zone.pos = current_eye_pos
            mouse.setPos(current_eye_pos)


# define a function to run trials
def run_trial(pos_lists, speed_lists, trial_index):
    """
    a function to run trials.
    :param pos_lists: 小方块的初始位置
    :param speed_lists: 小方块的速度
    :param trial_index: 试次数
    :return:
    """
    # get a reference to the currently active EyeLink connection
    el_tracker = pylink.getEYELINK()

    # put the tracker in the offline mode first
    el_tracker.setOfflineMode()

    # send a 'TRIALID' message to mark the start of a trial
    el_tracker.sendMessage('TRIALID %d' % trial_index)

    # record_status_message : show some info on the Host PC
    # here we show how many trial has been tested
    status_msg = 'TRIAL number %d ' % (trial_index)
    el_tracker.sendCommand("record_status_message '%s'" % status_msg)

    # draw a reference grid on the Host PC screen
    # For details, See section 25.6 'Drawing Commands' in the
    # EyeLink Programmers Guide manual
    # line_hor = (scnWidth / 2.0 - start_x, scnHeight / 2.0,
    #             scnWidth / 2.0 + start_x, scnHeight / 2.0)
    # line_ver = (scnWidth / 2.0, scnHeight / 2.0 - start_y,
    #             scnWidth / 2.0, scnHeight / 2.0 + start_y)
    # el_tracker.sendCommand('clear_screen 0')  # clear the host Display
    # el_tracker.sendCommand('draw_line %d %d %d %d 15' % line_hor)
    # el_tracker.sendCommand('draw_line %d %d %d %d 15' % line_ver)
    red_box = (rv_red[0][0] + scn_width / 2, scn_height / 2 - rv_red[0][1],
               rv_red[2][0] + scn_width / 2, scn_height / 2 - rv_red[2][1])
    blue_box = (rv_blue[0][0] + scn_width / 2, scn_height / 2 - rv_blue[0][1],
                rv_blue[2][0] + scn_width / 2, scn_height / 2 - rv_blue[2][1])
    green_box = (rv_green[0][0] + scn_width / 2, scn_height / 2 - rv_green[0][1],
                 rv_green[2][0] + scn_width / 2, scn_height / 2 - rv_green[2][1])
    yellow_box = (rv_yellow[0][0] + scn_width / 2, scn_height / 2 - rv_yellow[0][1],
                  rv_yellow[2][0] + scn_width / 2, scn_height / 2 - rv_yellow[2][1])
    el_tracker.sendCommand('clear_screen 0')  # clear the host Display
    el_tracker.sendCommand('draw_box %d %d %d %d 15' % red_box)
    el_tracker.sendCommand('draw_box %d %d %d %d 15' % blue_box)
    el_tracker.sendCommand('draw_box %d %d %d %d 15' % green_box)
    el_tracker.sendCommand('draw_box %d %d %d %d 15' % yellow_box)

    # put tracker in idle/offline mode before recording
    el_tracker.setOfflineMode()

    # Start recording
    # arguments: sample_to_file, events_to_file, sample_over_link,
    # event_over_link (1-yes, 0-no)
    try:
        el_tracker.startRecording(1, 1, 1, 1)
    except RuntimeError as error:
        print("ERROR:", error)
        abort_trial()
        return pylink.TRIAL_ERROR

    # Allocate some time for the tracker to cache some samples
    pylink.pumpDelay(100)

    # Send a message to clear the Data Viewer screen, get it ready for
    # drawing the pictures during visualization
    bgcolor_RGB = (116, 116, 116)
    el_tracker.sendMessage('!V CLEAR %d %d %d' % bgcolor_RGB)

    # open a INTEREAT AREA SET file to make a dynamic IA for the target
    ias = 'IA_%d.ias' % trial_index
    ias_file = open(os.path.join(aoi_folder, ias), 'w')

    frame_num = 0  # keep track of the frames displayed

    # 在每个试次开始时，更改小球位置属性
    s_rect_red = visual.ShapeStim(win, vertices=pos_lists[0], fillColor='red',
                                  lineColor=None)
    s_rect_green = visual.ShapeStim(win, vertices=pos_lists[1], fillColor='green',
                                    lineColor=None)
    s_rect_blue = visual.ShapeStim(win, vertices=pos_lists[2], fillColor='blue',
                                   lineColor=None)
    s_rect_yellow = visual.ShapeStim(win, vertices=pos_lists[3], fillColor='yellow',
                                     lineColor=None)

    # 大方块是否选中
    red_selected, green_selected, blue_selected, yellow_selected = False, False, False, False

    # 小方块是否选中
    s_red_selected, s_green_selected = False, False
    s_blue_selected, s_yellow_selected = False, False

    # 小方块是否超出屏幕边缘
    s_red_out, s_green_out, s_blue_out, s_yellow_out = False, False, False, False

    # 小方块是否选择错误
    red_wrong, green_wrong, blue_wrong, yellow_wrong = False, False, False, False

    # set a timer
    t = core.getTime()

    # draw a cross FIXATION
    el_tracker.sendMessage('FIXATION_SCREEN')
    while core.getTime() - t <= 0.5:
        msg.setText('+')
        msg.height = 50
        msg.draw()
        win.flip()

    # draw rect
    while True:
        # abort the current trial if the tracker is no longer recording
        error = el_tracker.isRecording()
        if error is not pylink.TRIAL_OK:
            el_tracker.sendMessage("tracker_disconnected")
            abort_trial()
            return error

        # check keyboard events
        for keycode, modifier in event.getKeys(modifiers=True):
            # abort a trial if 'ESCAPE' is pressed
            if keycode == 'escape':
                el_tracker.sendMessage('trial_skipped_by_user')
                # clear the screen
                clear_screen(win)
                # abort trial
                abort_trial()
                return pylink.SKIP_TRIAL

            # terminate the task if Ctrl-c
            if keycode == 'c' and (modifier['ctrl'] is True):
                el_tracker.sendMessage('terminated_by_user')
                terminate_task()
                return pylink.ABORT_EXPT

        # 获取鼠标或眼睛实时位置
        get_mouse_eye_pos()
        # draw mouse zone
        mouse_zone.draw()

        # draw 大方块
        rect_red.draw()
        rect_green.draw()
        rect_blue.draw()
        rect_yellow.draw()

        # draw 小方块
        s_rect_red.draw()
        s_rect_green.draw()
        s_rect_blue.draw()
        s_rect_yellow.draw()
        frame_num += 1

        if frame_num == 1:
            el_tracker.sendMessage('TARGET_ONSET')

            # record a message to let Data Viewer know where to find
            # the IA file for the current trial.
            ias_path = os.path.join('aoi', ias)
            el_tracker.sendMessage('!V IAREA FILE %s' % ias_path)
        else:
            # 对四个大方块设置兴趣区
            # RECTANGLE id left top right bottom [label]
            # el_tracker.sendMessage('!V IAREA RECTANGLE %s %d %d %d %d %s' %
            #                        (1, rv_red[0][0], rv_red[0][1],
            #                         rv_red[2][0], rv_red[2][1], 'red'))
            # el_tracker.sendMessage('!V IAREA RECTANGLE %s %d %d %d %d %s' %
            #                        (2, rv_blue[0][0], rv_blue[0][1],
            #                         rv_blue[2][0], rv_blue[2][1], 'blue'))
            # el_tracker.sendMessage('!V IAREA RECTANGLE %s %d %d %d %d %s' %
            #                        (3, rv_green[0][0], rv_green[0][1],
            #                         rv_green[2][0], rv_green[2][1], 'red'))
            # el_tracker.sendMessage('!V IAREA RECTANGLE %s %d %d %d %d %s' %
            #                        (4, rv_yellow[0][0], rv_yellow[0][1],
            #                         rv_yellow[2][0], rv_yellow[2][1], 'red'))
            # el_tracker.sendMessage('!V IAREA RECTANGLE %s %d %d %d %d %s' %
            #                        (5, rv_red[1][0], rv_red[1][1],
            #                         rv_green[3][0], rv_green[3][1], 'center'))
            ias_file.write('RECTANGLE %s %d %d %d %d %s\n' %
                           (1, rv_red[0][0] + scn_width / 2, scn_height / 2 - rv_red[0][1],
                            rv_red[2][0] + scn_width / 2, scn_height / 2 - rv_red[2][1], 'red'))
            ias_file.write('RECTANGLE %s %d %d %d %d %s\n' %
                           (2, rv_blue[0][0] + scn_width / 2, scn_height / 2 - rv_blue[0][1],
                            rv_blue[2][0] + scn_width / 2, scn_height / 2 - rv_blue[2][1], 'blue'))
            ias_file.write('RECTANGLE %s %d %d %d %d %s\n' %
                           (3, rv_green[0][0] + scn_width / 2, scn_height / 2 - rv_green[0][1],
                            rv_green[2][0] + scn_width / 2, scn_height / 2 - rv_green[2][1], 'green'))
            ias_file.write('RECTANGLE %s %d %d %d %d %s\n' %
                           (4, rv_yellow[0][0] + scn_width / 2, scn_height / 2 - rv_yellow[0][1],
                            rv_yellow[2][0] + scn_width / 2, scn_height / 2 - rv_yellow[2][1], 'yellow'))
            ias_file.write('RECTANGLE %s %d %d %d %d %s\n' %
                           (5, rv_red[1][0] + scn_width / 2, scn_height / 2 - rv_red[1][1],
                            rv_green[3][0] + scn_width / 2, scn_height / 2 - rv_green[3][1], 'center'))

        # 定义小方块下落的速度
        s_rect_red.pos -= (0, speed_lists[0])
        s_rect_green.pos -= (0, speed_lists[1])
        s_rect_blue.pos -= (0, speed_lists[2])
        s_rect_yellow.pos -= (0, speed_lists[3])

        win.flip()

        # 如果鼠标或眼睛移入大方块，则改变大方块颜色和透明度
        # 如果移出，则恢复原来的属性
        # 落在红色大方块区域
        if rect_red.contains(mouse):
            rect_red.fillColor = 'black'
            red_time = core.getTime() - t
            while True:
                s_rect_red.pos -= (0, speed_lists[0])
                s_rect_green.pos -= (0, speed_lists[1])
                s_rect_blue.pos -= (0, speed_lists[2])
                s_rect_yellow.pos -= (0, speed_lists[3])
                # mouse_zone.pos = mouse.getPos()
                get_mouse_eye_pos()

                if rect_red.opacity >= 0.5:
                    rect_red.opacity -= 0.02

                mouse_zone.draw()

                rect_red.draw()
                rect_green.draw()
                rect_blue.draw()
                rect_yellow.draw()

                s_rect_red.draw()
                s_rect_green.draw()
                s_rect_blue.draw()
                s_rect_yellow.draw()
                win.flip()
                red_stay = core.getTime() - t
                if red_stay - red_time > stay_time:
                    logging.info('red_stay: ' + str(red_stay - red_time))
                    logging.info('red_select')
                    red_selected = True
                    logging.info('red_break_1')
                    break
                elif not rect_red.contains(mouse):
                    logging.info('red_break_2')
                    break
        else:
            rect_red.fillColor = 'grey'
            rect_red.opacity = 1
        # 落在绿色大方块区域
        if rect_green.contains(mouse):
            rect_green.fillColor = 'black'
            green_time = core.getTime() - t
            while True:
                s_rect_red.pos -= (0, speed_lists[0])
                s_rect_green.pos -= (0, speed_lists[1])
                s_rect_blue.pos -= (0, speed_lists[2])
                s_rect_yellow.pos -= (0, speed_lists[3])
                # mouse_zone.pos = mouse.getPos()
                get_mouse_eye_pos()

                if rect_green.opacity >= 0.5:
                    rect_green.opacity -= 0.02

                mouse_zone.draw()

                rect_red.draw()
                rect_green.draw()
                rect_blue.draw()
                rect_yellow.draw()

                s_rect_red.draw()
                s_rect_green.draw()
                s_rect_blue.draw()
                s_rect_yellow.draw()
                win.flip()
                green_stay = core.getTime() - t
                if green_stay - green_time > stay_time:
                    logging.info('green_z: ' + str(green_stay - green_time))
                    logging.info('green_select')
                    green_selected = True
                    logging.info('green_break_1')
                    break
                if not rect_green.contains(mouse):
                    logging.info('green_break_2')
                    break
        else:
            rect_green.fillColor = 'grey'
            rect_green.opacity = 1
        # 落在蓝色大方块区域
        if rect_blue.contains(mouse):
            rect_blue.fillColor = 'black'
            blue_time = core.getTime() - t
            while True:
                s_rect_red.pos -= (0, speed_lists[0])
                s_rect_green.pos -= (0, speed_lists[1])
                s_rect_blue.pos -= (0, speed_lists[2])
                s_rect_yellow.pos -= (0, speed_lists[3])
                # mouse_zone.pos = mouse.getPos()
                get_mouse_eye_pos()

                if rect_blue.opacity >= 0.5:
                    rect_blue.opacity -= 0.02

                mouse_zone.draw()

                rect_red.draw()
                rect_green.draw()
                rect_blue.draw()
                rect_yellow.draw()

                s_rect_red.draw()
                s_rect_green.draw()
                s_rect_blue.draw()
                s_rect_yellow.draw()
                win.flip()
                blue_stay = core.getTime() - t
                if blue_stay - blue_time > stay_time:
                    logging.info('blue_z: ' + str(blue_stay - blue_time))
                    logging.info('blue_select')
                    blue_selected = True
                    logging.info('blue_break_1')
                    break
                if not rect_blue.contains(mouse):
                    logging.info('blue_break_2')
                    break
        else:
            rect_blue.fillColor = 'grey'
            rect_blue.opacity = 1
        # 落在黄色大方块区域
        if rect_yellow.contains(mouse):
            rect_yellow.fillColor = 'black'
            yellow_time = core.getTime() - t
            while True:
                s_rect_red.pos -= (0, speed_lists[0])
                s_rect_green.pos -= (0, speed_lists[1])
                s_rect_blue.pos -= (0, speed_lists[2])
                s_rect_yellow.pos -= (0, speed_lists[3])
                # mouse_zone.pos = mouse.getPos()
                get_mouse_eye_pos()

                if rect_yellow.opacity >= 0.5:
                    rect_yellow.opacity -= 0.02

                mouse_zone.draw()

                rect_red.draw()
                rect_green.draw()
                rect_blue.draw()
                rect_yellow.draw()

                s_rect_red.draw()
                s_rect_green.draw()
                s_rect_blue.draw()
                s_rect_yellow.draw()
                win.flip()
                yellow_stay = core.getTime() - t
                if yellow_stay - yellow_time > stay_time:
                    logging.info('yellow_z: ' + str(yellow_stay - yellow_time))
                    logging.info('yellow_select')
                    yellow_selected = True
                    logging.info('yellow_break_1')
                    break
                if not rect_yellow.contains(mouse):
                    logging.info('yellow_break_2')
                    break
        else:
            rect_yellow.fillColor = 'grey'
            rect_yellow.opacity = 1

        # 判断红色和绿色小方块的正确和错误选择
        if not (s_red_selected and s_green_selected):
            # 正确选择
            # 选中红色和绿色大方块，代表红色和绿色小方块被选中
            # 通过大方块选中的先后顺序，判断哪个小方块被选中
            if red_selected and green_selected:
                # 红色小方块被选中
                if red_time - green_time < 0:
                    s_rect_red.opacity = 0
                    s_red_selected = True
                    # 反应时
                    RT_red = abs(red_time - green_time)
                    logging.info('r: ' + str(RT_red))
                else:
                    # 绿色小方块被选中
                    s_rect_green.opacity = 0
                    s_green_selected = True
                    RT_green = abs(red_time - green_time)
                    logging.info('g: ' + str(RT_green))
                green_selected = False
                red_selected = False
            # 由红色大方块而产生的错误选择
            if red_selected:
                if blue_selected:  # red --> blue --> green
                    if not s_blue_selected:
                        red_wrong = True
                        logging.info('r1: ' + str(red_wrong))
                    blue_selected = False
                    red_selected = False
                if yellow_selected:  # red --> yellow --> green
                    if not s_yellow_selected:
                        red_wrong = True
                        logging.info('r2: ' + str(red_wrong))
                    yellow_selected = False
                    red_selected = False
            # 由绿色大方块而产生的错误选择
            if green_selected:
                if blue_selected:  # green --> blue --> red
                    if not s_blue_selected:
                        green_wrong = True
                        logging.info('g1: ' + str(green_wrong))
                    blue_selected = False
                    green_selected = False
                if yellow_selected:  # green --> yellow --> red
                    if not s_yellow_selected:
                        green_wrong = True
                        logging.info('g2: ' + str(green_wrong))
                    yellow_selected = False
                    green_selected = False
        # 判断蓝色和黄色小方块的正确和错误选择
        if not (s_blue_selected and s_yellow_selected):
            # 正确选择
            if blue_selected and yellow_selected:
                # 蓝色小方块被选中
                if blue_time - yellow_time < 0:
                    s_rect_blue.opacity = 0
                    s_blue_selected = True
                    RT_blue = abs(blue_time - yellow_time)
                    logging.info('b: ' + str(RT_blue))
                else:
                    # 绿色小方块被选中
                    s_rect_yellow.opacity = 0
                    s_yellow_selected = True
                    RT_yellow = abs(blue_time - yellow_time)
                    logging.info('y: ' + str(RT_yellow))
                yellow_selected = False
                blue_selected = False
            # 由蓝色大方块产生的错误选择
            if blue_selected:
                if red_selected:  # blue --> red --> yellow
                    if not s_red_selected:
                        blue_wrong = True
                        logging.info('b1: ' + str(blue_wrong))
                    red_selected = False
                    blue_selected = False
                if green_selected:  # blue --> green --> yellow
                    if not s_green_selected:
                        blue_wrong = True
                        logging.info('b2: ' + str(blue_wrong))
                    green_selected = False
                    blue_selected = False
            # 由黄色大方块产生的错误选择
            if yellow_selected:
                if red_selected:  # yellow --> red --> blue
                    if not s_red_selected:
                        yellow_wrong = True
                        logging.info('y1: ' + str(yellow_wrong))
                    red_selected = False
                    yellow_selected = False
                if green_selected:  # yellow --> green --> blue
                    if not s_green_selected:
                        yellow_wrong = True
                        logging.info('y2: ' + str(yellow_wrong))
                    green_selected = False
                    yellow_selected = False

        # 如果小方块没有被选择，判断其是否移动出屏幕之外
        # 如果是，则标记True，并返回相应的反应时为None值
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

        # 定义试次结束的条件
        # 以选中和未选中（错过）小方块的数量，作“组合”计算
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

    # 结束While循环时，计算试次所需要的时间
    trial_time = core.getTime() - t

    el_tracker.sendMessage('BLANK_SCREEN')
    clear_screen(win)
    core.wait(0.5)

    # send a message to clear the Data Viewer
    el_tracker.sendMessage('!V CLEAR 128 128 128')

    # close the IAS file
    ias_file.close()

    # record trial variables to the EDF data file
    el_tracker.sendMessage('!V TRIAL_VAR s_red_selected %s' % s_red_selected)
    el_tracker.sendMessage('!V TRIAL_VAR s_blue_selected %s' % s_blue_selected)
    el_tracker.sendMessage('!V TRIAL_VAR s_green_selected %s' % s_green_selected)
    el_tracker.sendMessage('!V TRIAL_VAR s_yellow_selected %s' % s_yellow_selected)
    pylink.msecDelay(4)  # take a break of 4 millisecond
    el_tracker.sendMessage('!V TRIAL_VAR s_red_out %s' % s_red_out)
    el_tracker.sendMessage('!V TRIAL_VAR s_blue_out %s' % s_blue_out)
    el_tracker.sendMessage('!V TRIAL_VAR s_green_out %s' % s_green_out)
    el_tracker.sendMessage('!V TRIAL_VAR s_yellow_out %s' % s_yellow_out)
    pylink.msecDelay(4)  # take a break of 4 millisecond
    el_tracker.sendMessage('!V TRIAL_VAR red_wrong %s' % red_wrong)
    el_tracker.sendMessage('!V TRIAL_VAR blue_wrong %s' % blue_wrong)
    el_tracker.sendMessage('!V TRIAL_VAR green_wrong %s' % green_wrong)
    el_tracker.sendMessage('!V TRIAL_VAR yellow_wrong %s' % yellow_wrong)
    pylink.msecDelay(4)  # take a break of 4 millisecond

    # send a 'TRIAL_RESULT' message to mark the end of trial
    el_tracker.sendMessage('TRIAL_RESULT %d' % pylink.TRIAL_OK)

    # write trial info to CSV
    red_data = [trial_index, 'red', s_red_selected, red_wrong, s_red_out, RT_red, trial_time]
    sub_data.write(','.join(map(str, red_data)) + '\n')
    green_data = [trial_index, 'green', s_green_selected, green_wrong, s_green_out, RT_green, trial_time]
    sub_data.write(','.join(map(str, green_data)) + '\n')
    blue_data = [trial_index, 'blue', s_blue_selected, blue_wrong, s_blue_out, RT_blue, trial_time]
    sub_data.write(','.join(map(str, blue_data)) + '\n')
    yellow_data = [trial_index, 'yellow', s_yellow_selected, yellow_wrong, s_yellow_out, RT_yellow, trial_time]
    sub_data.write(','.join(map(str, yellow_data)) + '\n')


# Show the task instructions
task_msg = u'你的任务是通过视线选择下落的小方块\n'
if dummy_mode:
    task_msg = task_msg + u'\n\n现在，请按空格键开始任务'
else:
    task_msg = task_msg + u'\n\n现在，请按空格键开始校准'
show_msg(win, task_msg, wait_for_keypress=True)

# skip this step if running the script in Dummy Mode
if not dummy_mode:
    try:
        el_tracker.doTrackerSetup()
    except RuntimeError as err:
        print('ERROR:', err)
        el_tracker.exitCalibration()

if not dummy_mode:
    task_msg = u'校准结束，按空格开始任务'
    show_msg(win, task_msg, wait_for_keypress=True)

random.Random(12345).shuffle(s_rv_vertices)
trial_index = 1
for i in range(10):
    s_rv_lists = random.sample(s_rv_vertices, k=4)  # random sample
    logging.info('Trial: ' + str(trial_index))
    logging.info(s_rv_lists)
    run_trial(s_rv_lists, speed_lists, trial_index)
    logging.info('--------------------------------------------')
    trial_index += 1

sub_data.close()

terminate_task()
