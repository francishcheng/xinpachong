from django.urls import path, include
from .views import index_view,download_view, week_view, days_view, weeks_view, months_view
urlpatterns = [
    path('', index_view, name='index'),
    path('download/', download_view, name='donwload'),
    path('week/', week_view, name='week', kwargs={'collection_name': ''}),
    path('week/<str:collection_name>', week_view, name='week'),
    path('days/', days_view, name='days'),
    path('weeks/', weeks_view, name='weeks'),
    path('months/', months_view, name='months')
    
]
