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
from datetime import datetime


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
        unique=True, null=True, blank=True
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


class Ticket(models.Model):
    event_id = models.CharField(max_length=30, blank=True, null=True)
    ticket_id = models.CharField(max_length=30, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    available_count = models.CharField(max_length=50, blank=True, null=True)
    price = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    discount_id = models.CharField(max_length=30, blank=True, null=True)
    canceled = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())

    def from_evand(self, data: dict):
        try:
            self.event_id = data.get('data[ticket][data][event_id]', None)
            self.ticket_id = data.get('data[ticket_id]', None)
            self.type = data.get('data[ticket][data][type]', None)
            self.title = data.get('data[ticket][data][type]', None)
            self.available_count = data.get('data[ticket][data][available_count]', None)
            self.price = data.get('data[ticket][data][price]', None)
            self.description = data.get('data[ticket][data][description]', None)
            self.first_name = data.get('data[first_name]', None)
            self.last_name = data.get('data[last_name]', None)
            self.email = data.get('data[email]', None)
            self.mobile = data.get('data[mobile]', None)
            self.discount_id = data.get('data[discount_id]', None)
            self.canceled = data.get('data[canceled]', None)

            date_format = '%Y-%m-%dT%H:%M:%S%z'
            date = data.get('data[created_at]', timezone.now().strftime('%Y-%m-%dT%H:%M:%S%z'))
            self.created_at = datetime.strptime(date, date_format)

            date = data.get('data[updated_at]', timezone.now().strftime('%Y-%m-%dT%H:%M:%S%z'))
            self.updated_at = datetime.strptime(date, date_format)

            self.save()
        except Exception as e:
            print('----------error:')
            print(str(e))
        return self
