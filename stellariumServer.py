import stellariumConnect
import angles

stelCon = stellariumConnect.stellariumConnect("localhost",10001)
stelCon.handshakeStellarium()
while True:
	reading = raw_input()
	radecS  = reading.split(":")
	Ra = angles.Angle(r=float(radecS[0]))
	Dec = angles.Angle(r=float(radecS[1]))
	stelCon.sendStellariumCoords(Ra,Dec)
