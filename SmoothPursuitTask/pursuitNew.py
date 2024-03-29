# Filename: pursuitTest.py

import random, os
from psychopy import event, visual, core, monitors, logging, gui
from math import pi, sin
import os, sys
from string import ascii_letters, digits
import time
import pylink
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
from pylink import *

# logging.console.setLevel(logging.CRITICAL)


# dummy_mode
dummy_mode = False

# full_screen or not
full_screen = True

# radius of the elliptical IA
ia_radius = 40

# set screen size
scnWidth, scnHeight = (1920, 1080)

# 500 pixels approximately 13.7°
# the speed of half and long movement, approximately 8.5°/s
hl_speed = 5

# the duration of lissajous movement
lissajous_duration = 16

# the duration of half and long movement
hl_duration = 2

# Horizontal or vertical movement border
hv_border = 250

# Tilt movement border
# ATTENTION: sin() and cos() 默认使用的是弧度值
# 圆上任意一点坐标公式
# cx, cy 为圆心坐标
# θ是相对水平轴的角度
# px = cx + r * cos(θ)
# py = cy + r * sin(θ)
# 角度45°： px = 177, py = 177
t_border = 177

# a list containing half movement parameters
# [movement, start_x, start_y, end_x, end_y]
# movement: movement type
# start_x: the movement starts x position
# start_y: the movement starts y position
# end_x: the movement ends x position
# end_y: the movement ends y position
trial_half = [
    ['Vertical_H_TC', 0, hv_border, 0, 0],  # half, top to center
    ['Vertical_H_BC', 0, -hv_border, 0, 0],  # half, bottom to center
    ['Vertical_H_CT', 0, 0, 0, hv_border],  # half, center to top
    ['Vertical_H_CB', 0, 0, 0, -hv_border],  # half, center to bottom
    ['Horizontal_H_RC', hv_border, 0, 0, 0],  # half, right to center
    ['Horizontal_H_LC', -hv_border, 0, 0, 0],  # half, left to center
    ['Horizontal_H_CR', 0, 0, hv_border, 0],  # half, center to right
    ['Horizontal_H_CL', 0, 0, -hv_border, 0],  # half, center to left
    ['Tilt_H_TRC', t_border, t_border, 0, 0],  # half, top-right to center
    ['Tilt_H_TLC', -t_border, t_border, 0, 0],  # half, top-left to center
    ['Tilt_H_BLC', -t_border, -t_border, 0, 0],  # half, bottom-left to center
    ['Tilt_H_BRC', t_border, -t_border, 0, 0],  # half, bottom-right to center
    ['Tilt_H_CTR', 0, 0, t_border, t_border],  # half, center to top-right
    ['Tilt_H_CTL', 0, 0, -t_border, t_border],  # half, center to top-left
    ['Tilt_H_CBL', 0, 0, -t_border, -t_border],  # half, center to bottom-left
    ['Tilt_H_CBR', 0, 0, t_border, -t_border],  # half, center to bottom-right
]

# a list containing long movement parameters
# [movement, start_x, start_y, end_x, end_y]
# movement: movement type
# start_x: the movement starts x position
# start_y: the movement starts y position
# end_x: the movement ends x position
# end_y: the movement ends y position
trial_long = [
    ['Vertical_L_TB', 0, hv_border, 0, -hv_border],  # long, top to bottom
    ['Vertical_L_BT', 0, -hv_border, 0, hv_border],  # long, bottom to top
    ['Horizontal_L_RL', hv_border, 0, -hv_border, 0],  # long, right to left
    ['Horizontal_L_LR', -hv_border, 0, hv_border, 0],  # long, left to right
    ['Tilt_L_TRBL', t_border, t_border, -t_border, -t_border],  # half, top-right to bottom-left
    ['Tilt_L_BLTR', -t_border, -t_border, t_border, t_border],  # half, bottom-left to top-right
    ['Tilt_L_TLBR', -t_border, t_border, t_border, -t_border],  # half, top-left to bottom-right
    ['Tilt_L_BRTL', t_border, -t_border, -t_border, t_border],  # half, bottom-right to top-left
]

