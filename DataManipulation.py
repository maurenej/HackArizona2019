import KalmanFilter 
# Data description
#  Time
#  AccX_HP - high precision acceleration signal
#  AccX_LP - low precision acceleration signal
#  RefPosX - real position (ground truth)
#  RefVelX - real velocity (ground truth)
dummyData = [[2, 0], [3, 0], [-7, 0], [4, 0], [2, 0], [5, 0], [3, 0]]

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

for i in range(len(dummyData)):


	new_AccX_Value = dummyData[i]
	initial_state_mean, initial_state_covariance, initial_AccX_Value, PositionChange = KalmanFilter.kalmanFilterPositionChange(initial_state_mean, initial_state_covariance, initial_AccX_Value, new_AccX_Value)

	print(PositionChange)
	#dx = (PositionChange * cos(yAngle)) * cos(xAngle)
	#x += dx
	#dy = (PositionChange * cos(yAngle)) * sin(xAngle)
	#y += dy
	#dz = PositionChange * sin(yAngle)
	#z += dz

	#print(x + ' ' + y + ' ' + z)