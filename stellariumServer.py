import stellariumConnect, angles, serial, datetime, numpy as np
from reportCoordinates import reportCoordinates

AVERAGE_LENGTH = 20.

stelCon = stellariumConnect.stellariumConnect("localhost",10001)
stelCon.handshakeStellarium()
stelCon.sendStellariumCoords(angles.Angle(r=0), angles.Angle(r=0))
imu = serial.Serial('/dev/tty.usbmodem1411', 115200)
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

		yaw = yawAvg.sum() / AVERAGE_LENGTH
		pitch = (pitchAvg.sum() / AVERAGE_LENGTH)*(-1)
		roll = rollAvg.sum() / AVERAGE_LENGTH
		zoom = zoomAvg.sum() / AVERAGE_LENGTH
		#print yaw, pitch
		if abs(pitch) > 90:
			pitch = (180 - abs(pitch))*(pitch/abs(pitch))

		reporter = reportCoordinates(datetime.datetime.utcnow())
		[rightAsc,declination] = reporter.getRaDec(yaw, pitch)
		print "%3.10f, %s"%(rightAsc.h, declination)
		stelCon.sendStellariumCoords(rightAsc, declination)
except KeyboardInterrupt:
	imu.close()
	stelCon.closeConnection()