# parameters for Sinusoidal movement patter
# [amp_x, amp_y, phase_x, phase_y, freq_x, freq_y]
# amp_*决定正弦波的振幅，amp_x为300的话，那么该正弦波则从-300px到300px运动（中心点为0）
# amp_y则是上下振幅
# phase_x则是决定正弦的起点位置，sin(pi*3/2) = -1，则从左侧开始，终点为右侧
# sin(pi/2) = 1，则有右侧开始，终点为左侧
# 如果为0，则从屏幕中心
# freq_*为一秒内正弦波有多少个周期
trial_lissajous = [
    ['Lissajous_slow', 250, 250, pi / 2, 0, 15 / 100, 2 / 10],  # Lissajous Curve slow
    ['Lissajous_fast', 250, 250, pi / 2, 0, 3 / 10, 4 / 10],  # Lissajous Curve fast
]

# Set up EDF data file name and local data folder
#
# The EDF data filename should not exceed 8 alphanumeric characters
# use ONLY number 0-9, letters, & _ (underscore) in the filename
edf_fname = 'TEST'

# Prompt user to specify an EDF data filename
# before we open a fullscreen window
# 1-2: 被试编号
# 3-5： 姓名缩写
# 7: 任务类型
dlg_title = 'Enter EDF File Name'
dlg_prompt = 'Please enter a file name with 8 or fewer characters\n' + \
             '[letters, numbers, and underscore].'

# loop until we get a valid filename
while True:
    dlg = gui.Dlg(dlg_title)
    dlg.addText(dlg_prompt)
    dlg.addField('File Name:', edf_fname)
    # show dialog and wait for OK or Cancel
    ok_data = dlg.show()
    if dlg.OK:  # if ok_data is not None
        print('EDF data filename: {}'.format(ok_data[0]))
    else:
        print('user cancelled')
        core.quit()
        sys.exit()

    # get the string entered by the experimenter
    tmp_str = dlg.data[0]
    # strip trailing characters, ignore the ".edf" extension
    edf_fname = tmp_str.rstrip().split('.')[0]

    # check if the filename is valid (length <= 8 & no special char)
    allowed_char = ascii_letters + digits + '_'
    if not all([c in allowed_char for c in edf_fname]):
        print('ERROR: Invalid EDF filename')
    elif len(edf_fname) > 8:
        print('ERROR: EDF filename should not exceed 8 characters')
    else:
        break

# set up a folder to store the EDF data files and the associated resources
# e.g., files defining the interest areas used in each trial
results_folder = os.path.join(os.path.dirname(__file__), 'results')
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

# We download EDF data file from the EyeLink Host PC to the local hard
# drive at the end of each testing session, here we rename the EDF to
# include session start date/time
time_str = time.strftime("_%Y_%m_%d_%H_%M", time.localtime())
session_identifier = edf_fname + time_str

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
edf_file = edf_fname + ".EDF"
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

# Step 4: set up a graphics environment for calibration
# open a window for graphics and calibration


# create a monitor object
# 24.5 inch monitor
# width = 55.3 cm
# height = 31.1 cm
myMon = monitors.Monitor(name='expMon', width=55.3, distance=60, )
myMon.setSizePix((scnWidth, scnHeight))

# open a window
win = visual.Window(size=(scnWidth, scnHeight), fullscr=full_screen, monitor=myMon, units='pix', )

# Pass the display pixel coordinates (left, top, right, bottom) to the tracker
# see the Eyelink Installation Guide, "Customizing Screen Settings"
el_coords = "screen_pixel_coords = 0 0 %d %d" % (scnWidth - 1, scnHeight - 1)
el_tracker.sendCommand(el_coords)

# Write a DISPLAY_COORDS message to the EDF file
# Data Viewer needs this piece of info for proper visualization, see Data
# Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"
dv_coords = "DISPLAY_COORDS  0 0 %d %d" % (scnWidth - 1, scnHeight - 1)
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


# define a few helper functions for trial handling


def clear_screen(win):
    """
    clear up the PsychoPy window
    :param win:
    :return:
    """
    win.fillColor = genv.getBackgroundColor()
    win.flip()


def show_msg(win, text, wait_for_keypress=True, any_key_to_terminate=True):
    '''Show task instructions on screen'''

    msg = visual.TextStim(win, text,
                          color=genv.getForegroundColor(),
                          wrapWidth=scnWidth / 2,
                          height=30)
    clear_screen(win)
    msg.draw()
    win.flip()

    # wait indifinitely, terminates upon any key press
    if any_key_to_terminate and wait_for_keypress:
        event.waitKeys()
        clear_screen(win)


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


# prepare the pursuit target, the clock and the movement parameters
# when set screen resolution = (1920, 1080)
# 1 cm = 34.7
# when the distance between subject and screen is 60 cm
# 1° visual angle approximately 1.05 cm, that is approximately 36 px
# when set screen resolution = (1280, 1024)
# 1 cm = 25.2 px
# so 1° visual angle approximately 26 px
# target = visual.GratingStim(win=win, tex=None, mask='circle', size=36)
target = visual.ImageStim(win=win, image='./images/target.png')
# target = visual.ImageStim(win=win, image='./images/target-ring.png')
pursuitClock = core.Clock()


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


