from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32  # Number of rows (adjust to your matrix size)
options.cols = 64  # Number of columns (adjust to your matrix size)
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # Set to 'adafruit-hat' for Adafruit HAT

# Initialize the matrix
matrix = RGBMatrix(options=options)

# Create a drawing canvas
canvas = matrix.CreateFrameCanvas()

# Load font (adjust path if needed)
font = graphics.Font()
font.LoadFont("rpi-rgb-led-matrix/fonts/7x13.bdf")  # Adjust path to your font file if necessary

# Set text color
color = graphics.Color(255, 255, 255)  # White color

# Draw text on the canvas
def draw_text():
    canvas.Clear()  # Clear previous content
    graphics.DrawText(canvas, font, 10, 20, color, "Hello")  # Position (10, 20) is where text starts
    matrix.SwapOnVSync(canvas)  # Update the matrix to display the text

try:
    while True:
        draw_text()  # Continuously draw text
        time.sleep(1)  # Adjust delay if needed (e.g., 1 second delay)
except KeyboardInterrupt:
    canvas.Clear()  # Clear the display when interrupted
    matrix.SwapOnVSync(canvas)
    print("Display cleared and script terminated.")


