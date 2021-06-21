from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('pred', views.pred, name='pred'),
    path('contact', views.contact, name='contact'),
    path('login', views.login_view, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('remove_pop/<id>', views.remove_pop, name='remove_pop'),
    path('transactions', views.transactions, name='transactions'),
    path('buy_stock', views.buy_stock, name='buy_stock'),
    path('sell_stock', views.sell_stock, name='sell_stock'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout_view, name='logout'),

]
