import stellariumConnect, angles, serial, numpy as np, sys
from datetime import datetime, timedelta
from reportCoordinates import reportCoordinates

AVERAGE_LENGTH = 15.

if len(sys.argv) == 1:
	print "Please call this script with the serial port identifier and optionally a time offset"
	exit()
elif len(sys.argv) > 1:
	portIdentifier = '/dev/tty.' + sys.argv[1]
	timeOffset = float(sys.argv[2]) if (len(sys.argv) == 3) else 0

stelCon = stellariumConnect.stellariumConnect("localhost",10001)
stelCon.handshakeStellarium()
stelCon.sendStellariumCoords(angles.Angle(r=0), angles.Angle(r=0))
imu = serial.Serial(portIdentifier, 115200)
try:
	avgIdx = 0
	while True:
		yawAvg, pitchAvg, rollAvg, zoomAvg = (np.zeros(AVERAGE_LENGTH), np.zeros(AVERAGE_LENGTH), np.zeros(AVERAGE_LENGTH), np.zeros(AVERAGE_LENGTH))
		for i in range(int(AVERAGE_LENGTH)):
			reading = imu.readline().strip()
			imuRes = reading.split(",")
			if len(imuRes) <> 4:
				continue
			try:
				yawAvg[avgIdx%AVERAGE_LENGTH] = float(imuRes[0])
				pitchAvg[avgIdx%AVERAGE_LENGTH] = float(imuRes[1])
				rollAvg[avgIdx%AVERAGE_LENGTH] = float(imuRes[2])
				zoomAvg[avgIdx%AVERAGE_LENGTH] = int(imuRes[3])
			except ValueError:
				continue
			avgIdx += 1

		yaw = ((yawAvg.sum() / AVERAGE_LENGTH) - 90) % 360
		pitch = (pitchAvg.sum() / AVERAGE_LENGTH)*(-1)
		roll = rollAvg.sum() / AVERAGE_LENGTH
		zoom = zoomAvg.sum() / AVERAGE_LENGTH
		#print yaw, pitch
		if abs(pitch) > 90:
			pitch = (180 - abs(pitch))*(pitch/abs(pitch))

		reporter = reportCoordinates(datetime.utcnow() + timedelta(hours=timeOffset))
		[rightAsc,declination] = reporter.getRaDec(yaw, pitch)
		#print "%3.10f, %s"%(rightAsc.h, declination)
		stelCon.sendStellariumCoords(rightAsc, declination)
except KeyboardInterrupt:
	imu.close()
	stelCon.closeConnection()
