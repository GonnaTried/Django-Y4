import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

# Adjust 'mainapp' to your actual app name
from tasks.models import Category, Tag, Task, TaskStatus

User = get_user_model()


class Command(BaseCommand):
    help = "Seeds the database with Faker data for Category, Tag, and Task models."

    def add_arguments(self, parser):
        parser.add_argument(
            "--num_categories",
            type=int,
            default=5,
            help="Number of categories to create.",
        )
        parser.add_argument(
            "--num_tags", type=int, default=10, help="Number of tags to create."
        )
        parser.add_argument(
            "--num_tasks", type=int, default=50, help="Number of tasks to create."
        )
        parser.add_argument(
            "--num_users",
            type=int,
            default=3,
            help="Number of users to create (if none exist).",
        )
        parser.add_argument(
            "--clear", action="store_true", help="Clear existing data before seeding."
        )

    def handle(self, *args, **options):
        fake = Faker()
        num_categories = options["num_categories"]
        num_tags = options["num_tags"]
        num_tasks = options["num_tasks"]
        num_users = options["num_users"]
        clear_data = options["clear"]

        self.stdout.write(self.style.NOTICE("Starting data seeding..."))

        if clear_data:
            self.stdout.write(self.style.WARNING("Clearing existing data..."))
            Task.objects.all().delete()
            Category.objects.all().delete()
            Tag.objects.all().delete()
            # Be cautious with deleting users, especially if you have a superuser you want to keep
            # User.objects.filter(is_superuser=False).delete() # Example to delete non-superusers

        # --- Create Users if none exist ---
        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.SUCCESS(f"Creating {num_users} users..."))
            for i in range(num_users):
                username = fake.user_name() + str(i)  # Ensure unique username
                email = fake.email()
                password = "password123"  # A simple password for seeding
                user = User.objects.create_user(
                    username=username, email=email, password=password
                )
                users.append(user)
            if not users:
                self.stdout.write(
                    self.style.ERROR(
                        "No users available to assign tasks to. Please create some users or a superuser first."
                    )
                )
                return

        # --- Create Categories ---
        self.stdout.write(
            self.style.SUCCESS(f"Creating {num_categories} categories...")
        )
        categories = []
        for _ in range(num_categories):
            name = fake.unique.word().capitalize()
            while Category.objects.filter(name=name).exists():
                name = fake.unique.word().capitalize()
            category = Category.objects.create(
                name=name,
                # Use 'hex_color' here, matching the model field name
                # Slicing to [:7] ensures it fits if max_length=7 in your model
                hex_color=fake.hex_color()[:7],
            )
            categories.append(category)
        if not categories:
            self.stdout.write(
                self.style.ERROR("No categories created. Cannot create tasks.")
            )
            return

        # --- Create Tags ---
        self.stdout.write(self.style.SUCCESS(f"Creating {num_tags} tags..."))
        tags = []
        for _ in range(num_tags):
            label = fake.unique.word().lower()
            # Ensure unique tag labels
            while Tag.objects.filter(label=label).exists():
                label = fake.unique.word().lower()
            tag = Tag.objects.create(label=label)
            tags.append(tag)
        if not tags:
            self.stdout.write(self.style.ERROR("No tags created."))

        # --- Create Tasks ---
        self.stdout.write(self.style.SUCCESS(f"Creating {num_tasks} tasks..."))
        for i in range(num_tasks):
            title = fake.sentence(nb_words=6).replace(".", "")
            # Corrected typo 'decription' to 'description'
            description = (
                fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
                if random.random() > 0.3
                else None
            )

            # Random status
            status_enum_member = random.choice(list(TaskStatus))
            status_value = status_enum_member.value

            # Random due date
            due_date = None
            if random.random() > 0.2:  # 80% chance of having a due date
                due_date = timezone.now() + timedelta(
                    days=random.randint(-10, 30)
                )  # Due in past or future

            # Assign random user and category
            user = random.choice(users)
            category = random.choice(
                categories
            )  # Category is mandatory if on_delete=CASCADE

            task = Task.objects.create(
                title=title,
                description=description,  # Corrected field name
                status=status_value,
                due_date=due_date,
                user=user,
                category=category,
            )

            # Add random tags (0 to 3 tags per task)
            if tags:  # Only try to add tags if some were created
                num_random_tags = random.randint(0, min(3, len(tags)))
                selected_tags = random.sample(tags, num_random_tags)
                # Use .set() to add multiple tags efficiently
                # IMPORTANT: The ManyToManyField is named 'tags' now
                task.tags.set(selected_tags)

        self.stdout.write(self.style.SUCCESS("Database seeding complete!"))
