from django.test import TestCase
from django.urls import reverse


class SolverViewTests(TestCase):

    def test_quadratic_two_roots(self):
        response = self.client.get(reverse("solve"), {"a": "1", "b": "-3", "c": "2"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Корни уравнения: x1 = 2.0, x2 = 1.0", html=True)

    def test_quadratic_one_root(self):
        response = self.client.get(reverse("solve"), {"a": "1", "b": "-2", "c": "1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Корень уравнения: x = 1.0", html=True)

    def test_quadratic_no_real_roots(self):
        response = self.client.get(reverse("solve"), {"a": "1", "b": "0", "c": "1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Нет действительных корней", html=True)

    def test_linear_equation(self):
        response = self.client.get(reverse("solve"), {"a": "0", "b": "2", "c": "-4"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Корень линейного уравнения: x = 2.0", html=True)

    def test_a_and_b_zero(self):
        response = self.client.get(reverse("solve"), {"a": "0", "b": "0", "c": "1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Ошибка: коэффициенты 'a' и 'b' не могут быть равны нулю одновременно.",
            html=True,
        )

    def test_invalid_input(self):
        response = self.client.get(reverse("solve"), {"a": "abc", "b": "2", "c": "1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ошибка: введены некорректные данные", html=True)
