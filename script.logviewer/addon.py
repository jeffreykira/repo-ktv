import os
import xbmc
import xbmcaddon
import xbmcgui
__addon__ = xbmcaddon.Addon()

def log(info):
    print '[############] %s'%repr(info)

log('Starting Log Viewer')

def text_viewer(title, text):
    WINDOW = 10147 # Text Viewer window in XBMC
    TITLEBAR = 1
    CONTENTS = 5
    xbmc.executebuiltin("ActivateWindow(%d)" % WINDOW)
    w = xbmcgui.Window(WINDOW)
    xbmc.sleep(500)
    w.getControl(TITLEBAR).setLabel(title)
    w.getControl(CONTENTS).setText(text)


path = xbmc.translatePath('special://logpath/kodi.log')
log(path)

if os.path.isfile(path):
    fileobj = open(path,'r')
    data = fileobj.read()
    fileobj.close()
else:
    data = 'File not found: %s'%path

text_viewer('Log Viewer', data)
