import re
import urllib2
import xbmc
import xbmcaddon
import xbmcgui
__addon__ = xbmcaddon.Addon()

def log(info):
    print '[############] %s'%repr(info)

log('Starting MVG Checker')
log(__addon__.getSetting('station'))
log(__addon__.getSetting('mintime'))
log(__addon__.getSetting('maxtime'))

station = __addon__.getSetting('station')
mintime = __addon__.getSetting('mintime')
maxtime = __addon__.getSetting('maxtime')

class MVG:

    """This Library gives MVG Departments fom any destination
    Thanks to pc-coholic: <fpletz@phidev.org>"""

    def encode_station_name(self, stationname):
        string = urllib2.quote(stationname.decode('utf-8').encode('latin1'))
        return string

    def get_url(self, stationname):
        enc_station = self.encode_station_name(station)
        return 'http://www.mvg-live.de/ims/dfiStaticAnzeige.svc?haltestelle=%s'%enc_station

    def get_departures(self, station, mintime=1,maxtime = 20):
        log('Station: %s'%station)
        log('Mintime: %s'%mintime)
        log('Maxtime: %s'%maxtime)

        mintime = int(mintime)
        maxtime = int(maxtime)
        enc_station = self.encode_station_name(station)

        REGEXP = re.compile(r'<tr class="[^"]+">'+
        '<td class="lineColumn">(\w+)</td>'+
        '<td class="stationColumn">([^<]+)<span class="spacer">&nbsp;</span>'+
        '</td><td class="inMinColumn">(\d+)')

        url = 'http://www.mvg-live.de/ims/dfiStaticAnzeige.svc?haltestelle=%s'%enc_station
        log('URL: %s'%repr(url))
        counter = 0
        while counter < 3:
            counter += 1
            try:
                s = urllib2.urlopen(url).read().replace('\r\n', '').replace('\t', '').decode('ISO-8859-1')
            except:
                pass
        d = REGEXP.findall(s)
        outlist = []
        if len(d) == 0:
            return []
        else:
            for (line, dest, t) in d:
                if int(t) <= maxtime and int(t) >= mintime:
                    outlist.append('%2s Minutes: %s %-24s' % (t,line, dest))
            outlist.sort()
            return outlist

def text_viewer(title, text):
    WINDOW = 10147 # Text Viewer window in XBMC
    TITLEBAR = 1
    CONTENTS = 5
    xbmc.executebuiltin("ActivateWindow(%d)" % WINDOW)
    w = xbmcgui.Window(WINDOW)
    xbmc.sleep(500)
    w.getControl(TITLEBAR).setLabel(title)
    w.getControl(CONTENTS).setText(text)


# Wrong Time Settings?
if int(mintime) >= int(maxtime):
    mintime = 1
    maxtime = 30
    __addon__.setSetting(id="mintime",value='1')
    __addon__.setSetting(id="maxtime",value='30')


# Wrong Station in Settings
mvg_obj = MVG()

if station == '':
    # No usable Station found
    while 1:
        kb = xbmc.Keyboard(heading='Station')
        kb.doModal()
        if (kb.isConfirmed()):
            # Station Confirmed
            station = kb.getText()#.decode('utf-8')
            log('Trying: %s'%station)

            data = mvg_obj.get_departures(station)
            if data == []:
                log('Got No Data: %s'%station)
                continue
            else:
                log('Save: %s'%station)
                __addon__.setSetting(id="station",value=station)
                break
        else:
            # Cancelled
            exit(0)

# Show Depart Infos
log('Showing Output: %s'%station)
data = mvg_obj.get_departures(station,mintime,maxtime)
if len(data) == 0:
    text_viewer(station,'No Info\n\n\nIf nothing happens you could try:\n\n1. check the URL:\n%s\n\n2. Check the Stationname: %s'%(mvg_obj.get_url(station),station))
    exit(0)
info = ''
for line in data:
    info += line + '\n'
text_viewer(station,info)


