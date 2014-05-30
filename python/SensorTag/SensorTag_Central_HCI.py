import serial
import os, sys
import struct
from select import select

# not posix system, we need msvcrt library for kbhit
# for posix, we need termios and atexit
if os.name <> 'posix':
  import msvcrt
else:
  import atexit
  import termios

#
#    Structures
#

class KB:
  
    def __init__(self):
        '''Creates a KBHit object that you can call to do various keyboard things.
        '''

        if os.name == 'nt':
            pass
        
        else:
    
            # Save the terminal settings
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd)
            self.old_term = termios.tcgetattr(self.fd)
    
            # New terminal setting unbuffered
            self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)
    
            # Support normal-terminal reset at exit
            atexit.register(self.set_normal_term)
    
    
    def set_normal_term(self):
        ''' Resets to normal terminal.  On Windows this is a no-op.
        '''
        
        if os.name == 'nt':
            pass
        
        else:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)


    def getch(self):
        ''' Returns a keyboard character after kbhit() has been called.
            Should not be called in the same program as getarrow().
        '''
        
        s = ''
        
        if os.name == 'nt':
            return msvcrt.getch().decode('utf-8')
        
        else:
            return sys.stdin.read(1)
                        

    def getarrow(self):
        ''' Returns an arrow-key code after kbhit() has been called. Codes are
        0 : up
        1 : right
        2 : down
        3 : left
        Should not be called in the same program as getch().
        '''
        
        if os.name == 'nt':
            msvcrt.getch() # skip 0xE0
            c = msvcrt.getch()
            vals = [72, 77, 80, 75]
            
        else:
            c = sys.stdin.read(3)[2]
            vals = [65, 67, 66, 68]
        
        return vals.index(ord(c.decode('utf-8')))
        

    def kbhit(self):
        ''' Returns True if keyboard character was hit, False otherwise.
        '''
        if os.name == 'nt':
            return msvcrt.kbhit()
        
        else:
            dr,dw,de = select([sys.stdin], [], [], 0)
            return dr != []

class gapDevDiscReq_t:
  taskID           = None
  mode             = None
  activeScan       = None
  whiteList        = None

class gapEstLinkReq_t:
  taskID           = None
  highDutyCycle    = None    
  whiteList        = None
  addrTypePeer     = None    
  peerAddr         = None

class attWriteReq_t:
  handle           = None              # Handle of the attribute to be written (must be first field)
  len              = None              # Length of value
  value            = None              # Value of the attribute to be written
  sig              = None              # Authentication Signature status (not included (0), valid (1), invalid (2))
  cmd              = None              # Command Flag

#
#    Constants
#

GAP_PROFILE_CENTRAL           = '\x08'

DEVDISC_MODE_NONDISCOVERABLE  = '\x00'
DEVDISC_MODE_GENERAL          = '\x01'
DEVDISC_MODE_LIMITED          = '\x02'
DEVDISC_MODE_ALL              = '\x03'

# Discovey mode (limited, general, all)
DEFAULT_DISCOVERY_MODE        = DEVDISC_MODE_ALL

# TRUE to use active scan
DEFAULT_DISCOVERY_ACTIVE_SCAN = '\x01' # True

# TRUE to use white list during discovery
DEFAULT_DISCOVERY_WHITE_LIST  = '\x00' # False

# TRUE to use high scan duty cycle when creating link
DEFAULT_LINK_HIGH_DUTY_CYCLE  = '\x00' # False

# TRUE to use white list when creating link
DEFAULT_LINK_WHITE_LIST       = '\x00' # False

#
#    Global
#

# our transport layer will be serial port
TX = serial.Serial()

# store the address found
found_address = None

#
is_connected = False

#
#    Defines the BLE GAP command APIs
#

def GAP_DeviceInit( taskID, profileRole, maxScanResponses, irk, srk, signCounter ):
  buf = ''

  buf += '\x01'                       # -Type    : 0x01 (Command)
  buf += '\x00'                 # -Opcode  : 0xFE00 (GAP_DeviceInit)
  buf +=  '\xFE'
 
  buf += '\x26'                 # -Data Length
  buf += profileRole            #  Profile Role
  buf += maxScanResponses       #  MaxScanRsps
  buf += irk                    #
  buf += srk                    #
  buf += signCounter            #

  TX.write(buf)

  # ToDo: here should wait for command status
  return True

