from django.db import migrations
from django.contrib.auth.models import User
from blog.models import Post
from faker import Faker


def create_fake_data(apps, schema_editor):
    fake = Faker()

    users = []
    for _ in range(10):
        user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password='password123'
        )
        users.append(user)

    # Create fake posts
    for user in users:
        for _ in range(5):
            Post.objects.create(
                author=user,
                content=fake.text(max_nb_chars=200),
                created_at=fake.date_time_this_year(),
                tags=fake.words(nb=3, ext_word_list=None, unique=True)
            )


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
    ]
