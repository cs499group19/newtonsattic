from django.core.management.base import BaseCommand
import faker
import random
from scheduling import models


def generate_availabilities(num_weeks):
    availability = ['m', 'a', '']
    rv = []

    for i in range(1, num_weeks + 1):
        times = random.randint(1, 2)
        choice = random.choice(availability)

        if times == 1:
            if choice:
                rv.append('{}{}'.format(i, choice))
        else:
            rv.append('{}m'.format(i))
            rv.append('{}a'.format(i))

    return rv


def create_classrooms(num_rooms):
    for i in range(1, num_rooms + 1):
        name = 'Room {}'.format(i)
        capacity = 30

        room = models.Classroom(name=name, capacity=capacity)
        room.save()

        print('Created classroom "{}".'.format(name))


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

        classes = list(models.Class.objects.all())
        availability = generate_availabilities(12)
        specialities = random.sample(
            classes,
            random.randint(1, len(classes)))

        instructor = models.Instructor()
        instructor.user = user
        instructor.availability = availability
        instructor.save()
        instructor.specialty = specialities


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
        main(options)


if __name__ == '__main__':
    pass