def half_long_new(move_pars, trial_index):
    """
    a function to run half and long movement.
    :param move_pars: a list containing trial parameters. i.e.,
                [movement, start_x, start_y, end_x, end_y]
    :param trial_index: record the order of trial presentation in the task
    :return:
    """
    movement, start_x, start_y, end_x, end_y = move_pars
    x_length = end_x - start_x
    y_length = end_y - start_y

    # get a reference to the currently active EyeLink connection
    el_tracker = pylink.getEYELINK()

    # put the tracker in the offline mode first
    el_tracker.setOfflineMode()

    # send a 'TRIALID' message to mark the start of a trial
    el_tracker.sendMessage('TRIALID %d' % trial_index)

    # record_status_message : show some info on the Host PC
    # here we show how many trial has been tested
    status_msg = 'TRIAL number %d, %s' % (trial_index, movement)
    el_tracker.sendCommand("record_status_message '%s'" % status_msg)

    # draw a reference grid on the Host PC screen
    # For details, See section 25.7 'Drawing Commands' in the
    # EyeLink Programmers Guide manual
    line_hor = (scnWidth / 2.0 - start_x, scnHeight / 2.0,
                scnWidth / 2.0 + start_x, scnHeight / 2.0)
    line_ver = (scnWidth / 2.0, scnHeight / 2.0 - start_y,
                scnWidth / 2.0, scnHeight / 2.0 + start_y)
    el_tracker.sendCommand('clear_screen 0')  # clear the host Display
    el_tracker.sendCommand('draw_line %d %d %d %d 15' % line_hor)
    el_tracker.sendCommand('draw_line %d %d %d %d 15' % line_ver)

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

    # ia_radius = 60  # radius of the elliptical IA
    frame_num = 0  # keep track of the frames displayed

    # used a fixation trigger in not dummy mode
    if not dummy_mode:
        fixation = visual.TextStim(win=win, text='+', height=50)
        fixation.draw()
        win.flip()
        el_tracker.sendMessage("FIXATION_TRIGGER")

        eye_used = el_tracker.eyeAvailable()
        if eye_used == 2:
            eye_used = 0

        fixation_time_list = []
        current_eye_pos = [100, 100]

        while True:
            ltype = el_tracker.getNextData()
            if ltype is None:
                pass
            if ltype == FIXUPDATE:
                # send a message to mark the arrival time of a fixation update event
                el_tracker.sendMessage('fixUpdate')
                ldata = el_tracker.getFloatData()
                if ldata.getEye() == eye_used:
                    gaze_pos = ldata.getAverageGaze()
                    current_eye_pos = [gaze_pos[0] - scnWidth / 2, scnHeight / 2 - gaze_pos[1]]
            if (-25 <= current_eye_pos[0] <= 25) and (-25 <= current_eye_pos[1] <= 25):
                fixation_time_list.append(core.getTime())
            else:
                fixation_time_list = []
            if len(fixation_time_list) > 1:
                # if fixation duration > 300 ms, break
                if fixation_time_list[-1] - fixation_time_list[0] > 0.3:
                    break


    tar_x, tar_y = start_x, start_y
    target.pos = (tar_x, tar_y)
    target.draw()
    win.flip()
    el_tracker.sendMessage('TARGET_WAIT')
    core.wait(0.5)  # wait 500 ms

    pursuitClock.reset()
    time_elapsed = 0
    
    while True:
        # abort the current trial if the tracker is no longer recording
        error = el_tracker.isRecording()
        if error is not pylink.TRIAL_OK:
            el_tracker.sendMessage('tracker_disconnected')
            abort_trial()
            return error

        frame_num += 1
        flip_time = pursuitClock.getTime()
        # flip_time = core.getTime()
        print('flip_time_a: ' + str(flip_time))

        if frame_num == 1:
            # send a message to mark movement onset
            el_tracker.sendMessage('TARGET_ONSET')

            # record a message to let Data Viewer know where to find
            # the dynamic IA file for the current trial.
            ias_path = os.path.join('aoi', ias)
            el_tracker.sendMessage('!V IAREA FILE %s' % ias_path)

            # pursuit start time
            movement_start = flip_time
            # print('start time ' + str(movement_start))
        else:
            # save the Interest Area info following movement onset
            ia_pars = (-1 * round((pre_frame_time - movement_start) * 1000),
                       -1 * round((flip_time - movement_start) * 1000) + 1,
                       int(scnWidth / 2.0 + pre_x - ia_radius),
                       int(scnHeight / 2.0 - pre_y - ia_radius),
                       int(scnWidth / 2.0 + pre_x + ia_radius),
                       int(scnHeight / 2.0 - pre_y + ia_radius))

            ia_msg = '%d %d ELLIPSE 1 %d %d %d %d TARGET\n' % ia_pars
            ias_file.write(ia_msg)

            # log the target position after each screen refresh
            tar_pos = (tar_x + int(scnWidth / 2), int(scnHeight / 2) - tar_y)
            tar_pos_msg = '!V TARGET_POS target %d, %d 1 0' % tar_pos
            el_tracker.sendMessage(tar_pos_msg)

            # OPTIONAL - send over another message to request Data Viewer
            # to draw the pursuit target when visualizing the data
            el_tracker.sendMessage('!V CLEAR 128 128 128')
            tar_msg = '!V FIXPOINT 255 0 0 255 0 0 %d %d 50 50' % tar_pos
            el_tracker.sendMessage(tar_msg)

            # keep track of target position and frame timing
        pre_frame_time = flip_time
        pre_x = tar_x
        pre_y = tar_y

        time_elapsed = flip_time - movement_start

        if movement.startswith('Vertical'):
            # 半程：小球从上方 - 中间运动 OR 小球从中间 - 下方
            # 全程：小球从上方 - 下方运动
            if y_length < 0:
                tar_y -= hl_speed
                if tar_y <= end_y:  # 到达终点后，跳出循环
                    el_tracker.sendMessage('TARGET_OFFSET')
                    break
            # 半程：小球从下方 - 中间 OR 小球小中间 - 上方
            # 全程：小球从下方 - 上方运动
            elif y_length > 0:
                tar_y += hl_speed
                if tar_y >= end_y:  # 到达终点后，跳出循环
                    el_tracker.sendMessage('TARGET_OFFSET')
                    break
        elif movement.startswith('Horizontal'):
            # 半程：小球从右方 - 中间运动 OR 小球从中间 - 左方
            # 全程：小球从右方 - 左方
            if x_length < 0:
                tar_x -= hl_speed
                if tar_x <= end_x:  # 到达终点后，跳出循环
                    el_tracker.sendMessage('TARGET_OFFSET')
                    break
            # 半程：小球从左方 - 中间运动 OR 小球从中间 - 右方
            # 全程：小球从左方 - 右方
            elif x_length > 0:
                tar_x += hl_speed
                if tar_x >= end_x:  # 到达终点后，跳出循环
                    el_tracker.sendMessage('TARGET_OFFSET')
                    break
        elif movement.startswith('Tilt'):
            # x_length < 0 and y_length < 0
            # 半程包含两种情况
            # 1. 小球从右上 - 中心
            # 2. 小球小中心 - 左下
            # 全程：小球从右上 - 左下
            if x_length < 0 and y_length < 0:
                tar_x -= hl_speed / 1.4
                tar_y -= hl_speed / 1.4
                if tar_x <= end_x or tar_y <= end_y:  # x或y到达终点后，跳出循环
                    el_tracker.sendMessage('TARGET_OFFSET')
                    break
            # x_length > 0 and y_length < 0
            # 半程包含两种情况
            # 1. 小球从左上 - 中心
            # 2. 小球从中心 - 右下
            # 全程：小球从左上 - 右下
            elif x_length > 0 > y_length:
                tar_x += hl_speed / 1.4
                tar_y -= hl_speed / 1.4
                if tar_x >= end_x or tar_y <= end_y:  # x或y到达终点后，跳出循环
                    el_tracker.sendMessage('TARGET_OFFSET')
                    break
            # x_length > 0 and y_length > 0
            # 半程包含两种情况
            # 1. 小球从左下 - 中心
            # 2. 小球从中心 - 右上
            # 全程：小球从左下 - 右上
            elif x_length > 0 and y_length > 0:
                tar_x += hl_speed / 1.4
                tar_y += hl_speed / 1.4
                if tar_x >= end_x or tar_y >= end_y:  # x或y到达终点后，跳出循环
                    el_tracker.sendMessage('TARGET_OFFSET')
                    break
            # x_length < 0 and y_length > 0
            # 半程包含两种情况
            # 1. 小球从右下 - 中心
            # 2. 小球从中心 - 左上
            # 全程：小球从右下 - 中心
            elif x_length < 0 < y_length:
                tar_x -= hl_speed / 1.4
                tar_y += hl_speed / 1.4
                if tar_x <= end_x or tar_y >= end_y:  # x或y到达终点后，跳出循环
                    el_tracker.sendMessage('TARGET_OFFSET')
                    break

        target.pos = (tar_x, tar_y)
        target.draw()
        win.flip()

    # clear the screen
    # clear_screen(win)
    win.color = (0, 0, 0)
    win.flip()
    el_tracker.sendMessage('black_screen')
    el_tracker.sendMessage('!V CLEAR 128 128 128')
    core.wait(0.5)

    # close the IAS file that contain the dynamic IA definition
    ias_file.close()

    # stop recording; add 100 msec to catch final events before stopping
    pylink.pumpDelay(100)
    el_tracker.stopRecording()

    el_tracker.sendMessage('!V TRIAL_VAR movement %s' % movement)
    el_tracker.sendMessage('!V TRIAL_VAR max_duration %d' % int(time_elapsed * 1000))
    el_tracker.sendMessage('!V TRIAL_VAR start_x %d' % start_x)
    pylink.msecDelay(4)  # take a break of 4 millisecond
    el_tracker.sendMessage('!V TRIAL_VAR start_y %d' % start_y)
    el_tracker.sendMessage('!V TRIAL_VAR end_x %d' % end_x)
    el_tracker.sendMessage('!V TRIAL_VAR end_y %d' % end_y)

    # send a 'TRIAL_RESULT' message to mark the end of trial, see Data
    # Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"
    el_tracker.sendMessage('TRIAL_RESULT %d' % pylink.TRIAL_OK)


