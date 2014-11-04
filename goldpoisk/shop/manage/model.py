from django.contrib import auth

class Admin(User):
    email = models.EmailField(_("Email"), max_length=128, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'password']

    class Meta:
        verbose_name = _('Admin')
        verbose_name_plural = _('Admins')


class Manager(AbstractBaseUser):
    email = models.EmailField(_("Email"), max_length=128, unique=True)
    shop = models.ForeignKey(Shop)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'password']

    class Meta:
        verbose_name = _('Manager')
        verbose_name_plural = _('Managers')
