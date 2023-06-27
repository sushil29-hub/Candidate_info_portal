from django.urls import path
from .views import CandidateView, GETResumeFile

urlpatterns = [
    path('candidate-details/', CandidateView.as_view()),
    path('update/candidate-details/<candidate_info_id>/', CandidateView.as_view()),
    path('s3/<candidate_info_id>/', GETResumeFile.as_view())
]