def lissajous_func(trial_dur, movement_pars, trial_index):
    """
    a function to run Lissajous movement trial.
    :param trial_dur: the duration of the pursuit movement
    :param movement_pars: [amp_x, amp_y, phase_x, phase_y, freq_x, freq_y]
    :param trial_index: record the order of trial presentation in the task
    :return:
    """

    # parse the movement patter parameters
    movement, amp_x, amp_y, phase_x, phase_y, freq_x, freq_y = movement_pars

    # get a reference to the currently active EyeLink connection
    el_tracker = pylink.getEYELINK()

    # put the tracker in the offline mode first
    el_tracker.setOfflineMode()

    # send a "TRIALID" message to mark the start of a trial, see Data
    # Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"
    el_tracker.sendMessage('TRIALID %d' % trial_index)

    # record_status_message : show some info on the Host PC
    # here we show how many trial has been tested
    status_msg = 'TRIAL number %d, %s' % (trial_index, movement)
    el_tracker.sendCommand("record_status_message '%s'" % status_msg)

    # draw a reference grid on the Host PC screen
    # For details, See section 25.7 'Drawing Commands' in the
    # EyeLink Programmers Guide manual
    line_hor = (scnWidth/2.0 - amp_x, scnHeight/2.0,
                scnWidth/2.0 + amp_x, scnHeight/2.0)
    line_ver = (scnWidth/2.0, scnHeight/2.0 - amp_y,
                scnWidth/2.0, scnHeight/2.0 + amp_x)
    el_tracker.sendCommand('clear_screen 0')  # clear the host Display
    el_tracker.sendCommand('draw_line %d %d %d %d 15' % line_hor)
    el_tracker.sendCommand('draw_line %d %d %d %d 15' % line_ver)

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

    # initial target position
    time_elapsed = 0
    tar_x = amp_x*sin(2 * pi * freq_x * time_elapsed + phase_x)
    tar_y = amp_y*sin(2 * pi * freq_y * time_elapsed + phase_y)

    ia_radius = 60  # radius of the elliptical IA
    frame_num = 0  # keep track of the frames displayed

    # used a fixation trigger in not dummy mode
    if not dummy_mode:
        fixation = visual.TextStim(win=win, text='+', height=50)
        fixation.draw()
        win.flip()
        el_tracker.sendMessage("FIXATION_TRIGGER")

        eye_used = el_tracker.eyeAvailable()
        if eye_used == 2:
            eye_used = 0

        fixation_time_list = []
        current_eye_pos = [100, 100]

        while True:
            ltype = el_tracker.getNextData()
            if ltype is None:
                pass
            if ltype == FIXUPDATE:
                # send a message to mark the arrival time of a fixation update event
                el_tracker.sendMessage('fixUpdate')
                ldata = el_tracker.getFloatData()
                if ldata.getEye() == eye_used:
                    gaze_pos = ldata.getAverageGaze()
                    current_eye_pos = [gaze_pos[0] - scnWidth / 2, scnHeight / 2 - gaze_pos[1]]
            if (-25 <= current_eye_pos[0] <= 25) and (-25 <= current_eye_pos[1] <= 25):
                fixation_time_list.append(core.getTime())
            else:
                fixation_time_list = []
            if len(fixation_time_list) > 1:
                # if fixation duration > 300 ms, break
                if fixation_time_list[-1] - fixation_time_list[0] > 0.3:
                    break

    target.pos = (tar_x, tar_y)
    target.draw()
    win.flip()
    el_tracker.sendMessage('TARGET_WAIT')
    core.wait(0.5)  # wait 500 ms for moving

    while True:
        # abort the current trial if the tracker is no longer recording
        error = el_tracker.isRecording()
        if error is not pylink.TRIAL_OK:
            el_tracker.sendMessage('tracker_disconnected')
            abort_trial()
            return error

        # check keyboard events
        for keycode, modifier in event.getKeys(modifiers=True):
            # Abort a trial if "ESCAPE" is pressed
            if keycode == 'escape':
                el_tracker.sendMessage('trial_skipped_by_user')
                # clear the screen
                clear_screen(win)
                # abort trial
                abort_trial()
                return pylink.SKIP_TRIAL

            # Terminate the task if Ctrl-c
            if keycode == 'c' and (modifier['ctrl'] is True):
                el_tracker.sendMessage('terminated_by_user')
                terminate_task()
                return pylink.ABORT_EXPT

        # draw the target
        target.pos = (tar_x, tar_y)
        target.draw()
        win.flip()
        frame_num += 1
        flip_time = core.getTime()

        if frame_num == 1:
            # send a message to mark movement onset
            el_tracker.sendMessage('TARGET_ONSET')

            # record a message to let Data Viewer know where to find
            # the dynamic IA file for the current trial.
            ias_path = os.path.join('aoi', ias)
            el_tracker.sendMessage('!V IAREA FILE %s' % ias_path)

            # pursuit start time
            movement_start = flip_time
        else:
            # save the Interest Area info following movement onset
            ia_pars = (-1 * round((pre_frame_time - movement_start) * 1000),
                       -1 * round((flip_time - movement_start) * 1000) + 1,
                       int(scnWidth/2.0 + pre_x - ia_radius),
                       int(scnHeight/2.0 - pre_y - ia_radius),
                       int(scnWidth/2.0 + pre_x + ia_radius),
                       int(scnHeight/2.0 - pre_y + ia_radius))

            ia_msg = '%d %d ELLIPSE 1 %d %d %d %d TARGET\n' % ia_pars
            ias_file.write(ia_msg)

            # log the target position after each screen refresh
            tar_pos = (tar_x + int(scnWidth/2), int(scnHeight/2) - tar_y)
            tar_pos_msg = '!V TARGET_POS target %d, %d 1 0' % tar_pos
            el_tracker.sendMessage(tar_pos_msg)

            # OPTIONAL - send over another message to request Data Viewer
            # to draw the pursuit target when visualizing the data
            el_tracker.sendMessage('!V CLEAR 128 128 128')
            tar_msg = '!V FIXPOINT 255 0 0 255 0 0 %d %d 50 50' % tar_pos
            el_tracker.sendMessage(tar_msg)

        # keep track of target position and frame timing
        pre_frame_time = flip_time
        pre_x = tar_x
        pre_y = tar_y

        # update target position and draw the target
        time_elapsed = flip_time - movement_start
        tar_x = amp_x*sin(2 * pi * freq_x * time_elapsed + phase_x)
        tar_y = amp_y*sin(2 * pi * freq_y * time_elapsed + phase_y)

        # check for time out
        if time_elapsed >= trial_dur:
            # send over a message to log movement offset
            el_tracker.sendMessage('TARGET_OFFSET')
            print(time_elapsed)
            break

    # clear the screen
    # clear_screen(win)
    win.color = (0, 0, 0)
    win.flip()
    el_tracker.sendMessage('black_screen')
    # send a message to clear the Data Viewer screen as well
    el_tracker.sendMessage('!V CLEAR 128 128 128')
    core.wait(0.5)

    # close the IAS file that contain the dynamic IA definition
    ias_file.close()

    # stop recording; add 100 msec to catch final events before stopping
    pylink.pumpDelay(100)
    el_tracker.stopRecording()

    # record trial variables to the EDF data file, for details, see Data
    # Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"
    # movement, dur, amp_x, amp_y, phase_x, phase_y, freq_x, freq_y
    el_tracker.sendMessage('!V TRIAL_VAR movement %s' % movement)
    el_tracker.sendMessage('!V TRIAL_VAR max_duration %d' % int(trial_dur*1000))
    el_tracker.sendMessage('!V TRIAL_VAR amp_x %.02f' % amp_x)
    pylink.msecDelay(4)  # take a break of 4 millisecond
    el_tracker.sendMessage('!V TRIAL_VAR amp_y %.02f' % amp_y)
    el_tracker.sendMessage('!V TRIAL_VAR phase_x %.02f' % (phase_x/pi*180))
    el_tracker.sendMessage('!V TRIAL_VAR phase_y %.02f' % (phase_y/pi*180))
    pylink.msecDelay(4)  # take a break of 4 millisecond
    el_tracker.sendMessage('!V TRIAL_VAR freq_x %.02f' % freq_x)
    el_tracker.sendMessage('!V TRIAL_VAR freq_y %.02f' % freq_y)

    # send a 'TRIAL_RESULT' message to mark the end of trial, see Data
    # Viewer User Manual, "Protocol for EyeLink Data to Viewer Integration"
    el_tracker.sendMessage('TRIAL_RESULT %d' % pylink.TRIAL_OK)


