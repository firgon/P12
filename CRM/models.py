from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from authentication.models import CRMUser


class CRMObject(models.Model):
    class Meta:
        abstract = True

    created_time = models.DateTimeField(verbose_name="Création",
                                        auto_now_add=True)
    last_update = models.DateTimeField(verbose_name="Dernière mise à jour",
                                       auto_now=True)

    objects = models.Manager()  # Only useful for pycharm developing


class Client(CRMObject):
    """Class to instance Client
        Exemple of data that must be stored:
        Id	PRIMARY KEY - INT	1
        First Name	VARCHAR(25)	Kevin
        Last Name	VARCHAR(25)	Casey
        Email	VARCHAR(100)	kevin@startup.io
        Phone	VARCHAR(20)	639168088812
        Mobile	VARCHAR(20)	639178089812
        Company Name	VARCHAR(250)	Cool Start Up Inc
        Date Created	DATETIME	19/01/2001 02:40:05
        Date Updated	DATETIME	24/01/2001 10:02:44
        Sales Contact	FOREIGN KEY - INT	12
        """

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(email__isnull=False) |
                                         models.Q(phone__isnull=False) |
                                         models.Q(mobile__isnull=False),
                                   name='one contact',
                                   violation_error_message='You must add '
                                                           'a phone, '
                                                           'a mobile or '
                                                           'a mail.'),
        ]

    POTENTIAL = "Potential"
    CONFIRMED = "Confirmed"

    first_name = models.CharField(verbose_name="First Name", max_length=25)
    last_name = models.CharField(verbose_name="Last Name", max_length=25)
    email = models.CharField(verbose_name="Email", max_length=100, null=True,
                             blank=True, )
    phone = models.CharField(verbose_name="Phone", max_length=20,
                             null=True,
                             blank=True, )
    mobile = models.CharField(verbose_name="Mobile", max_length=20,
                              null=True,
                              blank=True, )
    company = models.CharField(verbose_name="Company", max_length=250)
    assignee = models.ForeignKey(to=CRMUser,
                                 on_delete=models.DO_NOTHING,
                                 null=True,
                                 blank=True,
                                 limit_choices_to={'team': CRMUser.SALES})

    def is_related(self, user: CRMUser) -> bool:
        return user == self.assignee

    @property
    def is_confirmed(self) -> bool:
        return self.contract_set.exists()

    # def clean(self):
    #     if all(test is None for test in [self.email, self.phone, self.mobile]):
    #         raise ValidationError({'email': _('You should enter at least '
    #                                           'one contact.'),
    #                                'phone': _('You should enter at least '
    #                                           'one contact.'),
    #                                'mobile': _('You should enter at least '
    #                                            'one contact.'),
    #                                })

    def __str__(self):
        return f"{self.first_name} {self.last_name.upper()}"


class Contract(CRMObject):
    """Class to instance Contract that can be signed with Client
    Exemple of data that must be stored:
    Id	PRIMARY KEY - INT	1054 -> automatic in django
    Sales Contact	FOREIGN KEY - INT	12
    Client	FOREIGN KEY - INT	1
    Date Created	DATETIME	19/01/2001 02:40:05
    Date Updated	DATETIME	24/01/2001 10:02:44
    Status	BOOLEAN	1
    Amount	FLOAT	10080.35
    Payment Due	DATETIME	24/01/2001 10:02:44
    """

    class Status(models.IntegerChoices):
        CREATED = 0
        SIGNED = 1
        PAYED = 2

    # STATUS_NAME = ["Créé", "Signé", "Payé"]

    client = models.ForeignKey(to=Client,
                               on_delete=models.DO_NOTHING,
                               limit_choices_to={'assignee__isnull': False})
    assignee = models.ForeignKey(to=CRMUser,
                                 on_delete=models.DO_NOTHING,
                                 limit_choices_to={'team': CRMUser.SALES})
    status = models.IntegerField(choices=Status.choices,
                                 verbose_name="Status",
                                 default=Status.CREATED)
    amount = models.DecimalField(verbose_name="Montant",
                                 decimal_places=2,
                                 max_digits=8)
    payment_due = models.DateTimeField(verbose_name="Due on",
                                       blank=True,
                                       null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=(models.Q(status=1) &
                                          models.Q(
                                              payment_due__isnull=False)) |
                                         (models.Q(status=0) &
                                          models.Q(payment_due__isnull=True)),
                                   name='date of payment when signed',
                                   violation_error_message='A contract '
                                                           'must have '
                                                           'a date of payment '
                                                           'only once signed'),
        ]

    def clean(self):
        if self.status == self.Status.SIGNED and self.payment_due is None:
            raise ValidationError(
                _('When a contact is signed,'
                  ' you have to determine a date of payment.'))
        if self.status != self.Status.SIGNED and self.payment_due is not None:
            raise ValidationError(
                _('You can\'t determine a date of payment,'
                  'if contract have not been signed.'))

    def save(self, **kwargs):
        self.assignee = self.client.assignee
        super().save(**kwargs)

    def is_related(self, user: CRMUser) -> bool:
        return user == self.client.assignee

    def __str__(self):
        return f"{self.id}-{self.client}"


class Event(models.Model):
    """Class to instance Event that are created when a Client contract with us
    Exemple of data that must be stored :
    Id	PRIMARY KEY - INT	1054
    Client	FOREIGN KEY - INT	1
    Date Created	DATETIME	19/01/2001 02:40:05
    Date Updated	DATETIME	24/01/2001 10:02:44
    Support Contact	FOREIGN KEY - INT	24
    Event Status	FOREIGN KEY - INT	1
    Attendees	INT	200
    Event Date	DATETIME	24/01/2001 10:02:44
    Notes	TEXT	Event should be held by the river.
    """

    class Status(models.IntegerChoices):
        ON_GOING = 0
        CANCELED = 1
        DONE = 2

    STATUS_NAME = ["On Going", "Canceled", "Done"]

    contract = models.OneToOneField(to=Contract,
                                    on_delete=models.CASCADE,
                                    primary_key=True,
                                    limit_choices_to={
                                        'status': Contract.Status.SIGNED,
                                        'event__isnull': True
                                    })
    assignee = models.ForeignKey(to=CRMUser,
                                 on_delete=models.DO_NOTHING,
                                 limit_choices_to={
                                     'team': CRMUser.SUPPORT},
                                 null=True,
                                 blank=True)
    status = models.IntegerField(verbose_name="Statut",
                                 choices=Status.choices,
                                 default=Status.ON_GOING)
    attendees = models.IntegerField(verbose_name="Expected attendees",
                                    null=True, blank=True, default=None)
    date = models.DateField(verbose_name="Date")
    notes = models.TextField(verbose_name="Notes", blank=True, default="")

    objects = models.Manager()  # Only useful for pycharm developing

    def is_related(self, user: CRMUser) -> bool:
        return user == self.assignee or self.contract.is_related(user)

    @admin.display(ordering='date')
    def __str__(self):
        return f"{self.date} - {self.contract.client}"
