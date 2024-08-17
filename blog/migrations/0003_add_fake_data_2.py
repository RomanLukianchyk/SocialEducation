from django.db import migrations
from django.contrib.auth.hashers import make_password
from faker import Faker


def create_fake_data(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Post = apps.get_model('blog', 'Post')
    fake = Faker()

    users = []
    for _ in range(10):
        user = User.objects.create(
            username=fake.user_name(),
            email=fake.email(),
            password=make_password('password123')
        )
        users.append(user)

    # Create fake posts
    for user in users:
        for _ in range(5):
            Post.objects.create(
                author=user,
                content=fake.text(max_nb_chars=200),
                created_at=fake.date_time_this_year(),
                tags=', '.join(fake.words(nb=3))
            )


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_fake_data),
    ]
