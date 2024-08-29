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
    first_three_chars = string[:3]
    return color_map.get(first_three_chars, graphics.Color(255, 255, 255))

def scroll_text(array,text,delay=0.05):
    offscreen_canvas = matrix.CreateFrameCanvas()
    
    pos = offscreen_canvas.width
    color=graphics.Color(255, 255, 255)

    while True:
        offscreen_canvas.Clear()
        length = graphics.DrawText(offscreen_canvas, font, pos,32, graphics.Color(255, 255, 255), text)
        for i in range (len(array)):
            color=getcolor(array[i])
            graphics.DrawText(offscreen_canvas, font, 0 , 0+(i+1)*line_height+i, color, array[i])
        
        pos -= 1
        if pos + length < 0:
            pos = offscreen_canvas.width

        time.sleep(delay)
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

def draw_stacked_text(array, array2):
    canvas.Clear()  # Clear previous content
    
    #graphics.DrawText(canvas, font, 0 , 32, color, array2)
    matrix.SwapOnVSync(canvas)  # Update the matrix to display the text

def time_until(target_time_str):
    target_datetime = datetime.datetime.fromisoformat(target_time_str.replace('Z', '+00:00'))
    now = datetime.datetime.now(datetime.timezone.utc)
    time_diff = target_datetime - now
    hours, remainder = divmod(time_diff.total_seconds(), 3600)
    minutes, _ = divmod(remainder, 60)
    if time_diff.total_seconds() < 0:
        hours, minutes = 0, 0
    return int(hours), int(minutes)
def gettrainsit():
    url = "http://transport.opendata.ch/v1/stationboard"
    params = {'station': 'Zürich, Farbhof', 'limit': '10'}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()["stationboard"]
        # Process the data as needed
        res=[]
        for val in data:
            if val['stop']['prognosis']['departure']!=None:
                departure_time = datetime.datetime.strptime(val['stop']['prognosis']['departure'], "%Y-%m-%dT%H:%M:%S%z")
            else:
                departure_time = datetime.datetime.strptime(val['stop']['departure'], "%Y-%m-%dT%H:%M:%S%z")
            current_time = datetime.datetime.now(departure_time.tzinfo)
            time_until_departure = departure_time - current_time
            deltaT = int(time_until_departure.total_seconds() / 60)
            deltaTs=int(time_until_departure.total_seconds() % 60)
            #print(val["to"]+" "+time +" "+val["category"]+" "+val["number"]+" "+val["operator"]+" "+str(val["stop"]["prognosis"]))
            if deltaT>=0:
                if val['to'] in ["Zurich Tiefenbrunnen, Bahnhof","Zürich, Kienastenwies","Zürich Altstetten, Bahnhof"]:
                    if deltaT==0:
                        res.append(val["category"]+val["number"]+" o-oD")
                    else:
                        res.append(val["category"]+val["number"]+" "+str(deltaT)+"'"+str(deltaTs))
        return res[:3]
    else:
        print("Error:", response.status_code)
def getspace():
    url='https://lldev.thespacedevs.com/2.2.0/launch/'
    url2='https://ll.thespacedevs.com/2.2.0/launch/upcoming/'
    params = {}  #add params
    response = requests.get(url2)

    if response.status_code == 200:
        data = response.json()[ "results"]
    else:
        print("Error:", response.status_code)
    for res in data:
        time=time_until(res["net"])
        if time[0]>0 and time[1]>0:
            output=res["name"]+" | "+str(time[0])+":"+str(time[1])+" |  "
            if res["weather_concerns"]!=None:
                    output+=res["weather_concerns"]
            return output 
        else:
            return "No launches"
try:
    while True:
        data=gettrainsit()
        data2=getspace()
        scroll_text(data,data2,delay=0.05)
        #draw_stacked_text(data,data2)  # Continuously draw text
        time.sleep(60)  # Adjust delay if needed (e.g., 1 second delay)
except KeyboardInterrupt:
    canvas.Clear()  # Clear the display when interrupted
    matrix.SwapOnVSync(canvas)
    print("Display cleared and script terminated.")

