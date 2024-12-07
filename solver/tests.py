from django.test import TestCase
from django.urls import reverse

class SolverTests(TestCase):

    def test_solve_two_roots(self):
        response = self.client.get(reverse('solve'), {'a': 1, 'b': -3, 'c': 2})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Корни уравнения: x1 = 2.0, x2 = 1.0")

    def test_solve_one_root(self):
        response = self.client.get(reverse('solve'), {'a': 1, 'b': 2, 'c': 1})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Корень уравнения: x = -1.0")

    def test_solve_linear(self):
        response = self.client.get(reverse('solve'), {'a': 0, 'b': 2, 'c': -4})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Корень линейного уравнения: x = 2.0")

    def test_solve_no_real_roots(self):
        response = self.client.get(reverse('solve'), {'a': 1, 'b': 0, 'c': 1})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Нет действительных корней")

    def test_solve_invalid_input(self):
        response = self.client.get(reverse('solve'), {'a': 'abc', 'b': 'def', 'c': 'ghi'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ошибка: введены некорректные данные")


class TrainerTests(TestCase):

    def test_trainer_correct_solution(self):
        response = self.client.post(reverse('trainer'), {
            'a': 1, 'b': -3, 'c': 2,
            'solution': '1.0, 2.0'
        })
        self.assertEqual(response.status_code, 302)  # Перенаправление
        self.assertRedirects(response, f"{reverse('trainer')}?result=1&is_correct=True&correct_solution=1.0, 2.0&user_solution=1.0, 2.0")

    def test_trainer_incorrect_solution(self):
        response = self.client.post(reverse('trainer'), {
            'a': 1, 'b': -3, 'c': 2,
            'solution': '0.0, 0.0'
        })
        self.assertEqual(response.status_code, 302)  # Перенаправление
        self.assertRedirects(response, f"{reverse('trainer')}?result=1&is_correct=False&correct_solution=1.0, 2.0&user_solution=0.0, 0.0")

    def test_trainer_no_real_roots(self):
        response = self.client.post(reverse('trainer'), {
            'a': 1, 'b': 0, 'c': 1,
            'solution': 'нет корней'
        })
        self.assertEqual(response.status_code, 302)  # Перенаправление
        self.assertRedirects(response, f"{reverse('trainer')}?result=1&is_correct=True&correct_solution=Нет корней&user_solution=нет корней")
