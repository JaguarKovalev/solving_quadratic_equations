import math
import random
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from .models import QuadraticSolution
from django.urls import reverse

def menu(request):
    return render(request, 'solver/menu.html')

def solve(request):
    a = request.GET.get("a", "0")
    b = request.GET.get("b", "0")
    c = request.GET.get("c", "0")

    try:
        a, b, c = float(a), float(b), float(c)

        if a == 0 and b == 0 and c == 0:
            roots = "Ошибка: уравнение не определено (все коэффициенты равны нулю)."
        elif a == 0:
            if b == 0:
                roots = "Ошибка: коэффициенты 'a' и 'b' не могут быть равны нулю одновременно."
            else:
                root = -c / b
                roots = f"Корень линейного уравнения: x = {root}"
        else:
            discriminant = b**2 - 4 * a * c

            if discriminant > 0:
                root1 = (-b + math.sqrt(discriminant)) / (2 * a)
                root2 = (-b - math.sqrt(discriminant)) / (2 * a)
                roots = f"Корни уравнения: x1 = {root1}, x2 = {root2}"
            elif discriminant == 0:
                root = -b / (2 * a)
                roots = f"Корень уравнения: x = {root}"
            else:
                roots = "Нет действительных корней"
    except ValueError:
        roots = "Ошибка: введены некорректные данные"

    context = {
        "equation": f"{a}x² + {b}x + {c} = 0",
        "roots": roots
    }
    return render(
        request,
        "solver/solve.html",
        context,
    )

def trainer(request):
    if request.method == 'POST':
        # Считываем коэффициенты
        a = float(request.POST['a'])
        b = float(request.POST['b'])
        c = float(request.POST['c'])

        # Получаем пользовательский ввод (заменяем запятую на точку)
        root1_raw = request.POST.get('root1', '').replace(',', '.').strip()
        root2_raw = request.POST.get('root2', '').replace(',', '.').strip()

        # Если нажата кнопка "Нет корней"
        if request.POST.get('solution') == "нет корней":
            user_solution = "нет корней"
            user_solution_list = []
        else:
            # формируем список из введённых значений (если поле пустое, игнорируем)
            user_solution_list = list(filter(None, [root1_raw, root2_raw]))
            user_solution = ", ".join(user_solution_list)

        # Вычисляем дискриминант
        discriminant = b**2 - 4*a*c

        # Находим "истинные" корни (без округления)
        if discriminant < 0:
            correct_roots = None
        elif abs(discriminant) < 1e-15:
            # Один корень
            correct_roots = [(-b) / (2*a)]
        else:
            r1 = (-b + math.sqrt(discriminant)) / (2*a)
            r2 = (-b - math.sqrt(discriminant)) / (2*a)
            correct_roots = sorted([r1, r2])

        # ---- ЛОГИКА ПРОВЕРКИ "ОКРУГЛЕНИЕ ИЛИ ОТБРОС" ----
        def decimal_places(s):
            """Определяем сколько символов после точки пользователь указал.
               Если точки нет, считаем 0."""
            if '.' in s:
                return len(s.split('.')[-1])
            return 0

        # Эта функция вернёт True, если user_val «равен» корню correct_val
        # при допущении, что пользователь мог либо округлить, либо отбросить дробную часть
        # до d знаков (d >= 2).
        def matches_round_or_trunc(user_val, correct_val, d):
            """
            d - число знаков после запятой, которое пользователь 'формально' задал.
            Проверяем, совпадает ли user_val с:
              - округлённым correct_val до d знаков,
              - или усечённым correct_val до d знаков.
            """
            # 1) округление:
            rounded_val = round(correct_val, d)

            # 2) усечение (truncation):
            factor = 10**d
            truncated_val = math.floor(correct_val * factor) / factor

            eps = 1e-9  # небольшой допуск из-за float
            if abs(user_val - rounded_val) < eps:
                return True
            if abs(user_val - truncated_val) < eps:
                return True
            return False

        # Теперь, если уравнение не имеет корней:
        if correct_roots is None:
            is_correct = (user_solution.lower() == "нет корней")
            correct_solution = "нет корней"
        else:
            # Уравнение имеет корни correct_roots (1 или 2 шт)
            if not user_solution_list:
                # Пользователь не ввёл ничего, но корни существуют
                is_correct = False
            else:
                # Для проверки нам нужно сопоставить каждый пользовательский корень
                # с каким-то правильным корнем (как множества, порядок не важен)
                if len(user_solution_list) != len(correct_roots):
                    # Количество введённых корней не совпадает
                    is_correct = False
                else:
                    # Преобразуем ввод пользователя в числа
                    try:
                        user_vals = [float(x) for x in user_solution_list]
                    except ValueError:
                        # если введено что-то не парсящееся
                        user_vals = []
                    
                    # Пока предположим, что всё совпадает
                    matched = [False]*len(correct_roots)
                    is_correct_temp = True

                    # Проверяем каждый user_val в "мультимножестве" correct_roots:
                    for uv_str, uv in zip(user_solution_list, user_vals):
                        # Определяем d — кол-во знаков, но минимум 2
                        d = max(decimal_places(uv_str), 2)

                        found_pair = False
                        for i, correct_val in enumerate(correct_roots):
                            if not matched[i]:
                                if matches_round_or_trunc(uv, correct_val, d):
                                    matched[i] = True
                                    found_pair = True
                                    break
                        if not found_pair:
                            is_correct_temp = False
                            break
                    
                    if not all(matched):
                        is_correct_temp = False

                    is_correct = is_correct_temp

            # Формируем красивый вывод «правильных» корней. 
            # Для дружелюбного отображения — будем отображать каждый корень 
            # с 4 знаками (например), чтоб пользователь видел, каково "точное" значение.
            # Или можно оставить только 2-3, но иногда хочется чуть больше точности.
            correct_solution_list = [f"{cr:.4f}" for cr in correct_roots]
            correct_solution = ", ".join(correct_solution_list)

        # Сохраняем результат в БД
        QuadraticSolution.objects.create(
            a=a, b=b, c=c,
            user_solution=user_solution,
            correct_solution=correct_solution,
            is_correct=is_correct
        )

        # Редирект (POST -> GET)
        return redirect(
            f"{reverse('trainer')}?result=1&is_correct={is_correct}"
            f"&correct_solution={correct_solution}&user_solution={user_solution}"
        )

    # Если GET: показываем результат
    if 'result' in request.GET:
        is_correct = (request.GET.get('is_correct') == 'True')
        correct_solution = request.GET.get('correct_solution', '')
        user_solution = request.GET.get('user_solution', '')
    else:
        is_correct = None
        correct_solution = None
        user_solution = None

    # Генерация случайных коэффициентов
    random_a = random.randint(1, 10)  # a != 0
    random_b = random.randint(-10, 10)
    random_c = random.randint(-10, 10)

    return render(request, 'solver/trainer.html', {
        'a': random_a,
        'b': random_b,
        'c': random_c,
        'user_solution': user_solution,
        'correct_solution': correct_solution,
        'is_correct': is_correct
    })
