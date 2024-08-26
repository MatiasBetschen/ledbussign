
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32  # Number of rows
options.cols = 64  # Number of columns
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular'  # Adjust if using different hardware

# Initialize the matrix
matrix = RGBMatrix(options=options)

# Create a drawing canvas
canvas = matrix.CreateFrameCanvas()

# Set color for the square (e.g., white)
color = graphics.Color(255, 255, 255)  # RGB: White

# Define the square size
square_size = 10

# Calculate the center of the matrix
center_x = options.cols // 2
center_y = options.rows // 2

# Calculate the top-left corner of the square
top_left_x = center_x - (square_size // 2)
top_left_y = center_y - (square_size // 2)

# Draw the square
for x in range(top_left_x, top_left_x + square_size):
    for y in range(top_left_y, top_left_y + square_size):
        canvas.SetPixel(x, y, color.red, color.green, color.blue)

# Update the matrix to display the square
matrix.SwapOnVSync(canvas)
