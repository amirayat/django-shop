from django.conf import settings
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _



class Wallet(models.Model):
    """
    users wallet model
    """
    user  = models.OneToOneField(User, verbose_name=_("User"), on_delete=models.CASCADE)
    cash = models.IntegerField(_("Charge value"), default=0, help_text=_("Coupon values sumation"))

    class Meta:
        db_table = 'wallets'

    def __str__(self):
        return str(self.user)


@receiver(signals.post_save, sender = User)
def create_customer(sender, instance, created, *args, **kwargs):
    """
    create 0 cash wallet for each user on registry
    """
    if created:
        w = Wallet(user=instance) 
        w.save()

