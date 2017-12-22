# -*- coding: utf-8 -*-
from psychopy import visual, core, event, gui
import random

# get subject info use a dialog
expInfo = {'Subject':['01_M', '02_Y', '03_X'], 'Gender':['M', 'F'], 'Age':[18, 19, 20, 21, 22, 23, 24, 25]}
dlg = gui.DlgFromDict(expInfo, title = "FaceRating", order = ['Subject', 'Gender', 'Age'])
if not dlg.OK: 
    core.quit() # the user hit cancle so exit
    
    
# trail
trail = [[0, 0], [0, 1], [0, 2], [0,3], [0, 4], [0, 5], [0, 6],[0, 7],
         [1, 0], [1, 1], [1, 2], [1,3], [1, 4], [1, 5], [1, 6],[1, 7],
         [2, 0], [2, 1], [2, 2], [2,3], [2, 4], [2, 5], [2, 6],[2, 7],
         [3, 0], [3, 1], [3, 2], [3,3], [3, 4], [3, 5], [3, 6],[3, 7],
         [4, 0], [4, 1], [4, 2], [4,3], [4, 4], [4, 5], [4, 6],[4, 7],
         [5, 0], [5, 1], [5, 2], [5,3], [5, 4], [5, 5], [5, 6],[5, 7],
         [6, 0], [6, 1], [6, 2], [6,3], [6, 4], [6, 5], [6, 6],[6, 7],
         [7, 0], [7, 1], [7, 2], [7,3], [7, 4], [7, 5], [7, 6],[7, 7],
     ]   
random.shuffle(trail)

# open a data file
dataFile = open(expInfo['Subject'] + '.csv', 'w')

# prepare the window and instruction stimulis
win = visual.Window([800, 600], color = 'black', fullscr = True, monitor = 'lenovo', units = 'deg')
instruction = visual.ImageStim(win, image = 'instruction.jpg')

control = False

# present the instructions
while not control:
#    instr1.draw()
#    instr2.draw()
#    instr3.draw()
    instruction.draw()
    win.flip()
    
    # wait key for starting
    enterKeys = event.waitKeys()
    if enterKeys[0] in ['return']:
        break

#start the loop
for i in trail:
    if i[0] != i[1]:  # exclude the same number(picture)
        leftPicStim = visual.ImageStim(win, image = str(i[0]) + '.jpg', size = 5, pos = [-10, 0])
        rightPicStim = visual.ImageStim(win, image = str(i[1]) + '.jpg', size = 5, pos = [10, 0])
        
        # present the fixation 500ms
        fixation = visual.TextStim(win, text = '+')
        fixation.draw()
        win.flip()
        core.wait(0.5)
        
        # present pictures
        leftPicStim.draw()
        rightPicStim.draw()
        respStart = core.getTime()
        win.flip()
        
        # wait for user response and record the RT 
        enterKeys = event.waitKeys(keyList = ['j', 'k'])
        if enterKeys[0] in ['j', 'k']:
            respKey = enterKeys[0]
            respEnd = core.getTime()
        
        # save data
        data2save = [respStart] + expInfo.values() + [respEnd] + i + [respKey]
        data2save = map(str, data2save)
        dataFile.write(','.join(data2save) + '\n')

# close file
dataFile.close()

# say bye
msg = visual.TextStim(win, text = 'THANK YOU FOR ATTENDING!')
msg.draw()
win.flip()
core.wait(2)
core.quit()
