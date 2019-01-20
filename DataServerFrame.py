import socket
import sys
import KalmanFilter 
import math
 
# For data visualization
import numpy as np

from bokeh.io import output_notebook
#from bokeh.plotting import figure, curdoc, show, push_notebook
from bokeh.layouts import row
import matplotlib.pyplot as plt

# C:\Python37-32\python C:\Users\ericj\Documents\HackArizona\HackArizona2019\DataServerFrame.py
# C:\Python37-32\Scripts\jupyter notebook

HOST = '192.168.0.151' #this is your localhost
PORT = 8000
 
initial_state_mean = [0, 0, 0]
initial_state_covariance = [[0, 0, 0], [0, 0, 0], [0, 0, 0.0007]]
initial_AccX_Value = [0, 0]
new_AccX_Value = [0, 0]

PositionChange = 0
x = 0
dx = 0
y = 0
dy = 0
z = 0
dz = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socket.socket: must use to create a socket.
#socket.AF_INET: Address Format, Internet = IP Addresses.
#socket.SOCK_STREAM: two-way, connection-based byte streams.
print ('socket created')
 
#Bind socket to Host and Port
try:
    s.bind((HOST, PORT))
except socket.error as err:
    print ('Bind Failed')
    sys.exit()
 
print ('Socket Bind Success!')
 
 
#listen(): This method sets up and start TCP listener.
s.listen(10)
print ('Socket is now listening')
 
output_notebook
plt.axis([-1, 1, -1, 1])
# create a new plot with the tools above, and explicit ranges
#show(p)
colors = ["#111111"]
while 1:
    conn, addr = s.accept()
    #print ('Connect with ' + addr[0] + ':' + str(addr[1]))
    buf = conn.recv(128)
    buf = str(buf)
    buf = buf[2:-1]

    DataSet = buf.split(' ')
    DataSet = [float(i) for i in DataSet]

    initial_state_mean, initial_state_covariance, initial_AccX_Value, PositionChange = KalmanFilter.kalmanFilterPositionChange(initial_state_mean, initial_state_covariance, initial_AccX_Value, math.sqrt((DataSet[0]**2) + (DataSet[2]**2)))
    yAngle = DataSet[4]
    xAngle = DataSet[3]
    dx = (PositionChange * math.cos(yAngle)) * math.cos(xAngle)
    x += dx
    dy = (PositionChange * math.cos(yAngle)) * math.sin(xAngle)
    y += dy
    dz = PositionChange * math.sin(yAngle)
    z += dz
    print(str(x) + ' ' + str(y) + ' ' + str(z))

    # add a circle renderer with vectorized colors and sizes
    #p.circle(x, y, radius=1.5, fill_color=colors, fill_alpha=0.6, line_color=None)
    # show the results
    i, d = math.modf(z)
    color = int(d) + 10
    plt.scatter(x, y, c = "#" + "{:06x}".format(color))
    plt.pause(0.05)
mng = plt.get_current_fig_manager()
mng.frame.Maximize(True)
plt.show()
#session.loop_until_closed()
s.close()