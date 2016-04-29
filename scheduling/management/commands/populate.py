from django.core.management.base import BaseCommand
import faker
import scheduling.models


def create_classrooms(num_rooms):
    pass


def create_users(num_users):
    pass


def create_classes(num_classes):
    pass


def main(options):
    num_rooms = options['num_rooms']
    num_users = options['num_users']
    num_classes = options['num_classes']


class Command(BaseCommand):
    help = 'Generates fake data suitable for testing the application.'

    def add_arguments(self, parser):
        parser.add_argument('num_rooms', nargs='+', type=int)
        parser.add_argument('num_instructors', nargs='+', type=int)
        parser.add_argument('num_classes', nargs='+', type=int)

    def handle(self, *args, **options):
        main(options)


if __name__ == '__main__':
    pass
