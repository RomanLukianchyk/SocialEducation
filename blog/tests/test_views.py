from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from blog.models import Post, Tag, Like
import io
from PIL import Image


class PostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tester', password='password123')
        self.client.login(username='tester', password='password123')

    @staticmethod
    def create_test_image():
        file = io.BytesIO()
        image = Image.new('RGB', (100, 100), color='red')
        image.save(file, 'JPEG')
        file.name = 'test_image.jpg'
        file.seek(0)
        return file

    def test_create_post_with_tags(self):
        test_image = self.create_test_image()
        test_image.seek(0)
        response = self.client.post(reverse('create_post'), {
            'content': 'Test post content',
            'image': SimpleUploadedFile(name='test_image.jpg', content=test_image.read(), content_type='image/jpeg'),
            'tags': 'testtag1, testtag2'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(content='Test post content').exists())
        self.assertTrue(Tag.objects.filter(name='testtag1').exists())
        self.assertTrue(Tag.objects.filter(name='testtag2').exists())

    def test_create_post_without_tags(self):
        test_image = self.create_test_image()
        test_image.seek(0)
        response = self.client.post(reverse('create_post'), {
            'content': 'Test post content without tags',
            'image': SimpleUploadedFile(name='test_image.jpg', content=test_image.read(), content_type='image/jpeg'),
            'tags': ''
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(content='Test post content without tags').exists())

    def test_feed_view(self):
        response = self.client.get(reverse('feed'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/feed.html')

    def test_like_post(self):
        post = Post.objects.create(author=self.user, content='Another test post')
        response = self.client.get(reverse('like_post', args=[post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Like.objects.filter(user=self.user, post=post).exists())
