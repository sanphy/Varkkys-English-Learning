from django.urls import path
from . import views
from .views import candidate_detail,candidate_update,list_candidates,login_view
from django.urls import path

urlpatterns = [
    path('api/login/', login_view, name='login_view'),
    path('api/list-candidates/', list_candidates, name='list_candidates'),
    path('api/<str:phone>/', candidate_detail, name='candidate_detail'),
    path('api/candidates/<str:phone>/update/', candidate_update, name='candidate_update'),

]

