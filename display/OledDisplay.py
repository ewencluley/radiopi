from display.Display import Display


class OledDisplay(Display):
    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont

    # Raspberry Pi pin configuration:
    RST = None  # on the PiOLED this pin isnt used
    # Note the following are only used with SPI:
    DC = 24
    SPI_PORT = 0
    SPI_DEVICE = 0

    def __init__(self) -> None:
        # 128x32 display with hardware SPI:
        self.disp = display.drive.SSD1305.SSD1305_128_32(
            rst=self.RST, dc=self.DC, spi=display.drive.SPI.SpiDev(self.SPI_PORT, self.SPI_DEVICE, max_speed_hz=8000000)
        )
        self.disp.begin()
        self.disp.clear()
        self.disp.display()

        self.image = self.Image.new('1', (self.disp.width, self.disp.height))
        self.draw = self.ImageDraw.Draw(self.image)
        self.padding = 0
        self.top = self.padding
        self.bottom = self.disp.height - self.padding
        self.big_font = self.ImageFont.truetype('font/enhanced_dot_digital-7.ttf', 16)
        self.small_font = self.ImageFont.truetype('font/04B_08.ttf', 8)

    def clear(self):
        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.disp.width, self.disp.height), outline=0, fill=0)

    def draw_text(self, position, text, font):
        self.draw.text((position[0], self.top + position[1]), text, font=font, fill=255)

    def update(self):
        self.disp.image(self.image)
        self.disp.display()
