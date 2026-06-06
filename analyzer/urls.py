from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("analyze/seo/", views.seo_input, name="seo_input"),
    path("analyze/seo/<str:platform>/", views.seo_input, name="seo_input_platform"),
    path("analyze/seo/results/<int:pk>/", views.seo_results, name="seo_results"),
    path("analyze/grammar/", views.grammar_input, name="grammar_input"),
    path("analyze/grammar/results/<int:pk>/", views.grammar_results, name="grammar_results"),
    path("history/", views.history_list, name="history"),
    path("history/<int:pk>/", views.history_detail, name="history_detail"),
]
