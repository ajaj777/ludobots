import numpy as np
import matplotlib.pyplot

backLegSensorValues = np.load('data/backLegSensorValues.npy')
frontLegSensorValues = np.load('data/frontLegSensorValues.npy')
targetAnglesValues = np.load('data/targetAnglesValues.npy')
fl_targetAnglesValues = np.load('data/fl_targetAnglesValues.npy')
bl_targetAnglesValues = np.load('data/bl_targetAnglesValues.npy')
#print(backLegSensorValues)

#matplotlib.pyplot.plot(backLegSensorValues, label="backLeg", linewidth=4)
#matplotlib.pyplot.plot(frontLegSensorValues, label="frontLeg")
#matplotlib.pyplot.plot(targetAnglesValues, label="angles")
matplotlib.pyplot.plot(fl_targetAnglesValues, label="fl_angles")
matplotlib.pyplot.plot(bl_targetAnglesValues, label="bl_angles")
matplotlib.pyplot.legend()
matplotlib.pyplot.show()