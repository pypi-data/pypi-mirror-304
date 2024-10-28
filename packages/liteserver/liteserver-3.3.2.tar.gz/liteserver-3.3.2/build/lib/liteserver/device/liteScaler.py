#!/usr/bin/env python3
"""Example of user-defined Lite Data Objects"""
__version__ = '1.0.6 2021-11-19'# no_float32 removed 
 
import sys, time, threading
from timeit import default_timer as timer
import numpy as np

try:
    from liteserv import liteserver
except:
    from liteserver import liteserver
LDO = liteserver.LDO
Device = liteserver.Device

#````````````````````````````Helper functions`````````````````````````````````
def printi(msg): print('LiteScaler:INFO: '+msg)
def printw(msg): print('LiteScaler:WARNING: '+msg)
def printe(msg): print('LiteScaler:ERROR: '+msg)
def printd(msg): 
    if pargs.dbg:
        print('LiteScaler:dbgScaler: '+str(msg))
#````````````````````````````Lite Data Objects````````````````````````````````
class Scaler(Device):
    """ Derived from liteserver.Device.
    Note: All class members, which are not process variables should 
    be prefixed with _"""
    def __init__(self,name, bigImage=False):
        #initials = (np.random.rand(pargs.nCounters)*1000).round().astype(int).tolist()
        initials = [0]*pargs.nCounters
        #2000,3000,3 #works on localhost with 1ms delay 50MB/s, server busy 200%
        #960,1280,3 # 3.6 MB, OK on localhost with 60K chunks and 0.5ms ChunkSleep, 100MB/s, sporadic KeyError 'pid'
        #480,640,3 # 0.9 MB, OK on localhost with 60K chunks, 1ms ChunkSleep, 48MB/s chunk speed
        h,w,p = (960,1280,3) if bigImage else (120,160,3)
        img = np.arange(h*w*p).astype('uint8').reshape(h,w,p)
        incs = []
        for i in range(1,1+pargs.nCounters//2):
            incs += [-i,i]
        pars = {
          'counters':   LDO('R','%i of counters'%len(initials),initials),
          'increments': LDO('WE','Increments of the individual counters',incs),
          'frequency':  LDO('RWE','Update frequency of all counters',1.3\
                        ,units='Hz', opLimits=(0.001,1001.)),
          'reset':      LDO('WE','Reset all counters',[None]\
                        ,setter=self.reset),
          'image':      LDO('R','Image',img),
          'shape':      LDO('','Image shape',(h,w,p)),
          'coordinate': LDO('RW','Just 2-component numpy vector for testing'\
                        ,np.array([0.,1.]).astype('float32')),#
          'time':       LDO('R','Current time',0., getter=self.get_time),
          'number':     LDO('RWE','Test number',0., opLimits=(-1000000,1000000)\
          ,setter=self.set_number),
          'text':       LDO('RWE','Test text', ['Test'], setter=self.set_text),
          'cycle':      LDO('R','Cycle number',0),
          'rps':        LDO('R','Cycles per second',0.,units='Hz'),
          'publishingSpeed': LDO('R', 'Instanteneous publishing speed of published data', 0., units='MB/s'),
          'dataSize':   LDO('R', 'Size of published data', 0., units='KB'),
          'chunks':     LDO('R', 'Number of chunks in UDP transfer, for lowest latency it should be 1', 0.),
          'udpSpeed':   LDO('R', 'Instanteneous socket.send spped', 0., units='MB/s'),
        }
        super().__init__(name,pars)
        self.start()
    #``````````````Overridables```````````````````````````````````````````````        
    def start(self):
        printi('liteScaler started')
        thread = threading.Thread(target=self._state_machine)
        thread.daemon = False
        thread.start()
    #,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

    def reset(self):
        print('resetting scalers of %s'%self.name)
        for i in range(len(self.counters.value)):
            self.counters.value[i] = 0
        t = time.time()
        self.counters.timestamp = t
        self.reset.timestamp = t

    def set_number(self):
        print('Setting number to '+str(self.number.value))

    def set_text(self):
        msg = 'Setting text to '+str(self.text.value)
        print(msg)
        raise ValueError(msg)

    def get_time(self):
        self.time.value = time.time()

    def _state_machine(self):
        time.sleep(.2)# give time for server to startup

        self.cycle.value = 0
        prevCycle = 0
        ns = len(self.counters.value)
        timestamp = time.time()
        periodic_update = time.time()
        maxChanks = 0
        while not Device.EventExit.is_set():
            #TODO: with liteserver-v76 we have to use value[0]
            if self.run.value[0][:4] == 'Stop':
                break
            #waitTime = 1./self.frequency.value - (time.time() - timestamp)
            waitTime = 1./self.frequency.value[0] - (time.time() - timestamp)
            Device.EventExit.wait(waitTime)
            timestamp = time.time()
            dt = timestamp - periodic_update
            if dt > 10.:
                periodic_update = timestamp
                if server.Dbg > 0:
                    printi(f'cycle of {self.name}:{self.cycle.value}, wt:{round(waitTime,4)}')
                #print(f'periodic update: {dt}')
                if maxChanks > 1:
                    msg = 'WARNING: published data are chopped, latency will increase'
                    maxChanks = 0
                else:
                    msg = f'periodic update {self.name} @{round(timestamp,3)}'
                self.status.value = msg
                self.status.timestamp = timestamp
                #print(self.status.value[0])
                #Device.setServerStatusText('Cycle %i on '%self.cycle.value[0]+self.name)
                self.rps.value = (self.cycle.value - prevCycle)/dt
                self.rps.timestamp = timestamp
                prevCycle = self.cycle.value
            # increment counters individually
            for i,increment in enumerate(self.increments.value[:ns]):
                #print(instance+': c,i='+str((self.counters.value[i],increment)))
                self.counters.value[i] += increment
                
            # increment pixels in the image
            # this is very time consuming:
            #self.image.value[0] = (self.image.value[0] + 1).astype('uint8')

            # change only one pixel            
            self.image.value[0,0,0] = np.uint8(self.cycle.value)
     
            self.cycle.value += 1

            #print('publish all modified parameters of '+self.name)
            try:
                dt = server.Perf['Seconds'] - self._prevs[1]
                mbps = round((server.Perf['MBytes'] - self._prevs[0])/dt, 3)
            except:
                mbps = 0.
            self._prevs = server.Perf['MBytes'],server.Perf['Seconds']
            self.udpSpeed.value = mbps

            # invalidate timestamps for changing variables, otherwise the
            # publish() will ignore them
            for i in [self.counters, self.image, self.cycle, self.udpSpeed,
                self.publishingSpeed, self.dataSize, self.chunks, self.time]:
                i.timestamp = timestamp

            ts = timer()
            shippedBytes = self.publish()

            if shippedBytes:
                ss = round(shippedBytes / (timer() - ts) / 1.e6, 3)
                #print(f'sb: {shippedBytes}')            
                self.publishingSpeed.value = ss
                #printd(f'publishing speed of {self.name}: {ss}')
                self.dataSize.value = round(shippedBytes/1000.,1)
                self.chunks.value = (shippedBytes-1)//liteserver.ChunkSize + 1
                maxChanks = max(maxChanks, self.chunks.value)
        print('Scaler '+self.name+' exit')
#,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,S,,,,,,,,,,,,,,,,,,,,,,,,,,,,
# parse arguments
import argparse
parser = argparse.ArgumentParser(description=__doc__
    ,formatter_class=argparse.ArgumentDefaultsHelpFormatter
    ,epilog=f'liteScaler version {__version__}, liteserver {liteserver.__version__}')
parser.add_argument('-b','--bigImage', action='store_true', help=\
'Generate big image >64kB.')
defaultIP = liteserver.ip_address('')
parser.add_argument('-i','--interface', default = defaultIP, help=\
'Network interface. Default is the interface, which connected to internet.')
n = 1100# to fit liteScaler volume into one chunk
parser.add_argument('-n','--nCounters', type=int, default=n,
  help=f'Number of counters in each scaler, one transmission is 16K.')
  #default liteAcces accepts 1100 doubles, 9990 int16s
  #the UDP socket size is limited to 64k bytes
parser.add_argument('-p','--port', type=int, default=9700, help=\
'Serving port.') 
parser.add_argument('-s','--scalers', type=int, default=1, help=\
'Number of devices/scalers.')
parser.add_argument('-v','--verbose', nargs='*', help='Show more log messages.')
pargs = parser.parse_args()

liteserver.Server.Dbg = 0 if pargs.verbose is None else len(pargs.verbose)+1
devices = [
  Scaler('dev'+str(i+1), bigImage=pargs.bigImage)\
  for i in range(pargs.scalers)]

print('Serving:'+str([dev.name for dev in devices]))

server = liteserver.Server(devices, interface=pargs.interface,
    port=pargs.port)
server.loop()
