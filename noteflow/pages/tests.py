import json

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Note


class ModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_note_creation(self):
        note = Note.objects.create(
            user=self.user,
            text='Test note content'
        )
        self.assertEqual(note.text, 'Test note content')
        self.assertEqual(note.user.username, 'testuser')

    def test_note_delete(self):
        note = Note.objects.create(
            user=self.user,
            text='Note to be deleted'
        )
        note_id = note.id
        note.delete()
        with self.assertRaises(Note.DoesNotExist):
            Note.objects.get(id=note_id)

    def test_note_edit(self):
        note = Note.objects.create(
            user=self.user,
            text='Original text'
        )
        new_text = 'Updated text'
        note.text = new_text
        note.save()

        updated_note = Note.objects.get(id=note.id)
        self.assertEqual(updated_note.text, new_text)


class ViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.note = Note.objects.create(
            user=self.user,
            text='Test note'
        )

    def test_notes_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('notes'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test note')

    def test_notes_view_unauthenticated(self):

        # Выход из системы, если пользователь был авторизован
        self.client.logout()
        response = self.client.get(reverse('notes'))

        # Проверяем редирект на страницу входа (обычно 302)
        self.assertEqual(response.status_code, 302)

        # Если используется редирект на login, проверяем его
        if response.status_code == 302:
            self.assertTrue(response.url.startswith('/login/'))

    def test_create_note_api(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('create_note'),
            data=json.dumps({'text': 'API test note'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(Note.objects.count(), 2)

    def test_edit_note_api(self):
        self.client.login(username='testuser', password='testpass123')
        updated_text = 'Updated test note content'

        # Отправляем запрос на обновление заметки
        response = self.client.post(
            reverse('edit_note', args=[self.note.id]),
            data=json.dumps({'text': updated_text}),
            content_type='application/json'
        )

        # Проверяем ответ
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')

        # Проверяем, что заметка действительно изменилась в БД
        updated_note = Note.objects.get(id=self.note.id)
        self.assertEqual(updated_note.text, updated_text)



