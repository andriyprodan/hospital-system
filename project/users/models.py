from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext as _
from django.forms import ModelForm

from PIL import Image

class UserManager(BaseUserManager):
    """
    UserManager for User model with no username field
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):

    # User model uses email for authorization
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    phone = models.CharField(max_length=32, blank=True)

    objects = UserManager()

    is_doctor = models.BooleanField('doctor status', default=False)

class Specialization(models.Model):
    name = models.CharField(max_length=128, verbose_name=_("Specialization name"))

    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    spec = models.ManyToManyField(Specialization, blank=True)

class Patient(models.Model):
    """
    Every user has it's own Patient profile
    to prevent creating an extra accounts for doctors or staff
    """
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    doctors = models.ManyToManyField(Doctor, blank=True, related_name='patients')
    # Each user has their own patient profile, so we can use it for the profile photo.
    photo = models.ImageField(default='default.png', upload_to='profile_pics')

    def save(self):
        super().save()

        img = Image.open(self.photo.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)