from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Well, Lesson, Subscription
from lms.paginators import MyPagination
from lms.serializers import WellSerializers, LessonSerializers, SubscriptionSerializer
from users.permissions import IsModerator, IsOwner


class WellViewSet(viewsets.ModelViewSet):
    """ вывод информации о курсах """
    serializer_class = WellSerializers
    queryset = Well.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    pagination_class = MyPagination

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~IsModerator,)
        elif self.action in ['update', 'retrieve', 'partial_update']:
            self.permission_classes = (IsModerator | IsOwner, )
        elif self.action == 'destroy':
            self.permission_classes = (~IsModerator | IsOwner, )
        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    """ создание урока """
    serializer_class = LessonSerializers
    permission_classes = (~IsModerator, IsAuthenticated)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """ список всех уроков """
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    pagination_class = MyPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """ детальная информация по уроку """
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """ изменение урока """
    serializer_class = LessonSerializers
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """ удаление урока """
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner | ~IsModerator)


class SubscriptionAPIView(APIView):
    """Логика подписки на курс """
    serializer_class = SubscriptionSerializer

    def post(self, *args, **kwargs):
        """ Активация или деактивация подписки """
        user = self.request.user
        well_id = self.request.data.get("well")
        well = get_object_or_404(Well, pk=well_id)
        subs_item = Subscription.objects.all().filter(user=user).filter(well=well).first()

        if subs_item:
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            new_sub = Subscription.objects.create(user=user, well=well)
            message = 'Подписка добавлена'

        return Response({"message": message})
