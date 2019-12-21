#!/usr/bin/python3

import RPi.GPIO as gpio
import spidev
from time import sleep

# Create spi object
spi = spidev.SpiDev()
# Open spi port 0, device (CS) 0
spi.open(0,0)
spi.bits_per_word = 8
spi.max_speed_hz = 10000000
spi.mode = 0

gpio.setwarnings(False)
# Set mode: BOARD pines physical, BCM pines leveles
gpio.setmode(gpio.BOARD)
led = 7
ce = 15
irq = 16

gpio.setup(led, gpio.OUT, initial = gpio.LOW)
gpio.setup(ce,gpio.OUT, initial = gpio.LOW)
gpio.setup(irq, gpio.IN, pull_up_down = gpio.PUD_DOWN)

def configNrf():
	gpio.output(ce, gpio.LOW);

	#TX_ADDR
	spi.xfer2([0x2A, 0x78, 0x78, 0x78, 0x78, 0x78])

	# EN_AA Habilite Auto Ack
	spi.xfer2([0x21, 0x01])

	#EN_RXADD active Pipe0
	spi.xfer2([0x22, 0x01])

	#SETUP_AW
	spi.xfer2([0x23, 0x03])

	#SETUP_RETR
	spi.xfer2([0x24, 0x00])

	#RF_CH
	spi.xfer2([0x25, 0x0C])

	#CONFIG Colocamos en modo recepcion, y definimos CRC de 2 Bytes
	spi.xfer2([0x20, 0x0F])

	#tiempo para salir del modo stanby y entrar en modo recepcion
	sleep(2)
	gpio.output(ce, gpio.HIGH)
	sleep(0.15)
def envia_datos():
	gpio.output(ce, gpio.LOW)

	#STATUS
	spi.xfer2([0x27, 0x70])

	#W_TX_PAYLOAD
	 

def intEx(channel):
	print("Interrupcion")

gpio.add_event_detect(irq,gpio.FALLING, callback = intEx, bouncetime = 300)

try:
	while True:
		gpio.output(led,gpio.HIGH)
		sleep(0.2);
		gpio.output(led, gpio.LOW)
		sleep(0.2)
except KeyboardInterrupt:
	#gpio.output(led,gpio.LOW)
	spi.close()
	gpio.cleanup()

gpio.cleanup()
spi.close()
