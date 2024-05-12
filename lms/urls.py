from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lms.views import WellViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, \
    LessonDestroyAPIView, SubscriptionAPIView

app_name = 'lms'

router = DefaultRouter()
router.register(r'well', WellViewSet, basename='well')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/view/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_view'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),

    path('well/<int:pk>/subscribe/', SubscriptionAPIView.as_view(), name='subscribe'),
    ] + router.urls
