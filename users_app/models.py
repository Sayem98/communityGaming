from django.db import models
import random
from django.contrib.auth.models import User
from django.utils.text import slugify
import string


# Create your models here.

def get_random_number():
    gameid = random.randrange(1000000000, 9900000000)
    return gameid
    # old_user = UserInfoModel.objects.get(unique_id=gameid)
    # if old_user is not None:
    #     get_random_number()
    # else:
    #     return gameid


def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))


class UserInfoModel(models.Model):
    profile_image = models.ImageField(upload_to='user_profile', blank=True)
    unique_id = models.BigIntegerField(editable=False)
    user_slug = models.SlugField(max_length=255, unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_info')

    def save(self, *args, **kwargs):
        if not self.user_slug:
            self.user_slug = slugify(rand_slug() + '-' + self.user.first_name + '-' + self.user.last_name)
            self.unique_id = get_random_number()
            print(self.user_slug)
            print(self.unique_id)
        super(UserInfoModel, self).save(*args, **kwargs)