def run_half(prac_or_formal):
    """
    a function for run half movement trials.
    :param prac_or_formal: to run practice trials or formal trials.
    :return:
    """
    trial_index = 1
    if prac_or_formal == 'prac':
        trials = trial_half[:]
        random.Random(12).shuffle(trials)
        for trial in trials[:2]:
            half_long_new(trial, trial_index)
            trial_index += 1
    elif prac_or_formal == 'formal':
        trials = trial_half[:]
        random.Random(21).shuffle(trials)
        for trial in trials:
            half_long_new(trial, trial_index)
            if trial_index % 30 == 0:
                show_break()
            trial_index += 1


def run_long(prac_or_formal):
    """
    a function for run long movement  trials.
    :param prac_or_formal: to run practice trials or formal trials.
    :return:
    """
    trial_index = 1
    if prac_or_formal == 'prac':
        trials = trial_long[:]
        random.Random(13).shuffle(trials)
        for trial in trials[:2]:
            half_long_new(trial, trial_index)
            trial_index += 1
    elif prac_or_formal == 'formal':
        trials = trial_long[:] * 10
        random.Random(31).shuffle(trials)
        for trial in trials:
            half_long_new(trial, trial_index)
            if trial_index % 30 == 0:
                show_break()
            trial_index += 1


