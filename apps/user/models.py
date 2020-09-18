import PIL
from PIL import Image
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict
from stdimage import StdImageField

from canteros.settings import MEDIA_URL, STATIC_URL

SEXO = (
    (1, 'Masculino'),
    (0, 'Femenino'),
)

ESTADO = (
    (1, 'ACTIVO'),
    (0, 'INACTIVO'),
)


class User(AbstractUser):
    avatar = models.ImageField(upload_to='user/%Y/%m/%d', null=True, blank=True, default='user/admin.png')  # )
    cedula = models.CharField(max_length=10, unique=True, null=True)
    telefono = models.CharField(max_length=10, unique=True, null=True)
    direccion = models.CharField(max_length=500, blank=True, null=True)
    sexo = models.IntegerField(choices=SEXO, default=1)

    def get_image(self):
        if self.avatar:
            return '{}{}'.format(MEDIA_URL, self.avatar)
        return '{}{}'.format(STATIC_URL, 'user/admin.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['avatar'] = self.avatar.path
        return item

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.set_password(self.password)
        else:
            user = User.objects.get(pk=self.pk)
            if user.password != self.password:
                self.set_password(self.password)
        super().save(*args, **kwargs)

        if not self.avatar:
            return
        basewidth = 100
        img = Image.open(self.avatar)
        wpercent = 100
        hsize = 100
        img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        img.save(self.avatar.path)
        super().save(*args, **kwargs)

        # basewidth = 300
        #  img = Image.open(‘fullsized_image.jpg')
        #  wpercent = (basewidth / float(img.size[0]))
        #  hsize = int((float(img.size[1]) * float(wpercent)))
        #  img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        #  img.save(‘resized_image.jpg'