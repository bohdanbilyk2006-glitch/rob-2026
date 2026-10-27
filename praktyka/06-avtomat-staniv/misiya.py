from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor
import time
import math

tank = MoveTank(OUTPUT_A, OUTPUT_B)
color = ColorSensor(INPUT_1)
ultra = UltrasonicSensor(INPUT_2)
PORIH_PIDHODU = 45
PORIH_MITKY = 67
ZAIZD_CM = 18
DIAMETR_KOLESA = 5.6
TIMEOUT_STANU = 20
LIMIT_MISIYI = 90


def chervone():
    r, g, b = color.rgb
    return 100 * r / (r + g + b) if r + g + b > 0 else 0


def polozhennya_kolis():
    return (tank.left_motor.position + tank.right_motor.position) / 2


def perekhid(novyi, prychyna):
    global stan, vkhid
    tank.off()
    print("%.1f с: %s -> %s (%s)" %
          (time.time() - pochatok, stan, novyi, prychyna))
    stan = novyi
    vkhid = time.time()


time.sleep(0.5)
pochatok = time.time()
vkhid = pochatok
stan = "poshuk"
uspikh = False
pochatok_mitky = None
print("Старт: poshuk")

while stan != "gotovo":
    zaraz = time.time()
    r = chervone()

    if zaraz - pochatok >= LIMIT_MISIYI:
        perekhid("gotovo", "ліміт місії 90 с")
        continue
    if zaraz - vkhid >= TIMEOUT_STANU:
        print("таймаут у стані", stan)
        perekhid("gotovo", "таймаут 20 с")
        continue
    if ultra.distance_centimeters < 15:
        perekhid("gotovo", "перешкода ближче 15 см")
        continue

    if stan == "poshuk":
        if r >= PORIH_PIDHODU:
            perekhid("pidhid", "частка червоного %.1f%%" % r)
        else:
            tank.on(SpeedPercent(5), SpeedPercent(5))

    elif stan == "pidhid":
        # Відлік 18 см починається лише після виявлення червоної мітки.
        if pochatok_mitky is None and r >= PORIH_MITKY:
            pochatok_mitky = polozhennya_kolis()
            print("%.1f с: мітку знайдено, заїжджаю на 18 см" % (zaraz - pochatok))
        proydeno = 0
        if pochatok_mitky is not None:
            proydeno = (polozhennya_kolis() - pochatok_mitky) * math.pi * DIAMETR_KOLESA / 360
        if proydeno >= ZAIZD_CM:
            perekhid("zupynka", "заїзд %.1f см; червоне %.1f%%" % (proydeno, r))
        else:
            tank.on(SpeedPercent(4), SpeedPercent(4))

    elif stan == "zupynka":
        if r < PORIH_MITKY:
            perekhid("gotovo", "мітку втрачено під час зупинки")
        elif zaraz - vkhid >= 3:
            uspikh = True
            perekhid("gotovo", "3 с на мітці")

    time.sleep(0.02)

tank.off()
print("Результат:", "успіх" if uspikh else "не виконано")
print("Час: %.1f с" % (time.time() - pochatok))
