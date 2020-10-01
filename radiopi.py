import subprocess
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import AdminServer
from drive import SPI
from drive import SSD1305
import Clock

# Raspberry Pi pin configuration:
RST = None  # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 24
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware SPI:
disp = SSD1305.SSD1305_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = 0
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
# Load default font.
# font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font_big = ImageFont.truetype('font/enhanced_dot_digital-7.ttf', 16)
font = ImageFont.truetype('font/04B_08.ttf', 8)
AdminServer.start_in_background()

try:
    while True:
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        cmd = "hostname -I | cut -d\' \' -f1"
        IP = subprocess.check_output(cmd, shell=True)
        cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell=True)
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell=True)
        cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
        Disk = subprocess.check_output(cmd, shell=True)
        Clock.update()
        time_str = Clock.get_time()
        alarm = Clock.get_alarm()
        alarm_str = f'{str(alarm.hour).zfill(2)}:{str(alarm.minute).zfill(2)} [{Clock.get_days_str(alarm.day_of_week)}]'

        # Write two lines of text.
        draw.text((20, top), time_str, font=font_big, fill=255)
        # draw.text((x, top + 8), str(CPU), font=font, fill=255)
        if Clock.should_alarm() and Clock.on_beat():
            draw.text((x, top + 16), '*** ALARM ***', font=font, fill=255)
        elif alarm.enabled:
            draw.text((x, top + 16), alarm_str, font=font, fill=255)
        draw.text((x, top + 25), str(IP), font=font, fill=255)

        # Display image.
        disp.image(image)
        disp.display()
        time.sleep(0.01)
except KeyboardInterrupt:
    AdminServer.shutdown()