def run_lissajous(trial_dur, prac_or_formal):
    """
    a function for run Lissajous movement  trials.
    :param trial_dur: the duration of the Lissajous movement.
    :param prac_or_formal: to run practice trials or formal trials.
    :return:
    """
    trial_index = 1
    if prac_or_formal == 'prac':
        trials = trial_lissajous[:]
        random.Random(14).shuffle(trials)
        for trial in trials[:2]:
            lissajous_func(trial_dur, trial, trial_index)
            trial_index += 1
    elif prac_or_formal == 'formal':
        trials = trial_lissajous[:] * 10
        random.Random(41).shuffle(trials)
        for trial in trials:
            lissajous_func(trial_dur, trial, trial_index)
            if trial_index % 10 == 0:
                show_break()
            trial_index += 1


# Show the task instructions
task_msg = u'你的任务是使用眼睛追踪屏幕上出现的白色小球\n'

if dummy_mode:
    task_msg = task_msg + u'\n现在，请按回车键开始任务'
else:
    task_msg = task_msg + u'\n现在，请按回车键开始校准'
show_msg(win, task_msg, wait_for_keypress=False)

# skip this step if running the script in Dummy Mode
if not dummy_mode:
    try:
        el_tracker.doTrackerSetup()
    except RuntimeError as err:
        print("ERROR: ", err)
        el_tracker.exitCalibration()

