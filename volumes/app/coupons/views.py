from operator import and_
from functools import reduce
from datetime import datetime

from django.http import Http404
from django.db.models import Q

from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from coupons.models import Coupon
from coupons.serializers import CouponSerializer, CouponValidationSerializer



class CouponView(viewsets.GenericViewSet):
    """
    rest api methods for coupon managment
    access level: 
    admin 
    query parameters:
    valuelte/valuegte/type/limitlte/limitgte/validfrom/validto/active
    exp:
    /coupon/code/<code>/
    /coupon/list/?active=True&limitgte=1&valuegte=1000&validfrom=1656863922&type=percentage&limit=2&offset=2
    """
    permission_classes = [IsAdminUser]
    serializer_class   = CouponSerializer
    pagination_class   = LimitOffsetPagination

    def get_queryset(self, code=None):
        """
        catch client query parameters
        return Coupon objects
        """
        valuelte  = self.request.query_params.get('valuelte')
        valuegte  = self.request.query_params.get('valuegte')
        type      = self.request.query_params.get('type')
        limitlte  = self.request.query_params.get('limitlte')
        limitgte  = self.request.query_params.get('limitgte')
        validfrom = self.request.query_params.get('validfrom')
        validto   = self.request.query_params.get('validto')
        active    = self.request.query_params.get('active')

        Qlist=[
            Q(type             = type),
            Q(value__lte       = int(valuelte) if valuelte else None),
            Q(value__gte       = int(valuegte) if valuegte else None),
            Q(user_limit__lte  = int(limitlte) if limitlte else None),
            Q(user_limit__gte  = int(limitgte) if limitgte else None),
            Q(valid_until__lte = datetime.utcfromtimestamp(int(validto)) if validto else None),
            Q(valid_until__gte = datetime.utcfromtimestamp(int(validfrom)) if validfrom else None),
            Q(is_active        = True if active in ["true", "True", "TRUE", None] else False) 
        ]

        if code:
            try:
                return Coupon.objects.get(code=code)
            except Coupon.DoesNotExist:
                raise Http404
        return Coupon.objects.filter(reduce(and_, [q for q in Qlist if q.children[0][1] is not None]))

    def list(self, request):
        """
        return list of Coupon objects
        """
        coupons = self.get_queryset()
        limit   = request.query_params.get('limit')
        if limit:
            queryset = self.paginate_queryset(coupons)
            serializer = self.get_serializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(coupons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, code):
        """
        return single Coupon object
        """
        coupon = self.get_queryset(code=code)
        serializer = self.get_serializer(coupon)
        return Response(serializer.data)

    def create(self, request):
        """
        post new Coupon if it's valid  
        return created object
        """
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, code):
        """
        patch Coupon object 
        return updated object
        """
        coupon = self.get_queryset(code=code)
        data = request.data 
        serializer = self.get_serializer(coupon, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, code):
        """
        delete Coupon object
        """
        userstrat = self.get_queryset(code=code)
        userstrat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UseCoupon(generics.CreateAPIView):
    """
    rest api post method for coupon usage
    access level: 
     
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CouponValidationSerializer

    def get_queryset(self, code=None):
        pass
    
    def create(self, request):
        """
        post new CouponUser if it's valid  
        return created object
        """
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Your wallet has been charged."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


