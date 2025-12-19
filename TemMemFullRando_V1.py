#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2024.2.1),
    on Fri Dec 19 11:35:46 2025
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
prefs.hardware['audioLib'] = 'ptb'
prefs.hardware['audioLatencyMode'] = '3'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware
from psychopy.tools import environmenttools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER, priority)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2024.2.1'
expName = 'TemMemFullRando_V1'  # from the Builder filename that created this script
# information about this experiment
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
    'date|hid': data.getDateStr(),
    'expName|hid': expName,
    'psychopyVersion|hid': psychopyVersion,
}

# --- Define some variables which will change depending on pilot mode ---
'''
To run in pilot mode, either use the run/pilot toggle in Builder, Coder and Runner, 
or run the experiment with `--pilot` as an argument. To change what pilot 
#mode does, check out the 'Pilot mode' tab in preferences.
'''
# work out from system args whether we are running in pilot mode
PILOTING = core.setPilotModeFromArgs()
# start off with values from experiment settings
_fullScr = True
_winSize = [2240, 1260]
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting['forceWindowed']:
        _fullScr = False
        # set window size
        _winSize = prefs.piloting['forcedWindowSize']

def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # show participant info dialog
    dlg = gui.DlgFromDict(
        dictionary=expInfo, sortKeys=False, title=expName, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    # remove dialog-specific syntax from expInfo
    for key, val in expInfo.copy().items():
        newKey, _ = data.utils.parsePipeSyntax(key)
        expInfo[newKey] = expInfo.pop(key)
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath='/Users/aussie-dzmac/Documents/InfoShuffleProject/TemMem_W2026/TemMemFullRando_V1.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # set how much information should be printed to the console / app
    if PILOTING:
        logging.console.setLevel(
            prefs.piloting['pilotConsoleLoggingLevel']
        )
    else:
        logging.console.setLevel('warning')
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log')
    if PILOTING:
        logFile.setLevel(
            prefs.piloting['pilotLoggingLevel']
        )
    else:
        logFile.setLevel(
            logging.getLevel('info')
        )
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if PILOTING:
        logging.debug('Fullscreen settings ignored as running in pilot mode.')
    
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=_winSize, fullscr=_fullScr, screen=0,
            winType='pyglet', allowStencil=False,
            monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height', 
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0,0,0]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    if expInfo is not None:
        # get/measure frame rate if not already in expInfo
        if win._monitorFrameRate is None:
            win._monitorFrameRate = win.getActualFrameRate(infoMsg='Attempting to measure frame rate of screen, please wait...')
        expInfo['frameRate'] = win._monitorFrameRate
    win.mouseVisible = False
    win.hideMessage()
    # show a visual indicator if we're in piloting mode
    if PILOTING and prefs.piloting['showPilotingIndicator']:
        win.showPilotingIndicator()
    
    return win


def setupDevices(expInfo, thisExp, win):
    """
    Setup whatever devices are available (mouse, keyboard, speaker, eyetracker, etc.) and add them to 
    the device manager (deviceManager)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    bool
        True if completed successfully.
    """
    # --- Setup input devices ---
    ioConfig = {}
    
    # Setup iohub keyboard
    ioConfig['Keyboard'] = dict(use_keymap='psychopy')
    
    # Setup iohub experiment
    ioConfig['Experiment'] = dict(filename=thisExp.dataFileName)
    
    # Start ioHub server
    ioServer = io.launchHubServer(window=win, **ioConfig)
    
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='iohub'
        )
    if deviceManager.getDevice('helloResp') is None:
        # initialise helloResp
        helloResp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='helloResp',
        )
    if deviceManager.getDevice('IntroResp') is None:
        # initialise IntroResp
        IntroResp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='IntroResp',
        )
    if deviceManager.getDevice('LearningInst1Resp') is None:
        # initialise LearningInst1Resp
        LearningInst1Resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='LearningInst1Resp',
        )
    if deviceManager.getDevice('LearningInst2Resp') is None:
        # initialise LearningInst2Resp
        LearningInst2Resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='LearningInst2Resp',
        )
    if deviceManager.getDevice('LearningInst3Resp') is None:
        # initialise LearningInst3Resp
        LearningInst3Resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='LearningInst3Resp',
        )
    if deviceManager.getDevice('LearningInst4Resp') is None:
        # initialise LearningInst4Resp
        LearningInst4Resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='LearningInst4Resp',
        )
    if deviceManager.getDevice('LearningEncodingExample1Resp') is None:
        # initialise LearningEncodingExample1Resp
        LearningEncodingExample1Resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='LearningEncodingExample1Resp',
        )
    if deviceManager.getDevice('break1Resp') is None:
        # initialise break1Resp
        break1Resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='break1Resp',
        )
    if deviceManager.getDevice('LearningEncodingExample2Resp') is None:
        # initialise LearningEncodingExample2Resp
        LearningEncodingExample2Resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='LearningEncodingExample2Resp',
        )
    if deviceManager.getDevice('LearningEncodingExample3Resp') is None:
        # initialise LearningEncodingExample3Resp
        LearningEncodingExample3Resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='LearningEncodingExample3Resp',
        )
    if deviceManager.getDevice('LearningEncodingExample4Resp') is None:
        # initialise LearningEncodingExample4Resp
        LearningEncodingExample4Resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='LearningEncodingExample4Resp',
        )
    if deviceManager.getDevice('LearningQuestionResp') is None:
        # initialise LearningQuestionResp
        LearningQuestionResp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='LearningQuestionResp',
        )
    if deviceManager.getDevice('key_resp_2') is None:
        # initialise key_resp_2
        key_resp_2 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp_2',
        )
    if deviceManager.getDevice('key_resp_3') is None:
        # initialise key_resp_3
        key_resp_3 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp_3',
        )
    if deviceManager.getDevice('TimeEstimateResp') is None:
        # initialise TimeEstimateResp
        TimeEstimateResp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='TimeEstimateResp',
        )
    if deviceManager.getDevice('DistractorInstResp') is None:
        # initialise DistractorInstResp
        DistractorInstResp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='DistractorInstResp',
        )
    if deviceManager.getDevice('DistractorExample1Resp') is None:
        # initialise DistractorExample1Resp
        DistractorExample1Resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='DistractorExample1Resp',
        )
    if deviceManager.getDevice('DistractorExample2Resp') is None:
        # initialise DistractorExample2Resp
        DistractorExample2Resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='DistractorExample2Resp',
        )
    if deviceManager.getDevice('DistractorQuestionResp') is None:
        # initialise DistractorQuestionResp
        DistractorQuestionResp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='DistractorQuestionResp',
        )
    if deviceManager.getDevice('TestInstResp') is None:
        # initialise TestInstResp
        TestInstResp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='TestInstResp',
        )
    if deviceManager.getDevice('TestExampleResp') is None:
        # initialise TestExampleResp
        TestExampleResp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='TestExampleResp',
        )
    if deviceManager.getDevice('TestQuestionResp') is None:
        # initialise TestQuestionResp
        TestQuestionResp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='TestQuestionResp',
        )
    if deviceManager.getDevice('welcomeResp') is None:
        # initialise welcomeResp
        welcomeResp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='welcomeResp',
        )
    if deviceManager.getDevice('StudyReminderResp') is None:
        # initialise StudyReminderResp
        StudyReminderResp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='StudyReminderResp',
        )
    if deviceManager.getDevice('StudyTrialResp') is None:
        # initialise StudyTrialResp
        StudyTrialResp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='StudyTrialResp',
        )
    if deviceManager.getDevice('key_resp') is None:
        # initialise key_resp
        key_resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp',
        )
    if deviceManager.getDevice('DistractorReminderResp') is None:
        # initialise DistractorReminderResp
        DistractorReminderResp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='DistractorReminderResp',
        )
    if deviceManager.getDevice('DistractorResp') is None:
        # initialise DistractorResp
        DistractorResp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='DistractorResp',
        )
    if deviceManager.getDevice('TestReminderResp') is None:
        # initialise TestReminderResp
        TestReminderResp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='TestReminderResp',
        )
    if deviceManager.getDevice('TestResp') is None:
        # initialise TestResp
        TestResp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='TestResp',
        )
    if deviceManager.getDevice('GoodbyeResp') is None:
        # initialise GoodbyeResp
        GoodbyeResp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='GoodbyeResp',
        )
    # return True if completed successfully
    return True

def pauseExperiment(thisExp, win=None, timers=[], playbackComponents=[]):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    playbackComponents : list, tuple
        List of any components with a `pause` method which need to be paused.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # start a timer to figure out how long we're paused for
    pauseTimer = core.Clock()
    # pause any playback components
    for comp in playbackComponents:
        comp.pause()
    # make sure we have a keyboard
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        defaultKeyboard = deviceManager.addKeyboard(
            deviceClass='keyboard',
            deviceName='defaultKeyboard',
            backend='ioHub',
        )
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win)
        # sleep 1ms so other threads can execute
        clock.time.sleep(0.001)
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    for comp in playbackComponents:
        comp.play()
    # reset any timers
    for timer in timers:
        timer.addTime(-pauseTimer.getTime())


