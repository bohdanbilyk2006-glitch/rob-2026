"""Робота 2. Переклад блоків із власної роботи 1 у Python для Gears.

Перед запуском скиньте симуляцію: початковий кут гіроскопа має бути 0°.
Параметри та порядок команд збережено зі скриншота першої роботи.
"""

from ev3dev2.motor import LargeMotor, MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_3
from ev3dev2.sensor.lego import GyroSensor

motor_a = LargeMotor(OUTPUT_A)
motor_b = LargeMotor(OUTPUT_B)
tank = MoveTank(OUTPUT_A, OUTPUT_B)
gyro = GyroSensor(INPUT_3)

data = 90
rotation = gyro.angle

for _ in range(4):
    tank.on_for_seconds(SpeedPercent(20), SpeedPercent(20), 2)

    # «Повторювати до rotation >= data» означає «поки rotation < data».
    while rotation < data:
        motor_a.on(SpeedPercent(3))
        motor_b.on(SpeedPercent(-3))
        rotation = gyro.angle
        print(rotation)

    data = data + 90

motor_a.off(brake=True)
motor_b.off(brake=True)
