import qrcode

img_qr = qrcode.make("проверка")
img_qr.save("qr_img.png")
print(" QR-Код сохранен в папку проекта. Отсканировать код телефоном.")