# show some information for selecting when starts
half_prac = visual.TextStim(win=win, text=u'半程练习', pos=(-250, 150), height=30)
long_prac = visual.TextStim(win=win, text=u'全程练习', pos=(0, 150), height=30)
lissajous_prac = visual.TextStim(win=win, text=u'利萨如练习', pos=(250, 150), height=30)

half_test = visual.TextStim(win=win, text=u'半程正式', pos=(-250, -100), height=30)
long_test = visual.TextStim(win=win, text=u'全程正式', pos=(0, -100), height=30)
lissajous_test = visual.TextStim(win=win, text=u'利萨如正式', pos=(250, -100), height=30)

# calibration_text = visual.TextStim(win=win, text=u'校准眼动', pos=(0, 200), color='black', bold=True)
quit_text = visual.TextStim(win=win, text=u'退出实验', pos=(0, -350), color='black', bold=True, height=30)

half_prac.draw()
long_prac.draw()
lissajous_prac.draw()
half_test.draw()
long_test.draw()
lissajous_test.draw()
# calibration_text.draw()
quit_text.draw()

select_mouse = event.Mouse(win=win, visible=True)

win.flip()


def test_start():
    """
    a function for starting test.
    :return:
    """
    while True:
        if select_mouse.isPressedIn(half_prac):
            show_instruction()
            select_mouse.setVisible(False)
            run_half(prac_or_formal='prac')
            break
        elif select_mouse.isPressedIn(long_prac):
            show_instruction()
            select_mouse.setVisible(False)
            run_long(prac_or_formal='prac')
            break
        elif select_mouse.isPressedIn(lissajous_prac):
            show_instruction()
            select_mouse.setVisible(False)
            run_lissajous(lissajous_duration, prac_or_formal='prac')
            break
        elif select_mouse.isPressedIn(half_test):
            show_instruction()
            select_mouse.setVisible(False)
            run_half(prac_or_formal='formal')
            break
        elif select_mouse.isPressedIn(long_test):
            show_instruction()
            select_mouse.setVisible(False)
            run_long(prac_or_formal='formal')
            break
        elif select_mouse.isPressedIn(lissajous_test):
            show_instruction()
            select_mouse.setVisible(False)
            run_lissajous(lissajous_duration, prac_or_formal='formal')
            break
        elif select_mouse.isPressedIn(quit_text):
            terminate_task()
            break


