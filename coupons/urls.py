from django.urls import path

from coupons.views import CouponView, UseCoupon



coupons_router = {'get'     : 'list',
                  'post'    : 'create'}
coupon_router  = {'get'     : 'retrieve',
                  'patch'   : 'partial_update',
                  'delete'  : 'destroy'}

urlpatterns = [
    path('list/'             , CouponView.as_view(coupons_router)    , name="coupons"),
    path('code/<str:code>/'  , CouponView.as_view(coupon_router)     , name="coupon"),
    path('use/'              , UseCoupon.as_view()                   , name="coupon_usage")
]