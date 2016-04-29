from django.core.management.base import BaseCommand
import faker
from scheduling import models


def create_classrooms(num_rooms):
    pass


def create_users(num_users):
    fake = faker.Faker()

    for i in range(num_users):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = first_name.lower()
        email = '{}@example.com'.format(username)
        password = 'qazwsxedc'

        user = models.User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name

        user.save()

        print('Created user "{}".'.format(user.get_full_name()))


def create_classes(num_classes):
    pass


def main(options):
    num_rooms = options['num_rooms'][0]
    num_users = options['num_users'][0]
    num_classes = options['num_classes'][0]

    if num_rooms:
        create_classrooms(num_rooms)

    if num_users:
        create_users(num_users)

    if num_classes:
        create_classes(num_classes)


class Command(BaseCommand):
    help = 'Generates fake data suitable for testing the application.'

    def add_arguments(self, parser):
        parser.add_argument('num_rooms', nargs='+', type=int)
        parser.add_argument('num_users', nargs='+', type=int)
        parser.add_argument('num_classes', nargs='+', type=int)

    def handle(self, *args, **options):
        print(options)
        main(options)


if __name__ == '__main__':
    pass