def GAP_DeviceDiscoveryRequest( params ):    
  buf = ''

  buf += '\x01'                       # -Type    : 0x01 (Command)
  buf += '\x04'                 # -Opcode  : 0xFE04 (GAP_DeviceDiscoveryRequest)
  buf += '\xFE'
    
  buf += '\x03'                 # -Data Length
  buf += params.mode            #  Mode
  buf += params.activeScan      #  ActiveScan
  buf += params.whiteList       #  WhiteList
  
  TX.write(buf)

  # ToDo: here should wait for command status
  return True

def GAP_EstablishLinkReq( params ):
  buf = ''

  buf += '\x01'
  buf += '\x09\xFE'
  
  buf += struct.pack('B', 3 + 6)  # 6 is B_ADDR_LEN
  
  buf += params.highDutyCycle
  buf += params.whiteList  
  buf += params.addrTypePeer

  buf += params.peerAddr

  TX.write(buf)

  # ToDo: here should wait for command status
  return True;

#
#    Defines the BLE GATT command APIs
#

def GATT_WriteCharValue( connHandle, req, taskId ): 
  buf = ''

  buf += '\x01'
  buf += '\x92\xFD'
  
  buf += struct.pack('B', 4 + ord(req.len))
  
  buf += connHandle
  buf += req.handle
  buf += req.value
  
  TX.write(buf)

  # ToDo: here should wait for command status
  return True

#
#    Defines the BLE GAP Central Role APIs
#

gapCentralRoleTaskId      = '\x00'
gapCentralRoleIRK         = struct.pack('16s', '\x00')
gapCentralRoleSRK         = struct.pack('16s', '\x00')
gapCentralRoleSignCounter = '\x01'
gapCentralRoleMaxScanRes  = '\x05'

def GAPCentralRole_StartDevice():
  return GAP_DeviceInit( gapCentralRoleTaskId, GAP_PROFILE_CENTRAL,
                         gapCentralRoleMaxScanRes, gapCentralRoleIRK,
                         gapCentralRoleSRK, gapCentralRoleSignCounter )

def GAPCentralRole_EstablishLink( highDutyCycle, whiteList, addrTypePeer, peerAddr ):
  params = gapEstLinkReq_t

  params.taskID        = gapCentralRoleTaskId
  params.highDutyCycle = highDutyCycle
  params.whiteList     = whiteList
  params.addrTypePeer  = addrTypePeer
  params.peerAddr      = peerAddr

  return GAP_EstablishLinkReq( params )

def GAPCentralRole_StartDiscovery( mode, activeScan, whiteList ):
  params = gapDevDiscReq_t

  params.taskID     = gapCentralRoleTaskId
  params.mode       = mode
  params.activeScan = activeScan
  params.whiteList  = whiteList

  return GAP_DeviceDiscoveryRequest( params )

#
#
#

def ble_enable_notification(): 
  writeReq = attWriteReq_t
  
  writeReq.handle   = '\x6C\x00' # this is the handle of button in SensorTag, got from BTool
  writeReq.len      = '\x02'
  writeReq.value    = '\x01\x00'

  GATT_WriteCharValue( '\x00\x00', writeReq, '\x00' );

def ble_write_bytes(buf):
  writeReq = attWriteReq_t
  
  writeReq.handle = '\x16\x00'
  writeReq.len    = struct.pack('b', len(buf))
  writeReq.value  = buf

  GATT_WriteCharValue( '\x00\x00', writeReq, '\x00' )

def ble_event_available():
  return TX.inWaiting()

def ble_event_process():
  global found_address
  global is_connected

  type = ord(TX.read(1));
  event_code = ord(TX.read(1));
  data_len = ord(TX.read(1));

  print '-----------------------------'
  print '-Type        : 0x%02X' % (type)
  print '-EventCode   : 0x%02X' % (event_code)
  print '-Data Length : 0x%02X' % (data_len)
  
  buf = TX.read(data_len)
  
