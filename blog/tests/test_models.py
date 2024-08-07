from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Post, Tag, PostTag, Like
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.utils import create_test_image


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='password123')
        self.post = Post.objects.create(author=self.user, content='Test content')

    def test_post_creation(self):
        self.assertEqual(self.post.content, 'Test content')
        self.assertEqual(self.post.author.username, 'tester')


class ImageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='password123')
        self.post = Post.objects.create(author=self.user, content='Test content')
        self.image = SimpleUploadedFile(name='test_image.jpg', content=create_test_image().read(), content_type='image/jpeg')

class TagModelTest(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name='TestTag')

    def test_tag_creation(self):
        self.assertEqual(self.tag.name, 'TestTag')


class PostTagModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='password123')
        self.post = Post.objects.create(author=self.user, content='Test content')
        self.tag = Tag.objects.create(name='TestTag')
        self.post_tag = PostTag.objects.create(post=self.post, tag=self.tag)

    def test_post_tag_creation(self):
        self.assertEqual(self.post_tag.post, self.post)
        self.assertEqual(self.post_tag.tag, self.tag)


class LikeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='password123')
        self.post = Post.objects.create(author=self.user, content='Test content')
        self.like = Like.objects.create(user=self.user, post=self.post)

    def test_like_creation(self):
        self.assertEqual(self.like.user, self.user)
        self.assertEqual(self.like.post, self.post)
