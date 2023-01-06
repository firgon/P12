from django.contrib import admin
from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class CRMUser(AbstractUser):

    @admin.display(empty_value="NO GROUP !!! (should not happen)")
    def group(self):
        return ", ".join([g.name for g in self.groups.all()]) \
            if self.groups.all().count() else None

    @admin.display()
    def assignments(self):
        if self.team == CRMUser.MANAGEMENT:
            return "N.C."
        return self.client_set.count() + self.event_set.count()

    def save(self, *args, **kwargs):
        """Method override to make is_staff = true if management in groups"""

        super().save(*args, **kwargs)

        if self.team is not None:
            group = Group.objects.get(name=CRMUser.TEAM_CHOICES[self.team][1])
            self.groups.clear()
            self.groups.add(group)

            self.is_staff = self.team == CRMUser.MANAGEMENT
            super().save(*args, **kwargs)

    MANAGEMENT = 0
    SALES = 1
    SUPPORT = 2

    TEAM_CHOICES = (
        (MANAGEMENT, "Management"),
        (SALES, "Sales"),
        (SUPPORT, "Support")
    )

    team = models.SmallIntegerField(choices=TEAM_CHOICES, null=False)

    def __str__(self):
        if self.first_name == "" and self.last_name == "":
            return self.username
        return f"{self.first_name} {self.last_name.upper()}"