#  if event_code == '\x0E':
#    p(" Packets     : 0x%02X\r\n", buf[0]);
#    p(" Opcode      : 0x%02X%02X\r\n", buf[2], buf[1]);
#    byte rssi = buf[6];
#    p(" RSSI        : %d\r\n", rssi-255);
    
#    if (rssi-255) > -100:
#      print rssi
    
#    return True

  event = struct.unpack('H', buf[0]+buf[1])[0]
  status = ord(buf[2]);

  print ' Event       : 0x%04X' % event
  print ' Status      : 0x%02X' % status

  if event == 0x0601: # GAP_DeviceDiscoveryDone
      print 'GAP_DeviceDiscoveryDone'

      num_devs = ord(buf[3])
      print ' NumDevs     : 0x%02X' % num_devs

      # Store address so that we can link it up
      # only store first discovered device only in this demo
      if num_devs > 0:
        found_address = buf[6] + buf[7] + buf[8] + buf[9] + buf[10] + buf[11]

        print 'Address found: ' + hex(ord(found_address[0])) + ':'  + hex(ord(found_address[1])) + ':'  + hex(ord(found_address[2])) + ':'  + hex(ord(found_address[3])) + ':'  + hex(ord(found_address[4])) + ':'  + hex(ord(found_address[5]))
      else:
        print 'No device found'

  elif event == 0x067F:
      print 'GAP_HCI_ExtentionCommandStatus'
      print ' OpCode     : 0x%02X%02X' % (ord(buf[4]), ord(buf[3]))

  elif event == 0x0605:
      print 'GAP_EstablishLink'
      is_connected = True;

  elif event == 0x0606:
      print 'GAP_TerminateLink'
      is_connected = False;
      found = 0;

  elif event == 0x060D:
      print 'GAP_DeviceInformation'        
      event_type = ord(buf[3])        
      if event_type == 0x04:
          print 'Scan Response'
          if buf[15] == 0x1E:
            if buf[16] == 0x94:
      #        found_address = buf[5] + buf[6] + buf[7] + buf[8] + buf[9] + buf[10]
              found = 1;
      #        GAP_DeviceDiscoveryCancel()

  elif event == 0x051B:
        print 'ATT_HandleValueNotification'
        
        if ord(buf[6]) == 0x6B:
	        print ' -------------> Button: ' + hex(ord(buf[8]))
              
  else:
      print ' -> Not handled yet.'

#
#    Start our demo here
#

if os.name == 'posix':
  TX.port = '/dev/tty.usbmodem1431'
else:
  TX.port = 'COM5'
TX.baudrate = 115200
TX.open()

print 'Biscuit Central via HCI'
GAPCentralRole_StartDevice()

str = ''
kb = KB()
  
while True:
  if ble_event_available():
    ble_event_process()

  if kb.kbhit():
    ch = kb.getch()

    if ch == 'd':
      print 'Discovery...'
      GAPCentralRole_StartDiscovery( DEFAULT_DISCOVERY_MODE,
                                     DEFAULT_DISCOVERY_ACTIVE_SCAN,
                                     DEFAULT_DISCOVERY_WHITE_LIST )
    elif ch == 'e':
        print 'Establish Link...'
        print 'Connecting to: ' + hex(ord(found_address[0])) + ':'  + hex(ord(found_address[1])) + ':'  + hex(ord(found_address[2])) + ':'  + hex(ord(found_address[3])) + ':'  + hex(ord(found_address[4])) + ':'  + hex(ord(found_address[5]))

        GAPCentralRole_EstablishLink(DEFAULT_LINK_HIGH_DUTY_CYCLE,
                                DEFAULT_LINK_WHITE_LIST,
                                '\x00', found_address )

    elif ch == 'n':
        print 'Enable Notification...'
        ble_enable_notification()

    elif ch == 'q':
        print 'Quit'
        TX.close()
        break

    else:
        print 'Invalid command.'
