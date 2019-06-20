from m5stack import *
from m5ui import *
from uiflow import *

import _thread
import unit

setScreenColor(0x2e2828)

finger0 = unit.get(unit.FINGER, unit.PORTB)
# rfid0 = unit.get(unit.RFID, unit.PORTA)

uart = machine.UART(2, tx=17, rx=16)
uart.init(115200, bits=8, parity=None, stop=1)
uart_data = ''

label1 = M5TextBox(37, 35, "Text", lcd.FONT_DejaVu24,0xFFFFFF, rotate=0)
label3 = M5TextBox(19, 134, "Text", lcd.FONT_Default,0xFFFFFF, rotate=0)

finger_id = 0
finger_access = 0

cmd_1 = 0
cmd_2 = 0

def finger0_cb(user_id, access):
    global finger_id, finger_access
    finger_id = user_id
    filter_access = access

finger0.readFingerCb(callback=finger0_cb)

def addfinger():
    finger0.addUser(int(cmd_1), int(cmd_2))

def getfinger():
    global finger_id, finger_access
    print('rep,getFinger,{},{}\r\n'.format(finger_id, finger_access))
    uart.write('rep,getFinger,{},{}\r\n'.format(finger_id, finger_access))
    finger_id, finger_access = 0, 0

def cardOn():
    # cardOn = rfid0.isCardOn()
    uart.write('rep,getCard,{},0\r\n'.format(1 if cardOn else 0))

def writeCard():
    pass
    # rfid0.writeBlock(1,'{}'.format(cmd_1))

def readCard():
    pass
    # dataStr = rfid0.readBlockStr(1)
    # uart.write('rep,getCard,{},0\r\n'.format(rfid0.readBlockStr(1)))

cmd_map = {'setFinger': addfinger, "getFinger": getfinger, "clearFinger": finger0.removeAllUser}
cmd_map["getCard"] = cardOn
cmd_map["setCard"] = writeCard
cmd_map["getCardD"] = readCard

time.sleep(0.1)

finger0.removeAllUser()

while True:
    label1.setText(str(finger0.state))
    if uart.any():
        try:
            uart_data += uart.read().decode()
        except:
            print("read error")
            uart_data = ''
        if uart_data[-2:] == '\r\n':
            cmd_list = uart_data[:-2].replace(' ', '').split(',')
            label3.setText(str(cmd_list))
            print(cmd_list)
            if len(cmd_list) != 4:
                print("error cmd")
            else:
                cmd_1 = cmd_list[2]
                cmd_2 = cmd_list[3]
                cmd_map[cmd_list[1]]()
                uart_data = ''
            