from django.urls import path

from .views import *

app_name = 'chart'

urlpatterns = [
    path('', home, name='home'),
    path('ticket-class/1/',
         ticket_class_view_1, name='ticket_class_view_1'),
    path('ticket-class/2/',
         ticket_class_view_2, name='ticket_class_view_2'),
    path('ticket-class/3/',
         ticket_class_view_3, name='ticket_class_view_3'),
    path('world-population/',
         world_population, name='world_population'),  # !!!
    path('json-example/', json_example, name='json_example'),
    path('json-example/data/', chart_data, name='chart_data'),
    path('covid19/', covid19_view, name='covid19'),
]


