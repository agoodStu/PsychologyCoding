#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.85.6),
    on 2017_11_04_1059
If you publish work using this script please cite the PsychoPy publications:
    Peirce, JW (2007) PsychoPy - Psychophysics software in Python.
        Journal of Neuroscience Methods, 162(1-2), 8-13.
    Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy.
        Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)


# Store info about the experiment session
expName = 'exp1_py2'  # from the Builder filename that created this script
expInfo = {u'gender': u'', u'age': u'', u'participant': u'', u'name': u'', u'dominant eye': u'', u'block': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName


# block, need changed every repeat
# block1, 2, 3, 4, 5, 6, 7, 8
block = 'block' + expInfo['block']

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s' % (expInfo['participant'], expInfo['block'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(
    size=(1920, 1080), fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='eyemove', color=[-1.000,-1.000,-1.000], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='pix')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Initialize components for Routine "instuction"
instuctionClock = core.Clock()
instr_text = visual.TextStim(win=win, name='instr_text',
    text=u'\u6b22\u8fce\u53c2\u52a0\u5b9e\u9a8c,\u6309\u7a7a\u683c\u5f00\u59cb',
    font='Arial',
    pos=(0, 0), height=74.45, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "before_cal"
before_calClock = core.Clock()
before_text = visual.TextStim(win=win, name='before_text',
    text=u'\u6309\u7a7a\u683c\u5f00\u59cb\u773c\u52a8\u6821\u51c6',
    font='Arial',
    pos=(0, 0), height=74.45, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "tobii_calibra"
tobii_calibraClock = core.Clock()
from psychopy_tobii_controller import tobii_controller
ptc_controller_tobii_controller = tobii_controller(win, id=0)
ptc_controller_tobii_controller.open_datafile(_thisDir + os.sep +'eyedata' + 
    os.sep + expInfo['participant'] + '_' + expInfo['block'] + 'eyedata.xls', embed_events=True)

# Initialize components for Routine "before_test"
before_testClock = core.Clock()
before_test_text = visual.TextStim(win=win, name='before_test_text',
    text=u'\u6821\u51c6\u7ed3\u675f\uff0c\u6309\u7a7a\u683c\u5f00\u59cb\u6b63\u5f0f\u5b9e\u9a8c\u3002',
    font='Arial',
    pos=(0, 0), height=74.45, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "trial"
trialClock = core.Clock()
main_b = visual.TextStim(win=win, name='main_b',
    text=None,
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0);
main_fix = visual.TextStim(win=win, name='main_fix',
    text='+',
    font='Arial',
    pos=(0, 0), height=74.45, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=-2.0);
main_sound = sound.Sound('A', secs=-1)
main_sound.setVolume(1)
main_image = visual.ImageStim(
    win=win, name='main_image',
    image='sin', mask=None,
    ori=0, pos=[0,0], size=(312, 399),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-4.0)
sec_image = visual.ImageStim(
    win=win, name='sec_image',
    image='sec_task.png', mask=None,
    ori=0, pos=[0,0], size=(312, 413),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-5.0)
main_target = visual.TextStim(win=win, name='main_target',
    text=u'\u25cf',
    font='Arial',
    pos=[0,0], height=74.45, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=-6.0);
sec_cond = list(np.random.choice(np.arange(6, 66), 4, replace=False))

# Initialize components for Routine "main_blank"
main_blankClock = core.Clock()

main_blank_text = visual.TextStim(win=win, name='main_blank_text',
    text=None,
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0);

# Initialize components for Routine "thanks"
thanksClock = core.Clock()
thanks_text = visual.TextStim(win=win, name='thanks_text',
    text=u'\u672c\u7ec4\u5b9e\u9a8c\u7ed3\u675f\uff0c\u8bf7\u4f11\u606f\u4e24\u5206\u949f\u3002',
    font=u'Arial',
    pos=(0, 0), height=74.45, wrapWidth=None, ori=0, 
    color=u'white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "instuction"-------
t = 0
instuctionClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
instr_resp = event.BuilderKeyResponse()
# keep track of which components have finished
instuctionComponents = [instr_text, instr_resp]
for thisComponent in instuctionComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "instuction"-------
while continueRoutine:
    # get current time
    t = instuctionClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instr_text* updates
    if t >= 0.0 and instr_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        instr_text.tStart = t
        instr_text.frameNStart = frameN  # exact frame index
        instr_text.setAutoDraw(True)
    
    # *instr_resp* updates
    if t >= 0.0 and instr_resp.status == NOT_STARTED:
        # keep track of start time/frame for later
        instr_resp.tStart = t
        instr_resp.frameNStart = frameN  # exact frame index
        instr_resp.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(instr_resp.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if instr_resp.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            instr_resp.keys = theseKeys[-1]  # just the last key pressed
            instr_resp.rt = instr_resp.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instuctionComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "instuction"-------
for thisComponent in instuctionComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if instr_resp.keys in ['', [], None]:  # No response was made
    instr_resp.keys=None
thisExp.addData('instr_resp.keys',instr_resp.keys)
if instr_resp.keys != None:  # we had a response
    thisExp.addData('instr_resp.rt', instr_resp.rt)
thisExp.nextEntry()
# the Routine "instuction" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "before_cal"-------
t = 0
before_calClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
before_cal_resp = event.BuilderKeyResponse()
# keep track of which components have finished
before_calComponents = [before_text, before_cal_resp]
for thisComponent in before_calComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "before_cal"-------
while continueRoutine:
    # get current time
    t = before_calClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *before_text* updates
    if t >= 0.0 and before_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        before_text.tStart = t
        before_text.frameNStart = frameN  # exact frame index
        before_text.setAutoDraw(True)
    
    # *before_cal_resp* updates
    if t >= 0.0 and before_cal_resp.status == NOT_STARTED:
        # keep track of start time/frame for later
        before_cal_resp.tStart = t
        before_cal_resp.frameNStart = frameN  # exact frame index
        before_cal_resp.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(before_cal_resp.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if before_cal_resp.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            before_cal_resp.keys = theseKeys[-1]  # just the last key pressed
            before_cal_resp.rt = before_cal_resp.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in before_calComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "before_cal"-------
for thisComponent in before_calComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if before_cal_resp.keys in ['', [], None]:  # No response was made
    before_cal_resp.keys=None
thisExp.addData('before_cal_resp.keys',before_cal_resp.keys)
if before_cal_resp.keys != None:  # we had a response
    thisExp.addData('before_cal_resp.rt', before_cal_resp.rt)
thisExp.nextEntry()
# the Routine "before_cal" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "tobii_calibra"-------
t = 0
tobii_calibraClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
ptc_controller_tobii_controller.show_status(text_color='white', enable_mouse=True)
ptc_controller_tobii_controller.run_calibration(
    calibration_points=[[-800, -400], [800, -400], [0, 0], [-800, 400], [800, 400]],
    shuffle=True, start_key='space', decision_key='space',
    text_color='white', enable_mouse=True, move_duration=1.5)
# keep track of which components have finished
tobii_calibraComponents = []
for thisComponent in tobii_calibraComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "tobii_calibra"-------
while continueRoutine:
    # get current time
    t = tobii_calibraClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in tobii_calibraComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "tobii_calibra"-------
for thisComponent in tobii_calibraComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "tobii_calibra" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "before_test"-------
t = 0
before_testClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
before_test_resp = event.BuilderKeyResponse()
# keep track of which components have finished
before_testComponents = [before_test_text, before_test_resp]
for thisComponent in before_testComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "before_test"-------
while continueRoutine:
    # get current time
    t = before_testClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *before_test_text* updates
    if t >= 0.0 and before_test_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        before_test_text.tStart = t
        before_test_text.frameNStart = frameN  # exact frame index
        before_test_text.setAutoDraw(True)
    
    # *before_test_resp* updates
    if t >= 0.0 and before_test_resp.status == NOT_STARTED:
        # keep track of start time/frame for later
        before_test_resp.tStart = t
        before_test_resp.frameNStart = frameN  # exact frame index
        before_test_resp.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(before_test_resp.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if before_test_resp.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            before_test_resp.keys = theseKeys[-1]  # just the last key pressed
            before_test_resp.rt = before_test_resp.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in before_testComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "before_test"-------
for thisComponent in before_testComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if before_test_resp.keys in ['', [], None]:  # No response was made
    before_test_resp.keys=None
thisExp.addData('before_test_resp.keys',before_test_resp.keys)
if before_test_resp.keys != None:  # we had a response
    thisExp.addData('before_test_resp.rt', before_test_resp.rt)
thisExp.nextEntry()
# the Routine "before_test" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
main_loop = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions(block + '.xlsx'),
    seed=None, name='main_loop')
thisExp.addLoop(main_loop)  # add the loop to the experiment
thisMain_loop = main_loop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisMain_loop.rgb)
if thisMain_loop != None:
    for paramName in thisMain_loop.keys():
        exec(paramName + '= thisMain_loop.' + paramName)

for thisMain_loop in main_loop:
    currentLoop = main_loop
    # abbreviate parameter names if possible (e.g. rgb = thisMain_loop.rgb)
    if thisMain_loop != None:
        for paramName in thisMain_loop.keys():
            exec(paramName + '= thisMain_loop.' + paramName)
    
    # ------Prepare to start Routine "trial"-------
    t = 0
    trialClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    ptc_controller_tobii_controller.subscribe()
    main_sound.setSound('sounds/' + str(sound), secs=-1)
    main_image.setPos([picposition, 0])
    main_image.setImage('images/' + str(image))
    sec_image.setPos((picposition, 0))
    main_target.setPos([dotposition, 0])
    main_resp = event.BuilderKeyResponse()
    sec_resp = event.BuilderKeyResponse()
    psychopy.core.wait(0.12)
    
    # keep track of which components have finished
    trialComponents = [main_b, main_fix, main_sound, main_image, sec_image, main_target, main_resp, sec_resp]
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "trial"-------
    while continueRoutine:
        # get current time
        t = trialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *main_b* updates
        if frameN >= 0.0 and main_b.status == NOT_STARTED:
            # keep track of start time/frame for later
            main_b.tStart = t
            main_b.frameNStart = frameN  # exact frame index
            main_b.setAutoDraw(True)
        if main_b.status == STARTED and frameN >= (main_b.frameNStart + 12):
            main_b.setAutoDraw(False)
        
        # *main_fix* updates
        if frameN >= 12 and main_fix.status == NOT_STARTED:
            # keep track of start time/frame for later
            main_fix.tStart = t
            main_fix.frameNStart = frameN  # exact frame index
            main_fix.setAutoDraw(True)
            ptc_controller_tobii_controller.record_event(int(str(trigger) + '0'))
        # start/stop main_sound
        if frameN >= 12 and main_sound.status == NOT_STARTED:
            # keep track of start time/frame for later
            main_sound.tStart = t
            main_sound.frameNStart = frameN  # exact frame index
            main_sound.play()  # start the sound (it finishes automatically)
        
        # *main_image* updates
        if frameN >= 72 and main_image.status == NOT_STARTED:
            # keep track of start time/frame for later
            main_image.tStart = t
            main_image.frameNStart = frameN  # exact frame index
            main_image.setAutoDraw(True)
            ptc_controller_tobii_controller.record_event(int(str(trigger) + '1'))
        if main_image.status == STARTED and frameN >= (main_image.frameNStart + 12):
            main_image.setAutoDraw(False)
        
        # *sec_image* updates
        if main_loop.thisTrialN in sec_cond:
            if frameN >= 72 and sec_image.status == NOT_STARTED:
                # keep track of start time/frame for later
                sec_image.tStart = t
                sec_image.frameNStart = frameN  # exact frame index
                sec_image.setAutoDraw(True)
                ptc_controller_tobii_controller.record_event(int(str(trigger) + '3'))
            if sec_image.status == STARTED and frameN >= (sec_image.frameNStart + 12):
                sec_image.setAutoDraw(False)
        
        # *main_target* updates
        if frameN >= 87 and main_target.status == NOT_STARTED:
            # keep track of start time/frame for later
            main_target.tStart = t
            main_target.frameNStart = frameN  # exact frame index
            main_target.setAutoDraw(True)
            ptc_controller_tobii_controller.record_event(int(str(trigger) + '2'))
        
        # *main_resp* updates
        if frameN >= 87 and main_resp.status == NOT_STARTED:
            # keep track of start time/frame for later
            main_resp.tStart = t
            main_resp.frameNStart = frameN  # exact frame index
            main_resp.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(main_resp.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if main_resp.status == STARTED:
            theseKeys = event.getKeys(keyList=['f', 'j'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                main_resp.keys = theseKeys[-1]  # just the last key pressed
                main_resp.rt = main_resp.clock.getTime()
                # was this 'correct'?
                if (main_resp.keys == str(correctAns)) or (main_resp.keys == correctAns):
                    main_resp.corr = 1
                else:
                    main_resp.corr = 0
                # a response ends the routine
                ptc_controller_tobii_controller.record_event(main_resp.corr)
                continueRoutine = False
        
        # *sec_resp* updates
        if main_loop.thisTrialN in sec_cond:
            if frameN >= 72 and sec_resp.status == NOT_STARTED:
                # keep track of start time/frame for later
                sec_resp.tStart = t
                sec_resp.frameNStart = frameN  # exact frame index
                sec_resp.status = STARTED
                # keyboard checking is just starting
                win.callOnFlip(sec_resp.clock.reset)  # t=0 on next screen flip
                event.clearEvents(eventType='keyboard')
            if sec_resp.status == STARTED:
                theseKeys = event.getKeys(keyList=['space'])
                
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    sec_resp.keys = theseKeys[-1]  # just the last key pressed
                    sec_resp.rt = sec_resp.clock.getTime()
                    # was this 'correct'?
                    if (sec_resp.keys == str('space')) or (sec_resp.keys == 'space'):
                        sec_resp.corr = 1
                    else:
                        sec_resp.corr = 0
        
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    ptc_controller_tobii_controller.unsubscribe()
    main_sound.stop()  # ensure sound has stopped at end of routine
    # check responses
    if main_resp.keys in ['', [], None]:  # No response was made
        main_resp.keys=None
        # was no response the correct answer?!
        if str(correctAns).lower() == 'none':
           main_resp.corr = 1  # correct non-response
        else:
           main_resp.corr = 0  # failed to respond (incorrectly)
    # store data for main_loop (TrialHandler)
    main_loop.addData('main_resp.keys',main_resp.keys)
    main_loop.addData('main_resp.corr', main_resp.corr)
    if main_resp.keys != None:  # we had a response
        main_loop.addData('main_resp.rt', main_resp.rt)
    # check responses
    if sec_resp.keys in ['', [], None]:  # No response was made
        sec_resp.keys=None
        # was no response the correct answer?!
        if str('space').lower() == 'none':
           sec_resp.corr = 1  # correct non-response
        else:
           sec_resp.corr = 0  # failed to respond (incorrectly)
    # store data for main_loop (TrialHandler)
    main_loop.addData('sec_resp.keys',sec_resp.keys)
    main_loop.addData('sec_resp.corr', sec_resp.corr)
    if sec_resp.keys != None:  # we had a response
        main_loop.addData('sec_resp.rt', sec_resp.rt)
    
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "main_blank"-------
    t = 0
    main_blankClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    
    # keep track of which components have finished
    main_blankComponents = [main_blank_text]
    for thisComponent in main_blankComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "main_blank"-------
    while continueRoutine:
        # get current time
        t = main_blankClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        import random
        
        ITI = random.randint(800,1500)
        
        ITI = ITI * 0.001
        
        # *main_blank_text* updates
        if t >= 0.0 and main_blank_text.status == NOT_STARTED:
            # keep track of start time/frame for later
            main_blank_text.tStart = t
            main_blank_text.frameNStart = frameN  # exact frame index
            main_blank_text.setAutoDraw(True)
        frameRemains = 0.0 + ITI- win.monitorFramePeriod * 0.75  # most of one frame period left
        if main_blank_text.status == STARTED and t >= frameRemains:
            main_blank_text.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in main_blankComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "main_blank"-------
    for thisComponent in main_blankComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('ITI', ITI)
    # the Routine "main_blank" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1 repeats of 'main_loop'


# ------Prepare to start Routine "thanks"-------
t = 0
thanksClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
thanks_resp = event.BuilderKeyResponse()
# keep track of which components have finished
thanksComponents = [thanks_text, thanks_resp]
for thisComponent in thanksComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "thanks"-------
while continueRoutine:
    # get current time
    t = thanksClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *thanks_text* updates
    if t >= 0.0 and thanks_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        thanks_text.tStart = t
        thanks_text.frameNStart = frameN  # exact frame index
        thanks_text.setAutoDraw(True)
    
    # *thanks_resp* updates
    if t >= 0.0 and thanks_resp.status == NOT_STARTED:
        # keep track of start time/frame for later
        thanks_resp.tStart = t
        thanks_resp.frameNStart = frameN  # exact frame index
        thanks_resp.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(thanks_resp.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if thanks_resp.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            thanks_resp.keys = theseKeys[-1]  # just the last key pressed
            thanks_resp.rt = thanks_resp.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in thanksComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "thanks"-------
for thisComponent in thanksComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if thanks_resp.keys in ['', [], None]:  # No response was made
    thanks_resp.keys=None
thisExp.addData('thanks_resp.keys',thanks_resp.keys)
if thanks_resp.keys != None:  # we had a response
    thisExp.addData('thanks_resp.rt', thanks_resp.rt)
thisExp.nextEntry()
# the Routine "thanks" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()
ptc_controller_tobii_controller.close_datafile()


# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
