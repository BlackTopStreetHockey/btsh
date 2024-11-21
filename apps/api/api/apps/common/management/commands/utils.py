from users.models import User


def get_or_create(cls, get_kwargs, create_kwargs, exclude=None):
    try:
        obj = cls.objects.get(**get_kwargs)
        created = False
    except cls.DoesNotExist:
        obj = cls(**create_kwargs)
        obj.full_clean(exclude=exclude or [])
        obj.save()
        created = True
    print(f'[{cls._meta.verbose_name}] {obj} {"created" if created else "already exists"}.')
    return obj, created


def print_separator():
    print()
    print('*' * 50)
    print()


def get_default_created_by():
    superusers = User.objects.filter(is_superuser=True)
    if not superusers.exists():
        raise Exception('Please create a superuser to continue.')
    return superusers.first()
