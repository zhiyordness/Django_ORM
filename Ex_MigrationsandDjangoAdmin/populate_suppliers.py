
import os
import django
import random
import string

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Supplier

def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def generate_random_phone():
    return ''.join(random.choice(string.digits) for i in range(10))

for _ in range(30):
    name = generate_random_string(10)
    contact_person = generate_random_string(8)
    email = f"{generate_random_string(5)}@example.com"
    phone = f"1-555-{generate_random_phone()}"
    address = generate_random_string(20)
    
    # Ensure uniqueness
    while Supplier.objects.filter(email=email).exists() or Supplier.objects.filter(phone=phone).exists():
        email = f"{generate_random_string(5)}@example.com"
        phone = f"1-555-{generate_random_phone()}"

    Supplier.objects.create(
        name=name,
        contact_person=contact_person,
        email=email,
        phone=phone,
        address=address
    )
