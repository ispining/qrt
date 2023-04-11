"""
Курс Путь к автоматизации, основы python

1. Что такое python
2. Где используется python
3. Какие фирмы используют python
4. О чем будет курс
5.

"""


import threading
import time

import serial

stop_loops = False

ser = serial.Serial('COM3', 9600)

def read_loop():
    while True:
        # Читаем данные из Serial Port
        line = ser.read_all()
        # Если данные не пусты
        if line:
            # Декодируем байты в строку и выводим на экран
            line = line.decode().strip()
            print()
            print(line)
        if stop_loops:
            break

# Открываем Serial Port

time.sleep(5)
# Отправляем команду в Serial Port
ser.write(b'fire')

threading.Thread(target=read_loop, daemon=True).start()
threading.main_thread()

time.sleep(3)
# Закрываем Serial Port
stop_loops = True
ser.close()

