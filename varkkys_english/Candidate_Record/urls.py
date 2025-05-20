from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/login/', views.login_view),
    path('api/candidates/', views.list_candidates),
    path('api/candidate/<str:phone>/', views.candidate_detail), #patch
    # path('api/candidate/update/<str:phone>/', views.candidate_update),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


