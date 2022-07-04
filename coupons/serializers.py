from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.exceptions import ValidationError, NotFound, NotAuthenticated, NotAcceptable

from coupons.models import Coupon, CouponUser



class CouponSerializer(serializers.ModelSerializer):
    """
    coupons managment serializer
    """
    class Meta:
        model = Coupon
        fields = [
            'value', 
            'code', 
            'type', 
            'user_limit', 
            'created_at', 
            'valid_until',
            'campaign', 
            'is_active'
            ] 


class CouponValidationSerializer(serializers.Serializer):
    """
    coupon usage validation serializer
    """
    coupon_code = serializers.CharField(label=_("Coupon code"))
    coupon_type = serializers.CharField(label=_("Coupon type"), required=False)

    def save(self, **kwargs):
        user = self.context['request'].user
        code = self.validated_data.get("coupon_code")
        type = self.validated_data.get("coupon_type")

        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            raise NotFound(detail="This code is not valid.", code=404)

        if user is None and coupon.user_limit != 1:
            # coupons with can be used only once can be used without tracking the user, otherwise there is no chance
            # of excluding an unknown user from multiple usages.
            raise NotAuthenticated(
                detail="The system must provide an user to this form to allow you to use this code. Maybe you need to sign in?",
                code=401
            )

        if coupon.is_redeemed:
            raise NotAcceptable(detail="This code has already been used.", code=406)

        try:  # check if there is a user bound coupon existing
            user_coupon = coupon.users.get(user=user)
            if user_coupon.redeemed_at is not None:
                raise NotAcceptable(detail="This code has already been used by your account.", code=406)
        except CouponUser.DoesNotExist:
            if coupon.user_limit != 0:  # zero means no limit of user count
                # only user bound coupons left and you don't have one
                if coupon.user_limit is coupon.users.filter(user__isnull=False).count():
                    raise ValidationError(detail="This code is not valid for your account.", code=400)
                if coupon.user_limit is coupon.users.filter(redeemed_at__isnull=False).count():  # all coupons redeemed
                    raise NotAcceptable(detail="This code has already been used.", code=406)

        if type is not None and coupon.type not in type:
            raise NotAcceptable(detail="This code is not meant to be used here.", code=406)

        if coupon.expired():
            raise ValidationError(detail="This code is expired.", code=400)

        return CouponUser(coupon=coupon, user=user, redeemed_at=timezone.now()).save()