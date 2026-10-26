from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor
import time

tank = MoveTank(OUTPUT_A, OUTPUT_B)
color = ColorSensor(INPUT_1)

time.sleep(0.5)
tank.on(SpeedPercent(2), SpeedPercent(2))
for i in range(1, 21):
    r, g, b = color.rgb
    suma = r + g + b
    chastka = round(100 * r / suma, 1) if suma > 0 else 0
    print(i, chastka, r, g, b)
    time.sleep(0.5)
tank.off()
