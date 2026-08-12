import qrcode
from qrcode.constants import ERROR_CORRECT_H


#  Состояние программы: значения по умолчанию
data = "https://proverka.com"  # параметры URL или текст
box_size = 10                  # размер клетки в пикселях
error_level = ERROR_CORRECT_H  # уровень коррекции ошибок
state = 1  # текущий этап: 1 - ввод данных, 2 - настройка параметров, 3 - генерация

def main_menu():
    """ Делаем главное меню """
    global state
    
    print("\n Генератор QR-кодов")
    print("-" * 40)
    
    if state == 1:
        print("1. Ввести данные для QR-кода ")
        print("0. Выход")
    elif state == 2:
        print("2. Выбрать параметры для настройки генерации")
        print("0. Выход")
    elif state == 3:
        print("3. Сгенерировать и сохранить QR-код")
        print("0. Выход")
    
    print("-" * 40) 

def enter_data():
    """ Запрос данных у пользователя """
    global data, state
    data = input("Введите текст или ссылку: ").strip() 
    print("Данные сохранены.")
    state = 2  # переходим к следующему этапу

def choose_params():
    """ Здесь происходит изменение размера и уровня коррекции """
    global box_size, error_level, state
    print(f"Текущие параметры: размер={box_size}, уровень=H")
    
    size = input("Новый размер клеточки (Enter — не менять): ").strip()
    if size:
        box_size = int(size)
        
    level = input("Уровень коррекции L/M/Q/H (Enter — не менять): ").strip().upper()
    if level in ['L', 'M', 'Q', 'H']:
        if level == 'L':
            error_level = qrcode.constants.ERROR_CORRECT_L
        elif level == 'M':
            error_level = qrcode.constants.ERROR_CORRECT_M
        elif level == 'Q':
            error_level = qrcode.constants.ERROR_CORRECT_Q
        elif level == 'H':
            error_level = qrcode.constants.ERROR_CORRECT_H
    
    state = 3  # переходим к следующему этапу
    print("Параметры обновлены.")

def generate():
    """Генерируем QR из текущих данных и сохраняем в файл."""
    global state
    
    if not data:
        print("Данные пустые. Сначала выбери пункт 1.")
        return

    # Создание объекта QR-кода с текущими настройками
    qr = qrcode.QRCode(
        version=None,
        error_correction=error_level,
        box_size=box_size,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qr_result.png")
    print("Готово: QR-код сохранен в qr_result.png")
    
    # После генерации можно вернуться к началу
    state = 1

def main():
    """Главный цикл программы."""
    global state
    
    while True:
        main_menu()
        choice = input("Выбери пункт: ").strip()

        if state == 1 and choice == "1":
            enter_data()
        elif state == 2 and choice == "2":
            choose_params()
        elif state == 3 and choice == "3":
            generate()
        elif choice == "0":
            print("Вы вышли из программы")
            break
        else:
            print("Неизвестный пункт. Попробуй ещё раз.")

# Запускаем программу
if __name__ == "__main__":
    main()