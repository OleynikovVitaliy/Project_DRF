from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status, serializers
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from lms.services import create_product, create_price, create_session
from users.models import User, Payments
from users.permissions import IsModerator
from users.serializers import UserSerializer, PaymentsSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ вывод информации о пользователях """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserAPIListView(generics.ListAPIView):
    """Просмотр всех пользователей"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserCreateAPIView(generics.CreateAPIView):
    """Создание пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserUpdateAPIView(generics.UpdateAPIView):
    """Изменение пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsModerator]


class UserDeleteAPIView(generics.DestroyAPIView):
    """Удаление пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsModerator]


class PaymentsListAPIView(generics.ListAPIView):
    """ список всех платежей """
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_set_fields = ('paid_well', 'paid_lesson', 'payment_method',)
    ordering_fields = ('date_payment',)


class PaymentsCreateAPIView(generics.CreateAPIView):
    """ Работа с платежами """
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """ Создание платежа """
        try:
            payment = serializer.save(user=self.request.user)
            product = payment.paid_lesson if payment.paid_lesson else payment.paid_course
            stripe_product = create_product(product)
            price = create_price(product.price, stripe_product)
            session_id, payment_link = create_session(price)
            payment.session_id = session_id
            payment.link = payment_link
            payment.save()
        except serializers.ValidationError("Выберите урок или курс для оплаты") as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