# STARTFIX	=	7	#Start of fixation (with time only)
# ENDFIX	=	8	#End of fixation (with summary data)
# FIXUPDATE	=	9	#Update within fixation, summary data for interval


# just for testing
# the fixation trigger duration around 250 - 350 ms will work much better.
# according to ExperimentBuilder User Manual.pdf
def fixation_trigger():
    """
    """
    fixation = visual.TextStim(win=win, text='+', height=50)
    # fx = visual.GratingStim(win=win, tex=None, mask='circle', size=25)
    fixation.draw()
    # fx.draw()
    win.flip()
    el_tracker = pylink.getEYELINK()

    el_tracker.sendCommand("record_status_message 'EVENT RETRIEVAL'")
    el_tracker.sendMessage('TRIALID')

    error = el_tracker.startRecording(1, 1, 1, 1)
    pylink.msecDelay(100)

    eye_used = el_tracker.eyeAvailable()

    if eye_used == 2:
        eye_used = 0

    # start_time_list = []
    # end_time_list = []
    fixation_time_list = []
    current_eye_pos = [100, 100]

    while True:
        ltype = el_tracker.getNextData()
        if ltype is None:
            pass
        if ltype == FIXUPDATE:
            # send a message to mark the arrival time of a fixation update event
            el_tracker.sendMessage('fixUpdate')
            ldata = el_tracker.getFloatData()
            if ldata.getEye() == eye_used:
                gaze_pos = ldata.getAverageGaze()
                # print(fixation.wrapWidth)
                current_eye_pos = [gaze_pos[0] - scnWidth / 2, scnHeight / 2 - gaze_pos[1]]
                print(current_eye_pos)
        if (-25 <= current_eye_pos[0] <= 25) and (-25 <= current_eye_pos[1] <= 25):
            fixation_time_list.append(core.getTime())
        else:
            fixation_time_list = []
            print('haha ')
        if len(fixation_time_list) > 1:
            if fixation_time_list[-1] - fixation_time_list[0] > 1:
                print('1: ' + str(fixation_time_list[0]))
                print('2: ' + str(fixation_time_list[-1]))
                print('duration: ' + str(fixation_time_list[-1] - fixation_time_list[1]))
                break

    # Step 6.7 stop recording
    el_tracker().stopRecording()

    # Step 6.8: send messages to register trial variables
    # Send over messages to record variables useful for analysis
    el_tracker().sendMessage("!V TRIAL_VAR trial")

    # Step 6.9: send TRIAL_RESULT to mark the end of a trial
    # send over a "TRIAL_RESULT" message for Data Viewer to segment the 'trials'
    el_tracker().sendMessage("TRIAL_RESULT 0")


test_start()
# fixation_trigger()

terminate_task()

