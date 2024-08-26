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

# Define text strings
text_lines = ["Line 1", "Line 2", "Line 3"]

# Calculate the x position (far right)
x_position = 0  # Adjust if necessary for padding
# Calculate the y positions to stack the text vertically
line_height = 13
padding = 2  # Space between lines

def draw_stacked_text():
    canvas.Clear()  # Clear previous content
    y_position=0
    
    graphics.DrawText(canvas, font, 0 , 0+line_height, color, "Bus 31   5min")
    graphics.DrawText(canvas, font,0, 0+2*line_height+padding, color, "Tram 20  8min")
    graphics.DrawText(canvas, font, 0 , 0+3*line_height+2*padding, color, "Tram 2  10min")
    matrix.SwapOnVSync(canvas)  # Update the matrix to display the text

try:
    while True:
        draw_stacked_text()  # Continuously draw text
        time.sleep(5)  # Adjust delay if needed (e.g., 1 second delay)
except KeyboardInterrupt:
    canvas.Clear()  # Clear the display when interrupted
    matrix.SwapOnVSync(canvas)
    print("Display cleared and script terminated.")

