from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_3
from ev3dev2.sensor.lego import GyroSensor
import time

tank = MoveTank(OUTPUT_A, OUTPUT_B)
gyro = GyroSensor(INPUT_3)
time.sleep(0.5)

print("Прогноз: 90 градусів")
print("Початковий кут:", gyro.angle)

# 10 поворотів на час: 20%, 1 секунда.
na_chas = []
poperednii = gyro.angle
print("НА ЧАС")
for i in range(1, 11):
    tank.on_for_seconds(SpeedPercent(20), SpeedPercent(-20), 1.0)
    time.sleep(0.5)
    teper = gyro.angle
    kut = teper - poperednii
    na_chas.append(kut)
    print(i, kut)
    poperednii = teper

# 10 поворотів до показу гіроскопа 90 градусів.
po_gyro = []
print("ПО ГІРОСКОПУ")
for i in range(1, 11):
    gyro.reset()
    tank.on(SpeedPercent(20), SpeedPercent(-20))
    while gyro.angle < 90:
        pass
    tank.off()
    time.sleep(0.5)
    kut = gyro.angle
    po_gyro.append(kut)
    print(i, kut)

print("На час:", na_chas)
print("По гіроскопу:", po_gyro)
print("Середнє на час:", sum(na_chas) / 10)
print("Розкид на час:", max(na_chas) - min(na_chas))
print("Середнє по гіроскопу:", sum(po_gyro) / 10)
print("Розкид по гіроскопу:", max(po_gyro) - min(po_gyro))
print("ГОТОВО")
