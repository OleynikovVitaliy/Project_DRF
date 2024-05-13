from rest_framework.test import APITestCase, APIClient
from users.models import User
from lms.models import Well, Lesson, Subscription
from django.urls import reverse
from rest_framework import status


class LessonTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email="admin@admin.ru")
        self.user.set_password('12345')
        self.client.force_authenticate(user=self.user)
        self.well = Well.objects.create(title="test")
        self.lesson = Lesson.objects.create(title='test', well=self.well,
                                            video_link='youtube.com/skipro')

    def test_lesson_create(self):
        """Тестирование создания уроков"""
        url = reverse('lms:lesson_create')
        data = {
            'title': 'test',
            'description': 'test',
            'video_link': 'youtube.com/skipro'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        """Тестирование обновления уроков"""
        url = reverse('lms:lesson_update', args=(self.lesson.pk,))
        data = {
            'title': 'test',
            'video_link': 'youtube.com/skipro'
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), 'test')

    def test_lesson_delete(self):
        """Тестирование удаления уроков"""
        url = reverse('lms:lesson_delete', kwargs={'pk': self.lesson.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """Тестирование вывода списка уроков"""
        url = reverse('lms:lesson_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.all().count(), 1)


class SubscriptionTestCase(APITestCase):
    """Тестирование управления подписками"""

    def setUp(self):
        self.user = User.objects.create(email="admin@admin.ru")
        self.user.set_password('12345')
        self.client.force_authenticate(user=self.user)
        self.well = Well.objects.create(title="test", owner=self.user)
        self.data = {"user": self.user.pk, "well": self.well.pk}

    def test_subscribe(self):
        """ Добавление подписки"""
        url = reverse('lms:subscribe', args=(self.well.pk,))
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'Подписка добавлена'})

    def test_unsubscribe(self):
        """ Удаление подписки"""
        url = reverse('lms:subscribe', args=(self.well.pk,))
        Subscription.objects.create(well=self.well, user=self.user)
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'Подписка удалена'})
