import qrcode # подгружаем библиотеку                       

from qrcode.constants import ERROR_CORRECT_H # взята готовая константа из библиотеки со значениями

# Создаём объект QR-кода с детальными настройками
qr = qrcode.QRCode(
    version = None,                         # библиотека подберает размер сетки под текст
    error_correction = ERROR_CORRECT_H,     # коррекции ошибок: L, M, Q, H
    box_size = 10,                          # параметр пикселей на одну клеточку
    border = 4,                             # белая рамка в 4 клеточки (стандарт)
)


qr.add_data("https://proverka.com") # в параметры вносим данные URL или текст
qr.make(fit = True)                  # автоматически подбирает version под размер данных


img = qr.make_image(fill_color = "black", back_color = "white") # создаем картинку, цвет QR-кода стандарт
img.save("qr_img.png")

# вывод какую version подобрала библиотека
print(" QR-кода готов и сохранен. Версия:", qr.version)
