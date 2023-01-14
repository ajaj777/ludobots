import numpy as np
import matplotlib.pyplot

backLegSensorValues = np.load('data/backLegSensorValues.npy')
frontLegSensorValues = np.load('data/frontLegSensorValues.npy')
targetAnglesValues = np.load('data/targetAnglesValues.npy')
#print(backLegSensorValues)

#matplotlib.pyplot.plot(backLegSensorValues, label="backLeg", linewidth=4)
#matplotlib.pyplot.plot(frontLegSensorValues, label="frontLeg")
matplotlib.pyplot.plot(targetAnglesValues, label="angles")
matplotlib.pyplot.legend()
matplotlib.pyplot.show()