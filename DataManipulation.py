import KalmanFilter 
import math
import numpy as np
from bokeh.plotting import figure, output_file, show

# Data description
#  Time
#  AccX_HP - high precision acceleration signal
#  AccX_LP - low precision acceleration signal
#  RefPosX - real position (ground truth)
#  RefVelX - real velocity (ground truth)
dummyData = [[2, 0], [3, 0], [-7, 0], [4, 0], [2, 0], [5, 0], [3, 0]]
dummyAngles = [[0, 0.8], [0.2, 0.6], [0.1, 1.3], [0.5, 0.2], [0.1, 0.8], [0, 0.3], [0.2, 0.4]]

initial_state_mean = [0, 0, 0]
initial_state_covariance = [[0, 0, 0], [0, 0, 0], [0, 0, 0.0007]]
initial_AccX_Value = [0, 0]
new_AccX_Value = [0, 0]

# output to static HTML file (with CDN resources)
output_file("color_scatter.html", title="color_scatter.py example", mode="cdn")

TOOLS = "crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select"

# create a new plot with the tools above, and explicit ranges
p = figure(tools=TOOLS, x_range=(0, 100), y_range=(0, 100))

PositionChange = 0
x = 0
dx = 0
y = 0
dy = 0
z = 0
dz = 0

for i in range(len(dummyData)):


	new_AccX_Value = dummyData[i]
	initial_state_mean, initial_state_covariance, initial_AccX_Value, PositionChange = KalmanFilter.kalmanFilterPositionChange(initial_state_mean, initial_state_covariance, initial_AccX_Value, new_AccX_Value)
	yAngle = dummyAngles[i][0]
	xAngle = dummyAngles[i][1]
	print(PositionChange)
	dx = (PositionChange * math.cos(yAngle)) * math.cos(xAngle)
	x += dx
	dy = (PositionChange * math.cos(yAngle)) * math.sin(xAngle)
	y += dy
	dz = PositionChange * math.sin(yAngle)
	z += dz

	colors = ["#%02x%02x%02x" % (int(r), int(g), 150) for r, g in zip(50+2*x, 30+2*y)]

	# add a circle renderer with vectorized colors and sizes
	p.circle(x, y, radius=radii, fill_color=colors, fill_alpha=0.6, line_color=None)

	# show the results
	show(p)

