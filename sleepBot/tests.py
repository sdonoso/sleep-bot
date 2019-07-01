from django.test import TestCase, Client
from datetime import datetime
from .models import Person, Data
from django.utils import timezone


# Create your tests here
class SleepModelTest(TestCase):

    def setUp(self):
        person = Person.objects.create(id_telegram="juanito", name="juan")
        Data.objects.create(person=person, sleep_hours=8, mood=4)
        Data.objects.create(person=person, sleep_hours=10, mood=11)

    def test_get_person(self):
        person = Person.objects.get(id_telegram="juanito")
        self.assertEquals(person.name, "juan")
        self.assertEquals(person.creation_date.day, timezone.now().day) # Antes decia 27

    def test_data(self):
        person = Person.objects.get(id_telegram="juanito")
        data = Data.objects.filter(person=person)
        self.assertEquals(len(data),2)
        self.assertEquals(data[0].mood,4)
        self.assertEquals(data[1].mood,11)

class CreatePersonTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_create_person(self):
        response = self.client.post("/persons/", {"name":"Jorge", "id_telegram":"101"})
        self.assertEquals(response.status_code, 201)

        person = Person.objects.get(id_telegram="101")
        self.assertEquals(person.name, "Jorge")


class CreateDataTest(TestCase):

    def setUp(self):
        self.person = Person.objects.create(id_telegram="100", name="juan")
        self.client = Client()

    def test_create_data(self):
        id_person = self.person.pk
        response = self.client.post("/datas/", {"person":"/persons/"+str(id_person)+"/", "sleep_hours":8, "mood":4})
        self.assertEquals(response.status_code, 201)

        data = Data.objects.get(person=self.person)
        self.assertEquals(data.sleep_hours, 8)