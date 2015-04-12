import stellariumConnect, angles, serial, datetime
from reportCoordinates import reportCoordinates

AVERAGE_LENGTH = 10.

stelCon = stellariumConnect.stellariumConnect("localhost",10001)
stelCon.handshakeStellarium()
stelCon.sendStellariumCoords(angles.Angle(r=0), angles.Angle(r=0))
imu = serial.Serial('/dev/tty.usbmodem1411', 115200)
try:
	while True:
		yawAvg, pitchAvg, rollAvg, zoomAvg = (0,0,0,0)
		for i in range(int(AVERAGE_LENGTH)):
			reading = imu.readline().strip()
			imuRes = reading.split(",")
			if len(imuRes) <> 4:
				continue
			yawAvg += float(imuRes[0])
			pitchAvg += float(imuRes[1])
			rollAvg += float(imuRes[2])
			zoomAvg += int(imuRes[3])

			yaw = yawAvg / AVERAGE_LENGTH
			pitch = (pitchAvg / AVERAGE_LENGTH)*(-1)
			roll = rollAvg / AVERAGE_LENGTH
			zoom = zoomAvg / AVERAGE_LENGTH

			if abs(pitch) > 90:
				pitch = (180 - abs(pitch))*(pitch/abs(pitch))

			time = datetime.datetime
			reporter = reportCoordinates(time.utcnow())
			[rightAsc,declination] = reporter.getRaDec(yaw, pitch)
			print "%3.10f, %s"%(rightAsc.h, declination)
			stelCon.sendStellariumCoords(rightAsc, declination)
except KeyboardInterrupt:
	imu.close()
	stelCon.closeConnection()
