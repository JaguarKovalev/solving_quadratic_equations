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
        a = float(request.POST['a'])
        b = float(request.POST['b'])
        c = float(request.POST['c'])
        user_solution = request.POST.get('solution', '').strip()

        discriminant = b ** 2 - 4 * a * c
        if discriminant > 0:
            root1 = (-b + math.sqrt(discriminant)) / (2 * a)
            root2 = (-b - math.sqrt(discriminant)) / (2 * a)
            correct_solution_set = {round(root1, 2), round(root2, 2)}
        elif discriminant == 0:
            root = -b / (2 * a)
            correct_solution_set = {round(root, 2)}
        else:
            correct_solution_set = None

        if correct_solution_set is None:
            is_correct = user_solution.lower() == 'нет корней'
            correct_solution = "Нет корней"
        else:
            try:
                user_solution_set = {round(float(x.strip()), 2) for x in user_solution.split(',')}
                is_correct = user_solution_set == correct_solution_set
            except ValueError:
                is_correct = False
            correct_solution = ", ".join(map(str, sorted(correct_solution_set)))

        QuadraticSolution.objects.create(
            a=a, b=b, c=c,
            user_solution=user_solution,
            correct_solution=correct_solution,
            is_correct=is_correct
        )

        # Перенаправление на страницу с результатом
        return redirect(f"{reverse('trainer')}?result=1&is_correct={is_correct}&correct_solution={correct_solution}&user_solution={user_solution}")

    if 'result' in request.GET:
        is_correct = request.GET.get('is_correct') == 'True'
        correct_solution = request.GET.get('correct_solution', '')
        user_solution = request.GET.get('user_solution', '')
    else:
        is_correct = None
        correct_solution = None
        user_solution = None

    random_a = random.randint(1, 10)
    random_b = random.randint(-10, 10)
    random_c = random.randint(-10, 10)
    return render(request, 'solver/trainer.html', {
        'a': random_a, 'b': random_b, 'c': random_c,
        'user_solution': user_solution,
        'correct_solution': correct_solution,
        'is_correct': is_correct
    })