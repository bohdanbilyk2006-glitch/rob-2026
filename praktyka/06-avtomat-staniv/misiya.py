from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor
import time

tank = MoveTank(OUTPUT_A, OUTPUT_B)
color = ColorSensor(INPUT_1)
ultra = UltrasonicSensor(INPUT_2)
PORIH_PIDHODU = 45
PORIH_MITKY = 67
TIMEOUT_STANU = 20
LIMIT_MISIYI = 90


def chervone():
    r, g, b = color.rgb
    suma = r + g + b
    return 100 * r / suma if suma > 0 else 0


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
            tank.on(SpeedPercent(2), SpeedPercent(2))

    elif stan == "pidhid":
        if r >= PORIH_MITKY:
            perekhid("zupynka", "мітка %.1f%%" % r)
        else:
            tank.on(SpeedPercent(1), SpeedPercent(1))

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
