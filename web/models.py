import datetime
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
	def _create_user(self, email, name_first, name_last, password, is_admin):
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
			email=self.normalize_email(email),
			name_first=name_first,
			name_last=name_last,
			is_admin=is_admin,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, name_first, name_last, password):
		return self._create_user(email, name_first, name_last, password, False)

	def create_superuser(self, email, name_first, name_last, password):
		return self._create_user(email, name_first, name_last, password, True)

class User(AbstractBaseUser):
	class Meta:
		verbose_name = "user"
		verbose_name_plural = "users"
	
	email = models.EmailField(unique=True)
	USERNAME_FIELD = 'email'
	
	name_first = models.CharField(max_length=50)
	name_last = models.CharField(max_length=50)

	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=True)

	REQUIRED_FIELDS = ['name_first', 'name_last']
	objects = UserManager()

	def __str__(self):
		return self.email
	def get_full_name(self):
		return self.email
	def get_short_name(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return self.is_admin
	def has_module_perms(self, app_label):
		return self.is_admin
	@property
	def is_staff(self):
		return self.is_admin
