from django.test import TestCase
from django.urls import reverse
from .models import QuadraticSolution

class SolverTests(TestCase):
    def test_solver_correct_solution(self):
        response = self.client.get(reverse('solve') + '?a=1&b=-3&c=2')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Решение: x₁ = 2.0, x₂ = 1.0')

    def test_solver_no_real_roots(self):
        response = self.client.get(reverse('solve') + '?a=1&b=0&c=1')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Действительных корней нет')

    def test_solver_linear_equation(self):
        response = self.client.get(reverse('solve') + '?a=0&b=2&c=-4')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Решение: x = 2.0')

    def test_trainer_view(self):
        response = self.client.get(reverse('trainer'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тренажёр для решения квадратных уравнений')

    def test_trainer_submission(self):
        response = self.client.post(reverse('trainer'), {
            'a': 1, 'b': -3, 'c': 2, 'solution': '2,1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Верно')
        self.assertEqual(QuadraticSolution.objects.count(), 1)
