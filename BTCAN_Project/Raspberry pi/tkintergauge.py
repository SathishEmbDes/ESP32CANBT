
import tkinter as tk
import tk_tools
import serial
import sys

import bluetooth
#from tkinter import *
import tkinter.font as font

# import tkinter as tk
from tkinter import ttk

addr = "58:BF:25:35:FE:1A"
#addr = None

canID=0

if len(sys.argv) < 2:
    print("No device specified. Searching all nearby bluetooth devices for "
          "the SampleServer service...")
else:
    addr = sys.argv[1]
    print("Searching for SampleServer on {}...".format(addr))

# search for the SampleServer service
#uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
#service_matches = bluetooth.find_service(uuid=uuid, address=addr)
addr = "58:BF:25:35:FE:1A"
service_matches = bluetooth.find_service(address=addr)

if len(service_matches) == 0:
    print("Couldn't find the SampleServer service.")
    sys.exit(0)


first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

port=1
print("Connecting to \"{}\" on {}".format(name, host))

# Create the client socket
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((host, port))

print("Connected. Type something...")
def input_and_send():
    while True:
        data = a
        if not data:
            break
        sock.send(data)      

def rx_and_echo():
    sock.send("\n send anything\n")
    #while True:
    data=sock.recv(buf_size)
    if data:
       #print((data))
       return data
            
buf_size=1024;

root = tk.Tk()
#getting screen width and height of display
width= root.winfo_screenwidth()
height= root.winfo_screenheight()
#setting tkinter window size
#root.geometry("%dx%d" % (width, height))
# setting attribute
root.attributes('-fullscreen', False)
print (600)
print (300)
max_speed = 200


# Typical one-sided gauge that you might be expecting for a
# speedometer or tachometer.  Starts at zero and goes to
# max_value when full-scale.
speed_gauge = tk_tools.Gauge(root,height=200, width=350,
                            max_value=max_speed,
                            label='Speed',
                            unit=' KMPH',
                            bg='grey')
speed_gauge.grid(row=0, column=0, sticky='news')


tach_gauge = tk_tools.Gauge(root,height=200, width=350,
                            max_value=8000,
                            label='Tachometer',
                            unit=' RPM',
                            divisions=10)
tach_gauge.grid(row=1, column=0, sticky='news')

#strange_gauge = tk_tools.Gauge(root,
#                               max_value=30000,
#                               label='strange', unit=' blah',
#                               divisions=10, red=90, yellow=60)
#strange_gauge.grid(row=2, column=0, sticky='news')

# The battery voltage gauge has a lower voltage limit and an
# upper voltage limit.  These are automatically created when
# one imposes values on red_low and yellow_low along with
# using the min_value.
batV_gauge = tk_tools.Gauge(root, height=200, width=350,
                            max_value=16, min_value=8,
                            label='Bat Voltage',
                            unit='V',
                            divisions=8,
                            yellow=60,
                            red=75,
                            red_low=30,
                            yellow_low=40)
batV_gauge.grid(row=0, column=1, sticky='news')

# Similar to the previous gauge with bi-directional, but shows an
# imbalanced configuration along with support for negative numbers.
batI_gauge = tk_tools.Gauge(root, height=200, width=350,
                            max_value=6,
                            min_value=-8,
                            label='Bat Current',
                            unit='A',
                            divisions=14, yellow=80, red=90,
                            red_low=20, yellow_low=30, bg='lavender')
batI_gauge.grid(row=1, column=1, sticky='news')

# initialization of some variables.
count = 0
up = True


def update_gauge():
    global count, up
    mask=0x3001
    #canID=0
    sensorData = rx_and_echo()
    print ('SensorData =', sensorData)
    
    if(len(sensorData) > 12):
        
        canID=hex(((sensorData[0]<<24)|sensorData[1]<<16)|((sensorData[2]<<8)|sensorData[3]))
        speed= hex((sensorData[5] << 8) | sensorData[6] )
        tacho=hex((sensorData[7]<<8) | sensorData[8] )
        voltage=hex((sensorData[9]<<8) | sensorData[10] )
        current=hex((sensorData[11]<<8) | sensorData[12] )
        print ('Speed = ' )
        print( speed )
        print( 'can= '+canID)
        # update the gauges according to their value
        if int(canID,16)==mask:
            speed_gauge.set_value(int(speed,16))
            speed_button['text']='SPEED :'+ str(int(speed,16))+' KMPH'
        
            tach_gauge.set_value(int(tacho,16))
            tacho_button['text']='RPM :'+ str(int(tacho,16))+' RPM'
        
            batI_gauge.set_value(int(current,16))
            current_button['text']='CURRENT :'+ str(int(current,16))+' AMP'
           
       
            batV_gauge.set_value(int(voltage,16))
            voltage_button['text']='VOLTAGE :'+ str(int(voltage,16))+' V'
   
    root.after(50, update_gauge)
    

import tkinter as tk
from tkinter import ttk

# root window
root = tk.Tk()
root.geometry('300x200')
root.resizable(False, False)
root.title('CAN BT TFT DISPLAY DEMO')



myfont=font.Font(size=30)
# speed button
speed_button = ttk.Button(
    root,
    text='speed',
   
)
    
#exit_button['font']=myfont

speed_button.pack(
    ipadx=10,
    ipady=10,
    expand=True
)

# Tacho button
tacho_button = ttk.Button(
    root,
    text='tacho'
    
)
#tacho_button['font']=myfont
    
tacho_button.pack(
    ipadx=10,
    ipady=10,
    expand=True
)

#battery voltage
voltage_button = ttk.Button(
    root,
    text='voltage'
    
)

    
voltage_button.pack(
    ipadx=10,
    ipady=10,
    expand=True
)

#current button
current_button = ttk.Button(
    root,
    text='current'
    
)

    
current_button.pack(
    ipadx=10,
    ipady=10,
    expand=True
)

    

if __name__ == '__main__':
    root.after(100, update_gauge)
    

    root.mainloop()
    sock.close()
