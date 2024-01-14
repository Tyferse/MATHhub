from django.urls import path
from .views import survey_page, save_answers


app_name = 'survey'

urlpatterns = [
    path('what_mathematician_you_are/',
         survey_page, name='survey_page'),
    path('save-answers/', save_answers)
]
