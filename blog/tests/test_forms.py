from django.test import TestCase
from blog.forms import PostForm
from blog.models import Post
from django.contrib.auth.models import User


class PostFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', email='rlukianchyk@gmail.com', password='password123')

    def test_valid_post_form(self):
        form_data = {'content': 'Test content'}
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_post_form(self):
        form_data = {'content': ''}
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_save_post_form(self):
        form_data = {'content': 'Test content'}
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())
        post = form.save(commit=False)
        post.author = self.user
        post.save()
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().content, 'Test content')
