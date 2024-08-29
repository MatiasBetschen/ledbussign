from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time
import requests
import datetime


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
font.LoadFont("rpi-rgb-led-matrix/fonts/6x10.bdf")  # Adjust path to your font file if necessary

# Calculate the y positions to stack the text vertically
line_height = 7
padding = 0  # Space between lines
def getcolor(string):
    color_map = {
        'B31': graphics.Color(0, 0, 255),
        'T20': graphics.Color(255, 0, 0),
        'B35': graphics.Color(0, 255, 0)
    }
    first_three_chars = string[:3].lower()
    return color_map.get(first_three_chars, 'Unknown')


def draw_stacked_text(array, array2):
    canvas.Clear()  # Clear previous content
    for i in range (len(array)):
        color=getcolor(array[i])
        graphics.DrawText(canvas, font, 0 , 0+(i+1)*line_height+i, color, array[i])
    graphics.DrawText(canvas, font, 0 , 32, color, array2)
    matrix.SwapOnVSync(canvas)  # Update the matrix to display the text

def gettrainsit():
    url = "http://transport.opendata.ch/v1/stationboard"
    params = {'station': 'Zürich, Farbhof', 'limit': '10'}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()["stationboard"]
        # Process the data as needed
        res=[]
        for val in data:
            departure_time = datetime.datetime.strptime(val["stop"]["departure"], "%Y-%m-%dT%H:%M:%S%z")
            current_time = datetime.datetime.now(departure_time.tzinfo)
            time_until_departure = departure_time - current_time
            deltaT = int(time_until_departure.total_seconds() / 60)
            #print(val["to"]+" "+time +" "+val["category"]+" "+val["number"]+" "+val["operator"]+" "+str(val["stop"]["prognosis"]))
            if deltaT>=0:
                if val['to'] in ["Zurich Tiefenbrunnen, Bahnhof","Zürich, Kienastenwies","Zürich Altstetten, Bahnhof"]:
                    if deltaT==0:
                        res.append(val["category"]+val["number"]+" o-oD")
                    else:
                        res.append(val["category"]+val["number"]+" "+str(deltaT)+"'")
        return res[:3]
    else:
        print("Error:", response.status_code)
def getspace():


    return "Falcon 9"
try:
    while True:
        data=gettrainsit()
        data2=getspace()
        draw_stacked_text(data,data2)  # Continuously draw text
        time.sleep(60)  # Adjust delay if needed (e.g., 1 second delay)
except KeyboardInterrupt:
    canvas.Clear()  # Clear the display when interrupted
    matrix.SwapOnVSync(canvas)
    print("Display cleared and script terminated.")

