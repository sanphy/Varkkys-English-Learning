from django.urls import path
from . import views

urlpatterns = [
    path('api/login/', views.login_view),
    path('api/candidates/', views.list_candidates),
    path('api/candidate/<str:phone>/', views.candidate_detail), #patch
    path('api/candidate/update/<str:phone>/', views.candidate_update),
]
