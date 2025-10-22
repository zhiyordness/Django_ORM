import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Person

# Create and save person instances
names = ["John", "Jane", "Michael", "Emily", "William", "Olivia"]
for i in range(6):
    Person.objects.create(name=names[i], age=15 + i * 5)

print("6 persons created.")