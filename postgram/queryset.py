import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'postgram.settings')

import django
if django.VERSION >= (1, 7):  # check version
    django.setup()

from blogapp.models import User

jervis = User.objects.get(username='jervis')
john = User.objects.get(username='john')
john.follows.add(jervis)
print(john.follows.all())
# print(jervis.follows.all()Q)