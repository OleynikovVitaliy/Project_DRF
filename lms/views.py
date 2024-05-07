from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from lms.models import Well, Lesson
from lms.serializers import WellSerializers, LessonSerializers
from users.permissions import IsModerator, IsOwner


class WellViewSet(viewsets.ModelViewSet):
    """ вывод информации о курсах """
    serializer_class = WellSerializers
    queryset = Well.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]

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
