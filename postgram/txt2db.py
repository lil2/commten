import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'postgram.settings')

import django
if django.VERSION >= (1, 7):  # check version
    django.setup()


def main():
    from blogapp.models import Post, User
    with open('db.txt') as f:
        for line in f:
            author, title, content = line.split('****')
            Post.objects.get_or_create(author=User.objects.all()[3], title=title, body=content)

if __name__ == "__main__":
    main()
    print('Done!')

