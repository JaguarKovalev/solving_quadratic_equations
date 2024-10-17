import math

from django.shortcuts import render


def solve(request):
    a = request.GET.get("a", "0")
    b = request.GET.get("b", "0")
    c = request.GET.get("c", "0")

    try:
        a, b, c = float(a), float(b), float(c)
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

    return render(
        request,
        "solver/solve.html",
        {"equation": f"{a}x² + {b}x + {c} = 0", "roots": roots},
    )
