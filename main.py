from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32  # Number of rows (adjust to your matrix size)
options.cols = 64  # Number of columns (adjust to your matrix size)
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular'  # Adjust based on your hardware setup

# Initialize the matrix
matrix = RGBMatrix(options=options)

# Create a drawing canvas
canvas = matrix.CreateFrameCanvas()

# Load font (adjust path if needed)
font = graphics.Font()
font.LoadFont("rpi-rgb-led-matrix/fonts/7x13.bdf")  # Change path to your font file if necessary

# Set text color
color = graphics.Color(255, 255, 255)  # White color

# Draw text on the canvas
graphics.DrawText(canvas, font, 10, 20, color, "Hello")  # Position (10, 20) is where text starts

# Update the matrix to display the text
matrix.SwapOnVSync(canvas)

