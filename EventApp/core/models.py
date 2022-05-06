from django.utils import timezone
from django.db import models
from django.contrib.auth.models import PermissionsMixin, BaseUserManager, \
    Group
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.core.exceptions import ImproperlyConfigured

from jdatetime import datetime as jdt


class WebHookMessage(models.Model):
    recieved_at = models.DateTimeField(
        help_text=_('When message has recieved.'),
        default=timezone.now()
    )
    payload = models.JSONField(default=None, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['recieved_at',]),
        ]


class UserManager(BaseUserManager):
    ''' User Model Manager '''
    def create_user(self, username, email, password=None, **extra_fields):
        ''' Exclusive create user function '''
        if not email:
            raise ValueError('Email MUST be included!')

        user = self.model(email=self.normalize_email(email),
            username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, username, email, password, **params):
        ''' Exclusive create superuser function '''
        user = self.create_user(username, email, password, **params)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user

    def create_or_get_user(self, username, email, password, **extra_fields):
        """Create or get user with credentials"""
        if not email:
            raise ValueError('Email MUST be included!')

        if self.filter(email=email).count() == 0:
            return (self.create_user(username, email, password, **extra_fields),
                True)
        else:
            return (self.get(email=email), False)

class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.IntegerField(
        _('phone_number'),
        max_length=15, unique=True, null=True, blank=True
    )
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        _('Email Address'),
        unique=True, null=True, blank=True
    )
    name = models.CharField(_('name'), max_length=255, default=username)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    groups = models.ManyToManyField(
            Group,
            blank=True,
            related_name="user_set",
            related_query_name="user",
            default=1
        )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    objects = UserManager()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def set_username_by_name(self):
        if not self.name:
            raise ImproperlyConfigured('User must have a name!')
        self.username = f'{self.name}{self.id}'
        return self.username

    def is_joined_recently(self):
        """
        Check if the user has joined recently or not
        """
        return \
            timezone.now()-timezone.timedelta(hours=24) \
            <= self.date_joined \
            <= timezone.now()

    def jdate_joined(self):
        return jdt.fromgregorian(datetime=self.date_joined)
