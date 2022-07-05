from django import forms
from django.utils.translation import gettext_lazy as _

from coupons.models import Campaign
from coupons.settings import COUPON_TYPES


class CouponGenerationForm(forms.Form):
    quantity = forms.IntegerField(label=_("Quantity"))
    value = forms.IntegerField(label=_("Value"))
    type = forms.ChoiceField(label=_("Type"), choices=COUPON_TYPES)
    valid_until = forms.SplitDateTimeField(
        label=_("Valid until"), required=False,
        help_text=_("Leave empty for coupons that never expire")
    )
    prefix = forms.CharField(label="Prefix", required=False)
    campaign = forms.ModelChoiceField(
        label=_("Campaign"), queryset=Campaign.objects.all(), required=False
    )