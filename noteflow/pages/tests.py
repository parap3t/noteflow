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


