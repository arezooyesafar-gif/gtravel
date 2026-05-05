from django.urls import path, include
from .ajax_views import *
from .views import *

urlpatterns = [
    path('', online_order_dashboard, name='online_order_dashboard'),
    path('ajax_paid_order', ajax_paid_order, name='ajax_paid_order'),
    path('all_ajax_paid_order', all_ajax_paid_order, name='all_ajax_paid_order'),
    path('all_ajax_pending_order', all_ajax_pending_order, name='all_ajax_pending_order'),
    path('ajax_pending_order', ajax_pending_order, name='ajax_pending_order'),
    path('ajax_wallet_transaction', ajax_wallet_transaction, name='ajax_wallet_transaction'),
    path('single_order/<int:order_id>', single_order, name='single_order'),
    path('all_paid_orders', all_paid_orders, name='all_paid_orders'),
    path('all_pending_orders', all_pending_orders, name='all_pending_orders'),
]