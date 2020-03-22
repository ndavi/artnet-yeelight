from yeelight import Bulb
from artnetServer.ArtNetServer import ArtNetServer
import colorsys


class ArtNetToYeelight:

    def __init__(self):
        self.bulbs = [Bulb("192.168.1.102")]
        for bulb in self.bulbs:
            bulb.start_music()
            bulb.turn_on()
        self.artNetReceiver = ArtNetServer()
        self.artNetReceiver.run(self.onArtnetReceived)

    def onArtnetReceived(self, data):
        iterator = 0
        for bulb in self.bulbs:
            hsv = colorsys.rgb_to_hsv(self.translate(data.framedata[iterator], 0, 255, 0, 1),
                                      self.translate(data.framedata[iterator + 1], 0, 255, 0, 1),
                                      self.translate(data.framedata[iterator + 2], 0, 255, 0, 1))
            if hsv[2] == 0:
                    if bulb.music_mode:
                        bulb.turn_off()
                        bulb.stop_music()
            else:
                if(bulb.music_mode == False):
                    bulb.start_music()
                    bulb.turn_on()

                bulb.set_hsv(self.translate(hsv[0], 0, 1, 0, 359),
                             self.translate(hsv[1], 0, 1, 0, 100),
                             self.translate(hsv[2], 0, 1, 0, 100))
            iterator += 1
        pass

    def translate(self, value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return rightMin + (valueScaled * rightSpan)


if __name__ == "__main__":
    # execute only if run as a script
    ArtNetToYeelight()
