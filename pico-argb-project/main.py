"""
Simple ARGB LED Rainbow Cycle
Continuous rainbow effect for Raspberry Pi Pico
"""

from machine import Pin
from neopixel import NeoPixel
import time
import math

# LED Strip Configuration
LED_COUNT = 60      # Number of LEDs in your strip
LED_PIN = 0         # GPIO pin connected to LED data line

# Initialize LED strip
pin = Pin(LED_PIN, Pin.OUT)
strip = NeoPixel(pin, LED_COUNT)

def clear_strip():
    """Turn off all LEDs"""
    for i in range(LED_COUNT):
        strip[i] = (0, 0, 0)
    strip.write()

def set_all_color(r, g, b):
    """Set all LEDs to the same color"""
    for i in range(LED_COUNT):
        strip[i] = (r, g, b)
    strip.write()

def hsv_to_rgb(h, s, v):
    """Convert HSV to RGB (simplified)"""
    h = h / 360.0
    s = s / 100.0
    v = v / 100.0
    
    if s == 0.0:
        return (int(v * 255), int(v * 255), int(v * 255))
    
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    
    if i == 0:
        r, g, b = v, t, p
    elif i == 1:
        r, g, b = q, v, p
    elif i == 2:
        r, g, b = p, v, t
    elif i == 3:
        r, g, b = p, q, v
    elif i == 4:
        r, g, b = t, p, v
    else:
        r, g, b = v, p, q
    
    return (int(r * 255), int(g * 255), int(b * 255))

def rainbow_cycle():
    """Continuous rainbow cycle effect"""
    print("Starting continuous rainbow cycle...")
    print("Press Ctrl+C to stop")
    
    offset = 0
    while True:
        for i in range(LED_COUNT):
            hue = (i * 360 // LED_COUNT + offset) % 360
            r, g, b = hsv_to_rgb(hue, 100, 50)  # 50% brightness
            strip[i] = (r, g, b)
        strip.write()
        offset = (offset + 2) % 360  # Speed of rainbow movement
        time.sleep(0.05)  # Smooth animation

if __name__ == "__main__":
    try:
        rainbow_cycle()
    except KeyboardInterrupt:
        print("\nStopping rainbow cycle...")
        clear_strip()
    except Exception as e:
        print(f"Error: {e}")
        clear_strip()
