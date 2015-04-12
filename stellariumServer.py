import stellariumConnect, angles, serial

stelCon = stellariumConnect.stellariumConnect("localhost",10001)
stelCon.handshakeStellarium()
stelCon.sendStellariumCoords(angles.Angle(r=0), angles.Angle(r=0))
imu = serial.Serial('/dev/ttyUSB0', 115200)
try:
	while True:
		reading = imu.readline()
		rascDecl = reading.split(",")
		stelCon.sendStellariumCoords(angles.Angle(r=float(rascDecl[0])), angles.Angle(r=float(rascDecl[1])))
except KeyboardInterrupt:
	imu.close()
	stelCon.closeConnection()
