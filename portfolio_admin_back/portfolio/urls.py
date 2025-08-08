from django.urls import path
from . import views

urlpatterns = [
    path('holdings', views.portfolio_holdings),
    path('allocation', views.portfolio_allocation),
    path('performance', views.portfolio_performance),
    path('summary', views.portfolio_summary),
]
