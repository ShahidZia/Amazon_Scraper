from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Brand


class Command(BaseCommand):
    help = "Create superuser and sample brand to fetch data from Nike!"

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating superuser and sample brand to fetch data from Nike!")
        # create superuser
        User = get_user_model()
        is_username_exist = User.objects.filter(username="admin").exists()
        if not is_username_exist:
            User.objects.create_superuser(
                username="admin", email="admin@admin.com", password="adminpassword",
            )

        # create nike brand
        Brand.objects.get_or_create(
            name="Nike",
            website_url="https://www.amazon.co.uk/stores/Nike/page/48A10D47-F452-4AC0-8B10-C8D88B964AA0"
        )
        self.stdout.write("Completed!")
