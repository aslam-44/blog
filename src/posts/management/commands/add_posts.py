import wget
import csv
import uuid

from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth.models import User
from posts.models import Author, Post, Category

class Command(BaseCommand):
    help = 'Import posts from a CSV file'

    def handle(self, *args, **kwargs):
        Author.objects.all().delete()
        Post.objects.all().delete()
        Category.objects.all().delete()

        file_path = settings.BASE_DIR / "new_posts.csv"
        
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header

            for row in csv_reader:
                author_name = row[1].strip()  # Assuming this is a single name
                content = row[2]
                date = row[3]
                tags = row[5]
                title = row[6]
                featured_image = "https://picsum.photos/1500/1000"
                file_name = f'{uuid.uuid4()}.jpg'
                image_path = f'{settings.BASE_DIR}/media/posts/{file_name}'
                wget.download(featured_image, image_path)
                uploaded_file_url = f'posts/{file_name}'

                # Check if author exists
                author, created = Author.objects.get_or_create(
                    name=author_name,
                    defaults={
                        'user': User.objects.create_user(
                            username=str(uuid.uuid4()),
                            password="password",
                            first_name=author_name.split()[0],  # Get first name for username
                        )
                    }
                )

                # Create the post
                post = Post.objects.create(
                    title=title,
                    description=content,
                    short_description=content[:100],
                    time_to_read="5 min",
                    featured_image=uploaded_file_url,
                    published_date=date,
                    author=author  # Ensure the author is linked
                )

                # Handle tags
                tags_list = tags.split(',')
                for tag in tags_list:
                    tag = tag.strip()
                    if tag:  # Check if tag is not empty
                        item, created = Category.objects.get_or_create(title=tag)
                        post.category.add(item)  # Add category to post

        print("Process completed successfully")

                  
