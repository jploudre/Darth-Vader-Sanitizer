# CircuitPlaygroundExpress_NeoPixel

import board
import neopixel
import time
from digitalio import DigitalInOut, Direction
import audioio
import touchio

# Ready the Neopixels
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=1.0)
pixels.fill((0,0,0))
pixels.show()

# enable the speaker
spkrenable = DigitalInOut(board.SPEAKER_ENABLE)
spkrenable.direction = Direction.OUTPUT
spkrenable.value = True

# make the input cap sense pads
capPins = (board.A1, board.A2, board.A3, board.A4, board.A5,
           board.A6, board.A7)

touchPad = []
for i in range(7):
    touchPad.append(touchio.TouchIn(capPins[i]))

# The seven files assigned to the touchpads
audiofiles = ["T00RAND0.wav", "T00RAND1.wav", "T00RAND2.WAV",
               "T00RAND3.WAV", "T10HOLDL.wav", "",
               ""]


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 85:
        return (int(pos*3), int(255 - (pos*3)), 0)
    elif pos < 170:
        pos -= 85
        return (int(255 - (pos*3)), 0, int(pos*3))
    else:
        pos -= 170
        return (0, int(pos*3), int(255 - pos*3))

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(len(pixels)):
            idx = int ((i * 256 / len(pixels)) + j*10)
            pixels[i] = wheel(idx & 255)
        pixels.show()
        time.sleep(wait)

def play_file(filename):
    print("playing file "+filename)
    f = open(filename, "rb")
    a = audioio.AudioOut(board.A0, f)
    a.play()

while True:
    for i in range(7):
        if touchPad[i].value:
            play_file(audiofiles[i])

