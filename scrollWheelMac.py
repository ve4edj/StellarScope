from Quartz.CoreGraphics import CGEventCreateScrollWheelEvent, CGEventPost, kCGHIDEventTap
import time

def scrollWheelUp(numTicks):
    for i in xrange(1, numTicks):
        time.sleep(.005)
        multiplier = 1 - (float(i) / numTicks)
        speed = 4 * multiplier
        event = CGEventCreateScrollWheelEvent(None, 0, 1, speed)
        CGEventPost(kCGHIDEventTap, event)

def scrollWheelDown(numTicks):
    for i in xrange(1, numTicks):
        time.sleep(.005)
        multiplier = 1 - (float(i) / numTicks)
        speed = 4 * multiplier
        event = CGEventCreateScrollWheelEvent(None, 0, 1, (-1)*speed)
        CGEventPost(kCGHIDEventTap, event)