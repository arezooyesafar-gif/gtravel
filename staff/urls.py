from django.urls import path

from .message_views import bulk_delete_messages
from .views import change_log, change_log_delete, staff_create, staff_delete, staff_list, staff_update

urlpatterns = [
    path('', staff_list, name='staff-list'),
    path('create', staff_create, name='staff-create'),
    path('update/<int:id>', staff_update, name='staff-update'),
    path('delete/<int:id>', staff_delete, name='staff-delete'),
    path('change-log', change_log, name='staff-change-log'),
    path('change-log/delete', change_log_delete, name='staff-change-log-delete'),
    path('messages/delete', bulk_delete_messages, name='messages-bulk-delete'),
]
