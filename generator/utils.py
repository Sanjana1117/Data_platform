import random
import uuid

from faker import Faker

fake = Faker("en_IN")

random.seed(42)
Faker.seed(42)


def random_bool(true_probability=0.8):
    return random.random() < true_probability


def random_uuid():
    return str(uuid.uuid4())


def random_date(start_year=2018):
    return fake.date_between(
        start_date=f"{start_year}-01-01",
        end_date="today"
    )


def random_company():
    return fake.company()


def random_person():
    return fake.name()


def random_city():
    return fake.city()


def random_state():
    return fake.state()


def random_pincode():
    return fake.postcode()


def random_address():
    return fake.address().replace("\n", ", ")