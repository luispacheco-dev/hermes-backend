from random import choices
from string import digits, ascii_uppercase

def get_upload_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

def get_friend_code(cls):
    friend_code = get_random_string()
    while len(cls.objects.filter(code=friend_code)) != 0:
        friend_code = get_random_string()
    return friend_code

def get_random_string():
    return ''.join(choices(ascii_uppercase+digits, k=8))
