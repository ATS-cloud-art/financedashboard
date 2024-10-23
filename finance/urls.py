from django.urls import path
from . views import add_transaction
from . import views


urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('',views.login_view,name='login_view'),
    path('transaction/', add_transaction, name='add_transaction'),
]
