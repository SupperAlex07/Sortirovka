import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#  ряд чисел для проверки -1 18 -7 23 -4 29 -12 2 -26 15 -9 30 -5 21 -11 3 -27 16 -8 24 -13 19 -6 28 -14 10 25 -17 22 -20


# ============================================================
# 1. Алгоритмы сортировки. Каждый алгоритм сохраняет состояния
#    списка, чтобы их можно было показать в анимации.
# ============================================================

def bubble_sort_steps(numbers):



    arr = numbers.copy()

   

    states = []

    for i in range(len(arr)):
        for j in range(len(arr) - 1 - i):
            states.append((arr.copy(), j, j + 1, None, "Сравнение"))
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                states.append((arr.copy(), j, j + 1, None, "Обмен"))
    states.append((arr.copy(), -1, -1, None, "Готово"))
    return arr, states


def insertion_sort_steps(numbers):
    arr = numbers.copy()

    

    states = []

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        states.append((arr.copy(), i, j, key, "Выбран элемент"))

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            states.append((arr.copy(), j, j + 1, key, "Сдвиг"))
            j -= 1

        arr[j + 1] = key
        states.append((arr.copy(), j + 1, i, key, "Вставка"))

    states.append((arr.copy(), -1, -1, None, "Готово"))
    return arr, states


def quick_sort_steps(numbers):
    arr = numbers.copy()

   

    states = []

    def sort(left, right):
        if left >= right:
            return

        pivot = arr[(left + right) // 2]
        i = left
        j = right

        while i <= j:
            while arr[i] < pivot:
                i += 1
            while arr[j] > pivot:
                j -= 1

            if i <= j:
                states.append((arr.copy(), i, j, pivot, "Сравнение с опорным элементом"))
                arr[i], arr[j] = arr[j], arr[i]
                states.append((arr.copy(), i, j, pivot, "Обмен"))
                i += 1
                j -= 1

        if left < j:
            sort(left, j)
        if i < right:
            sort(i, right)

    sort(0, len(arr) - 1)
    states.append((arr.copy(), -1, -1, None, "Готово"))
    return arr, states


def heap_sort_steps(numbers):
    arr = numbers.copy()

   

    states = []

    def left(i):
        return 2 * i + 1

    def right(i):
        return 2 * i + 2

    def max_heapify(size, index):
        largest = index
        l = left(index)
        r = right(index)

        if l < size and arr[l] > arr[largest]:
            largest = l
        if r < size and arr[r] > arr[largest]:
            largest = r

        if largest != index:
            states.append((arr.copy(), index, largest, None, "Восстановление кучи"))
            arr[index], arr[largest] = arr[largest], arr[index]
            states.append((arr.copy(), index, largest, None, "Обмен в куче"))
            max_heapify(size, largest)

    for i in range(len(arr) // 2 - 1, -1, -1):
        max_heapify(len(arr), i)

    states.append((arr.copy(), -1, -1, None, "Максимальная куча построена"))

    for i in range(len(arr) - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        states.append((arr.copy(), 0, i, None, "Максимум перенесён в конец"))
        max_heapify(i, 0)

    states.append((arr.copy(), -1, -1, None, "Готово"))
    return arr, states


# ============================================================
# 2. Ввод чисел и выбор алгоритма
# ============================================================

while True:
    try:
        text = input("Введите целые числа через пробел: ").split()

        if len(text) < 2:
            print("Ошибка: введите хотя бы два числа.")
            continue

        numbers = [int(value) for value in text]
        break

    except ValueError:
        print("Ошибка: вводите только целые числа, разделённые пробелами.")

print("\nВыберите вид сортировки:")
print("1 — Пузырьковая сортировка")
print("2 — Сортировка вставками")
print("3 — Быстрая сортировка")
print("4 — Сортировка кучей")

while True:
    choice = input("Введите номер (1–4): ").strip()

    match choice:
        case "1":
            algorithm = bubble_sort_steps
            algorithm_name = "Пузырьковая сортировка"
        case "2":
            algorithm = insertion_sort_steps
            algorithm_name = "Сортировка вставками"
        case "3":
            algorithm = quick_sort_steps
            algorithm_name = "Быстрая сортировка"
        case "4":
            algorithm = heap_sort_steps
            algorithm_name = "Сортировка кучей"
        case _:
            print("Ошибка: выберите номер от 1 до 4.")
            continue

    break

sorted_numbers, states = algorithm(numbers)


# ============================================================
# 3. Анимация
# ============================================================

fig, ax = plt.subplots(figsize=(10, 6))


def update(frame):
    ax.clear()

    current_array, first, second, pivot, action = states[frame]

    colors = []
    for index in range(len(current_array)):
        if index == first or index == second:
            colors.append("tomato")
        else:
            colors.append("lightgreen")

    # Горизонтальные столбцы подходят и для отрицательных чисел.
    ax.barh(range(len(current_array)), current_array, color=colors)
    ax.set_title(f"{algorithm_name}\nДействие: {action}")
    ax.set_xlabel("Значение")
    ax.set_ylabel("Индекс")
    ax.set_yticks(range(len(current_array)))
    ax.invert_yaxis()

    min_value = min(current_array)
    max_value = max(current_array)
    margin = max((max_value - min_value) * 0.1, 1)
    ax.set_xlim(min(0, min_value - margin), max(0, max_value + margin))

    if pivot is not None:
        ax.text(
            0.02, 0.96,
            f"Опорный элемент: {pivot}",
            transform=ax.transAxes,
            va="top"
        )

    ax.text(
        0.98, 0.96,
        f"Шаг: {frame + 1}/{len(states)}",
        transform=ax.transAxes,
        ha="right",
        va="top"
    )

    # Подписываем значения на столбцах.
    for index, value in enumerate(current_array):
        offset = margin * 0.08
        if value >= 0:
            ax.text(value + offset, index, str(value), va="center")
        else:
            ax.text(value - offset, index, str(value), va="center", ha="right")


animation = FuncAnimation(
    fig,
    update,
    frames=len(states),
    interval=350,
    repeat=False,
    cache_frame_data=False
)

plt.tight_layout()
plt.show()

print("\nВыбранный алгоритм:", algorithm_name)
print("Исходный ряд:", numbers)
print("Отсортированный ряд:", sorted_numbers)







