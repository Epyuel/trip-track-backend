from django.urls import path
from trip.views import add_log, delete_log, get_log, get_log_by_range, get_logs, update_log


urlpatterns = [
    path('logs/', get_logs, name='get_logs'),
    path('logs/add/', add_log, name='add_log'),
    path('logs/<str:date>/', get_log, name='get_log'),
    path("logs/by-range", get_log_by_range, name="get_log_by_range"),
    path('logs/<str:log_id>/update/', update_log, name='update_log'),
    path('logs/<str:log_id>/delete/', delete_log, name='delete_log'),
]
