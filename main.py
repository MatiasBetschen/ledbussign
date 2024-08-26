from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from time import sleep

# Configuration for the LED matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # Use 'regular' for non-HAT/Bonnet

# Create the RGBMatrix object
matrix = RGBMatrix(options=options)

# Load font
font = graphics.Font()
font.LoadFont("rpi-rgb-led-matrix/fonts/7x13.bdf")

# Set color
color = graphics.Color(255, 255, 0)  # Yellow

# Create a canvas to draw on
canvas = matrix.CreateFrameCanvas()

# Display "Hello World"
text = "Hello World"
pos = canvas.width  # Start text off the right side of the screen

# Loop to scroll text across the screen
while True:
    canvas.Clear()
    len = graphics.DrawText(canvas, font, pos, 20, color, text)
    pos -= 1

    if pos + len < 0:
        pos = canvas.width

    # Update the display and sleep for a short time
    canvas = matrix.SwapOnVSync(canvas)
    sleep(0.05)  # Adjust speed of scrolling text
