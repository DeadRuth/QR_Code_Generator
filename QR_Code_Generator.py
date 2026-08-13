import qrcode
from qrcode.constants import (ERROR_CORRECT_L, ERROR_CORRECT_M,
                              ERROR_CORRECT_Q, ERROR_CORRECT_H)
from datetime import datetime

# --- Состояние программы: значения по умолчанию ---
data = ""                        # параметры URL или текст
box_size = 10                    # размер клетки в пикселях
error_level = ERROR_CORRECT_H    # уровень коррекции ошибок
state = 1                        # текущий этап: 1 - ввод, 2 - настройка, 3 - генерация

# Словарь: константа уровня коррекции -> буква для вывода на экран
LEVEL_NAMES = {
    ERROR_CORRECT_L: "L",
    ERROR_CORRECT_M: "M",
    ERROR_CORRECT_Q: "Q",
    ERROR_CORRECT_H: "H",
}

fill_color = "black"             # цвет QR-кода (передний план)
back_color = "white"             # цвет фона

# Допустимые цвета для проверки ввода
VALID_COLORS = {"black", "white", "red", "green", "blue", "yellow",
                "orange", "purple", "pink", "brown", "gray"}

def main_menu():
    """Выводит главное меню в зависимости от текущего этапа."""
    print("\nГенератор QR-кодов")
    print("-" * 40)

    if state == 1:
        print("1. Ввести данные для QR-кода")
        print("0. Выход")
    elif state == 2:
        print("2. Выбрать параметры генерации")
        print("0. Выход")
    elif state == 3:
        print("3. Сгенерировать и сохранить QR-код")
        print("0. Выход")

    print("-" * 40)


def enter_data():
    """Запрос данных у пользователя с проверкой пустоты и длины."""
    global data, state

    user_input = input("Введите текст или ссылку: ").strip()

    # Проверка на пустую строку
    if not user_input:
        print("Ошибка: Данные не могут быть пустыми.")
        return  # Не меняем state, остаемся на шаге 1

    # Проверка длины (QR-код >2000 символов невозможно отсканировать телефоном)
    if len(user_input) > 2000:
        print(f"Ошибка: Слишком длинный текст ({len(user_input)} символов). Максимум 2000.")
        return

    data = user_input
    print("Данные сохранены.")
    state = 2  # переходим к следующему этапу только при успехе

def choose_params():
    """Изменение размера, уровня коррекции и цветов с защитой от некорректного ввода."""
    global box_size, error_level, state, fill_color, back_color
    print(f"Текущие параметры: размер={box_size}, уровень={LEVEL_NAMES[error_level]}")
    
    # Безопасный ввод размера
    size = input("Новый размер клеточки (Enter — не менять): ").strip()
    if size:
        try:
            new_size = int(size)
            if new_size < 1 or new_size > 100:
                print("Размер должен быть от 1 до 100. Параметр не изменен.")
            else:
                box_size = new_size
                print("Размер обновлен.")
        except ValueError:
            print("Некорректное число. Параметр не изменен.")
    
    # Ввод уровня коррекции (безопасная проверка через список)
    level = input("Уровень коррекции L/M/Q/H (Enter — не менять): ").strip().upper()
    if level in ['L', 'M', 'Q', 'H']:
        if level == 'L':
            error_level = ERROR_CORRECT_L
        elif level == 'M':
            error_level = ERROR_CORRECT_M
        elif level == 'Q':
            error_level = ERROR_CORRECT_Q
        elif level == 'H':
            error_level = ERROR_CORRECT_H
        print(f"Уровень коррекции обновлен на {level}.")
    elif level:
        print("Недопустимый уровень. Используйте L, M, Q или H.")
    
    # Выбор цветов
    print(f"Текущие цвета: код={fill_color}, фон={back_color}")
    print("Доступные цвета:", ", ".join(sorted(VALID_COLORS)))
    
    # Цикл для цвета кода - повторяем, пока не будет верный ввод
    while True:
        new_fill = input("Цвет QR-кода (Enter — не менять): ").strip().lower()
        if not new_fill:
            print("Цвет кода не изменен.")
            break
        if new_fill in VALID_COLORS:
            fill_color = new_fill
            print("Цвет кода обновлен.")
            break
        print("Недопустимый цвет. Попробуйте еще раз.")
    
    # Цикл для цвета фона - повторяем, пока не будет верный ввод
    while True:
        new_back = input("Цвет фона (Enter — не менять): ").strip().lower()
        if not new_back:
            print("Цвет фона не изменен.")
            break
        if new_back in VALID_COLORS:
            back_color = new_back
            print("Цвет фона обновлен.")
            break
        print("Недопустимый цвет. Попробуйте еще раз.")
    
    # Предупреждение, если цвета совпадают и код станет нечитаемым
    if fill_color == back_color:
        print("Внимание: цвета кода и фона совпадают, QR-код может не считаться.")
    
    state = 3
    print("Параметры обновлены.")


def get_filename():
    """Возвращает имя файла для сохранения.
    Если пользователь нажал Enter, имя генерируется автоматически."""

    user_name = input("Имя файла (Enter - автоматическое): ").strip()

    # Пользователь ничего не ввёл - создаём имя автоматически
    if not user_name:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return "qr_" + timestamp + ".png"

    # Проверка на недопустимые символы в имени файла
    forbidden = '\\/:*?"<>|'
    for ch in user_name:
        if ch in forbidden:
            print(f"Имя файла содержит недопустимый символ: {ch}")
            return None

    # Проверка длины имени
    if len(user_name) > 100:
        print("Имя файла слишком длинное. Максимум 100 символов.")
        return None

    # Если расширение не указано, добавляем .png
    if not user_name.lower().endswith(".png"):
        user_name += ".png"

    return user_name


def generate():
    """Генерируем QR из текущих данных и сохраняем в файл с обработкой ошибок."""
    global state

    if not data:
        print("Данные пустые. Сначала выбери пункт 1.")
        return

    filename = get_filename()
    if filename is None:
        print("Сохранение отменено из-за неверного имени файла.")
        return

    try:
        # Создание объекта QR-кода
        qr = qrcode.QRCode(
            version=None,
            error_correction=error_level,
            box_size=box_size,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        img.save(filename)

        print(f"Готово: QR-код сохранен в {filename}")
        state = 1

    except PermissionError:
        print(f"Ошибка сохранения: Нет прав на запись или файл '{filename}' занят другим процессом.")
    except OSError as e:
        print(f"Ошибка файловой системы: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка при генерации: {e}")


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