def run(expInfo, thisExp, win, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = deviceManager.ioServer
    # get/create a default keyboard (e.g. to check for escape)
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='ioHub'
        )
    eyetracker = deviceManager.getDevice('eyetracker')
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    
    # --- Initialize components for Routine "block_counter" ---
    # Run 'Begin Experiment' code from code_6
    block_num = 1
    
    # --- Initialize components for Routine "hello" ---
    helleText = visual.TextStim(win=win, name='helleText',
        text='Welcome to the experiment! \n\n\n\n\n\nPress SPACEBAR for instructions',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    helloResp = keyboard.Keyboard(deviceName='helloResp')
    
    # --- Initialize components for Routine "Intro" ---
    IntroText = visual.TextStim(win=win, name='IntroText',
        text='In this experiment, you will complete a series of mini-experiments called Blocks. In total, you will complete 10 Blocks. \n\nEach Block will consist of 4 phases:\n\n(1) Learning phase\n(2) Time estimation task \n(3) Odd/even task\n(4) Test phase\n  \n\n\nPress SPACEBAR to continue ',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    IntroResp = keyboard.Keyboard(deviceName='IntroResp')
    
    # --- Initialize components for Routine "LearningInst" ---
    LearningInst1Text = visual.TextStim(win=win, name='LearningInst1Text',
        text='LEARNING PHASE\n\n\n\nIn this task, you will see a series of images presented one at a time. \n\nYour task will be to remember the order in which you saw the images. \n\n\n\nPress SPACEBAR to continue\n',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    LearningInst1Resp = keyboard.Keyboard(deviceName='LearningInst1Resp')
    
    # --- Initialize components for Routine "LearningInst2" ---
    LearningInst2Text = visual.TextStim(win=win, name='LearningInst2Text',
        text='LEARNING PHASE \n\n\n\nTo help you remember, we encourage you to link the images together by making up a story that connects them in the order you see them. \n\nFor example, if you see see an APPLE, then a CHAIR, then a PEN, you could imagine yourself eating an apple while sitting on a chair and writing a letter with the pen...\n\n\n\nPress SPACEBAR to continue',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    LearningInst2Resp = keyboard.Keyboard(deviceName='LearningInst2Resp')
    
    # --- Initialize components for Routine "LearningInst3" ---
    LearningInst3Text = visual.TextStim(win=win, name='LearningInst3Text',
        text='LEARNING PHASE\n\n\nAlso, for each image, you will be asked to answer a question. There are 5 possible questions: \n\n1. Would this item fit in a shoebox?\n2. Does this item contain any metal?\n3. Do you know the word for this item in any other languages?\n4. Do you find this item to be pleasant?\n5. Is this item man-made?\n\n\nPress SPACEBAR to continue',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    LearningInst3Resp = keyboard.Keyboard(deviceName='LearningInst3Resp')
    
    # --- Initialize components for Routine "LearningIns4" ---
    LearningInst4Text = visual.TextStim(win=win, name='LearningInst4Text',
        text='LEARNING PHASE\n \n\nThe question may be different for each image. \n\nYou will have 4 seconds after the question appears to make your response before the screen advances. \n\nThe screen will NOT advance immediately when you make your response. \n\n\nPress SPACEBAR to continue',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    LearningInst4Resp = keyboard.Keyboard(deviceName='LearningInst4Resp')
    
    # --- Initialize components for Routine "LearningExample1" ---
    LearningExample1Image = visual.ImageStim(
        win=win,
        name='LearningExample1Image', 
        image='strawberry.jpg', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(0.5, 0.5),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    LearningEncodingQuestion1Text = visual.TextStim(win=win, name='LearningEncodingQuestion1Text',
        text='Does this item contain any metal?',
        font='Arial',
        pos=(0, 0.3), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    LearningEncodingOptions1Text = visual.TextStim(win=win, name='LearningEncodingOptions1Text',
        text='left arrow: yes                    right arrow: no',
        font='Arial',
        pos=(0, -0.4), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    LearningEncodingExample1Resp = keyboard.Keyboard(deviceName='LearningEncodingExample1Resp')
    
    # --- Initialize components for Routine "break1" ---
    break1Text = visual.TextStim(win=win, name='break1Text',
        text='LEARNING PHASE \n\n\n\nIn the next example, you will get a chance to practice using the actual timing of the task. \n\nRemember: you have 4 seconds to answer the question before the screen automatically advances. \n\nPractice creating a story that links the items and say it out loud. \n\nPress 5 to practice',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    break1Resp = keyboard.Keyboard(deviceName='break1Resp')
    
    # --- Initialize components for Routine "LearningExample2" ---
    LearningExample2Image = visual.ImageStim(
        win=win,
        name='LearningExample2Image', 
        image='rubberduck.jpg', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(0.5, 0.5),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    LearningEncodingQuestion2Text = visual.TextStim(win=win, name='LearningEncodingQuestion2Text',
        text='Do you find this item to be pleasant?',
        font='Arial',
        pos=(0, 0.3), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    LearningEncodingOptions2Text = visual.TextStim(win=win, name='LearningEncodingOptions2Text',
        text='left arrow: yes                    right arrow: no ',
        font='Arial',
        pos=(0, -0.4), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    LearningEncodingExample2Resp = keyboard.Keyboard(deviceName='LearningEncodingExample2Resp')
    
    # --- Initialize components for Routine "LearningExample3" ---
    LearningExample3Image = visual.ImageStim(
        win=win,
        name='LearningExample3Image', 
        image='umbrella.jpg', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(0.5, 0.5),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    LearningEncodingQuestion3Text = visual.TextStim(win=win, name='LearningEncodingQuestion3Text',
        text='Is this item man-made?',
        font='Arial',
        pos=(0, 0.3), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    LearningEncodingOption3Text = visual.TextStim(win=win, name='LearningEncodingOption3Text',
        text='left arrow: yes                    right arrow: no ',
        font='Arial',
        pos=(0, -0.4), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    LearningEncodingExample3Resp = keyboard.Keyboard(deviceName='LearningEncodingExample3Resp')
    
    # --- Initialize components for Routine "LearningExample4" ---
    LearningExample4Image = visual.ImageStim(
        win=win,
        name='LearningExample4Image', 
        image='pbj.jpg', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(0.5, 0.5),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    LearningEncodingQuestion4Text = visual.TextStim(win=win, name='LearningEncodingQuestion4Text',
        text='Would this item fit in a shoe box?',
        font='Arial',
        pos=(0, 0.3), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    LearningEncodingOption4Text = visual.TextStim(win=win, name='LearningEncodingOption4Text',
        text='left arrow: yes                    right arrow: no ',
        font='Arial',
        pos=(0, -0.4), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    LearningEncodingExample4Resp = keyboard.Keyboard(deviceName='LearningEncodingExample4Resp')
    
    # --- Initialize components for Routine "LearningQuestion" ---
    LearningQuestionText = visual.TextStim(win=win, name='LearningQuestionText',
        text='LEARNING PHASE\n\n\n\nDo you have any questions about this phase of the experiment? \n\n\n\nPress SPACEBAR to continue ',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    LearningQuestionResp = keyboard.Keyboard(deviceName='LearningQuestionResp')
    
    # --- Initialize components for Routine "TimeEstimateInst" ---
    text_2 = visual.TextStim(win=win, name='text_2',
        text='TIME ESTIMATION TASK \n\n\nYou will be asked to estimate how long you think the LEARNING PHASE you just completed lasted for. \n\nYou will use the LEFT and RIGHT arrows to toggle between MINUTES AND SECONDS. \n\nYou will use the UP and DOWN arrows to adjust the timer.\n\n\nPress SPACEBAR for an example',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    key_resp_2 = keyboard.Keyboard(deviceName='key_resp_2')
    
    # --- Initialize components for Routine "TimeEstimateExample" ---
    TimeEstimateDsiplay = visual.TextStim(win=win, name='TimeEstimateDsiplay',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.15, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, 0.0902], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    key_resp_3 = keyboard.Keyboard(deviceName='key_resp_3')
    TimeEstimateExampleInst = visual.TextStim(win=win, name='TimeEstimateExampleInst',
        text='Estimate how long the LEARNING PHASE lasted for. \n\nUse the LEFT and RIGHT arrows to toggle between MINUTES AND SECONDS. \n\nUse the UP and DOWN arrows to adjust the timer.',
        font='Arial',
        pos=(0, 0.25), draggable=False, height=0.04, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    TimeEstimateExampleConfirm = visual.TextStim(win=win, name='TimeEstimateExampleConfirm',
        text='Press RETURN to confirm ',
        font='Arial',
        pos=(0, -0.35), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0);
    TimeEstimateExampleUnits = visual.TextStim(win=win, name='TimeEstimateExampleUnits',
        text='minutes   :   seconds',
        font='Arial',
        pos=(0, -0.16), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-4.0);
    
    # --- Initialize components for Routine "TimeEstimateQuestion_2" ---
    TimeEstimateQuestion = visual.TextStim(win=win, name='TimeEstimateQuestion',
        text='TIME ESTIMATION TASK \n\nDo you have any questions about this phase of the experiment? \n\n\n\nPress SPACEBAR to continue ',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    TimeEstimateResp = keyboard.Keyboard(deviceName='TimeEstimateResp')
    
    # --- Initialize components for Routine "DistractorInst" ---
    DistractorInstText = visual.TextStim(win=win, name='DistractorInstText',
        text='ODD/EVEN TASK\n\n\nYou will be shown a series of numbers one at a time. \n\nYour task is to use the keyboard to indicate if you think the presented number is an ODD or EVEN number. \n\nYou will have 2 seconds to make your response before the screen advances. \n\n\nPress 5 to practice ',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    DistractorInstResp = keyboard.Keyboard(deviceName='DistractorInstResp')
    
    # --- Initialize components for Routine "DistractorExample1" ---
    DistractorExample1Number = visual.TextStim(win=win, name='DistractorExample1Number',
        text='3',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    DistractorExample1OptionsText = visual.TextStim(win=win, name='DistractorExample1OptionsText',
        text='left arrow: odd                  right arrow: even',
        font='Arial',
        pos=(0, -0.4), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    DistractorExample1Resp = keyboard.Keyboard(deviceName='DistractorExample1Resp')
    
    # --- Initialize components for Routine "DistractorExample2" ---
    DistractorExample2Number = visual.TextStim(win=win, name='DistractorExample2Number',
        text='34',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    DistractorExample2OptionsText = visual.TextStim(win=win, name='DistractorExample2OptionsText',
        text='left arrow: odd                  right arrow: even',
        font='Arial',
        pos=(0, -0.4), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    DistractorExample2Resp = keyboard.Keyboard(deviceName='DistractorExample2Resp')
    
    # --- Initialize components for Routine "DistractorQuestion" ---
    DistractorQuestionText = visual.TextStim(win=win, name='DistractorQuestionText',
        text='ODD/EVEN PHASE\n\n\nDo you have any questions about this phase of the experiment? \n\n\n\nPress SPACEBAR to continue ',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    DistractorQuestionResp = keyboard.Keyboard(deviceName='DistractorQuestionResp')
    
    # --- Initialize components for Routine "TestInst" ---
    TestInstText = visual.TextStim(win=win, name='TestInstText',
        text='TEST PHASE\n\n\n\nYou will be presented with pairs of images. \n\nYour task will be to indicate which image you remember seeing first during the learning phase. \n\nYou will have a maximum of 8 seconds to make your response before the screen advances. \n\n\n\nPress 5 to practice',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    TestInstResp = keyboard.Keyboard(deviceName='TestInstResp')
    
    # --- Initialize components for Routine "TestExample" ---
    TestExampleLeftImage = visual.ImageStim(
        win=win,
        name='TestExampleLeftImage', 
        image='umbrella.jpg', mask=None, anchor='center',
        ori=0.0, pos=(-0.3, 0), draggable=False, size=(0.5, 0.5),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    TestExampleRightImage = visual.ImageStim(
        win=win,
        name='TestExampleRightImage', 
        image='rubberduck.jpg', mask=None, anchor='center',
        ori=0.0, pos=(0.3, 0), draggable=False, size=(0.5, 0.5),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-1.0)
    TestExampleResp = keyboard.Keyboard(deviceName='TestExampleResp')
    TestExampleOptions = visual.TextStim(win=win, name='TestExampleOptions',
        text='left arrow                             right arrow ',
        font='Arial',
        pos=(0, -0.4), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0);
    TestExampleQuestion = visual.TextStim(win=win, name='TestExampleQuestion',
        text='Which did you see first?',
        font='Arial',
        pos=(0, 0.3), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-4.0);
    
    # --- Initialize components for Routine "TestQuestion" ---
    TestQuestionText = visual.TextStim(win=win, name='TestQuestionText',
        text='TEST PHASE\n\n\nDo you have any questions about this phase of the experiment? \n\n\n\nPress SPACEBAR to continue ',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    TestQuestionResp = keyboard.Keyboard(deviceName='TestQuestionResp')
    
    # --- Initialize components for Routine "SpecifyingSubSpecificFolder" ---
    # Run 'Begin Experiment' code from code_10
    conditionsFile = os.path.join(
        '/Users',
        'aussie-dzmac',
        'Documents/InfoShuffleProject/TemMem_W2026/SubjectFiles_TemMemFullRando',
        expInfo['participant'],
        'blocks_V1.csv'
    )
    
    # --- Initialize components for Routine "welcome" ---
    welcomeText = visual.TextStim(win=win, name='welcomeText',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    welcomeResp = keyboard.Keyboard(deviceName='welcomeResp')
    
    # --- Initialize components for Routine "StudyReminder" ---
    StudyReminderText = visual.TextStim(win=win, name='StudyReminderText',
        text='LEARNING PHASE\n\n\nYour task is to: \n\n(1) remember the order in which you see the images; create a story in mind your mind to help you remember \n\n(2) use the keyboard to answer the question \n\nYou will have 4 seconds to make your response before the screen advances. \n\n\nPress 5 to begin',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    StudyReminderResp = keyboard.Keyboard(deviceName='StudyReminderResp')
    
    # --- Initialize components for Routine "StudyTrial" ---
    StudyTrialText = visual.TextStim(win=win, name='StudyTrialText',
        text='',
        font='Arial',
        pos=(0, 0.35), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    studyTrialImage = visual.ImageStim(
        win=win,
        name='studyTrialImage', 
        image='default.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(0.5, 0.5),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-1.0)
    StudyTrialResp = keyboard.Keyboard(deviceName='StudyTrialResp')
    StudyTrialOptions = visual.TextStim(win=win, name='StudyTrialOptions',
        text='left arrow: yes                    right arrow: no',
        font='Arial',
        pos=(0, -0.4), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0);
    
    # --- Initialize components for Routine "transition1" ---
    transition1Text = visual.TextStim(win=win, name='transition1Text',
        text='Please wait. The next phase will begin shortly. ',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "timeEstimate" ---
    time_display = visual.TextStim(win=win, name='time_display',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.15, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, 0.0902], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    key_resp = keyboard.Keyboard(deviceName='key_resp')
    timeEstimateInstructions = visual.TextStim(win=win, name='timeEstimateInstructions',
        text='Estimate how long this block lasted for. \n\nUse the LEFT and RIGHT arrows to toggle between MINUTES AND SECONDS. \n\nUse the UP and DOWN arrows to adjust the timer.',
        font='Arial',
        pos=(0, 0.25), draggable=False, height=0.04, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0);
    TimeEstimateConfirm = visual.TextStim(win=win, name='TimeEstimateConfirm',
        text='Press RETURN to confirm ',
        font='Arial',
        pos=(0, -0.35), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-4.0);
    TimeEstimateTimerText = visual.TextStim(win=win, name='TimeEstimateTimerText',
        text='minutes   :   seconds',
        font='Arial',
        pos=(0, -0.16), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-5.0);
    
    # --- Initialize components for Routine "transition2" ---
    Transition2Text = visual.TextStim(win=win, name='Transition2Text',
        text='Please wait. The next phase will begin shortly. ',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "DistractorReminder" ---
    DistractorReminderText = visual.TextStim(win=win, name='DistractorReminderText',
        text='ODD/EVEN TASK\n\n\n\nYour task is to use the keyboard to indicate if the presented number is an ODD or EVEN number\n\nYou will have 2 seconds to make your response before the screen advances. \n\n\n\nPress 5 to begin',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    DistractorReminderResp = keyboard.Keyboard(deviceName='DistractorReminderResp')
    
    # --- Initialize components for Routine "distractor_start" ---
    
    # --- Initialize components for Routine "Distractor" ---
    # Run 'Begin Experiment' code from code_4
    import random
    
    # The distractor loop is set for 1000 repeats
    # which is why the outout data file will have 500 
    # rows total (each trial is 2 seconds); this will 
    # include the actual participant trials plus all 
    # the 'extras' that will be blank
    numberText = visual.TextStim(win=win, name='numberText',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.1, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    DistractorResp = keyboard.Keyboard(deviceName='DistractorResp')
    DistractorOptions = visual.TextStim(win=win, name='DistractorOptions',
        text='left: odd                              right: even',
        font='Arial',
        pos=(0, -0.4), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0);
    
    # --- Initialize components for Routine "transition3" ---
    transition3Text = visual.TextStim(win=win, name='transition3Text',
        text='Please wait. The next phase will begin shortly. ',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "TestReminder" ---
    TestReminderText = visual.TextStim(win=win, name='TestReminderText',
        text='TEST PHASE\n\n\n\nYour task will be to indicate which image you remember seeing first during the learning phase. \n\nYou will have a miximum of 8 seconds to make your response before the screen advances. \n\n\n\nPress 5 to begin',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    TestReminderResp = keyboard.Keyboard(deviceName='TestReminderResp')
    
    # --- Initialize components for Routine "TestTrial" ---
    leftImg = visual.ImageStim(
        win=win,
        name='leftImg', 
        image='default.png', mask=None, anchor='center',
        ori=0.0, pos=(-0.3, 0), draggable=False, size=(0.5, 0.5),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    rightImg = visual.ImageStim(
        win=win,
        name='rightImg', 
        image='default.png', mask=None, anchor='center',
        ori=0.0, pos=(0.3, 0), draggable=False, size=(0.5, 0.5),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-1.0)
    TestResp = keyboard.Keyboard(deviceName='TestResp')
    TestOptions = visual.TextStim(win=win, name='TestOptions',
        text='left arrow                             right arrow ',
        font='Arial',
        pos=(0, -0.4), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0);
    TestQuestionPrompt = visual.TextStim(win=win, name='TestQuestionPrompt',
        text='Which did you see first?',
        font='Arial',
        pos=(0, 0.3), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-4.0);
    
    # --- Initialize components for Routine "block_end" ---
    blockendText = visual.TextStim(win=win, name='blockendText',
        text='The next block will begin shortly. Please wait. ',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "goodbye" ---
    GoodbyeText = visual.TextStim(win=win, name='GoodbyeText',
        text='This is the end of the experiment. \n\nThank you for your participation!!\n\n\n\n\n\nPress SPACEBAR to exit',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    GoodbyeResp = keyboard.Keyboard(deviceName='GoodbyeResp')
    
    # create some handy timers
    
    # global clock to track the time since experiment started
    if globalClock is None:
        # create a clock if not given one
        globalClock = core.Clock()
    if isinstance(globalClock, str):
        # if given a string, make a clock accoridng to it
        if globalClock == 'float':
            # get timestamps as a simple value
            globalClock = core.Clock(format='float')
        elif globalClock == 'iso':
            # get timestamps in ISO format
            globalClock = core.Clock(format='%Y-%m-%d_%H:%M:%S.%f%z')
        else:
            # get timestamps in a custom format
            globalClock = core.Clock(format=globalClock)
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    # routine timer to track time remaining of each (possibly non-slip) routine
    routineTimer = core.Clock()
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(
        format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6
    )
    
    # --- Prepare to start Routine "block_counter" ---
    # create an object to store info about Routine block_counter
    block_counter = data.Routine(
        name='block_counter',
        components=[],
    )
    block_counter.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # store start times for block_counter
    block_counter.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    block_counter.tStart = globalClock.getTime(format='float')
    block_counter.status = STARTED
    thisExp.addData('block_counter.started', block_counter.tStart)
    block_counter.maxDuration = None
    # keep track of which components have finished
    block_counterComponents = block_counter.components
    for thisComponent in block_counter.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "block_counter" ---
    block_counter.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            block_counter.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in block_counter.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "block_counter" ---
    for thisComponent in block_counter.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for block_counter
    block_counter.tStop = globalClock.getTime(format='float')
    block_counter.tStopRefresh = tThisFlipGlobal
    thisExp.addData('block_counter.stopped', block_counter.tStop)
    thisExp.nextEntry()
    # the Routine "block_counter" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "hello" ---
    # create an object to store info about Routine hello
    hello = data.Routine(
        name='hello',
        components=[helleText, helloResp],
    )
    hello.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for helloResp
    helloResp.keys = []
    helloResp.rt = []
    _helloResp_allKeys = []
    # store start times for hello
    hello.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    hello.tStart = globalClock.getTime(format='float')
    hello.status = STARTED
    thisExp.addData('hello.started', hello.tStart)
    hello.maxDuration = None
    # keep track of which components have finished
    helloComponents = hello.components
    for thisComponent in hello.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "hello" ---
    hello.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *helleText* updates
        
        # if helleText is starting this frame...
        if helleText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            helleText.frameNStart = frameN  # exact frame index
            helleText.tStart = t  # local t and not account for scr refresh
            helleText.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(helleText, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'helleText.started')
            # update status
            helleText.status = STARTED
            helleText.setAutoDraw(True)
        
        # if helleText is active this frame...
        if helleText.status == STARTED:
            # update params
            pass
        
        # *helloResp* updates
        waitOnFlip = False
        
        # if helloResp is starting this frame...
        if helloResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            helloResp.frameNStart = frameN  # exact frame index
            helloResp.tStart = t  # local t and not account for scr refresh
            helloResp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(helloResp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'helloResp.started')
            # update status
            helloResp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(helloResp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(helloResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if helloResp.status == STARTED and not waitOnFlip:
            theseKeys = helloResp.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _helloResp_allKeys.extend(theseKeys)
            if len(_helloResp_allKeys):
                helloResp.keys = _helloResp_allKeys[-1].name  # just the last key pressed
                helloResp.rt = _helloResp_allKeys[-1].rt
                helloResp.duration = _helloResp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            hello.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in hello.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "hello" ---
    for thisComponent in hello.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for hello
    hello.tStop = globalClock.getTime(format='float')
    hello.tStopRefresh = tThisFlipGlobal
    thisExp.addData('hello.stopped', hello.tStop)
    # check responses
    if helloResp.keys in ['', [], None]:  # No response was made
        helloResp.keys = None
    thisExp.addData('helloResp.keys',helloResp.keys)
    if helloResp.keys != None:  # we had a response
        thisExp.addData('helloResp.rt', helloResp.rt)
        thisExp.addData('helloResp.duration', helloResp.duration)
    thisExp.nextEntry()
    # the Routine "hello" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "Intro" ---
    # create an object to store info about Routine Intro
    Intro = data.Routine(
        name='Intro',
        components=[IntroText, IntroResp],
    )
    Intro.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for IntroResp
    IntroResp.keys = []
    IntroResp.rt = []
    _IntroResp_allKeys = []
    # store start times for Intro
    Intro.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    Intro.tStart = globalClock.getTime(format='float')
    Intro.status = STARTED
    thisExp.addData('Intro.started', Intro.tStart)
    Intro.maxDuration = None
    # keep track of which components have finished
    IntroComponents = Intro.components
    for thisComponent in Intro.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Intro" ---
    Intro.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *IntroText* updates
        
        # if IntroText is starting this frame...
        if IntroText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            IntroText.frameNStart = frameN  # exact frame index
            IntroText.tStart = t  # local t and not account for scr refresh
            IntroText.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(IntroText, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'IntroText.started')
            # update status
            IntroText.status = STARTED
            IntroText.setAutoDraw(True)
        
        # if IntroText is active this frame...
        if IntroText.status == STARTED:
            # update params
            pass
        
        # *IntroResp* updates
        waitOnFlip = False
        
        # if IntroResp is starting this frame...
        if IntroResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            IntroResp.frameNStart = frameN  # exact frame index
            IntroResp.tStart = t  # local t and not account for scr refresh
            IntroResp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(IntroResp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'IntroResp.started')
            # update status
            IntroResp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(IntroResp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(IntroResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if IntroResp.status == STARTED and not waitOnFlip:
            theseKeys = IntroResp.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _IntroResp_allKeys.extend(theseKeys)
            if len(_IntroResp_allKeys):
                IntroResp.keys = _IntroResp_allKeys[-1].name  # just the last key pressed
                IntroResp.rt = _IntroResp_allKeys[-1].rt
                IntroResp.duration = _IntroResp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            Intro.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Intro.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Intro" ---
    for thisComponent in Intro.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for Intro
    Intro.tStop = globalClock.getTime(format='float')
    Intro.tStopRefresh = tThisFlipGlobal
    thisExp.addData('Intro.stopped', Intro.tStop)
    # check responses
    if IntroResp.keys in ['', [], None]:  # No response was made
        IntroResp.keys = None
    thisExp.addData('IntroResp.keys',IntroResp.keys)
    if IntroResp.keys != None:  # we had a response
        thisExp.addData('IntroResp.rt', IntroResp.rt)
        thisExp.addData('IntroResp.duration', IntroResp.duration)
    thisExp.nextEntry()
    # the Routine "Intro" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "LearningInst" ---
    # create an object to store info about Routine LearningInst
    LearningInst = data.Routine(
        name='LearningInst',
        components=[LearningInst1Text, LearningInst1Resp],
    )
    LearningInst.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for LearningInst1Resp
    LearningInst1Resp.keys = []
    LearningInst1Resp.rt = []
    _LearningInst1Resp_allKeys = []
    # store start times for LearningInst
    LearningInst.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    LearningInst.tStart = globalClock.getTime(format='float')
    LearningInst.status = STARTED
    thisExp.addData('LearningInst.started', LearningInst.tStart)
    LearningInst.maxDuration = None
    # keep track of which components have finished
    LearningInstComponents = LearningInst.components
    for thisComponent in LearningInst.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "LearningInst" ---
    LearningInst.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *LearningInst1Text* updates
        
        # if LearningInst1Text is starting this frame...
        if LearningInst1Text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            LearningInst1Text.frameNStart = frameN  # exact frame index
            LearningInst1Text.tStart = t  # local t and not account for scr refresh
            LearningInst1Text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(LearningInst1Text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'LearningInst1Text.started')
            # update status
            LearningInst1Text.status = STARTED
            LearningInst1Text.setAutoDraw(True)
        
        # if LearningInst1Text is active this frame...
        if LearningInst1Text.status == STARTED:
            # update params
            pass
        
        # *LearningInst1Resp* updates
        waitOnFlip = False
        
        # if LearningInst1Resp is starting this frame...
        if LearningInst1Resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            LearningInst1Resp.frameNStart = frameN  # exact frame index
            LearningInst1Resp.tStart = t  # local t and not account for scr refresh
            LearningInst1Resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(LearningInst1Resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'LearningInst1Resp.started')
            # update status
            LearningInst1Resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(LearningInst1Resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(LearningInst1Resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if LearningInst1Resp.status == STARTED and not waitOnFlip:
            theseKeys = LearningInst1Resp.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _LearningInst1Resp_allKeys.extend(theseKeys)
            if len(_LearningInst1Resp_allKeys):
                LearningInst1Resp.keys = _LearningInst1Resp_allKeys[-1].name  # just the last key pressed
                LearningInst1Resp.rt = _LearningInst1Resp_allKeys[-1].rt
                LearningInst1Resp.duration = _LearningInst1Resp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            LearningInst.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in LearningInst.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "LearningInst" ---
    for thisComponent in LearningInst.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for LearningInst
    LearningInst.tStop = globalClock.getTime(format='float')
    LearningInst.tStopRefresh = tThisFlipGlobal
    thisExp.addData('LearningInst.stopped', LearningInst.tStop)
    # check responses
    if LearningInst1Resp.keys in ['', [], None]:  # No response was made
        LearningInst1Resp.keys = None
    thisExp.addData('LearningInst1Resp.keys',LearningInst1Resp.keys)
    if LearningInst1Resp.keys != None:  # we had a response
        thisExp.addData('LearningInst1Resp.rt', LearningInst1Resp.rt)
        thisExp.addData('LearningInst1Resp.duration', LearningInst1Resp.duration)
    thisExp.nextEntry()
    # the Routine "LearningInst" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "LearningInst2" ---
    # create an object to store info about Routine LearningInst2
    LearningInst2 = data.Routine(
        name='LearningInst2',
        components=[LearningInst2Text, LearningInst2Resp],
    )
    LearningInst2.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for LearningInst2Resp
    LearningInst2Resp.keys = []
    LearningInst2Resp.rt = []
    _LearningInst2Resp_allKeys = []
    # store start times for LearningInst2
    LearningInst2.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    LearningInst2.tStart = globalClock.getTime(format='float')
    LearningInst2.status = STARTED
    thisExp.addData('LearningInst2.started', LearningInst2.tStart)
    LearningInst2.maxDuration = None
    # keep track of which components have finished
    LearningInst2Components = LearningInst2.components
    for thisComponent in LearningInst2.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "LearningInst2" ---
    LearningInst2.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *LearningInst2Text* updates
        
        # if LearningInst2Text is starting this frame...
        if LearningInst2Text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            LearningInst2Text.frameNStart = frameN  # exact frame index
            LearningInst2Text.tStart = t  # local t and not account for scr refresh
            LearningInst2Text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(LearningInst2Text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'LearningInst2Text.started')
            # update status
            LearningInst2Text.status = STARTED
            LearningInst2Text.setAutoDraw(True)
        
        # if LearningInst2Text is active this frame...
        if LearningInst2Text.status == STARTED:
            # update params
            pass
        
        # *LearningInst2Resp* updates
        waitOnFlip = False
        
        # if LearningInst2Resp is starting this frame...
        if LearningInst2Resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            LearningInst2Resp.frameNStart = frameN  # exact frame index
            LearningInst2Resp.tStart = t  # local t and not account for scr refresh
            LearningInst2Resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(LearningInst2Resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'LearningInst2Resp.started')
            # update status
            LearningInst2Resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(LearningInst2Resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(LearningInst2Resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if LearningInst2Resp.status == STARTED and not waitOnFlip:
            theseKeys = LearningInst2Resp.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _LearningInst2Resp_allKeys.extend(theseKeys)
            if len(_LearningInst2Resp_allKeys):
                LearningInst2Resp.keys = _LearningInst2Resp_allKeys[-1].name  # just the last key pressed
                LearningInst2Resp.rt = _LearningInst2Resp_allKeys[-1].rt
                LearningInst2Resp.duration = _LearningInst2Resp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            LearningInst2.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in LearningInst2.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "LearningInst2" ---
    for thisComponent in LearningInst2.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for LearningInst2
    LearningInst2.tStop = globalClock.getTime(format='float')
    LearningInst2.tStopRefresh = tThisFlipGlobal
    thisExp.addData('LearningInst2.stopped', LearningInst2.tStop)
    # check responses
    if LearningInst2Resp.keys in ['', [], None]:  # No response was made
        LearningInst2Resp.keys = None
    thisExp.addData('LearningInst2Resp.keys',LearningInst2Resp.keys)
    if LearningInst2Resp.keys != None:  # we had a response
        thisExp.addData('LearningInst2Resp.rt', LearningInst2Resp.rt)
        thisExp.addData('LearningInst2Resp.duration', LearningInst2Resp.duration)
    thisExp.nextEntry()
    # the Routine "LearningInst2" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "LearningInst3" ---
    # create an object to store info about Routine LearningInst3
    LearningInst3 = data.Routine(
        name='LearningInst3',
        components=[LearningInst3Text, LearningInst3Resp],
    )
    LearningInst3.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for LearningInst3Resp
    LearningInst3Resp.keys = []
    LearningInst3Resp.rt = []
    _LearningInst3Resp_allKeys = []
    # store start times for LearningInst3
    LearningInst3.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    LearningInst3.tStart = globalClock.getTime(format='float')
    LearningInst3.status = STARTED
    thisExp.addData('LearningInst3.started', LearningInst3.tStart)
    LearningInst3.maxDuration = None
    # keep track of which components have finished
    LearningInst3Components = LearningInst3.components
    for thisComponent in LearningInst3.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "LearningInst3" ---
    LearningInst3.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *LearningInst3Text* updates
        
        # if LearningInst3Text is starting this frame...
        if LearningInst3Text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            LearningInst3Text.frameNStart = frameN  # exact frame index
            LearningInst3Text.tStart = t  # local t and not account for scr refresh
            LearningInst3Text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(LearningInst3Text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'LearningInst3Text.started')
            # update status
            LearningInst3Text.status = STARTED
            LearningInst3Text.setAutoDraw(True)
        
        # if LearningInst3Text is active this frame...
        if LearningInst3Text.status == STARTED:
            # update params
            pass
        
        # *LearningInst3Resp* updates
        waitOnFlip = False
        
        # if LearningInst3Resp is starting this frame...
        if LearningInst3Resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            LearningInst3Resp.frameNStart = frameN  # exact frame index
            LearningInst3Resp.tStart = t  # local t and not account for scr refresh
            LearningInst3Resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(LearningInst3Resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'LearningInst3Resp.started')
            # update status
            LearningInst3Resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(LearningInst3Resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(LearningInst3Resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if LearningInst3Resp.status == STARTED and not waitOnFlip:
            theseKeys = LearningInst3Resp.getKeys(keyList=['y','n','left','right','space'], ignoreKeys=["escape"], waitRelease=False)
            _LearningInst3Resp_allKeys.extend(theseKeys)
            if len(_LearningInst3Resp_allKeys):
                LearningInst3Resp.keys = _LearningInst3Resp_allKeys[-1].name  # just the last key pressed
                LearningInst3Resp.rt = _LearningInst3Resp_allKeys[-1].rt
                LearningInst3Resp.duration = _LearningInst3Resp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            LearningInst3.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in LearningInst3.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "LearningInst3" ---
    for thisComponent in LearningInst3.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for LearningInst3
    LearningInst3.tStop = globalClock.getTime(format='float')
    LearningInst3.tStopRefresh = tThisFlipGlobal
    thisExp.addData('LearningInst3.stopped', LearningInst3.tStop)
    # check responses
    if LearningInst3Resp.keys in ['', [], None]:  # No response was made
        LearningInst3Resp.keys = None
    thisExp.addData('LearningInst3Resp.keys',LearningInst3Resp.keys)
    if LearningInst3Resp.keys != None:  # we had a response
        thisExp.addData('LearningInst3Resp.rt', LearningInst3Resp.rt)
        thisExp.addData('LearningInst3Resp.duration', LearningInst3Resp.duration)
    thisExp.nextEntry()
    # the Routine "LearningInst3" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "LearningIns4" ---
    # create an object to store info about Routine LearningIns4
    LearningIns4 = data.Routine(
        name='LearningIns4',
        components=[LearningInst4Text, LearningInst4Resp],
    )
    LearningIns4.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for LearningInst4Resp
    LearningInst4Resp.keys = []
    LearningInst4Resp.rt = []
    _LearningInst4Resp_allKeys = []
    # store start times for LearningIns4
    LearningIns4.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    LearningIns4.tStart = globalClock.getTime(format='float')
    LearningIns4.status = STARTED
    thisExp.addData('LearningIns4.started', LearningIns4.tStart)
    LearningIns4.maxDuration = None
    # keep track of which components have finished
    LearningIns4Components = LearningIns4.components
    for thisComponent in LearningIns4.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "LearningIns4" ---
    LearningIns4.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *LearningInst4Text* updates
        
        # if LearningInst4Text is starting this frame...
        if LearningInst4Text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            LearningInst4Text.frameNStart = frameN  # exact frame index
            LearningInst4Text.tStart = t  # local t and not account for scr refresh
            LearningInst4Text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(LearningInst4Text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'LearningInst4Text.started')
            # update status
            LearningInst4Text.status = STARTED
            LearningInst4Text.setAutoDraw(True)
        
        # if LearningInst4Text is active this frame...
        if LearningInst4Text.status == STARTED:
            # update params
            pass
        
        # *LearningInst4Resp* updates
        waitOnFlip = False
        
        # if LearningInst4Resp is starting this frame...
        if LearningInst4Resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            LearningInst4Resp.frameNStart = frameN  # exact frame index
            LearningInst4Resp.tStart = t  # local t and not account for scr refresh
            LearningInst4Resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(LearningInst4Resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'LearningInst4Resp.started')
            # update status
            LearningInst4Resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(LearningInst4Resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(LearningInst4Resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if LearningInst4Resp.status == STARTED and not waitOnFlip:
            theseKeys = LearningInst4Resp.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _LearningInst4Resp_allKeys.extend(theseKeys)
            if len(_LearningInst4Resp_allKeys):
                LearningInst4Resp.keys = _LearningInst4Resp_allKeys[-1].name  # just the last key pressed
                LearningInst4Resp.rt = _LearningInst4Resp_allKeys[-1].rt
                LearningInst4Resp.duration = _LearningInst4Resp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            LearningIns4.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in LearningIns4.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "LearningIns4" ---
    for thisComponent in LearningIns4.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for LearningIns4
    LearningIns4.tStop = globalClock.getTime(format='float')
    LearningIns4.tStopRefresh = tThisFlipGlobal
    thisExp.addData('LearningIns4.stopped', LearningIns4.tStop)
    # check responses
    if LearningInst4Resp.keys in ['', [], None]:  # No response was made
        LearningInst4Resp.keys = None
    thisExp.addData('LearningInst4Resp.keys',LearningInst4Resp.keys)
    if LearningInst4Resp.keys != None:  # we had a response
        thisExp.addData('LearningInst4Resp.rt', LearningInst4Resp.rt)
        thisExp.addData('LearningInst4Resp.duration', LearningInst4Resp.duration)
    thisExp.nextEntry()
    # the Routine "LearningIns4" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "LearningExample1" ---
    # create an object to store info about Routine LearningExample1
    LearningExample1 = data.Routine(
        name='LearningExample1',
        components=[LearningExample1Image, LearningEncodingQuestion1Text, LearningEncodingOptions1Text, LearningEncodingExample1Resp],
    )
    LearningExample1.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for LearningEncodingExample1Resp
    LearningEncodingExample1Resp.keys = []
    LearningEncodingExample1Resp.rt = []
    _LearningEncodingExample1Resp_allKeys = []
    # store start times for LearningExample1
    LearningExample1.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    LearningExample1.tStart = globalClock.getTime(format='float')
    LearningExample1.status = STARTED
    thisExp.addData('LearningExample1.started', LearningExample1.tStart)
    LearningExample1.maxDuration = None
    # keep track of which components have finished
    LearningExample1Components = LearningExample1.components
    for thisComponent in LearningExample1.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "LearningExample1" ---
    LearningExample1.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *LearningExample1Image* updates
        
        # if LearningExample1Image is starting this frame...
        if LearningExample1Image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            LearningExample1Image.frameNStart = frameN  # exact frame index
            LearningExample1Image.tStart = t  # local t and not account for scr refresh
            LearningExample1Image.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(LearningExample1Image, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'LearningExample1Image.started')
            # update status
            LearningExample1Image.status = STARTED
            LearningExample1Image.setAutoDraw(True)
        
        # if LearningExample1Image is active this frame...
        if LearningExample1Image.status == STARTED:
            # update params
            pass
        
        # *LearningEncodingQuestion1Text* updates
        
        # if LearningEncodingQuestion1Text is starting this frame...
        if LearningEncodingQuestion1Text.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
            # keep track of start time/frame for later
            LearningEncodingQuestion1Text.frameNStart = frameN  # exact frame index
            LearningEncodingQuestion1Text.tStart = t  # local t and not account for scr refresh
            LearningEncodingQuestion1Text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(LearningEncodingQuestion1Text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'LearningEncodingQuestion1Text.started')
            # update status
            LearningEncodingQuestion1Text.status = STARTED
            LearningEncodingQuestion1Text.setAutoDraw(True)
        
        # if LearningEncodingQuestion1Text is active this frame...
        if LearningEncodingQuestion1Text.status == STARTED:
            # update params
            pass
        
        # *LearningEncodingOptions1Text* updates
        
        # if LearningEncodingOptions1Text is starting this frame...
        if LearningEncodingOptions1Text.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
            # keep track of start time/frame for later
            LearningEncodingOptions1Text.frameNStart = frameN  # exact frame index
            LearningEncodingOptions1Text.tStart = t  # local t and not account for scr refresh
            LearningEncodingOptions1Text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(LearningEncodingOptions1Text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'LearningEncodingOptions1Text.started')
            # update status
            LearningEncodingOptions1Text.status = STARTED
            LearningEncodingOptions1Text.setAutoDraw(True)
        
        # if LearningEncodingOptions1Text is active this frame...
        if LearningEncodingOptions1Text.status == STARTED:
            # update params
            pass
        
        # *LearningEncodingExample1Resp* updates
        waitOnFlip = False
        
        # if LearningEncodingExample1Resp is starting this frame...
        if LearningEncodingExample1Resp.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
            # keep track of start time/frame for later
            LearningEncodingExample1Resp.frameNStart = frameN  # exact frame index
            LearningEncodingExample1Resp.tStart = t  # local t and not account for scr refresh
            LearningEncodingExample1Resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(LearningEncodingExample1Resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'LearningEncodingExample1Resp.started')
            # update status
            LearningEncodingExample1Resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(LearningEncodingExample1Resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(LearningEncodingExample1Resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if LearningEncodingExample1Resp.status == STARTED and not waitOnFlip:
            theseKeys = LearningEncodingExample1Resp.getKeys(keyList=['left','right'], ignoreKeys=["escape"], waitRelease=False)
            _LearningEncodingExample1Resp_allKeys.extend(theseKeys)
            if len(_LearningEncodingExample1Resp_allKeys):
                LearningEncodingExample1Resp.keys = _LearningEncodingExample1Resp_allKeys[-1].name  # just the last key pressed
                LearningEncodingExample1Resp.rt = _LearningEncodingExample1Resp_allKeys[-1].rt
                LearningEncodingExample1Resp.duration = _LearningEncodingExample1Resp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            LearningExample1.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in LearningExample1.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "LearningExample1" ---
    for thisComponent in LearningExample1.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for LearningExample1
    LearningExample1.tStop = globalClock.getTime(format='float')
    LearningExample1.tStopRefresh = tThisFlipGlobal
    thisExp.addData('LearningExample1.stopped', LearningExample1.tStop)
    # check responses
    if LearningEncodingExample1Resp.keys in ['', [], None]:  # No response was made
        LearningEncodingExample1Resp.keys = None
    thisExp.addData('LearningEncodingExample1Resp.keys',LearningEncodingExample1Resp.keys)
    if LearningEncodingExample1Resp.keys != None:  # we had a response
        thisExp.addData('LearningEncodingExample1Resp.rt', LearningEncodingExample1Resp.rt)
        thisExp.addData('LearningEncodingExample1Resp.duration', LearningEncodingExample1Resp.duration)
    thisExp.nextEntry()
    # the Routine "LearningExample1" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "break1" ---
    # create an object to store info about Routine break1
    break1 = data.Routine(
        name='break1',
        components=[break1Text, break1Resp],
    )
    break1.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for break1Resp
    break1Resp.keys = []
    break1Resp.rt = []
    _break1Resp_allKeys = []
    # store start times for break1
    break1.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    break1.tStart = globalClock.getTime(format='float')
    break1.status = STARTED
    thisExp.addData('break1.started', break1.tStart)
    break1.maxDuration = None
    # keep track of which components have finished
    break1Components = break1.components
    for thisComponent in break1.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "break1" ---
    break1.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *break1Text* updates
        
        # if break1Text is starting this frame...
        if break1Text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            break1Text.frameNStart = frameN  # exact frame index
            break1Text.tStart = t  # local t and not account for scr refresh
            break1Text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(break1Text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'break1Text.started')
            # update status
            break1Text.status = STARTED
            break1Text.setAutoDraw(True)
        
        # if break1Text is active this frame...
        if break1Text.status == STARTED:
            # update params
            pass
        
        # *break1Resp* updates
        waitOnFlip = False
        
        # if break1Resp is starting this frame...
        if break1Resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            break1Resp.frameNStart = frameN  # exact frame index
            break1Resp.tStart = t  # local t and not account for scr refresh
            break1Resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(break1Resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'break1Resp.started')
            # update status
            break1Resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(break1Resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(break1Resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if break1Resp.status == STARTED and not waitOnFlip:
            theseKeys = break1Resp.getKeys(keyList=['5'], ignoreKeys=["escape"], waitRelease=False)
            _break1Resp_allKeys.extend(theseKeys)
            if len(_break1Resp_allKeys):
                break1Resp.keys = _break1Resp_allKeys[-1].name  # just the last key pressed
                break1Resp.rt = _break1Resp_allKeys[-1].rt
                break1Resp.duration = _break1Resp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break1.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in break1.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "break1" ---
    for thisComponent in break1.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for break1
    break1.tStop = globalClock.getTime(format='float')
    break1.tStopRefresh = tThisFlipGlobal
    thisExp.addData('break1.stopped', break1.tStop)
    # check responses
    if break1Resp.keys in ['', [], None]:  # No response was made
        break1Resp.keys = None
    thisExp.addData('break1Resp.keys',break1Resp.keys)
    if break1Resp.keys != None:  # we had a response
        thisExp.addData('break1Resp.rt', break1Resp.rt)
        thisExp.addData('break1Resp.duration', break1Resp.duration)
    thisExp.nextEntry()
    # the Routine "break1" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "LearningExample2" ---
    # create an object to store info about Routine LearningExample2
    LearningExample2 = data.Routine(
        name='LearningExample2',
        components=[LearningExample2Image, LearningEncodingQuestion2Text, LearningEncodingOptions2Text, LearningEncodingExample2Resp],
    )
    LearningExample2.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for LearningEncodingExample2Resp
    LearningEncodingExample2Resp.keys = []
    LearningEncodingExample2Resp.rt = []
    _LearningEncodingExample2Resp_allKeys = []
    # store start times for LearningExample2
    LearningExample2.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    LearningExample2.tStart = globalClock.getTime(format='float')
    LearningExample2.status = STARTED
    thisExp.addData('LearningExample2.started', LearningExample2.tStart)
    LearningExample2.maxDuration = None
    # keep track of which components have finished
    LearningExample2Components = LearningExample2.components
    for thisComponent in LearningExample2.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "LearningExample2" ---
    LearningExample2.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 6.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *LearningExample2Image* updates
        
        # if LearningExample2Image is starting this frame...
        if LearningExample2Image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            LearningExample2Image.frameNStart = frameN  # exact frame index
            LearningExample2Image.tStart = t  # local t and not account for scr refresh
            LearningExample2Image.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(LearningExample2Image, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'LearningExample2Image.started')
            # update status
            LearningExample2Image.status = STARTED
            LearningExample2Image.setAutoDraw(True)
        
        # if LearningExample2Image is active this frame...
        if LearningExample2Image.status == STARTED:
            # update params
            pass
        
        # if LearningExample2Image is stopping this frame...
        if LearningExample2Image.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > LearningExample2Image.tStartRefresh + 6-frameTolerance:
                # keep track of stop time/frame for later
                LearningExample2Image.tStop = t  # not accounting for scr refresh
                LearningExample2Image.tStopRefresh = tThisFlipGlobal  # on global time
                LearningExample2Image.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'LearningExample2Image.stopped')
                # update status
                LearningExample2Image.status = FINISHED
                LearningExample2Image.setAutoDraw(False)
        
        # *LearningEncodingQuestion2Text* updates
        
        # if LearningEncodingQuestion2Text is starting this frame...
        if LearningEncodingQuestion2Text.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
            # keep track of start time/frame for later
            LearningEncodingQuestion2Text.frameNStart = frameN  # exact frame index
            LearningEncodingQuestion2Text.tStart = t  # local t and not account for scr refresh
            LearningEncodingQuestion2Text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(LearningEncodingQuestion2Text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'LearningEncodingQuestion2Text.started')
            # update status
            LearningEncodingQuestion2Text.status = STARTED
            LearningEncodingQuestion2Text.setAutoDraw(True)
        
        # if LearningEncodingQuestion2Text is active this frame...
        if LearningEncodingQuestion2Text.status == STARTED:
            # update params
            pass
        
        # if LearningEncodingQuestion2Text is stopping this frame...
        if LearningEncodingQuestion2Text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > LearningEncodingQuestion2Text.tStartRefresh + 4-frameTolerance:
                # keep track of stop time/frame for later
                LearningEncodingQuestion2Text.tStop = t  # not accounting for scr refresh
                LearningEncodingQuestion2Text.tStopRefresh = tThisFlipGlobal  # on global time
                LearningEncodingQuestion2Text.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'LearningEncodingQuestion2Text.stopped')
                # update status
                LearningEncodingQuestion2Text.status = FINISHED
                LearningEncodingQuestion2Text.setAutoDraw(False)
        
        # *LearningEncodingOptions2Text* updates
        
        # if LearningEncodingOptions2Text is starting this frame...
        if LearningEncodingOptions2Text.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
            # keep track of start time/frame for later
            LearningEncodingOptions2Text.frameNStart = frameN  # exact frame index
            LearningEncodingOptions2Text.tStart = t  # local t and not account for scr refresh
            LearningEncodingOptions2Text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(LearningEncodingOptions2Text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'LearningEncodingOptions2Text.started')
            # update status
            LearningEncodingOptions2Text.status = STARTED
            LearningEncodingOptions2Text.setAutoDraw(True)
        
        # if LearningEncodingOptions2Text is active this frame...
        if LearningEncodingOptions2Text.status == STARTED:
            # update params
            pass
        
        # if LearningEncodingOptions2Text is stopping this frame...
        if LearningEncodingOptions2Text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > LearningEncodingOptions2Text.tStartRefresh + 4-frameTolerance:
                # keep track of stop time/frame for later
                LearningEncodingOptions2Text.tStop = t  # not accounting for scr refresh
                LearningEncodingOptions2Text.tStopRefresh = tThisFlipGlobal  # on global time
                LearningEncodingOptions2Text.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'LearningEncodingOptions2Text.stopped')
                # update status
                LearningEncodingOptions2Text.status = FINISHED
                LearningEncodingOptions2Text.setAutoDraw(False)
        
        # *LearningEncodingExample2Resp* updates
        waitOnFlip = False
        
        # if LearningEncodingExample2Resp is starting this frame...
        if LearningEncodingExample2Resp.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
            # keep track of start time/frame for later
            LearningEncodingExample2Resp.frameNStart = frameN  # exact frame index
            LearningEncodingExample2Resp.tStart = t  # local t and not account for scr refresh
            LearningEncodingExample2Resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(LearningEncodingExample2Resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'LearningEncodingExample2Resp.started')
            # update status
            LearningEncodingExample2Resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(LearningEncodingExample2Resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(LearningEncodingExample2Resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        
        # if LearningEncodingExample2Resp is stopping this frame...
        if LearningEncodingExample2Resp.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > LearningEncodingExample2Resp.tStartRefresh + 4-frameTolerance:
                # keep track of stop time/frame for later
                LearningEncodingExample2Resp.tStop = t  # not accounting for scr refresh
                LearningEncodingExample2Resp.tStopRefresh = tThisFlipGlobal  # on global time
                LearningEncodingExample2Resp.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'LearningEncodingExample2Resp.stopped')
                # update status
                LearningEncodingExample2Resp.status = FINISHED
                LearningEncodingExample2Resp.status = FINISHED
        if LearningEncodingExample2Resp.status == STARTED and not waitOnFlip:
            theseKeys = LearningEncodingExample2Resp.getKeys(keyList=['left','right'], ignoreKeys=["escape"], waitRelease=False)
            _LearningEncodingExample2Resp_allKeys.extend(theseKeys)
            if len(_LearningEncodingExample2Resp_allKeys):
                LearningEncodingExample2Resp.keys = _LearningEncodingExample2Resp_allKeys[-1].name  # just the last key pressed
                LearningEncodingExample2Resp.rt = _LearningEncodingExample2Resp_allKeys[-1].rt
                LearningEncodingExample2Resp.duration = _LearningEncodingExample2Resp_allKeys[-1].duration
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            LearningExample2.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in LearningExample2.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "LearningExample2" ---
    for thisComponent in LearningExample2.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for LearningExample2
    LearningExample2.tStop = globalClock.getTime(format='float')
    LearningExample2.tStopRefresh = tThisFlipGlobal
    thisExp.addData('LearningExample2.stopped', LearningExample2.tStop)
    # check responses
    if LearningEncodingExample2Resp.keys in ['', [], None]:  # No response was made
        LearningEncodingExample2Resp.keys = None
    thisExp.addData('LearningEncodingExample2Resp.keys',LearningEncodingExample2Resp.keys)
    if LearningEncodingExample2Resp.keys != None:  # we had a response
        thisExp.addData('LearningEncodingExample2Resp.rt', LearningEncodingExample2Resp.rt)
        thisExp.addData('LearningEncodingExample2Resp.duration', LearningEncodingExample2Resp.duration)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if LearningExample2.maxDurationReached:
        routineTimer.addTime(-LearningExample2.maxDuration)
    elif LearningExample2.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-6.000000)
    thisExp.nextEntry()
    
    # --- Prepare to start Routine "LearningExample3" ---
    # create an object to store info about Routine LearningExample3
    LearningExample3 = data.Routine(
        name='LearningExample3',
        components=[LearningExample3Image, LearningEncodingQuestion3Text, LearningEncodingOption3Text, LearningEncodingExample3Resp],
    )
    LearningExample3.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for LearningEncodingExample3Resp
    LearningEncodingExample3Resp.keys = []
    LearningEncodingExample3Resp.rt = []
    _LearningEncodingExample3Resp_allKeys = []
    # store start times for LearningExample3
    LearningExample3.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    LearningExample3.tStart = globalClock.getTime(format='float')
    LearningExample3.status = STARTED
    thisExp.addData('LearningExample3.started', LearningExample3.tStart)
    LearningExample3.maxDuration = None
    # keep track of which components have finished
    LearningExample3Components = LearningExample3.components
    for thisComponent in LearningExample3.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "LearningExample3" ---
    LearningExample3.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 6.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *LearningExample3Image* updates
        
        # if LearningExample3Image is starting this frame...
        if LearningExample3Image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            LearningExample3Image.frameNStart = frameN  # exact frame index
            LearningExample3Image.tStart = t  # local t and not account for scr refresh
            LearningExample3Image.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(LearningExample3Image, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'LearningExample3Image.started')
            # update status
            LearningExample3Image.status = STARTED
            LearningExample3Image.setAutoDraw(True)
        
        # if LearningExample3Image is active this frame...
        if LearningExample3Image.status == STARTED:
            # update params
            pass
        
        # if LearningExample3Image is stopping this frame...
        if LearningExample3Image.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > LearningExample3Image.tStartRefresh + 6-frameTolerance:
                # keep track of stop time/frame for later
                LearningExample3Image.tStop = t  # not accounting for scr refresh
                LearningExample3Image.tStopRefresh = tThisFlipGlobal  # on global time
                LearningExample3Image.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'LearningExample3Image.stopped')
                # update status
                LearningExample3Image.status = FINISHED
                LearningExample3Image.setAutoDraw(False)
        
        # *LearningEncodingQuestion3Text* updates
        
        # if LearningEncodingQuestion3Text is starting this frame...
        if LearningEncodingQuestion3Text.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
            # keep track of start time/frame for later
            LearningEncodingQuestion3Text.frameNStart = frameN  # exact frame index
            LearningEncodingQuestion3Text.tStart = t  # local t and not account for scr refresh
            LearningEncodingQuestion3Text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(LearningEncodingQuestion3Text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'LearningEncodingQuestion3Text.started')
            # update status
            LearningEncodingQuestion3Text.status = STARTED
            LearningEncodingQuestion3Text.setAutoDraw(True)
        
        # if LearningEncodingQuestion3Text is active this frame...
        if LearningEncodingQuestion3Text.status == STARTED:
            # update params
            pass
        
        # if LearningEncodingQuestion3Text is stopping this frame...
        if LearningEncodingQuestion3Text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > LearningEncodingQuestion3Text.tStartRefresh + 4-frameTolerance:
                # keep track of stop time/frame for later
                LearningEncodingQuestion3Text.tStop = t  # not accounting for scr refresh
                LearningEncodingQuestion3Text.tStopRefresh = tThisFlipGlobal  # on global time
                LearningEncodingQuestion3Text.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'LearningEncodingQuestion3Text.stopped')
                # update status
                LearningEncodingQuestion3Text.status = FINISHED
                LearningEncodingQuestion3Text.setAutoDraw(False)
        
        # *LearningEncodingOption3Text* updates
        
        # if LearningEncodingOption3Text is starting this frame...
        if LearningEncodingOption3Text.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
            # keep track of start time/frame for later
            LearningEncodingOption3Text.frameNStart = frameN  # exact frame index
            LearningEncodingOption3Text.tStart = t  # local t and not account for scr refresh
            LearningEncodingOption3Text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(LearningEncodingOption3Text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'LearningEncodingOption3Text.started')
            # update status
            LearningEncodingOption3Text.status = STARTED
            LearningEncodingOption3Text.setAutoDraw(True)
        
        # if LearningEncodingOption3Text is active this frame...
        if LearningEncodingOption3Text.status == STARTED:
            # update params
            pass
        
        # if LearningEncodingOption3Text is stopping this frame...
        if LearningEncodingOption3Text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > LearningEncodingOption3Text.tStartRefresh + 4-frameTolerance:
                # keep track of stop time/frame for later
                LearningEncodingOption3Text.tStop = t  # not accounting for scr refresh
                LearningEncodingOption3Text.tStopRefresh = tThisFlipGlobal  # on global time
                LearningEncodingOption3Text.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'LearningEncodingOption3Text.stopped')
                # update status
                LearningEncodingOption3Text.status = FINISHED
                LearningEncodingOption3Text.setAutoDraw(False)
        
        # *LearningEncodingExample3Resp* updates
        waitOnFlip = False
        
        # if LearningEncodingExample3Resp is starting this frame...
        if LearningEncodingExample3Resp.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
            # keep track of start time/frame for later
            LearningEncodingExample3Resp.frameNStart = frameN  # exact frame index
            LearningEncodingExample3Resp.tStart = t  # local t and not account for scr refresh
            LearningEncodingExample3Resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(LearningEncodingExample3Resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'LearningEncodingExample3Resp.started')
            # update status
            LearningEncodingExample3Resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(LearningEncodingExample3Resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(LearningEncodingExample3Resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        
        # if LearningEncodingExample3Resp is stopping this frame...
        if LearningEncodingExample3Resp.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > LearningEncodingExample3Resp.tStartRefresh + 4-frameTolerance:
                # keep track of stop time/frame for later
                LearningEncodingExample3Resp.tStop = t  # not accounting for scr refresh
                LearningEncodingExample3Resp.tStopRefresh = tThisFlipGlobal  # on global time
                LearningEncodingExample3Resp.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'LearningEncodingExample3Resp.stopped')
                # update status
                LearningEncodingExample3Resp.status = FINISHED
                LearningEncodingExample3Resp.status = FINISHED
        if LearningEncodingExample3Resp.status == STARTED and not waitOnFlip:
            theseKeys = LearningEncodingExample3Resp.getKeys(keyList=['left','right'], ignoreKeys=["escape"], waitRelease=False)
            _LearningEncodingExample3Resp_allKeys.extend(theseKeys)
            if len(_LearningEncodingExample3Resp_allKeys):
                LearningEncodingExample3Resp.keys = _LearningEncodingExample3Resp_allKeys[-1].name  # just the last key pressed
                LearningEncodingExample3Resp.rt = _LearningEncodingExample3Resp_allKeys[-1].rt
                LearningEncodingExample3Resp.duration = _LearningEncodingExample3Resp_allKeys[-1].duration
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            LearningExample3.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in LearningExample3.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "LearningExample3" ---
    for thisComponent in LearningExample3.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for LearningExample3
    LearningExample3.tStop = globalClock.getTime(format='float')
    LearningExample3.tStopRefresh = tThisFlipGlobal
    thisExp.addData('LearningExample3.stopped', LearningExample3.tStop)
    # check responses
    if LearningEncodingExample3Resp.keys in ['', [], None]:  # No response was made
        LearningEncodingExample3Resp.keys = None
    thisExp.addData('LearningEncodingExample3Resp.keys',LearningEncodingExample3Resp.keys)
    if LearningEncodingExample3Resp.keys != None:  # we had a response
        thisExp.addData('LearningEncodingExample3Resp.rt', LearningEncodingExample3Resp.rt)
        thisExp.addData('LearningEncodingExample3Resp.duration', LearningEncodingExample3Resp.duration)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if LearningExample3.maxDurationReached:
        routineTimer.addTime(-LearningExample3.maxDuration)
    elif LearningExample3.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-6.000000)
    thisExp.nextEntry()
    
    # --- Prepare to start Routine "LearningExample4" ---
    # create an object to store info about Routine LearningExample4
    LearningExample4 = data.Routine(
        name='LearningExample4',
        components=[LearningExample4Image, LearningEncodingQuestion4Text, LearningEncodingOption4Text, LearningEncodingExample4Resp],
    )
    LearningExample4.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for LearningEncodingExample4Resp
    LearningEncodingExample4Resp.keys = []
    LearningEncodingExample4Resp.rt = []
    _LearningEncodingExample4Resp_allKeys = []
    # store start times for LearningExample4
    LearningExample4.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    LearningExample4.tStart = globalClock.getTime(format='float')
    LearningExample4.status = STARTED
    thisExp.addData('LearningExample4.started', LearningExample4.tStart)
    LearningExample4.maxDuration = None
    # keep track of which components have finished
    LearningExample4Components = LearningExample4.components
    for thisComponent in LearningExample4.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "LearningExample4" ---
    LearningExample4.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 6.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *LearningExample4Image* updates
        
        # if LearningExample4Image is starting this frame...
        if LearningExample4Image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            LearningExample4Image.frameNStart = frameN  # exact frame index
            LearningExample4Image.tStart = t  # local t and not account for scr refresh
            LearningExample4Image.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(LearningExample4Image, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'LearningExample4Image.started')
            # update status
            LearningExample4Image.status = STARTED
            LearningExample4Image.setAutoDraw(True)
        
        # if LearningExample4Image is active this frame...
        if LearningExample4Image.status == STARTED:
            # update params
            pass
        
        # if LearningExample4Image is stopping this frame...
        if LearningExample4Image.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > LearningExample4Image.tStartRefresh + 6-frameTolerance:
                # keep track of stop time/frame for later
                LearningExample4Image.tStop = t  # not accounting for scr refresh
                LearningExample4Image.tStopRefresh = tThisFlipGlobal  # on global time
                LearningExample4Image.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'LearningExample4Image.stopped')
                # update status
                LearningExample4Image.status = FINISHED
                LearningExample4Image.setAutoDraw(False)
        
        # *LearningEncodingQuestion4Text* updates
        
        # if LearningEncodingQuestion4Text is starting this frame...
        if LearningEncodingQuestion4Text.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
            # keep track of start time/frame for later
            LearningEncodingQuestion4Text.frameNStart = frameN  # exact frame index
            LearningEncodingQuestion4Text.tStart = t  # local t and not account for scr refresh
            LearningEncodingQuestion4Text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(LearningEncodingQuestion4Text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'LearningEncodingQuestion4Text.started')
            # update status
            LearningEncodingQuestion4Text.status = STARTED
            LearningEncodingQuestion4Text.setAutoDraw(True)
        
        # if LearningEncodingQuestion4Text is active this frame...
        if LearningEncodingQuestion4Text.status == STARTED:
            # update params
            pass
        
        # if LearningEncodingQuestion4Text is stopping this frame...
        if LearningEncodingQuestion4Text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > LearningEncodingQuestion4Text.tStartRefresh + 4-frameTolerance:
                # keep track of stop time/frame for later
                LearningEncodingQuestion4Text.tStop = t  # not accounting for scr refresh
                LearningEncodingQuestion4Text.tStopRefresh = tThisFlipGlobal  # on global time
                LearningEncodingQuestion4Text.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'LearningEncodingQuestion4Text.stopped')
                # update status
                LearningEncodingQuestion4Text.status = FINISHED
                LearningEncodingQuestion4Text.setAutoDraw(False)
        
        # *LearningEncodingOption4Text* updates
        
        # if LearningEncodingOption4Text is starting this frame...
        if LearningEncodingOption4Text.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
            # keep track of start time/frame for later
            LearningEncodingOption4Text.frameNStart = frameN  # exact frame index
            LearningEncodingOption4Text.tStart = t  # local t and not account for scr refresh
            LearningEncodingOption4Text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(LearningEncodingOption4Text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'LearningEncodingOption4Text.started')
            # update status
            LearningEncodingOption4Text.status = STARTED
            LearningEncodingOption4Text.setAutoDraw(True)
        
        # if LearningEncodingOption4Text is active this frame...
        if LearningEncodingOption4Text.status == STARTED:
            # update params
            pass
        
        # if LearningEncodingOption4Text is stopping this frame...
        if LearningEncodingOption4Text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > LearningEncodingOption4Text.tStartRefresh + 4-frameTolerance:
                # keep track of stop time/frame for later
                LearningEncodingOption4Text.tStop = t  # not accounting for scr refresh
                LearningEncodingOption4Text.tStopRefresh = tThisFlipGlobal  # on global time
                LearningEncodingOption4Text.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'LearningEncodingOption4Text.stopped')
                # update status
                LearningEncodingOption4Text.status = FINISHED
                LearningEncodingOption4Text.setAutoDraw(False)
        
        # *LearningEncodingExample4Resp* updates
        waitOnFlip = False
        
        # if LearningEncodingExample4Resp is starting this frame...
        if LearningEncodingExample4Resp.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
            # keep track of start time/frame for later
            LearningEncodingExample4Resp.frameNStart = frameN  # exact frame index
            LearningEncodingExample4Resp.tStart = t  # local t and not account for scr refresh
            LearningEncodingExample4Resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(LearningEncodingExample4Resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'LearningEncodingExample4Resp.started')
            # update status
            LearningEncodingExample4Resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(LearningEncodingExample4Resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(LearningEncodingExample4Resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        
        # if LearningEncodingExample4Resp is stopping this frame...
        if LearningEncodingExample4Resp.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > LearningEncodingExample4Resp.tStartRefresh + 4-frameTolerance:
                # keep track of stop time/frame for later
                LearningEncodingExample4Resp.tStop = t  # not accounting for scr refresh
                LearningEncodingExample4Resp.tStopRefresh = tThisFlipGlobal  # on global time
                LearningEncodingExample4Resp.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'LearningEncodingExample4Resp.stopped')
                # update status
                LearningEncodingExample4Resp.status = FINISHED
                LearningEncodingExample4Resp.status = FINISHED
        if LearningEncodingExample4Resp.status == STARTED and not waitOnFlip:
            theseKeys = LearningEncodingExample4Resp.getKeys(keyList=['left','right'], ignoreKeys=["escape"], waitRelease=False)
            _LearningEncodingExample4Resp_allKeys.extend(theseKeys)
            if len(_LearningEncodingExample4Resp_allKeys):
                LearningEncodingExample4Resp.keys = _LearningEncodingExample4Resp_allKeys[-1].name  # just the last key pressed
                LearningEncodingExample4Resp.rt = _LearningEncodingExample4Resp_allKeys[-1].rt
                LearningEncodingExample4Resp.duration = _LearningEncodingExample4Resp_allKeys[-1].duration
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            LearningExample4.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in LearningExample4.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "LearningExample4" ---
    for thisComponent in LearningExample4.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for LearningExample4
    LearningExample4.tStop = globalClock.getTime(format='float')
    LearningExample4.tStopRefresh = tThisFlipGlobal
    thisExp.addData('LearningExample4.stopped', LearningExample4.tStop)
    # check responses
    if LearningEncodingExample4Resp.keys in ['', [], None]:  # No response was made
        LearningEncodingExample4Resp.keys = None
    thisExp.addData('LearningEncodingExample4Resp.keys',LearningEncodingExample4Resp.keys)
    if LearningEncodingExample4Resp.keys != None:  # we had a response
        thisExp.addData('LearningEncodingExample4Resp.rt', LearningEncodingExample4Resp.rt)
        thisExp.addData('LearningEncodingExample4Resp.duration', LearningEncodingExample4Resp.duration)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if LearningExample4.maxDurationReached:
        routineTimer.addTime(-LearningExample4.maxDuration)
    elif LearningExample4.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-6.000000)
    thisExp.nextEntry()
    
    # --- Prepare to start Routine "LearningQuestion" ---
    # create an object to store info about Routine LearningQuestion
    LearningQuestion = data.Routine(
        name='LearningQuestion',
        components=[LearningQuestionText, LearningQuestionResp],
    )
    LearningQuestion.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for LearningQuestionResp
    LearningQuestionResp.keys = []
    LearningQuestionResp.rt = []
    _LearningQuestionResp_allKeys = []
    # store start times for LearningQuestion
    LearningQuestion.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    LearningQuestion.tStart = globalClock.getTime(format='float')
    LearningQuestion.status = STARTED
    thisExp.addData('LearningQuestion.started', LearningQuestion.tStart)
    LearningQuestion.maxDuration = None
    # keep track of which components have finished
    LearningQuestionComponents = LearningQuestion.components
    for thisComponent in LearningQuestion.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "LearningQuestion" ---
    LearningQuestion.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *LearningQuestionText* updates
        
        # if LearningQuestionText is starting this frame...
        if LearningQuestionText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            LearningQuestionText.frameNStart = frameN  # exact frame index
            LearningQuestionText.tStart = t  # local t and not account for scr refresh
            LearningQuestionText.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(LearningQuestionText, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'LearningQuestionText.started')
            # update status
            LearningQuestionText.status = STARTED
            LearningQuestionText.setAutoDraw(True)
        
        # if LearningQuestionText is active this frame...
        if LearningQuestionText.status == STARTED:
            # update params
            pass
        
        # *LearningQuestionResp* updates
        waitOnFlip = False
        
        # if LearningQuestionResp is starting this frame...
        if LearningQuestionResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            LearningQuestionResp.frameNStart = frameN  # exact frame index
            LearningQuestionResp.tStart = t  # local t and not account for scr refresh
            LearningQuestionResp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(LearningQuestionResp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'LearningQuestionResp.started')
            # update status
            LearningQuestionResp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(LearningQuestionResp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(LearningQuestionResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if LearningQuestionResp.status == STARTED and not waitOnFlip:
            theseKeys = LearningQuestionResp.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _LearningQuestionResp_allKeys.extend(theseKeys)
            if len(_LearningQuestionResp_allKeys):
                LearningQuestionResp.keys = _LearningQuestionResp_allKeys[-1].name  # just the last key pressed
                LearningQuestionResp.rt = _LearningQuestionResp_allKeys[-1].rt
                LearningQuestionResp.duration = _LearningQuestionResp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            LearningQuestion.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in LearningQuestion.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "LearningQuestion" ---
    for thisComponent in LearningQuestion.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for LearningQuestion
    LearningQuestion.tStop = globalClock.getTime(format='float')
    LearningQuestion.tStopRefresh = tThisFlipGlobal
    thisExp.addData('LearningQuestion.stopped', LearningQuestion.tStop)
    # check responses
    if LearningQuestionResp.keys in ['', [], None]:  # No response was made
        LearningQuestionResp.keys = None
    thisExp.addData('LearningQuestionResp.keys',LearningQuestionResp.keys)
    if LearningQuestionResp.keys != None:  # we had a response
        thisExp.addData('LearningQuestionResp.rt', LearningQuestionResp.rt)
        thisExp.addData('LearningQuestionResp.duration', LearningQuestionResp.duration)
    thisExp.nextEntry()
    # the Routine "LearningQuestion" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "TimeEstimateInst" ---
    # create an object to store info about Routine TimeEstimateInst
    TimeEstimateInst = data.Routine(
        name='TimeEstimateInst',
        components=[text_2, key_resp_2],
    )
    TimeEstimateInst.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for key_resp_2
    key_resp_2.keys = []
    key_resp_2.rt = []
    _key_resp_2_allKeys = []
    # store start times for TimeEstimateInst
    TimeEstimateInst.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    TimeEstimateInst.tStart = globalClock.getTime(format='float')
    TimeEstimateInst.status = STARTED
    thisExp.addData('TimeEstimateInst.started', TimeEstimateInst.tStart)
    TimeEstimateInst.maxDuration = None
    # keep track of which components have finished
    TimeEstimateInstComponents = TimeEstimateInst.components
    for thisComponent in TimeEstimateInst.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "TimeEstimateInst" ---
    TimeEstimateInst.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_2* updates
        
        # if text_2 is starting this frame...
        if text_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_2.frameNStart = frameN  # exact frame index
            text_2.tStart = t  # local t and not account for scr refresh
            text_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_2.started')
            # update status
            text_2.status = STARTED
            text_2.setAutoDraw(True)
        
        # if text_2 is active this frame...
        if text_2.status == STARTED:
            # update params
            pass
        
        # *key_resp_2* updates
        waitOnFlip = False
        
        # if key_resp_2 is starting this frame...
        if key_resp_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_2.frameNStart = frameN  # exact frame index
            key_resp_2.tStart = t  # local t and not account for scr refresh
            key_resp_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_2.started')
            # update status
            key_resp_2.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_2.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_2.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _key_resp_2_allKeys.extend(theseKeys)
            if len(_key_resp_2_allKeys):
                key_resp_2.keys = _key_resp_2_allKeys[-1].name  # just the last key pressed
                key_resp_2.rt = _key_resp_2_allKeys[-1].rt
                key_resp_2.duration = _key_resp_2_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            TimeEstimateInst.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in TimeEstimateInst.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "TimeEstimateInst" ---
    for thisComponent in TimeEstimateInst.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for TimeEstimateInst
    TimeEstimateInst.tStop = globalClock.getTime(format='float')
    TimeEstimateInst.tStopRefresh = tThisFlipGlobal
    thisExp.addData('TimeEstimateInst.stopped', TimeEstimateInst.tStop)
    # check responses
    if key_resp_2.keys in ['', [], None]:  # No response was made
        key_resp_2.keys = None
    thisExp.addData('key_resp_2.keys',key_resp_2.keys)
    if key_resp_2.keys != None:  # we had a response
        thisExp.addData('key_resp_2.rt', key_resp_2.rt)
        thisExp.addData('key_resp_2.duration', key_resp_2.duration)
    thisExp.nextEntry()
    # the Routine "TimeEstimateInst" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "TimeEstimateExample" ---
    # create an object to store info about Routine TimeEstimateExample
    TimeEstimateExample = data.Routine(
        name='TimeEstimateExample',
        components=[TimeEstimateDsiplay, key_resp_3, TimeEstimateExampleInst, TimeEstimateExampleConfirm, TimeEstimateExampleUnits],
    )
    TimeEstimateExample.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for key_resp_3
    key_resp_3.keys = []
    key_resp_3.rt = []
    _key_resp_3_allKeys = []
    # Run 'Begin Routine' code from code_9
    minutes = 0
    seconds = 0
    focus = 'minutes'  # 'minutes' or 'seconds'
    time_str = f"{minutes:02d}:{seconds:02d}"
    
    # store start times for TimeEstimateExample
    TimeEstimateExample.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    TimeEstimateExample.tStart = globalClock.getTime(format='float')
    TimeEstimateExample.status = STARTED
    thisExp.addData('TimeEstimateExample.started', TimeEstimateExample.tStart)
    TimeEstimateExample.maxDuration = None
    # keep track of which components have finished
    TimeEstimateExampleComponents = TimeEstimateExample.components
    for thisComponent in TimeEstimateExample.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "TimeEstimateExample" ---
    TimeEstimateExample.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *TimeEstimateDsiplay* updates
        
        # if TimeEstimateDsiplay is starting this frame...
        if TimeEstimateDsiplay.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            TimeEstimateDsiplay.frameNStart = frameN  # exact frame index
            TimeEstimateDsiplay.tStart = t  # local t and not account for scr refresh
            TimeEstimateDsiplay.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(TimeEstimateDsiplay, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'TimeEstimateDsiplay.started')
            # update status
            TimeEstimateDsiplay.status = STARTED
            TimeEstimateDsiplay.setAutoDraw(True)
        
        # if TimeEstimateDsiplay is active this frame...
        if TimeEstimateDsiplay.status == STARTED:
            # update params
            TimeEstimateDsiplay.setText(time_str, log=False)
        
        # *key_resp_3* updates
        waitOnFlip = False
        
        # if key_resp_3 is starting this frame...
        if key_resp_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_3.frameNStart = frameN  # exact frame index
            key_resp_3.tStart = t  # local t and not account for scr refresh
            key_resp_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_3, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_3.started')
            # update status
            key_resp_3.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_3.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_3.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_3.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_3.getKeys(keyList=['up','down','left','right','return'], ignoreKeys=["escape"], waitRelease=False)
            _key_resp_3_allKeys.extend(theseKeys)
            if len(_key_resp_3_allKeys):
                key_resp_3.keys = _key_resp_3_allKeys[-1].name  # just the last key pressed
                key_resp_3.rt = _key_resp_3_allKeys[-1].rt
                key_resp_3.duration = _key_resp_3_allKeys[-1].duration
        
        # *TimeEstimateExampleInst* updates
        
        # if TimeEstimateExampleInst is starting this frame...
        if TimeEstimateExampleInst.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            TimeEstimateExampleInst.frameNStart = frameN  # exact frame index
            TimeEstimateExampleInst.tStart = t  # local t and not account for scr refresh
            TimeEstimateExampleInst.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(TimeEstimateExampleInst, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'TimeEstimateExampleInst.started')
            # update status
            TimeEstimateExampleInst.status = STARTED
            TimeEstimateExampleInst.setAutoDraw(True)
        
        # if TimeEstimateExampleInst is active this frame...
        if TimeEstimateExampleInst.status == STARTED:
            # update params
            pass
        
        # *TimeEstimateExampleConfirm* updates
        
        # if TimeEstimateExampleConfirm is starting this frame...
        if TimeEstimateExampleConfirm.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            TimeEstimateExampleConfirm.frameNStart = frameN  # exact frame index
            TimeEstimateExampleConfirm.tStart = t  # local t and not account for scr refresh
            TimeEstimateExampleConfirm.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(TimeEstimateExampleConfirm, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'TimeEstimateExampleConfirm.started')
            # update status
            TimeEstimateExampleConfirm.status = STARTED
            TimeEstimateExampleConfirm.setAutoDraw(True)
        
        # if TimeEstimateExampleConfirm is active this frame...
        if TimeEstimateExampleConfirm.status == STARTED:
            # update params
            pass
        
        # *TimeEstimateExampleUnits* updates
        
        # if TimeEstimateExampleUnits is starting this frame...
        if TimeEstimateExampleUnits.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            TimeEstimateExampleUnits.frameNStart = frameN  # exact frame index
            TimeEstimateExampleUnits.tStart = t  # local t and not account for scr refresh
            TimeEstimateExampleUnits.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(TimeEstimateExampleUnits, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'TimeEstimateExampleUnits.started')
            # update status
            TimeEstimateExampleUnits.status = STARTED
            TimeEstimateExampleUnits.setAutoDraw(True)
        
        # if TimeEstimateExampleUnits is active this frame...
        if TimeEstimateExampleUnits.status == STARTED:
            # update params
            pass
        # Run 'Each Frame' code from code_9
        keys = event.getKeys()
        
        for key in keys:
            if key == 'left':
                focus = 'minutes'
            elif key == 'right':
                focus = 'seconds'
            elif key == 'up':
                if focus == 'minutes':
                    minutes = (minutes + 1) % 60  
                elif focus == 'seconds':
                    seconds = (seconds + 1) % 60
            elif key == 'down':
                if focus == 'minutes':
                    minutes = (minutes - 1) % 60
                elif focus == 'seconds':
                    seconds = (seconds - 1) % 60
            elif key == 'return':
                continueRoutine = False  # finish routine
        
        # Update display text
        if focus == 'minutes':
            time_str = f"[{minutes:02d}]:{seconds:02d}"
        else:
            time_str = f"{minutes:02d}:[{seconds:02d}]"
        
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            TimeEstimateExample.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in TimeEstimateExample.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "TimeEstimateExample" ---
    for thisComponent in TimeEstimateExample.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for TimeEstimateExample
    TimeEstimateExample.tStop = globalClock.getTime(format='float')
    TimeEstimateExample.tStopRefresh = tThisFlipGlobal
    thisExp.addData('TimeEstimateExample.stopped', TimeEstimateExample.tStop)
    # check responses
    if key_resp_3.keys in ['', [], None]:  # No response was made
        key_resp_3.keys = None
    thisExp.addData('key_resp_3.keys',key_resp_3.keys)
    if key_resp_3.keys != None:  # we had a response
        thisExp.addData('key_resp_3.rt', key_resp_3.rt)
        thisExp.addData('key_resp_3.duration', key_resp_3.duration)
    # Run 'End Routine' code from code_9
    #Save data
    #thisExp.addData('estimated_minutes', minutes)
    #thisExp.addData('estimated_seconds', seconds)
    
    thisExp.nextEntry()
    # the Routine "TimeEstimateExample" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "TimeEstimateQuestion_2" ---
    # create an object to store info about Routine TimeEstimateQuestion_2
    TimeEstimateQuestion_2 = data.Routine(
        name='TimeEstimateQuestion_2',
        components=[TimeEstimateQuestion, TimeEstimateResp],
    )
    TimeEstimateQuestion_2.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for TimeEstimateResp
    TimeEstimateResp.keys = []
    TimeEstimateResp.rt = []
    _TimeEstimateResp_allKeys = []
    # store start times for TimeEstimateQuestion_2
    TimeEstimateQuestion_2.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    TimeEstimateQuestion_2.tStart = globalClock.getTime(format='float')
    TimeEstimateQuestion_2.status = STARTED
    thisExp.addData('TimeEstimateQuestion_2.started', TimeEstimateQuestion_2.tStart)
    TimeEstimateQuestion_2.maxDuration = None
    # keep track of which components have finished
    TimeEstimateQuestion_2Components = TimeEstimateQuestion_2.components
    for thisComponent in TimeEstimateQuestion_2.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "TimeEstimateQuestion_2" ---
    TimeEstimateQuestion_2.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *TimeEstimateQuestion* updates
        
        # if TimeEstimateQuestion is starting this frame...
        if TimeEstimateQuestion.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            TimeEstimateQuestion.frameNStart = frameN  # exact frame index
            TimeEstimateQuestion.tStart = t  # local t and not account for scr refresh
            TimeEstimateQuestion.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(TimeEstimateQuestion, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'TimeEstimateQuestion.started')
            # update status
            TimeEstimateQuestion.status = STARTED
            TimeEstimateQuestion.setAutoDraw(True)
        
        # if TimeEstimateQuestion is active this frame...
        if TimeEstimateQuestion.status == STARTED:
            # update params
            pass
        
        # *TimeEstimateResp* updates
        waitOnFlip = False
        
        # if TimeEstimateResp is starting this frame...
        if TimeEstimateResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            TimeEstimateResp.frameNStart = frameN  # exact frame index
            TimeEstimateResp.tStart = t  # local t and not account for scr refresh
            TimeEstimateResp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(TimeEstimateResp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'TimeEstimateResp.started')
            # update status
            TimeEstimateResp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(TimeEstimateResp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(TimeEstimateResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if TimeEstimateResp.status == STARTED and not waitOnFlip:
            theseKeys = TimeEstimateResp.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _TimeEstimateResp_allKeys.extend(theseKeys)
            if len(_TimeEstimateResp_allKeys):
                TimeEstimateResp.keys = _TimeEstimateResp_allKeys[-1].name  # just the last key pressed
                TimeEstimateResp.rt = _TimeEstimateResp_allKeys[-1].rt
                TimeEstimateResp.duration = _TimeEstimateResp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            TimeEstimateQuestion_2.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in TimeEstimateQuestion_2.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "TimeEstimateQuestion_2" ---
    for thisComponent in TimeEstimateQuestion_2.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for TimeEstimateQuestion_2
    TimeEstimateQuestion_2.tStop = globalClock.getTime(format='float')
    TimeEstimateQuestion_2.tStopRefresh = tThisFlipGlobal
    thisExp.addData('TimeEstimateQuestion_2.stopped', TimeEstimateQuestion_2.tStop)
    # check responses
    if TimeEstimateResp.keys in ['', [], None]:  # No response was made
        TimeEstimateResp.keys = None
    thisExp.addData('TimeEstimateResp.keys',TimeEstimateResp.keys)
    if TimeEstimateResp.keys != None:  # we had a response
        thisExp.addData('TimeEstimateResp.rt', TimeEstimateResp.rt)
        thisExp.addData('TimeEstimateResp.duration', TimeEstimateResp.duration)
    thisExp.nextEntry()
    # the Routine "TimeEstimateQuestion_2" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "DistractorInst" ---
    # create an object to store info about Routine DistractorInst
    DistractorInst = data.Routine(
        name='DistractorInst',
        components=[DistractorInstText, DistractorInstResp],
    )
    DistractorInst.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for DistractorInstResp
    DistractorInstResp.keys = []
    DistractorInstResp.rt = []
    _DistractorInstResp_allKeys = []
    # store start times for DistractorInst
    DistractorInst.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    DistractorInst.tStart = globalClock.getTime(format='float')
    DistractorInst.status = STARTED
    thisExp.addData('DistractorInst.started', DistractorInst.tStart)
    DistractorInst.maxDuration = None
    # keep track of which components have finished
    DistractorInstComponents = DistractorInst.components
    for thisComponent in DistractorInst.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "DistractorInst" ---
    DistractorInst.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *DistractorInstText* updates
        
        # if DistractorInstText is starting this frame...
        if DistractorInstText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            DistractorInstText.frameNStart = frameN  # exact frame index
            DistractorInstText.tStart = t  # local t and not account for scr refresh
            DistractorInstText.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(DistractorInstText, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'DistractorInstText.started')
            # update status
            DistractorInstText.status = STARTED
            DistractorInstText.setAutoDraw(True)
        
        # if DistractorInstText is active this frame...
        if DistractorInstText.status == STARTED:
            # update params
            pass
        
        # *DistractorInstResp* updates
        waitOnFlip = False
        
        # if DistractorInstResp is starting this frame...
        if DistractorInstResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            DistractorInstResp.frameNStart = frameN  # exact frame index
            DistractorInstResp.tStart = t  # local t and not account for scr refresh
            DistractorInstResp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(DistractorInstResp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'DistractorInstResp.started')
            # update status
            DistractorInstResp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(DistractorInstResp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(DistractorInstResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if DistractorInstResp.status == STARTED and not waitOnFlip:
            theseKeys = DistractorInstResp.getKeys(keyList=['5'], ignoreKeys=["escape"], waitRelease=False)
            _DistractorInstResp_allKeys.extend(theseKeys)
            if len(_DistractorInstResp_allKeys):
                DistractorInstResp.keys = _DistractorInstResp_allKeys[-1].name  # just the last key pressed
                DistractorInstResp.rt = _DistractorInstResp_allKeys[-1].rt
                DistractorInstResp.duration = _DistractorInstResp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            DistractorInst.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in DistractorInst.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "DistractorInst" ---
    for thisComponent in DistractorInst.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for DistractorInst
    DistractorInst.tStop = globalClock.getTime(format='float')
    DistractorInst.tStopRefresh = tThisFlipGlobal
    thisExp.addData('DistractorInst.stopped', DistractorInst.tStop)
    # check responses
    if DistractorInstResp.keys in ['', [], None]:  # No response was made
        DistractorInstResp.keys = None
    thisExp.addData('DistractorInstResp.keys',DistractorInstResp.keys)
    if DistractorInstResp.keys != None:  # we had a response
        thisExp.addData('DistractorInstResp.rt', DistractorInstResp.rt)
        thisExp.addData('DistractorInstResp.duration', DistractorInstResp.duration)
    thisExp.nextEntry()
    # the Routine "DistractorInst" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "DistractorExample1" ---
    # create an object to store info about Routine DistractorExample1
    DistractorExample1 = data.Routine(
        name='DistractorExample1',
        components=[DistractorExample1Number, DistractorExample1OptionsText, DistractorExample1Resp],
    )
    DistractorExample1.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for DistractorExample1Resp
    DistractorExample1Resp.keys = []
    DistractorExample1Resp.rt = []
    _DistractorExample1Resp_allKeys = []
    # store start times for DistractorExample1
    DistractorExample1.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    DistractorExample1.tStart = globalClock.getTime(format='float')
    DistractorExample1.status = STARTED
    thisExp.addData('DistractorExample1.started', DistractorExample1.tStart)
    DistractorExample1.maxDuration = None
    # keep track of which components have finished
    DistractorExample1Components = DistractorExample1.components
    for thisComponent in DistractorExample1.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "DistractorExample1" ---
    DistractorExample1.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 2.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *DistractorExample1Number* updates
        
        # if DistractorExample1Number is starting this frame...
        if DistractorExample1Number.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            DistractorExample1Number.frameNStart = frameN  # exact frame index
            DistractorExample1Number.tStart = t  # local t and not account for scr refresh
            DistractorExample1Number.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(DistractorExample1Number, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'DistractorExample1Number.started')
            # update status
            DistractorExample1Number.status = STARTED
            DistractorExample1Number.setAutoDraw(True)
        
        # if DistractorExample1Number is active this frame...
        if DistractorExample1Number.status == STARTED:
            # update params
            pass
        
        # if DistractorExample1Number is stopping this frame...
        if DistractorExample1Number.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > DistractorExample1Number.tStartRefresh + 2-frameTolerance:
                # keep track of stop time/frame for later
                DistractorExample1Number.tStop = t  # not accounting for scr refresh
                DistractorExample1Number.tStopRefresh = tThisFlipGlobal  # on global time
                DistractorExample1Number.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'DistractorExample1Number.stopped')
                # update status
                DistractorExample1Number.status = FINISHED
                DistractorExample1Number.setAutoDraw(False)
        
        # *DistractorExample1OptionsText* updates
        
        # if DistractorExample1OptionsText is starting this frame...
        if DistractorExample1OptionsText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            DistractorExample1OptionsText.frameNStart = frameN  # exact frame index
            DistractorExample1OptionsText.tStart = t  # local t and not account for scr refresh
            DistractorExample1OptionsText.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(DistractorExample1OptionsText, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'DistractorExample1OptionsText.started')
            # update status
            DistractorExample1OptionsText.status = STARTED
            DistractorExample1OptionsText.setAutoDraw(True)
        
        # if DistractorExample1OptionsText is active this frame...
        if DistractorExample1OptionsText.status == STARTED:
            # update params
            pass
        
        # if DistractorExample1OptionsText is stopping this frame...
        if DistractorExample1OptionsText.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > DistractorExample1OptionsText.tStartRefresh + 2-frameTolerance:
                # keep track of stop time/frame for later
                DistractorExample1OptionsText.tStop = t  # not accounting for scr refresh
                DistractorExample1OptionsText.tStopRefresh = tThisFlipGlobal  # on global time
                DistractorExample1OptionsText.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'DistractorExample1OptionsText.stopped')
                # update status
                DistractorExample1OptionsText.status = FINISHED
                DistractorExample1OptionsText.setAutoDraw(False)
        
        # *DistractorExample1Resp* updates
        waitOnFlip = False
        
        # if DistractorExample1Resp is starting this frame...
        if DistractorExample1Resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            DistractorExample1Resp.frameNStart = frameN  # exact frame index
            DistractorExample1Resp.tStart = t  # local t and not account for scr refresh
            DistractorExample1Resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(DistractorExample1Resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'DistractorExample1Resp.started')
            # update status
            DistractorExample1Resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(DistractorExample1Resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(DistractorExample1Resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        
        # if DistractorExample1Resp is stopping this frame...
        if DistractorExample1Resp.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > DistractorExample1Resp.tStartRefresh + 2-frameTolerance:
                # keep track of stop time/frame for later
                DistractorExample1Resp.tStop = t  # not accounting for scr refresh
                DistractorExample1Resp.tStopRefresh = tThisFlipGlobal  # on global time
                DistractorExample1Resp.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'DistractorExample1Resp.stopped')
                # update status
                DistractorExample1Resp.status = FINISHED
                DistractorExample1Resp.status = FINISHED
        if DistractorExample1Resp.status == STARTED and not waitOnFlip:
            theseKeys = DistractorExample1Resp.getKeys(keyList=['left','right'], ignoreKeys=["escape"], waitRelease=False)
            _DistractorExample1Resp_allKeys.extend(theseKeys)
            if len(_DistractorExample1Resp_allKeys):
                DistractorExample1Resp.keys = _DistractorExample1Resp_allKeys[-1].name  # just the last key pressed
                DistractorExample1Resp.rt = _DistractorExample1Resp_allKeys[-1].rt
                DistractorExample1Resp.duration = _DistractorExample1Resp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            DistractorExample1.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in DistractorExample1.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "DistractorExample1" ---
    for thisComponent in DistractorExample1.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for DistractorExample1
    DistractorExample1.tStop = globalClock.getTime(format='float')
    DistractorExample1.tStopRefresh = tThisFlipGlobal
    thisExp.addData('DistractorExample1.stopped', DistractorExample1.tStop)
    # check responses
    if DistractorExample1Resp.keys in ['', [], None]:  # No response was made
        DistractorExample1Resp.keys = None
    thisExp.addData('DistractorExample1Resp.keys',DistractorExample1Resp.keys)
    if DistractorExample1Resp.keys != None:  # we had a response
        thisExp.addData('DistractorExample1Resp.rt', DistractorExample1Resp.rt)
        thisExp.addData('DistractorExample1Resp.duration', DistractorExample1Resp.duration)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if DistractorExample1.maxDurationReached:
        routineTimer.addTime(-DistractorExample1.maxDuration)
    elif DistractorExample1.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-2.000000)
    thisExp.nextEntry()
    
    # --- Prepare to start Routine "DistractorExample2" ---
    # create an object to store info about Routine DistractorExample2
    DistractorExample2 = data.Routine(
        name='DistractorExample2',
        components=[DistractorExample2Number, DistractorExample2OptionsText, DistractorExample2Resp],
    )
    DistractorExample2.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for DistractorExample2Resp
    DistractorExample2Resp.keys = []
    DistractorExample2Resp.rt = []
    _DistractorExample2Resp_allKeys = []
    # store start times for DistractorExample2
    DistractorExample2.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    DistractorExample2.tStart = globalClock.getTime(format='float')
    DistractorExample2.status = STARTED
    thisExp.addData('DistractorExample2.started', DistractorExample2.tStart)
    DistractorExample2.maxDuration = None
    # keep track of which components have finished
    DistractorExample2Components = DistractorExample2.components
    for thisComponent in DistractorExample2.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "DistractorExample2" ---
    DistractorExample2.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 2.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *DistractorExample2Number* updates
        
        # if DistractorExample2Number is starting this frame...
        if DistractorExample2Number.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            DistractorExample2Number.frameNStart = frameN  # exact frame index
            DistractorExample2Number.tStart = t  # local t and not account for scr refresh
            DistractorExample2Number.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(DistractorExample2Number, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'DistractorExample2Number.started')
            # update status
            DistractorExample2Number.status = STARTED
            DistractorExample2Number.setAutoDraw(True)
        
        # if DistractorExample2Number is active this frame...
        if DistractorExample2Number.status == STARTED:
            # update params
            pass
        
        # if DistractorExample2Number is stopping this frame...
        if DistractorExample2Number.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > DistractorExample2Number.tStartRefresh + 2-frameTolerance:
                # keep track of stop time/frame for later
                DistractorExample2Number.tStop = t  # not accounting for scr refresh
                DistractorExample2Number.tStopRefresh = tThisFlipGlobal  # on global time
                DistractorExample2Number.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'DistractorExample2Number.stopped')
                # update status
                DistractorExample2Number.status = FINISHED
                DistractorExample2Number.setAutoDraw(False)
        
        # *DistractorExample2OptionsText* updates
        
        # if DistractorExample2OptionsText is starting this frame...
        if DistractorExample2OptionsText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            DistractorExample2OptionsText.frameNStart = frameN  # exact frame index
            DistractorExample2OptionsText.tStart = t  # local t and not account for scr refresh
            DistractorExample2OptionsText.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(DistractorExample2OptionsText, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'DistractorExample2OptionsText.started')
            # update status
            DistractorExample2OptionsText.status = STARTED
            DistractorExample2OptionsText.setAutoDraw(True)
        
        # if DistractorExample2OptionsText is active this frame...
        if DistractorExample2OptionsText.status == STARTED:
            # update params
            pass
        
        # if DistractorExample2OptionsText is stopping this frame...
        if DistractorExample2OptionsText.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > DistractorExample2OptionsText.tStartRefresh + 2-frameTolerance:
                # keep track of stop time/frame for later
                DistractorExample2OptionsText.tStop = t  # not accounting for scr refresh
                DistractorExample2OptionsText.tStopRefresh = tThisFlipGlobal  # on global time
                DistractorExample2OptionsText.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'DistractorExample2OptionsText.stopped')
                # update status
                DistractorExample2OptionsText.status = FINISHED
                DistractorExample2OptionsText.setAutoDraw(False)
        
        # *DistractorExample2Resp* updates
        waitOnFlip = False
        
        # if DistractorExample2Resp is starting this frame...
        if DistractorExample2Resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            DistractorExample2Resp.frameNStart = frameN  # exact frame index
            DistractorExample2Resp.tStart = t  # local t and not account for scr refresh
            DistractorExample2Resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(DistractorExample2Resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'DistractorExample2Resp.started')
            # update status
            DistractorExample2Resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(DistractorExample2Resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(DistractorExample2Resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        
        # if DistractorExample2Resp is stopping this frame...
        if DistractorExample2Resp.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > DistractorExample2Resp.tStartRefresh + 2-frameTolerance:
                # keep track of stop time/frame for later
                DistractorExample2Resp.tStop = t  # not accounting for scr refresh
                DistractorExample2Resp.tStopRefresh = tThisFlipGlobal  # on global time
                DistractorExample2Resp.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'DistractorExample2Resp.stopped')
                # update status
                DistractorExample2Resp.status = FINISHED
                DistractorExample2Resp.status = FINISHED
        if DistractorExample2Resp.status == STARTED and not waitOnFlip:
            theseKeys = DistractorExample2Resp.getKeys(keyList=['left','right'], ignoreKeys=["escape"], waitRelease=False)
            _DistractorExample2Resp_allKeys.extend(theseKeys)
            if len(_DistractorExample2Resp_allKeys):
                DistractorExample2Resp.keys = _DistractorExample2Resp_allKeys[-1].name  # just the last key pressed
                DistractorExample2Resp.rt = _DistractorExample2Resp_allKeys[-1].rt
                DistractorExample2Resp.duration = _DistractorExample2Resp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            DistractorExample2.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in DistractorExample2.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "DistractorExample2" ---
    for thisComponent in DistractorExample2.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for DistractorExample2
    DistractorExample2.tStop = globalClock.getTime(format='float')
    DistractorExample2.tStopRefresh = tThisFlipGlobal
    thisExp.addData('DistractorExample2.stopped', DistractorExample2.tStop)
    # check responses
    if DistractorExample2Resp.keys in ['', [], None]:  # No response was made
        DistractorExample2Resp.keys = None
    thisExp.addData('DistractorExample2Resp.keys',DistractorExample2Resp.keys)
    if DistractorExample2Resp.keys != None:  # we had a response
        thisExp.addData('DistractorExample2Resp.rt', DistractorExample2Resp.rt)
        thisExp.addData('DistractorExample2Resp.duration', DistractorExample2Resp.duration)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if DistractorExample2.maxDurationReached:
        routineTimer.addTime(-DistractorExample2.maxDuration)
    elif DistractorExample2.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-2.000000)
    thisExp.nextEntry()
    
    # --- Prepare to start Routine "DistractorQuestion" ---
    # create an object to store info about Routine DistractorQuestion
    DistractorQuestion = data.Routine(
        name='DistractorQuestion',
        components=[DistractorQuestionText, DistractorQuestionResp],
    )
    DistractorQuestion.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for DistractorQuestionResp
    DistractorQuestionResp.keys = []
    DistractorQuestionResp.rt = []
    _DistractorQuestionResp_allKeys = []
    # store start times for DistractorQuestion
    DistractorQuestion.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    DistractorQuestion.tStart = globalClock.getTime(format='float')
    DistractorQuestion.status = STARTED
    thisExp.addData('DistractorQuestion.started', DistractorQuestion.tStart)
    DistractorQuestion.maxDuration = None
    # keep track of which components have finished
    DistractorQuestionComponents = DistractorQuestion.components
    for thisComponent in DistractorQuestion.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "DistractorQuestion" ---
    DistractorQuestion.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *DistractorQuestionText* updates
        
        # if DistractorQuestionText is starting this frame...
        if DistractorQuestionText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            DistractorQuestionText.frameNStart = frameN  # exact frame index
            DistractorQuestionText.tStart = t  # local t and not account for scr refresh
            DistractorQuestionText.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(DistractorQuestionText, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'DistractorQuestionText.started')
            # update status
            DistractorQuestionText.status = STARTED
            DistractorQuestionText.setAutoDraw(True)
        
        # if DistractorQuestionText is active this frame...
        if DistractorQuestionText.status == STARTED:
            # update params
            pass
        
        # *DistractorQuestionResp* updates
        waitOnFlip = False
        
        # if DistractorQuestionResp is starting this frame...
        if DistractorQuestionResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            DistractorQuestionResp.frameNStart = frameN  # exact frame index
            DistractorQuestionResp.tStart = t  # local t and not account for scr refresh
            DistractorQuestionResp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(DistractorQuestionResp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'DistractorQuestionResp.started')
            # update status
            DistractorQuestionResp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(DistractorQuestionResp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(DistractorQuestionResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if DistractorQuestionResp.status == STARTED and not waitOnFlip:
            theseKeys = DistractorQuestionResp.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _DistractorQuestionResp_allKeys.extend(theseKeys)
            if len(_DistractorQuestionResp_allKeys):
                DistractorQuestionResp.keys = _DistractorQuestionResp_allKeys[-1].name  # just the last key pressed
                DistractorQuestionResp.rt = _DistractorQuestionResp_allKeys[-1].rt
                DistractorQuestionResp.duration = _DistractorQuestionResp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            DistractorQuestion.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in DistractorQuestion.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "DistractorQuestion" ---
    for thisComponent in DistractorQuestion.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for DistractorQuestion
    DistractorQuestion.tStop = globalClock.getTime(format='float')
    DistractorQuestion.tStopRefresh = tThisFlipGlobal
    thisExp.addData('DistractorQuestion.stopped', DistractorQuestion.tStop)
    # check responses
    if DistractorQuestionResp.keys in ['', [], None]:  # No response was made
        DistractorQuestionResp.keys = None
    thisExp.addData('DistractorQuestionResp.keys',DistractorQuestionResp.keys)
    if DistractorQuestionResp.keys != None:  # we had a response
        thisExp.addData('DistractorQuestionResp.rt', DistractorQuestionResp.rt)
        thisExp.addData('DistractorQuestionResp.duration', DistractorQuestionResp.duration)
    thisExp.nextEntry()
    # the Routine "DistractorQuestion" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "TestInst" ---
    # create an object to store info about Routine TestInst
    TestInst = data.Routine(
        name='TestInst',
        components=[TestInstText, TestInstResp],
    )
    TestInst.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for TestInstResp
    TestInstResp.keys = []
    TestInstResp.rt = []
    _TestInstResp_allKeys = []
    # store start times for TestInst
    TestInst.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    TestInst.tStart = globalClock.getTime(format='float')
    TestInst.status = STARTED
    thisExp.addData('TestInst.started', TestInst.tStart)
    TestInst.maxDuration = None
    # keep track of which components have finished
    TestInstComponents = TestInst.components
    for thisComponent in TestInst.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "TestInst" ---
    TestInst.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *TestInstText* updates
        
        # if TestInstText is starting this frame...
        if TestInstText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            TestInstText.frameNStart = frameN  # exact frame index
            TestInstText.tStart = t  # local t and not account for scr refresh
            TestInstText.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(TestInstText, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'TestInstText.started')
            # update status
            TestInstText.status = STARTED
            TestInstText.setAutoDraw(True)
        
        # if TestInstText is active this frame...
        if TestInstText.status == STARTED:
            # update params
            pass
        
        # *TestInstResp* updates
        waitOnFlip = False
        
        # if TestInstResp is starting this frame...
        if TestInstResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            TestInstResp.frameNStart = frameN  # exact frame index
            TestInstResp.tStart = t  # local t and not account for scr refresh
            TestInstResp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(TestInstResp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'TestInstResp.started')
            # update status
            TestInstResp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(TestInstResp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(TestInstResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if TestInstResp.status == STARTED and not waitOnFlip:
            theseKeys = TestInstResp.getKeys(keyList=['5'], ignoreKeys=["escape"], waitRelease=False)
            _TestInstResp_allKeys.extend(theseKeys)
            if len(_TestInstResp_allKeys):
                TestInstResp.keys = _TestInstResp_allKeys[-1].name  # just the last key pressed
                TestInstResp.rt = _TestInstResp_allKeys[-1].rt
                TestInstResp.duration = _TestInstResp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            TestInst.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in TestInst.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "TestInst" ---
    for thisComponent in TestInst.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for TestInst
    TestInst.tStop = globalClock.getTime(format='float')
    TestInst.tStopRefresh = tThisFlipGlobal
    thisExp.addData('TestInst.stopped', TestInst.tStop)
    # check responses
    if TestInstResp.keys in ['', [], None]:  # No response was made
        TestInstResp.keys = None
    thisExp.addData('TestInstResp.keys',TestInstResp.keys)
    if TestInstResp.keys != None:  # we had a response
        thisExp.addData('TestInstResp.rt', TestInstResp.rt)
        thisExp.addData('TestInstResp.duration', TestInstResp.duration)
    thisExp.nextEntry()
    # the Routine "TestInst" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "TestExample" ---
    # create an object to store info about Routine TestExample
    TestExample = data.Routine(
        name='TestExample',
        components=[TestExampleLeftImage, TestExampleRightImage, TestExampleResp, TestExampleOptions, TestExampleQuestion],
    )
    TestExample.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for TestExampleResp
    TestExampleResp.keys = []
    TestExampleResp.rt = []
    _TestExampleResp_allKeys = []
    # store start times for TestExample
    TestExample.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    TestExample.tStart = globalClock.getTime(format='float')
    TestExample.status = STARTED
    thisExp.addData('TestExample.started', TestExample.tStart)
    TestExample.maxDuration = None
    # keep track of which components have finished
    TestExampleComponents = TestExample.components
    for thisComponent in TestExample.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "TestExample" ---
    TestExample.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 8.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *TestExampleLeftImage* updates
        
        # if TestExampleLeftImage is starting this frame...
        if TestExampleLeftImage.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            TestExampleLeftImage.frameNStart = frameN  # exact frame index
            TestExampleLeftImage.tStart = t  # local t and not account for scr refresh
            TestExampleLeftImage.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(TestExampleLeftImage, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'TestExampleLeftImage.started')
            # update status
            TestExampleLeftImage.status = STARTED
            TestExampleLeftImage.setAutoDraw(True)
        
        # if TestExampleLeftImage is active this frame...
        if TestExampleLeftImage.status == STARTED:
            # update params
            pass
        
        # if TestExampleLeftImage is stopping this frame...
        if TestExampleLeftImage.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > TestExampleLeftImage.tStartRefresh + 8-frameTolerance:
                # keep track of stop time/frame for later
                TestExampleLeftImage.tStop = t  # not accounting for scr refresh
                TestExampleLeftImage.tStopRefresh = tThisFlipGlobal  # on global time
                TestExampleLeftImage.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'TestExampleLeftImage.stopped')
                # update status
                TestExampleLeftImage.status = FINISHED
                TestExampleLeftImage.setAutoDraw(False)
        
        # *TestExampleRightImage* updates
        
        # if TestExampleRightImage is starting this frame...
        if TestExampleRightImage.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            TestExampleRightImage.frameNStart = frameN  # exact frame index
            TestExampleRightImage.tStart = t  # local t and not account for scr refresh
            TestExampleRightImage.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(TestExampleRightImage, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'TestExampleRightImage.started')
            # update status
            TestExampleRightImage.status = STARTED
            TestExampleRightImage.setAutoDraw(True)
        
        # if TestExampleRightImage is active this frame...
        if TestExampleRightImage.status == STARTED:
            # update params
            pass
        
        # if TestExampleRightImage is stopping this frame...
        if TestExampleRightImage.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > TestExampleRightImage.tStartRefresh + 8-frameTolerance:
                # keep track of stop time/frame for later
                TestExampleRightImage.tStop = t  # not accounting for scr refresh
                TestExampleRightImage.tStopRefresh = tThisFlipGlobal  # on global time
                TestExampleRightImage.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'TestExampleRightImage.stopped')
                # update status
                TestExampleRightImage.status = FINISHED
                TestExampleRightImage.setAutoDraw(False)
        
        # *TestExampleResp* updates
        waitOnFlip = False
        
        # if TestExampleResp is starting this frame...
        if TestExampleResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            TestExampleResp.frameNStart = frameN  # exact frame index
            TestExampleResp.tStart = t  # local t and not account for scr refresh
            TestExampleResp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(TestExampleResp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'TestExampleResp.started')
            # update status
            TestExampleResp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(TestExampleResp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(TestExampleResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        
        # if TestExampleResp is stopping this frame...
        if TestExampleResp.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > TestExampleResp.tStartRefresh + 8-frameTolerance:
                # keep track of stop time/frame for later
                TestExampleResp.tStop = t  # not accounting for scr refresh
                TestExampleResp.tStopRefresh = tThisFlipGlobal  # on global time
                TestExampleResp.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'TestExampleResp.stopped')
                # update status
                TestExampleResp.status = FINISHED
                TestExampleResp.status = FINISHED
        if TestExampleResp.status == STARTED and not waitOnFlip:
            theseKeys = TestExampleResp.getKeys(keyList=['left','right'], ignoreKeys=["escape"], waitRelease=False)
            _TestExampleResp_allKeys.extend(theseKeys)
            if len(_TestExampleResp_allKeys):
                TestExampleResp.keys = _TestExampleResp_allKeys[-1].name  # just the last key pressed
                TestExampleResp.rt = _TestExampleResp_allKeys[-1].rt
                TestExampleResp.duration = _TestExampleResp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # *TestExampleOptions* updates
        
        # if TestExampleOptions is starting this frame...
        if TestExampleOptions.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            TestExampleOptions.frameNStart = frameN  # exact frame index
            TestExampleOptions.tStart = t  # local t and not account for scr refresh
            TestExampleOptions.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(TestExampleOptions, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'TestExampleOptions.started')
            # update status
            TestExampleOptions.status = STARTED
            TestExampleOptions.setAutoDraw(True)
        
        # if TestExampleOptions is active this frame...
        if TestExampleOptions.status == STARTED:
            # update params
            pass
        
        # if TestExampleOptions is stopping this frame...
        if TestExampleOptions.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > TestExampleOptions.tStartRefresh + 8-frameTolerance:
                # keep track of stop time/frame for later
                TestExampleOptions.tStop = t  # not accounting for scr refresh
                TestExampleOptions.tStopRefresh = tThisFlipGlobal  # on global time
                TestExampleOptions.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'TestExampleOptions.stopped')
                # update status
                TestExampleOptions.status = FINISHED
                TestExampleOptions.setAutoDraw(False)
        
        # *TestExampleQuestion* updates
        
        # if TestExampleQuestion is starting this frame...
        if TestExampleQuestion.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            TestExampleQuestion.frameNStart = frameN  # exact frame index
            TestExampleQuestion.tStart = t  # local t and not account for scr refresh
            TestExampleQuestion.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(TestExampleQuestion, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'TestExampleQuestion.started')
            # update status
            TestExampleQuestion.status = STARTED
            TestExampleQuestion.setAutoDraw(True)
        
        # if TestExampleQuestion is active this frame...
        if TestExampleQuestion.status == STARTED:
            # update params
            pass
        
        # if TestExampleQuestion is stopping this frame...
        if TestExampleQuestion.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > TestExampleQuestion.tStartRefresh + 8-frameTolerance:
                # keep track of stop time/frame for later
                TestExampleQuestion.tStop = t  # not accounting for scr refresh
                TestExampleQuestion.tStopRefresh = tThisFlipGlobal  # on global time
                TestExampleQuestion.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'TestExampleQuestion.stopped')
                # update status
                TestExampleQuestion.status = FINISHED
                TestExampleQuestion.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            TestExample.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in TestExample.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "TestExample" ---
    for thisComponent in TestExample.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for TestExample
    TestExample.tStop = globalClock.getTime(format='float')
    TestExample.tStopRefresh = tThisFlipGlobal
    thisExp.addData('TestExample.stopped', TestExample.tStop)
    # check responses
    if TestExampleResp.keys in ['', [], None]:  # No response was made
        TestExampleResp.keys = None
    thisExp.addData('TestExampleResp.keys',TestExampleResp.keys)
    if TestExampleResp.keys != None:  # we had a response
        thisExp.addData('TestExampleResp.rt', TestExampleResp.rt)
        thisExp.addData('TestExampleResp.duration', TestExampleResp.duration)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if TestExample.maxDurationReached:
        routineTimer.addTime(-TestExample.maxDuration)
    elif TestExample.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-8.000000)
    thisExp.nextEntry()
    
    # --- Prepare to start Routine "TestQuestion" ---
    # create an object to store info about Routine TestQuestion
    TestQuestion = data.Routine(
        name='TestQuestion',
        components=[TestQuestionText, TestQuestionResp],
    )
    TestQuestion.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for TestQuestionResp
    TestQuestionResp.keys = []
    TestQuestionResp.rt = []
    _TestQuestionResp_allKeys = []
    # store start times for TestQuestion
    TestQuestion.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    TestQuestion.tStart = globalClock.getTime(format='float')
    TestQuestion.status = STARTED
    thisExp.addData('TestQuestion.started', TestQuestion.tStart)
    TestQuestion.maxDuration = None
    # keep track of which components have finished
    TestQuestionComponents = TestQuestion.components
    for thisComponent in TestQuestion.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "TestQuestion" ---
    TestQuestion.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *TestQuestionText* updates
        
        # if TestQuestionText is starting this frame...
        if TestQuestionText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            TestQuestionText.frameNStart = frameN  # exact frame index
            TestQuestionText.tStart = t  # local t and not account for scr refresh
            TestQuestionText.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(TestQuestionText, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'TestQuestionText.started')
            # update status
            TestQuestionText.status = STARTED
            TestQuestionText.setAutoDraw(True)
        
        # if TestQuestionText is active this frame...
        if TestQuestionText.status == STARTED:
            # update params
            pass
        
        # *TestQuestionResp* updates
        waitOnFlip = False
        
        # if TestQuestionResp is starting this frame...
        if TestQuestionResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            TestQuestionResp.frameNStart = frameN  # exact frame index
            TestQuestionResp.tStart = t  # local t and not account for scr refresh
            TestQuestionResp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(TestQuestionResp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'TestQuestionResp.started')
            # update status
            TestQuestionResp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(TestQuestionResp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(TestQuestionResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if TestQuestionResp.status == STARTED and not waitOnFlip:
            theseKeys = TestQuestionResp.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _TestQuestionResp_allKeys.extend(theseKeys)
            if len(_TestQuestionResp_allKeys):
                TestQuestionResp.keys = _TestQuestionResp_allKeys[-1].name  # just the last key pressed
                TestQuestionResp.rt = _TestQuestionResp_allKeys[-1].rt
                TestQuestionResp.duration = _TestQuestionResp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            TestQuestion.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in TestQuestion.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "TestQuestion" ---
    for thisComponent in TestQuestion.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for TestQuestion
    TestQuestion.tStop = globalClock.getTime(format='float')
    TestQuestion.tStopRefresh = tThisFlipGlobal
    thisExp.addData('TestQuestion.stopped', TestQuestion.tStop)
    # check responses
    if TestQuestionResp.keys in ['', [], None]:  # No response was made
        TestQuestionResp.keys = None
    thisExp.addData('TestQuestionResp.keys',TestQuestionResp.keys)
    if TestQuestionResp.keys != None:  # we had a response
        thisExp.addData('TestQuestionResp.rt', TestQuestionResp.rt)
        thisExp.addData('TestQuestionResp.duration', TestQuestionResp.duration)
    thisExp.nextEntry()
    # the Routine "TestQuestion" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "SpecifyingSubSpecificFolder" ---
    # create an object to store info about Routine SpecifyingSubSpecificFolder
    SpecifyingSubSpecificFolder = data.Routine(
        name='SpecifyingSubSpecificFolder',
        components=[],
    )
    SpecifyingSubSpecificFolder.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # store start times for SpecifyingSubSpecificFolder
    SpecifyingSubSpecificFolder.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    SpecifyingSubSpecificFolder.tStart = globalClock.getTime(format='float')
    SpecifyingSubSpecificFolder.status = STARTED
    thisExp.addData('SpecifyingSubSpecificFolder.started', SpecifyingSubSpecificFolder.tStart)
    SpecifyingSubSpecificFolder.maxDuration = None
    # keep track of which components have finished
    SpecifyingSubSpecificFolderComponents = SpecifyingSubSpecificFolder.components
    for thisComponent in SpecifyingSubSpecificFolder.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "SpecifyingSubSpecificFolder" ---
    SpecifyingSubSpecificFolder.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            SpecifyingSubSpecificFolder.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in SpecifyingSubSpecificFolder.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "SpecifyingSubSpecificFolder" ---
    for thisComponent in SpecifyingSubSpecificFolder.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for SpecifyingSubSpecificFolder
    SpecifyingSubSpecificFolder.tStop = globalClock.getTime(format='float')
    SpecifyingSubSpecificFolder.tStopRefresh = tThisFlipGlobal
    thisExp.addData('SpecifyingSubSpecificFolder.stopped', SpecifyingSubSpecificFolder.tStop)
    thisExp.nextEntry()
    # the Routine "SpecifyingSubSpecificFolder" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    BlockLoop = data.TrialHandler2(
        name='BlockLoop',
        nReps=1.0, 
        method='random', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions(conditionsFile), 
        seed=None, 
    )
    thisExp.addLoop(BlockLoop)  # add the loop to the experiment
    thisBlockLoop = BlockLoop.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisBlockLoop.rgb)
    if thisBlockLoop != None:
        for paramName in thisBlockLoop:
            globals()[paramName] = thisBlockLoop[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisBlockLoop in BlockLoop:
        currentLoop = BlockLoop
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisBlockLoop.rgb)
        if thisBlockLoop != None:
            for paramName in thisBlockLoop:
                globals()[paramName] = thisBlockLoop[paramName]
        
        # --- Prepare to start Routine "welcome" ---
        # create an object to store info about Routine welcome
        welcome = data.Routine(
            name='welcome',
            components=[welcomeText, welcomeResp],
        )
        welcome.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from code_8
        welcome_message = "Welcome to Block " + str(block_num) + "\n\nPress SPACEBAR to begin."
        
        welcomeText.setText(welcome_message
        )
        # create starting attributes for welcomeResp
        welcomeResp.keys = []
        welcomeResp.rt = []
        _welcomeResp_allKeys = []
        # store start times for welcome
        welcome.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        welcome.tStart = globalClock.getTime(format='float')
        welcome.status = STARTED
        thisExp.addData('welcome.started', welcome.tStart)
        welcome.maxDuration = None
        # keep track of which components have finished
        welcomeComponents = welcome.components
        for thisComponent in welcome.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "welcome" ---
        # if trial has changed, end Routine now
        if isinstance(BlockLoop, data.TrialHandler2) and thisBlockLoop.thisN != BlockLoop.thisTrial.thisN:
            continueRoutine = False
        welcome.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *welcomeText* updates
            
            # if welcomeText is starting this frame...
            if welcomeText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                welcomeText.frameNStart = frameN  # exact frame index
                welcomeText.tStart = t  # local t and not account for scr refresh
                welcomeText.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(welcomeText, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'welcomeText.started')
                # update status
                welcomeText.status = STARTED
                welcomeText.setAutoDraw(True)
            
            # if welcomeText is active this frame...
            if welcomeText.status == STARTED:
                # update params
                pass
            
            # *welcomeResp* updates
            waitOnFlip = False
            
            # if welcomeResp is starting this frame...
            if welcomeResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                welcomeResp.frameNStart = frameN  # exact frame index
                welcomeResp.tStart = t  # local t and not account for scr refresh
                welcomeResp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(welcomeResp, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'welcomeResp.started')
                # update status
                welcomeResp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(welcomeResp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(welcomeResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if welcomeResp.status == STARTED and not waitOnFlip:
                theseKeys = welcomeResp.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
                _welcomeResp_allKeys.extend(theseKeys)
                if len(_welcomeResp_allKeys):
                    welcomeResp.keys = _welcomeResp_allKeys[-1].name  # just the last key pressed
                    welcomeResp.rt = _welcomeResp_allKeys[-1].rt
                    welcomeResp.duration = _welcomeResp_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                welcome.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in welcome.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "welcome" ---
        for thisComponent in welcome.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for welcome
        welcome.tStop = globalClock.getTime(format='float')
        welcome.tStopRefresh = tThisFlipGlobal
        thisExp.addData('welcome.stopped', welcome.tStop)
        # check responses
        if welcomeResp.keys in ['', [], None]:  # No response was made
            welcomeResp.keys = None
        BlockLoop.addData('welcomeResp.keys',welcomeResp.keys)
        if welcomeResp.keys != None:  # we had a response
            BlockLoop.addData('welcomeResp.rt', welcomeResp.rt)
            BlockLoop.addData('welcomeResp.duration', welcomeResp.duration)
        # the Routine "welcome" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "StudyReminder" ---
        # create an object to store info about Routine StudyReminder
        StudyReminder = data.Routine(
            name='StudyReminder',
            components=[StudyReminderText, StudyReminderResp],
        )
        StudyReminder.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # create starting attributes for StudyReminderResp
        StudyReminderResp.keys = []
        StudyReminderResp.rt = []
        _StudyReminderResp_allKeys = []
        # store start times for StudyReminder
        StudyReminder.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        StudyReminder.tStart = globalClock.getTime(format='float')
        StudyReminder.status = STARTED
        thisExp.addData('StudyReminder.started', StudyReminder.tStart)
        StudyReminder.maxDuration = None
        # keep track of which components have finished
        StudyReminderComponents = StudyReminder.components
        for thisComponent in StudyReminder.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "StudyReminder" ---
        # if trial has changed, end Routine now
        if isinstance(BlockLoop, data.TrialHandler2) and thisBlockLoop.thisN != BlockLoop.thisTrial.thisN:
            continueRoutine = False
        StudyReminder.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *StudyReminderText* updates
            
            # if StudyReminderText is starting this frame...
            if StudyReminderText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                StudyReminderText.frameNStart = frameN  # exact frame index
                StudyReminderText.tStart = t  # local t and not account for scr refresh
                StudyReminderText.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(StudyReminderText, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'StudyReminderText.started')
                # update status
                StudyReminderText.status = STARTED
                StudyReminderText.setAutoDraw(True)
            
            # if StudyReminderText is active this frame...
            if StudyReminderText.status == STARTED:
                # update params
                pass
            
            # *StudyReminderResp* updates
            waitOnFlip = False
            
            # if StudyReminderResp is starting this frame...
            if StudyReminderResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                StudyReminderResp.frameNStart = frameN  # exact frame index
                StudyReminderResp.tStart = t  # local t and not account for scr refresh
                StudyReminderResp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(StudyReminderResp, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'StudyReminderResp.started')
                # update status
                StudyReminderResp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(StudyReminderResp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(StudyReminderResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if StudyReminderResp.status == STARTED and not waitOnFlip:
                theseKeys = StudyReminderResp.getKeys(keyList=['5'], ignoreKeys=["escape"], waitRelease=False)
                _StudyReminderResp_allKeys.extend(theseKeys)
                if len(_StudyReminderResp_allKeys):
                    StudyReminderResp.keys = _StudyReminderResp_allKeys[-1].name  # just the last key pressed
                    StudyReminderResp.rt = _StudyReminderResp_allKeys[-1].rt
                    StudyReminderResp.duration = _StudyReminderResp_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                StudyReminder.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in StudyReminder.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "StudyReminder" ---
        for thisComponent in StudyReminder.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for StudyReminder
        StudyReminder.tStop = globalClock.getTime(format='float')
        StudyReminder.tStopRefresh = tThisFlipGlobal
        thisExp.addData('StudyReminder.stopped', StudyReminder.tStop)
        # check responses
        if StudyReminderResp.keys in ['', [], None]:  # No response was made
            StudyReminderResp.keys = None
        BlockLoop.addData('StudyReminderResp.keys',StudyReminderResp.keys)
        if StudyReminderResp.keys != None:  # we had a response
            BlockLoop.addData('StudyReminderResp.rt', StudyReminderResp.rt)
            BlockLoop.addData('StudyReminderResp.duration', StudyReminderResp.duration)
        # the Routine "StudyReminder" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # set up handler to look after randomisation of conditions etc
        StudyLoop = data.TrialHandler2(
            name='StudyLoop',
            nReps=1.0, 
            method='sequential', 
            extraInfo=expInfo, 
            originPath=-1, 
            trialList=data.importConditions(csv_filename), 
            seed=None, 
        )
        thisExp.addLoop(StudyLoop)  # add the loop to the experiment
        thisStudyLoop = StudyLoop.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisStudyLoop.rgb)
        if thisStudyLoop != None:
            for paramName in thisStudyLoop:
                globals()[paramName] = thisStudyLoop[paramName]
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        
        for thisStudyLoop in StudyLoop:
            currentLoop = StudyLoop
            thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
            if thisSession is not None:
                # if running in a Session with a Liaison client, send data up to now
                thisSession.sendExperimentData()
            # abbreviate parameter names if possible (e.g. rgb = thisStudyLoop.rgb)
            if thisStudyLoop != None:
                for paramName in thisStudyLoop:
                    globals()[paramName] = thisStudyLoop[paramName]
            
            # --- Prepare to start Routine "StudyTrial" ---
            # create an object to store info about Routine StudyTrial
            StudyTrial = data.Routine(
                name='StudyTrial',
                components=[StudyTrialText, studyTrialImage, StudyTrialResp, StudyTrialOptions],
            )
            StudyTrial.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            StudyTrialText.setText(encoding_question)
            studyTrialImage.setImage(image_filename)
            # create starting attributes for StudyTrialResp
            StudyTrialResp.keys = []
            StudyTrialResp.rt = []
            _StudyTrialResp_allKeys = []
            # store start times for StudyTrial
            StudyTrial.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            StudyTrial.tStart = globalClock.getTime(format='float')
            StudyTrial.status = STARTED
            thisExp.addData('StudyTrial.started', StudyTrial.tStart)
            StudyTrial.maxDuration = None
            # keep track of which components have finished
            StudyTrialComponents = StudyTrial.components
            for thisComponent in StudyTrial.components:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "StudyTrial" ---
            # if trial has changed, end Routine now
            if isinstance(StudyLoop, data.TrialHandler2) and thisStudyLoop.thisN != StudyLoop.thisTrial.thisN:
                continueRoutine = False
            StudyTrial.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine and routineTimer.getTime() < 6.0:
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *StudyTrialText* updates
                
                # if StudyTrialText is starting this frame...
                if StudyTrialText.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
                    # keep track of start time/frame for later
                    StudyTrialText.frameNStart = frameN  # exact frame index
                    StudyTrialText.tStart = t  # local t and not account for scr refresh
                    StudyTrialText.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(StudyTrialText, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'StudyTrialText.started')
                    # update status
                    StudyTrialText.status = STARTED
                    StudyTrialText.setAutoDraw(True)
                
                # if StudyTrialText is active this frame...
                if StudyTrialText.status == STARTED:
                    # update params
                    pass
                
                # if StudyTrialText is stopping this frame...
                if StudyTrialText.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > StudyTrialText.tStartRefresh + 4-frameTolerance:
                        # keep track of stop time/frame for later
                        StudyTrialText.tStop = t  # not accounting for scr refresh
                        StudyTrialText.tStopRefresh = tThisFlipGlobal  # on global time
                        StudyTrialText.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'StudyTrialText.stopped')
                        # update status
                        StudyTrialText.status = FINISHED
                        StudyTrialText.setAutoDraw(False)
                
                # *studyTrialImage* updates
                
                # if studyTrialImage is starting this frame...
                if studyTrialImage.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    studyTrialImage.frameNStart = frameN  # exact frame index
                    studyTrialImage.tStart = t  # local t and not account for scr refresh
                    studyTrialImage.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(studyTrialImage, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'studyTrialImage.started')
                    # update status
                    studyTrialImage.status = STARTED
                    studyTrialImage.setAutoDraw(True)
                
                # if studyTrialImage is active this frame...
                if studyTrialImage.status == STARTED:
                    # update params
                    pass
                
                # if studyTrialImage is stopping this frame...
                if studyTrialImage.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > studyTrialImage.tStartRefresh + 6-frameTolerance:
                        # keep track of stop time/frame for later
                        studyTrialImage.tStop = t  # not accounting for scr refresh
                        studyTrialImage.tStopRefresh = tThisFlipGlobal  # on global time
                        studyTrialImage.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'studyTrialImage.stopped')
                        # update status
                        studyTrialImage.status = FINISHED
                        studyTrialImage.setAutoDraw(False)
                
                # *StudyTrialResp* updates
                waitOnFlip = False
                
                # if StudyTrialResp is starting this frame...
                if StudyTrialResp.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
                    # keep track of start time/frame for later
                    StudyTrialResp.frameNStart = frameN  # exact frame index
                    StudyTrialResp.tStart = t  # local t and not account for scr refresh
                    StudyTrialResp.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(StudyTrialResp, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'StudyTrialResp.started')
                    # update status
                    StudyTrialResp.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(StudyTrialResp.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(StudyTrialResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
                
                # if StudyTrialResp is stopping this frame...
                if StudyTrialResp.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > StudyTrialResp.tStartRefresh + 4-frameTolerance:
                        # keep track of stop time/frame for later
                        StudyTrialResp.tStop = t  # not accounting for scr refresh
                        StudyTrialResp.tStopRefresh = tThisFlipGlobal  # on global time
                        StudyTrialResp.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'StudyTrialResp.stopped')
                        # update status
                        StudyTrialResp.status = FINISHED
                        StudyTrialResp.status = FINISHED
                if StudyTrialResp.status == STARTED and not waitOnFlip:
                    theseKeys = StudyTrialResp.getKeys(keyList=['left','right'], ignoreKeys=["escape"], waitRelease=False)
                    _StudyTrialResp_allKeys.extend(theseKeys)
                    if len(_StudyTrialResp_allKeys):
                        StudyTrialResp.keys = _StudyTrialResp_allKeys[-1].name  # just the last key pressed
                        StudyTrialResp.rt = _StudyTrialResp_allKeys[-1].rt
                        StudyTrialResp.duration = _StudyTrialResp_allKeys[-1].duration
                
                # *StudyTrialOptions* updates
                
                # if StudyTrialOptions is starting this frame...
                if StudyTrialOptions.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
                    # keep track of start time/frame for later
                    StudyTrialOptions.frameNStart = frameN  # exact frame index
                    StudyTrialOptions.tStart = t  # local t and not account for scr refresh
                    StudyTrialOptions.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(StudyTrialOptions, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'StudyTrialOptions.started')
                    # update status
                    StudyTrialOptions.status = STARTED
                    StudyTrialOptions.setAutoDraw(True)
                
                # if StudyTrialOptions is active this frame...
                if StudyTrialOptions.status == STARTED:
                    # update params
                    pass
                
                # if StudyTrialOptions is stopping this frame...
                if StudyTrialOptions.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > StudyTrialOptions.tStartRefresh + 4-frameTolerance:
                        # keep track of stop time/frame for later
                        StudyTrialOptions.tStop = t  # not accounting for scr refresh
                        StudyTrialOptions.tStopRefresh = tThisFlipGlobal  # on global time
                        StudyTrialOptions.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'StudyTrialOptions.stopped')
                        # update status
                        StudyTrialOptions.status = FINISHED
                        StudyTrialOptions.setAutoDraw(False)
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, win=win)
                    return
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        win=win, 
                        timers=[routineTimer], 
                        playbackComponents=[]
                    )
                    # skip the frame we paused on
                    continue
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    StudyTrial.forceEnded = routineForceEnded = True
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in StudyTrial.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "StudyTrial" ---
            for thisComponent in StudyTrial.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for StudyTrial
            StudyTrial.tStop = globalClock.getTime(format='float')
            StudyTrial.tStopRefresh = tThisFlipGlobal
            thisExp.addData('StudyTrial.stopped', StudyTrial.tStop)
            # check responses
            if StudyTrialResp.keys in ['', [], None]:  # No response was made
                StudyTrialResp.keys = None
            StudyLoop.addData('StudyTrialResp.keys',StudyTrialResp.keys)
            if StudyTrialResp.keys != None:  # we had a response
                StudyLoop.addData('StudyTrialResp.rt', StudyTrialResp.rt)
                StudyLoop.addData('StudyTrialResp.duration', StudyTrialResp.duration)
            # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
            if StudyTrial.maxDurationReached:
                routineTimer.addTime(-StudyTrial.maxDuration)
            elif StudyTrial.forceEnded:
                routineTimer.reset()
            else:
                routineTimer.addTime(-6.000000)
            thisExp.nextEntry()
            
        # completed 1.0 repeats of 'StudyLoop'
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        
        # --- Prepare to start Routine "transition1" ---
        # create an object to store info about Routine transition1
        transition1 = data.Routine(
            name='transition1',
            components=[transition1Text],
        )
        transition1.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # store start times for transition1
        transition1.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        transition1.tStart = globalClock.getTime(format='float')
        transition1.status = STARTED
        thisExp.addData('transition1.started', transition1.tStart)
        transition1.maxDuration = None
        # keep track of which components have finished
        transition1Components = transition1.components
        for thisComponent in transition1.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "transition1" ---
        # if trial has changed, end Routine now
        if isinstance(BlockLoop, data.TrialHandler2) and thisBlockLoop.thisN != BlockLoop.thisTrial.thisN:
            continueRoutine = False
        transition1.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 4.0:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *transition1Text* updates
            
            # if transition1Text is starting this frame...
            if transition1Text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                transition1Text.frameNStart = frameN  # exact frame index
                transition1Text.tStart = t  # local t and not account for scr refresh
                transition1Text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(transition1Text, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'transition1Text.started')
                # update status
                transition1Text.status = STARTED
                transition1Text.setAutoDraw(True)
            
            # if transition1Text is active this frame...
            if transition1Text.status == STARTED:
                # update params
                pass
            
            # if transition1Text is stopping this frame...
            if transition1Text.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > transition1Text.tStartRefresh + 4-frameTolerance:
                    # keep track of stop time/frame for later
                    transition1Text.tStop = t  # not accounting for scr refresh
                    transition1Text.tStopRefresh = tThisFlipGlobal  # on global time
                    transition1Text.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'transition1Text.stopped')
                    # update status
                    transition1Text.status = FINISHED
                    transition1Text.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                transition1.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in transition1.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "transition1" ---
        for thisComponent in transition1.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for transition1
        transition1.tStop = globalClock.getTime(format='float')
        transition1.tStopRefresh = tThisFlipGlobal
        thisExp.addData('transition1.stopped', transition1.tStop)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if transition1.maxDurationReached:
            routineTimer.addTime(-transition1.maxDuration)
        elif transition1.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-4.000000)
        
        # --- Prepare to start Routine "timeEstimate" ---
        # create an object to store info about Routine timeEstimate
        timeEstimate = data.Routine(
            name='timeEstimate',
            components=[time_display, key_resp, timeEstimateInstructions, TimeEstimateConfirm, TimeEstimateTimerText],
        )
        timeEstimate.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from code_3
        minutes = 0
        seconds = 0
        focus = 'minutes'  # 'minutes' or 'seconds'
        time_str = f"{minutes:02d}:{seconds:02d}"
        
        # create starting attributes for key_resp
        key_resp.keys = []
        key_resp.rt = []
        _key_resp_allKeys = []
        # store start times for timeEstimate
        timeEstimate.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        timeEstimate.tStart = globalClock.getTime(format='float')
        timeEstimate.status = STARTED
        thisExp.addData('timeEstimate.started', timeEstimate.tStart)
        timeEstimate.maxDuration = None
        # keep track of which components have finished
        timeEstimateComponents = timeEstimate.components
        for thisComponent in timeEstimate.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "timeEstimate" ---
        # if trial has changed, end Routine now
        if isinstance(BlockLoop, data.TrialHandler2) and thisBlockLoop.thisN != BlockLoop.thisTrial.thisN:
            continueRoutine = False
        timeEstimate.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *time_display* updates
            
            # if time_display is starting this frame...
            if time_display.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                time_display.frameNStart = frameN  # exact frame index
                time_display.tStart = t  # local t and not account for scr refresh
                time_display.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(time_display, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'time_display.started')
                # update status
                time_display.status = STARTED
                time_display.setAutoDraw(True)
            
            # if time_display is active this frame...
            if time_display.status == STARTED:
                # update params
                time_display.setText(time_str, log=False)
            # Run 'Each Frame' code from code_3
            keys = event.getKeys()
            
            for key in keys:
                if key == 'left':
                    focus = 'minutes'
                elif key == 'right':
                    focus = 'seconds'
                elif key == 'up':
                    if focus == 'minutes':
                        minutes = (minutes + 1) % 60  
                    elif focus == 'seconds':
                        seconds = (seconds + 1) % 60
                elif key == 'down':
                    if focus == 'minutes':
                        minutes = (minutes - 1) % 60
                    elif focus == 'seconds':
                        seconds = (seconds - 1) % 60
                elif key == 'return':
                    continueRoutine = False  # finish routine
            
            # Update display text
            if focus == 'minutes':
                time_str = f"[{minutes:02d}]:{seconds:02d}"
            else:
                time_str = f"{minutes:02d}:[{seconds:02d}]"
            
            
            # *key_resp* updates
            waitOnFlip = False
            
            # if key_resp is starting this frame...
            if key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                key_resp.frameNStart = frameN  # exact frame index
                key_resp.tStart = t  # local t and not account for scr refresh
                key_resp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_resp.started')
                # update status
                key_resp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if key_resp.status == STARTED and not waitOnFlip:
                theseKeys = key_resp.getKeys(keyList=['up','down','left','right','return'], ignoreKeys=["escape"], waitRelease=False)
                _key_resp_allKeys.extend(theseKeys)
                if len(_key_resp_allKeys):
                    key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                    key_resp.rt = _key_resp_allKeys[-1].rt
                    key_resp.duration = _key_resp_allKeys[-1].duration
            
            # *timeEstimateInstructions* updates
            
            # if timeEstimateInstructions is starting this frame...
            if timeEstimateInstructions.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                timeEstimateInstructions.frameNStart = frameN  # exact frame index
                timeEstimateInstructions.tStart = t  # local t and not account for scr refresh
                timeEstimateInstructions.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(timeEstimateInstructions, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'timeEstimateInstructions.started')
                # update status
                timeEstimateInstructions.status = STARTED
                timeEstimateInstructions.setAutoDraw(True)
            
            # if timeEstimateInstructions is active this frame...
            if timeEstimateInstructions.status == STARTED:
                # update params
                pass
            
            # *TimeEstimateConfirm* updates
            
            # if TimeEstimateConfirm is starting this frame...
            if TimeEstimateConfirm.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                TimeEstimateConfirm.frameNStart = frameN  # exact frame index
                TimeEstimateConfirm.tStart = t  # local t and not account for scr refresh
                TimeEstimateConfirm.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(TimeEstimateConfirm, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'TimeEstimateConfirm.started')
                # update status
                TimeEstimateConfirm.status = STARTED
                TimeEstimateConfirm.setAutoDraw(True)
            
            # if TimeEstimateConfirm is active this frame...
            if TimeEstimateConfirm.status == STARTED:
                # update params
                pass
            
            # *TimeEstimateTimerText* updates
            
            # if TimeEstimateTimerText is starting this frame...
            if TimeEstimateTimerText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                TimeEstimateTimerText.frameNStart = frameN  # exact frame index
                TimeEstimateTimerText.tStart = t  # local t and not account for scr refresh
                TimeEstimateTimerText.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(TimeEstimateTimerText, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'TimeEstimateTimerText.started')
                # update status
                TimeEstimateTimerText.status = STARTED
                TimeEstimateTimerText.setAutoDraw(True)
            
            # if TimeEstimateTimerText is active this frame...
            if TimeEstimateTimerText.status == STARTED:
                # update params
                pass
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                timeEstimate.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in timeEstimate.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "timeEstimate" ---
        for thisComponent in timeEstimate.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for timeEstimate
        timeEstimate.tStop = globalClock.getTime(format='float')
        timeEstimate.tStopRefresh = tThisFlipGlobal
        thisExp.addData('timeEstimate.stopped', timeEstimate.tStop)
        # Run 'End Routine' code from code_3
        #Save data
        thisExp.addData('estimated_minutes', minutes)
        thisExp.addData('estimated_seconds', seconds)
        
        # check responses
        if key_resp.keys in ['', [], None]:  # No response was made
            key_resp.keys = None
        BlockLoop.addData('key_resp.keys',key_resp.keys)
        if key_resp.keys != None:  # we had a response
            BlockLoop.addData('key_resp.rt', key_resp.rt)
            BlockLoop.addData('key_resp.duration', key_resp.duration)
        # the Routine "timeEstimate" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "transition2" ---
        # create an object to store info about Routine transition2
        transition2 = data.Routine(
            name='transition2',
            components=[Transition2Text],
        )
        transition2.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # store start times for transition2
        transition2.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        transition2.tStart = globalClock.getTime(format='float')
        transition2.status = STARTED
        thisExp.addData('transition2.started', transition2.tStart)
        transition2.maxDuration = None
        # keep track of which components have finished
        transition2Components = transition2.components
        for thisComponent in transition2.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "transition2" ---
        # if trial has changed, end Routine now
        if isinstance(BlockLoop, data.TrialHandler2) and thisBlockLoop.thisN != BlockLoop.thisTrial.thisN:
            continueRoutine = False
        transition2.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 4.0:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Transition2Text* updates
            
            # if Transition2Text is starting this frame...
            if Transition2Text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Transition2Text.frameNStart = frameN  # exact frame index
                Transition2Text.tStart = t  # local t and not account for scr refresh
                Transition2Text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Transition2Text, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Transition2Text.started')
                # update status
                Transition2Text.status = STARTED
                Transition2Text.setAutoDraw(True)
            
            # if Transition2Text is active this frame...
            if Transition2Text.status == STARTED:
                # update params
                pass
            
            # if Transition2Text is stopping this frame...
            if Transition2Text.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > Transition2Text.tStartRefresh + 4-frameTolerance:
                    # keep track of stop time/frame for later
                    Transition2Text.tStop = t  # not accounting for scr refresh
                    Transition2Text.tStopRefresh = tThisFlipGlobal  # on global time
                    Transition2Text.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'Transition2Text.stopped')
                    # update status
                    Transition2Text.status = FINISHED
                    Transition2Text.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                transition2.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in transition2.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "transition2" ---
        for thisComponent in transition2.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for transition2
        transition2.tStop = globalClock.getTime(format='float')
        transition2.tStopRefresh = tThisFlipGlobal
        thisExp.addData('transition2.stopped', transition2.tStop)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if transition2.maxDurationReached:
            routineTimer.addTime(-transition2.maxDuration)
        elif transition2.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-4.000000)
        
        # --- Prepare to start Routine "DistractorReminder" ---
        # create an object to store info about Routine DistractorReminder
        DistractorReminder = data.Routine(
            name='DistractorReminder',
            components=[DistractorReminderText, DistractorReminderResp],
        )
        DistractorReminder.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # create starting attributes for DistractorReminderResp
        DistractorReminderResp.keys = []
        DistractorReminderResp.rt = []
        _DistractorReminderResp_allKeys = []
        # store start times for DistractorReminder
        DistractorReminder.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        DistractorReminder.tStart = globalClock.getTime(format='float')
        DistractorReminder.status = STARTED
        thisExp.addData('DistractorReminder.started', DistractorReminder.tStart)
        DistractorReminder.maxDuration = None
        # keep track of which components have finished
        DistractorReminderComponents = DistractorReminder.components
        for thisComponent in DistractorReminder.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "DistractorReminder" ---
        # if trial has changed, end Routine now
        if isinstance(BlockLoop, data.TrialHandler2) and thisBlockLoop.thisN != BlockLoop.thisTrial.thisN:
            continueRoutine = False
        DistractorReminder.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *DistractorReminderText* updates
            
            # if DistractorReminderText is starting this frame...
            if DistractorReminderText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                DistractorReminderText.frameNStart = frameN  # exact frame index
                DistractorReminderText.tStart = t  # local t and not account for scr refresh
                DistractorReminderText.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(DistractorReminderText, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'DistractorReminderText.started')
                # update status
                DistractorReminderText.status = STARTED
                DistractorReminderText.setAutoDraw(True)
            
            # if DistractorReminderText is active this frame...
            if DistractorReminderText.status == STARTED:
                # update params
                pass
            
            # *DistractorReminderResp* updates
            waitOnFlip = False
            
            # if DistractorReminderResp is starting this frame...
            if DistractorReminderResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                DistractorReminderResp.frameNStart = frameN  # exact frame index
                DistractorReminderResp.tStart = t  # local t and not account for scr refresh
                DistractorReminderResp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(DistractorReminderResp, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'DistractorReminderResp.started')
                # update status
                DistractorReminderResp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(DistractorReminderResp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(DistractorReminderResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if DistractorReminderResp.status == STARTED and not waitOnFlip:
                theseKeys = DistractorReminderResp.getKeys(keyList=['5'], ignoreKeys=["escape"], waitRelease=False)
                _DistractorReminderResp_allKeys.extend(theseKeys)
                if len(_DistractorReminderResp_allKeys):
                    DistractorReminderResp.keys = _DistractorReminderResp_allKeys[-1].name  # just the last key pressed
                    DistractorReminderResp.rt = _DistractorReminderResp_allKeys[-1].rt
                    DistractorReminderResp.duration = _DistractorReminderResp_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                DistractorReminder.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in DistractorReminder.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "DistractorReminder" ---
        for thisComponent in DistractorReminder.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for DistractorReminder
        DistractorReminder.tStop = globalClock.getTime(format='float')
        DistractorReminder.tStopRefresh = tThisFlipGlobal
        thisExp.addData('DistractorReminder.stopped', DistractorReminder.tStop)
        # check responses
        if DistractorReminderResp.keys in ['', [], None]:  # No response was made
            DistractorReminderResp.keys = None
        BlockLoop.addData('DistractorReminderResp.keys',DistractorReminderResp.keys)
        if DistractorReminderResp.keys != None:  # we had a response
            BlockLoop.addData('DistractorReminderResp.rt', DistractorReminderResp.rt)
            BlockLoop.addData('DistractorReminderResp.duration', DistractorReminderResp.duration)
        # the Routine "DistractorReminder" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "distractor_start" ---
        # create an object to store info about Routine distractor_start
        distractor_start = data.Routine(
            name='distractor_start',
            components=[],
        )
        distractor_start.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from code_5
        distractor_start_time = globalClock.getTime()
        # store start times for distractor_start
        distractor_start.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        distractor_start.tStart = globalClock.getTime(format='float')
        distractor_start.status = STARTED
        thisExp.addData('distractor_start.started', distractor_start.tStart)
        distractor_start.maxDuration = None
        # keep track of which components have finished
        distractor_startComponents = distractor_start.components
        for thisComponent in distractor_start.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "distractor_start" ---
        # if trial has changed, end Routine now
        if isinstance(BlockLoop, data.TrialHandler2) and thisBlockLoop.thisN != BlockLoop.thisTrial.thisN:
            continueRoutine = False
        distractor_start.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                distractor_start.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in distractor_start.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "distractor_start" ---
        for thisComponent in distractor_start.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for distractor_start
        distractor_start.tStop = globalClock.getTime(format='float')
        distractor_start.tStopRefresh = tThisFlipGlobal
        thisExp.addData('distractor_start.stopped', distractor_start.tStop)
        # the Routine "distractor_start" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # set up handler to look after randomisation of conditions etc
        DistractorLoop = data.TrialHandler2(
            name='DistractorLoop',
            nReps=1000.0, 
            method='sequential', 
            extraInfo=expInfo, 
            originPath=-1, 
            trialList=[None], 
            seed=None, 
        )
        thisExp.addLoop(DistractorLoop)  # add the loop to the experiment
        thisDistractorLoop = DistractorLoop.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisDistractorLoop.rgb)
        if thisDistractorLoop != None:
            for paramName in thisDistractorLoop:
                globals()[paramName] = thisDistractorLoop[paramName]
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        
        for thisDistractorLoop in DistractorLoop:
            currentLoop = DistractorLoop
            thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
            if thisSession is not None:
                # if running in a Session with a Liaison client, send data up to now
                thisSession.sendExperimentData()
            # abbreviate parameter names if possible (e.g. rgb = thisDistractorLoop.rgb)
            if thisDistractorLoop != None:
                for paramName in thisDistractorLoop:
                    globals()[paramName] = thisDistractorLoop[paramName]
            
            # --- Prepare to start Routine "Distractor" ---
            # create an object to store info about Routine Distractor
            Distractor = data.Routine(
                name='Distractor',
                components=[numberText, DistractorResp, DistractorOptions],
            )
            Distractor.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            # Run 'Begin Routine' code from code_4
            # Generate random numbers 
            current_number = random.randint(1, 99)
            numberText.setText(current_number)
            # create starting attributes for DistractorResp
            DistractorResp.keys = []
            DistractorResp.rt = []
            _DistractorResp_allKeys = []
            # store start times for Distractor
            Distractor.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            Distractor.tStart = globalClock.getTime(format='float')
            Distractor.status = STARTED
            thisExp.addData('Distractor.started', Distractor.tStart)
            Distractor.maxDuration = None
            # keep track of which components have finished
            DistractorComponents = Distractor.components
            for thisComponent in Distractor.components:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "Distractor" ---
            # if trial has changed, end Routine now
            if isinstance(DistractorLoop, data.TrialHandler2) and thisDistractorLoop.thisN != DistractorLoop.thisTrial.thisN:
                continueRoutine = False
            Distractor.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine and routineTimer.getTime() < 2.0:
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                # Run 'Each Frame' code from code_4
                # Run for xx seconds
                if globalClock.getTime() - distractor_start_time > 30: 
                    continueRoutine = False 
                
                # *numberText* updates
                
                # if numberText is starting this frame...
                if numberText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    numberText.frameNStart = frameN  # exact frame index
                    numberText.tStart = t  # local t and not account for scr refresh
                    numberText.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(numberText, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'numberText.started')
                    # update status
                    numberText.status = STARTED
                    numberText.setAutoDraw(True)
                
                # if numberText is active this frame...
                if numberText.status == STARTED:
                    # update params
                    pass
                
                # if numberText is stopping this frame...
                if numberText.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > numberText.tStartRefresh + 2-frameTolerance:
                        # keep track of stop time/frame for later
                        numberText.tStop = t  # not accounting for scr refresh
                        numberText.tStopRefresh = tThisFlipGlobal  # on global time
                        numberText.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'numberText.stopped')
                        # update status
                        numberText.status = FINISHED
                        numberText.setAutoDraw(False)
                
                # *DistractorResp* updates
                waitOnFlip = False
                
                # if DistractorResp is starting this frame...
                if DistractorResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    DistractorResp.frameNStart = frameN  # exact frame index
                    DistractorResp.tStart = t  # local t and not account for scr refresh
                    DistractorResp.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(DistractorResp, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'DistractorResp.started')
                    # update status
                    DistractorResp.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(DistractorResp.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(DistractorResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
                
                # if DistractorResp is stopping this frame...
                if DistractorResp.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > DistractorResp.tStartRefresh + 2-frameTolerance:
                        # keep track of stop time/frame for later
                        DistractorResp.tStop = t  # not accounting for scr refresh
                        DistractorResp.tStopRefresh = tThisFlipGlobal  # on global time
                        DistractorResp.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'DistractorResp.stopped')
                        # update status
                        DistractorResp.status = FINISHED
                        DistractorResp.status = FINISHED
                if DistractorResp.status == STARTED and not waitOnFlip:
                    theseKeys = DistractorResp.getKeys(keyList=['left','right'], ignoreKeys=["escape"], waitRelease=False)
                    _DistractorResp_allKeys.extend(theseKeys)
                    if len(_DistractorResp_allKeys):
                        DistractorResp.keys = _DistractorResp_allKeys[-1].name  # just the last key pressed
                        DistractorResp.rt = _DistractorResp_allKeys[-1].rt
                        DistractorResp.duration = _DistractorResp_allKeys[-1].duration
                        # a response ends the routine
                        continueRoutine = False
                
                # *DistractorOptions* updates
                
                # if DistractorOptions is starting this frame...
                if DistractorOptions.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    DistractorOptions.frameNStart = frameN  # exact frame index
                    DistractorOptions.tStart = t  # local t and not account for scr refresh
                    DistractorOptions.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(DistractorOptions, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'DistractorOptions.started')
                    # update status
                    DistractorOptions.status = STARTED
                    DistractorOptions.setAutoDraw(True)
                
                # if DistractorOptions is active this frame...
                if DistractorOptions.status == STARTED:
                    # update params
                    pass
                
                # if DistractorOptions is stopping this frame...
                if DistractorOptions.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > DistractorOptions.tStartRefresh + 2-frameTolerance:
                        # keep track of stop time/frame for later
                        DistractorOptions.tStop = t  # not accounting for scr refresh
                        DistractorOptions.tStopRefresh = tThisFlipGlobal  # on global time
                        DistractorOptions.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'DistractorOptions.stopped')
                        # update status
                        DistractorOptions.status = FINISHED
                        DistractorOptions.setAutoDraw(False)
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, win=win)
                    return
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        win=win, 
                        timers=[routineTimer], 
                        playbackComponents=[]
                    )
                    # skip the frame we paused on
                    continue
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    Distractor.forceEnded = routineForceEnded = True
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in Distractor.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "Distractor" ---
            for thisComponent in Distractor.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for Distractor
            Distractor.tStop = globalClock.getTime(format='float')
            Distractor.tStopRefresh = tThisFlipGlobal
            thisExp.addData('Distractor.stopped', Distractor.tStop)
            # check responses
            if DistractorResp.keys in ['', [], None]:  # No response was made
                DistractorResp.keys = None
            DistractorLoop.addData('DistractorResp.keys',DistractorResp.keys)
            if DistractorResp.keys != None:  # we had a response
                DistractorLoop.addData('DistractorResp.rt', DistractorResp.rt)
                DistractorLoop.addData('DistractorResp.duration', DistractorResp.duration)
            # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
            if Distractor.maxDurationReached:
                routineTimer.addTime(-Distractor.maxDuration)
            elif Distractor.forceEnded:
                routineTimer.reset()
            else:
                routineTimer.addTime(-2.000000)
            thisExp.nextEntry()
            
        # completed 1000.0 repeats of 'DistractorLoop'
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        
        # --- Prepare to start Routine "transition3" ---
        # create an object to store info about Routine transition3
        transition3 = data.Routine(
            name='transition3',
            components=[transition3Text],
        )
        transition3.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # store start times for transition3
        transition3.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        transition3.tStart = globalClock.getTime(format='float')
        transition3.status = STARTED
        thisExp.addData('transition3.started', transition3.tStart)
        transition3.maxDuration = None
        # keep track of which components have finished
        transition3Components = transition3.components
        for thisComponent in transition3.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "transition3" ---
        # if trial has changed, end Routine now
        if isinstance(BlockLoop, data.TrialHandler2) and thisBlockLoop.thisN != BlockLoop.thisTrial.thisN:
            continueRoutine = False
        transition3.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 4.0:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *transition3Text* updates
            
            # if transition3Text is starting this frame...
            if transition3Text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                transition3Text.frameNStart = frameN  # exact frame index
                transition3Text.tStart = t  # local t and not account for scr refresh
                transition3Text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(transition3Text, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'transition3Text.started')
                # update status
                transition3Text.status = STARTED
                transition3Text.setAutoDraw(True)
            
            # if transition3Text is active this frame...
            if transition3Text.status == STARTED:
                # update params
                pass
            
            # if transition3Text is stopping this frame...
            if transition3Text.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > transition3Text.tStartRefresh + 4-frameTolerance:
                    # keep track of stop time/frame for later
                    transition3Text.tStop = t  # not accounting for scr refresh
                    transition3Text.tStopRefresh = tThisFlipGlobal  # on global time
                    transition3Text.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'transition3Text.stopped')
                    # update status
                    transition3Text.status = FINISHED
                    transition3Text.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                transition3.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in transition3.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "transition3" ---
        for thisComponent in transition3.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for transition3
        transition3.tStop = globalClock.getTime(format='float')
        transition3.tStopRefresh = tThisFlipGlobal
        thisExp.addData('transition3.stopped', transition3.tStop)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if transition3.maxDurationReached:
            routineTimer.addTime(-transition3.maxDuration)
        elif transition3.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-4.000000)
        
        # --- Prepare to start Routine "TestReminder" ---
        # create an object to store info about Routine TestReminder
        TestReminder = data.Routine(
            name='TestReminder',
            components=[TestReminderText, TestReminderResp],
        )
        TestReminder.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # create starting attributes for TestReminderResp
        TestReminderResp.keys = []
        TestReminderResp.rt = []
        _TestReminderResp_allKeys = []
        # store start times for TestReminder
        TestReminder.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        TestReminder.tStart = globalClock.getTime(format='float')
        TestReminder.status = STARTED
        thisExp.addData('TestReminder.started', TestReminder.tStart)
        TestReminder.maxDuration = None
        # keep track of which components have finished
        TestReminderComponents = TestReminder.components
        for thisComponent in TestReminder.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "TestReminder" ---
        # if trial has changed, end Routine now
        if isinstance(BlockLoop, data.TrialHandler2) and thisBlockLoop.thisN != BlockLoop.thisTrial.thisN:
            continueRoutine = False
        TestReminder.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *TestReminderText* updates
            
            # if TestReminderText is starting this frame...
            if TestReminderText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                TestReminderText.frameNStart = frameN  # exact frame index
                TestReminderText.tStart = t  # local t and not account for scr refresh
                TestReminderText.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(TestReminderText, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'TestReminderText.started')
                # update status
                TestReminderText.status = STARTED
                TestReminderText.setAutoDraw(True)
            
            # if TestReminderText is active this frame...
            if TestReminderText.status == STARTED:
                # update params
                pass
            
            # *TestReminderResp* updates
            waitOnFlip = False
            
            # if TestReminderResp is starting this frame...
            if TestReminderResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                TestReminderResp.frameNStart = frameN  # exact frame index
                TestReminderResp.tStart = t  # local t and not account for scr refresh
                TestReminderResp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(TestReminderResp, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'TestReminderResp.started')
                # update status
                TestReminderResp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(TestReminderResp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(TestReminderResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if TestReminderResp.status == STARTED and not waitOnFlip:
                theseKeys = TestReminderResp.getKeys(keyList=['5'], ignoreKeys=["escape"], waitRelease=False)
                _TestReminderResp_allKeys.extend(theseKeys)
                if len(_TestReminderResp_allKeys):
                    TestReminderResp.keys = _TestReminderResp_allKeys[-1].name  # just the last key pressed
                    TestReminderResp.rt = _TestReminderResp_allKeys[-1].rt
                    TestReminderResp.duration = _TestReminderResp_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                TestReminder.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in TestReminder.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "TestReminder" ---
        for thisComponent in TestReminder.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for TestReminder
        TestReminder.tStop = globalClock.getTime(format='float')
        TestReminder.tStopRefresh = tThisFlipGlobal
        thisExp.addData('TestReminder.stopped', TestReminder.tStop)
        # check responses
        if TestReminderResp.keys in ['', [], None]:  # No response was made
            TestReminderResp.keys = None
        BlockLoop.addData('TestReminderResp.keys',TestReminderResp.keys)
        if TestReminderResp.keys != None:  # we had a response
            BlockLoop.addData('TestReminderResp.rt', TestReminderResp.rt)
            BlockLoop.addData('TestReminderResp.duration', TestReminderResp.duration)
        # the Routine "TestReminder" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # set up handler to look after randomisation of conditions etc
        TestLoop = data.TrialHandler2(
            name='TestLoop',
            nReps=1.0, 
            method='sequential', 
            extraInfo=expInfo, 
            originPath=-1, 
            trialList=data.importConditions(test_file), 
            seed=None, 
        )
        thisExp.addLoop(TestLoop)  # add the loop to the experiment
        thisTestLoop = TestLoop.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisTestLoop.rgb)
        if thisTestLoop != None:
            for paramName in thisTestLoop:
                globals()[paramName] = thisTestLoop[paramName]
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        
        for thisTestLoop in TestLoop:
            currentLoop = TestLoop
            thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
            if thisSession is not None:
                # if running in a Session with a Liaison client, send data up to now
                thisSession.sendExperimentData()
            # abbreviate parameter names if possible (e.g. rgb = thisTestLoop.rgb)
            if thisTestLoop != None:
                for paramName in thisTestLoop:
                    globals()[paramName] = thisTestLoop[paramName]
            
            # --- Prepare to start Routine "TestTrial" ---
            # create an object to store info about Routine TestTrial
            TestTrial = data.Routine(
                name='TestTrial',
                components=[leftImg, rightImg, TestResp, TestOptions, TestQuestionPrompt],
            )
            TestTrial.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            leftImg.setImage(left_image)
            rightImg.setImage(right_image)
            # create starting attributes for TestResp
            TestResp.keys = []
            TestResp.rt = []
            _TestResp_allKeys = []
            # store start times for TestTrial
            TestTrial.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            TestTrial.tStart = globalClock.getTime(format='float')
            TestTrial.status = STARTED
            thisExp.addData('TestTrial.started', TestTrial.tStart)
            TestTrial.maxDuration = None
            # keep track of which components have finished
            TestTrialComponents = TestTrial.components
            for thisComponent in TestTrial.components:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "TestTrial" ---
            # if trial has changed, end Routine now
            if isinstance(TestLoop, data.TrialHandler2) and thisTestLoop.thisN != TestLoop.thisTrial.thisN:
                continueRoutine = False
            TestTrial.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine and routineTimer.getTime() < 8.0:
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *leftImg* updates
                
                # if leftImg is starting this frame...
                if leftImg.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    leftImg.frameNStart = frameN  # exact frame index
                    leftImg.tStart = t  # local t and not account for scr refresh
                    leftImg.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(leftImg, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'leftImg.started')
                    # update status
                    leftImg.status = STARTED
                    leftImg.setAutoDraw(True)
                
                # if leftImg is active this frame...
                if leftImg.status == STARTED:
                    # update params
                    pass
                
                # if leftImg is stopping this frame...
                if leftImg.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > leftImg.tStartRefresh + 8-frameTolerance:
                        # keep track of stop time/frame for later
                        leftImg.tStop = t  # not accounting for scr refresh
                        leftImg.tStopRefresh = tThisFlipGlobal  # on global time
                        leftImg.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'leftImg.stopped')
                        # update status
                        leftImg.status = FINISHED
                        leftImg.setAutoDraw(False)
                
                # *rightImg* updates
                
                # if rightImg is starting this frame...
                if rightImg.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    rightImg.frameNStart = frameN  # exact frame index
                    rightImg.tStart = t  # local t and not account for scr refresh
                    rightImg.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(rightImg, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'rightImg.started')
                    # update status
                    rightImg.status = STARTED
                    rightImg.setAutoDraw(True)
                
                # if rightImg is active this frame...
                if rightImg.status == STARTED:
                    # update params
                    pass
                
                # if rightImg is stopping this frame...
                if rightImg.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > rightImg.tStartRefresh + 8-frameTolerance:
                        # keep track of stop time/frame for later
                        rightImg.tStop = t  # not accounting for scr refresh
                        rightImg.tStopRefresh = tThisFlipGlobal  # on global time
                        rightImg.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'rightImg.stopped')
                        # update status
                        rightImg.status = FINISHED
                        rightImg.setAutoDraw(False)
                
                # *TestResp* updates
                waitOnFlip = False
                
                # if TestResp is starting this frame...
                if TestResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    TestResp.frameNStart = frameN  # exact frame index
                    TestResp.tStart = t  # local t and not account for scr refresh
                    TestResp.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(TestResp, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'TestResp.started')
                    # update status
                    TestResp.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(TestResp.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(TestResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
                
                # if TestResp is stopping this frame...
                if TestResp.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > TestResp.tStartRefresh + 8-frameTolerance:
                        # keep track of stop time/frame for later
                        TestResp.tStop = t  # not accounting for scr refresh
                        TestResp.tStopRefresh = tThisFlipGlobal  # on global time
                        TestResp.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'TestResp.stopped')
                        # update status
                        TestResp.status = FINISHED
                        TestResp.status = FINISHED
                if TestResp.status == STARTED and not waitOnFlip:
                    theseKeys = TestResp.getKeys(keyList=['left','right'], ignoreKeys=["escape"], waitRelease=False)
                    _TestResp_allKeys.extend(theseKeys)
                    if len(_TestResp_allKeys):
                        TestResp.keys = _TestResp_allKeys[-1].name  # just the last key pressed
                        TestResp.rt = _TestResp_allKeys[-1].rt
                        TestResp.duration = _TestResp_allKeys[-1].duration
                        # was this correct?
                        if (TestResp.keys == str(correct_answer)) or (TestResp.keys == correct_answer):
                            TestResp.corr = 1
                        else:
                            TestResp.corr = 0
                        # a response ends the routine
                        continueRoutine = False
                
                # *TestOptions* updates
                
                # if TestOptions is starting this frame...
                if TestOptions.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    TestOptions.frameNStart = frameN  # exact frame index
                    TestOptions.tStart = t  # local t and not account for scr refresh
                    TestOptions.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(TestOptions, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'TestOptions.started')
                    # update status
                    TestOptions.status = STARTED
                    TestOptions.setAutoDraw(True)
                
                # if TestOptions is active this frame...
                if TestOptions.status == STARTED:
                    # update params
                    pass
                
                # if TestOptions is stopping this frame...
                if TestOptions.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > TestOptions.tStartRefresh + 8-frameTolerance:
                        # keep track of stop time/frame for later
                        TestOptions.tStop = t  # not accounting for scr refresh
                        TestOptions.tStopRefresh = tThisFlipGlobal  # on global time
                        TestOptions.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'TestOptions.stopped')
                        # update status
                        TestOptions.status = FINISHED
                        TestOptions.setAutoDraw(False)
                
                # *TestQuestionPrompt* updates
                
                # if TestQuestionPrompt is starting this frame...
                if TestQuestionPrompt.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    TestQuestionPrompt.frameNStart = frameN  # exact frame index
                    TestQuestionPrompt.tStart = t  # local t and not account for scr refresh
                    TestQuestionPrompt.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(TestQuestionPrompt, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'TestQuestionPrompt.started')
                    # update status
                    TestQuestionPrompt.status = STARTED
                    TestQuestionPrompt.setAutoDraw(True)
                
                # if TestQuestionPrompt is active this frame...
                if TestQuestionPrompt.status == STARTED:
                    # update params
                    pass
                
                # if TestQuestionPrompt is stopping this frame...
                if TestQuestionPrompt.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > TestQuestionPrompt.tStartRefresh + 8-frameTolerance:
                        # keep track of stop time/frame for later
                        TestQuestionPrompt.tStop = t  # not accounting for scr refresh
                        TestQuestionPrompt.tStopRefresh = tThisFlipGlobal  # on global time
                        TestQuestionPrompt.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'TestQuestionPrompt.stopped')
                        # update status
                        TestQuestionPrompt.status = FINISHED
                        TestQuestionPrompt.setAutoDraw(False)
                
                # check for quit (typically the Esc key)
                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thisExp.status = FINISHED
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, win=win)
                    return
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        win=win, 
                        timers=[routineTimer], 
                        playbackComponents=[]
                    )
                    # skip the frame we paused on
                    continue
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    TestTrial.forceEnded = routineForceEnded = True
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in TestTrial.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "TestTrial" ---
            for thisComponent in TestTrial.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for TestTrial
            TestTrial.tStop = globalClock.getTime(format='float')
            TestTrial.tStopRefresh = tThisFlipGlobal
            thisExp.addData('TestTrial.stopped', TestTrial.tStop)
            # check responses
            if TestResp.keys in ['', [], None]:  # No response was made
                TestResp.keys = None
                # was no response the correct answer?!
                if str(correct_answer).lower() == 'none':
                   TestResp.corr = 1;  # correct non-response
                else:
                   TestResp.corr = 0;  # failed to respond (incorrectly)
            # store data for TestLoop (TrialHandler)
            TestLoop.addData('TestResp.keys',TestResp.keys)
            TestLoop.addData('TestResp.corr', TestResp.corr)
            if TestResp.keys != None:  # we had a response
                TestLoop.addData('TestResp.rt', TestResp.rt)
                TestLoop.addData('TestResp.duration', TestResp.duration)
            # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
            if TestTrial.maxDurationReached:
                routineTimer.addTime(-TestTrial.maxDuration)
            elif TestTrial.forceEnded:
                routineTimer.reset()
            else:
                routineTimer.addTime(-8.000000)
            thisExp.nextEntry()
            
        # completed 1.0 repeats of 'TestLoop'
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        
        # --- Prepare to start Routine "block_end" ---
        # create an object to store info about Routine block_end
        block_end = data.Routine(
            name='block_end',
            components=[blockendText],
        )
        block_end.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # store start times for block_end
        block_end.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        block_end.tStart = globalClock.getTime(format='float')
        block_end.status = STARTED
        thisExp.addData('block_end.started', block_end.tStart)
        block_end.maxDuration = None
        # keep track of which components have finished
        block_endComponents = block_end.components
        for thisComponent in block_end.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "block_end" ---
        # if trial has changed, end Routine now
        if isinstance(BlockLoop, data.TrialHandler2) and thisBlockLoop.thisN != BlockLoop.thisTrial.thisN:
            continueRoutine = False
        block_end.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 4.0:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *blockendText* updates
            
            # if blockendText is starting this frame...
            if blockendText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                blockendText.frameNStart = frameN  # exact frame index
                blockendText.tStart = t  # local t and not account for scr refresh
                blockendText.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blockendText, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blockendText.started')
                # update status
                blockendText.status = STARTED
                blockendText.setAutoDraw(True)
            
            # if blockendText is active this frame...
            if blockendText.status == STARTED:
                # update params
                pass
            
            # if blockendText is stopping this frame...
            if blockendText.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > blockendText.tStartRefresh + 4-frameTolerance:
                    # keep track of stop time/frame for later
                    blockendText.tStop = t  # not accounting for scr refresh
                    blockendText.tStopRefresh = tThisFlipGlobal  # on global time
                    blockendText.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'blockendText.stopped')
                    # update status
                    blockendText.status = FINISHED
                    blockendText.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                block_end.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in block_end.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "block_end" ---
        for thisComponent in block_end.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for block_end
        block_end.tStop = globalClock.getTime(format='float')
        block_end.tStopRefresh = tThisFlipGlobal
        thisExp.addData('block_end.stopped', block_end.tStop)
        # Run 'End Routine' code from code_7
        block_num += 1
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if block_end.maxDurationReached:
            routineTimer.addTime(-block_end.maxDuration)
        elif block_end.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-4.000000)
        thisExp.nextEntry()
        
    # completed 1.0 repeats of 'BlockLoop'
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "goodbye" ---
    # create an object to store info about Routine goodbye
    goodbye = data.Routine(
        name='goodbye',
        components=[GoodbyeText, GoodbyeResp],
    )
    goodbye.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for GoodbyeResp
    GoodbyeResp.keys = []
    GoodbyeResp.rt = []
    _GoodbyeResp_allKeys = []
    # store start times for goodbye
    goodbye.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    goodbye.tStart = globalClock.getTime(format='float')
    goodbye.status = STARTED
    thisExp.addData('goodbye.started', goodbye.tStart)
    goodbye.maxDuration = None
    # keep track of which components have finished
    goodbyeComponents = goodbye.components
    for thisComponent in goodbye.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "goodbye" ---
    goodbye.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *GoodbyeText* updates
        
        # if GoodbyeText is starting this frame...
        if GoodbyeText.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            GoodbyeText.frameNStart = frameN  # exact frame index
            GoodbyeText.tStart = t  # local t and not account for scr refresh
            GoodbyeText.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(GoodbyeText, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'GoodbyeText.started')
            # update status
            GoodbyeText.status = STARTED
            GoodbyeText.setAutoDraw(True)
        
        # if GoodbyeText is active this frame...
        if GoodbyeText.status == STARTED:
            # update params
            pass
        
        # *GoodbyeResp* updates
        waitOnFlip = False
        
        # if GoodbyeResp is starting this frame...
        if GoodbyeResp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            GoodbyeResp.frameNStart = frameN  # exact frame index
            GoodbyeResp.tStart = t  # local t and not account for scr refresh
            GoodbyeResp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(GoodbyeResp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'GoodbyeResp.started')
            # update status
            GoodbyeResp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(GoodbyeResp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(GoodbyeResp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if GoodbyeResp.status == STARTED and not waitOnFlip:
            theseKeys = GoodbyeResp.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _GoodbyeResp_allKeys.extend(theseKeys)
            if len(_GoodbyeResp_allKeys):
                GoodbyeResp.keys = _GoodbyeResp_allKeys[-1].name  # just the last key pressed
                GoodbyeResp.rt = _GoodbyeResp_allKeys[-1].rt
                GoodbyeResp.duration = _GoodbyeResp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            goodbye.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in goodbye.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "goodbye" ---
    for thisComponent in goodbye.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for goodbye
    goodbye.tStop = globalClock.getTime(format='float')
    goodbye.tStopRefresh = tThisFlipGlobal
    thisExp.addData('goodbye.stopped', goodbye.tStop)
    # check responses
    if GoodbyeResp.keys in ['', [], None]:  # No response was made
        GoodbyeResp.keys = None
    thisExp.addData('GoodbyeResp.keys',GoodbyeResp.keys)
    if GoodbyeResp.keys != None:  # we had a response
        thisExp.addData('GoodbyeResp.rt', GoodbyeResp.rt)
        thisExp.addData('GoodbyeResp.duration', GoodbyeResp.duration)
    thisExp.nextEntry()
    # the Routine "goodbye" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # mark experiment as finished
    endExperiment(thisExp, win=win)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # return console logger level to WARNING
    logging.console.setLevel(logging.WARNING)
    # mark experiment handler as finished
    thisExp.status = FINISHED
    logging.flush()


def quit(thisExp, win=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win,
        globalClock='float'
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win)
