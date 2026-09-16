from django.urls import path
from main.views import (
    show_main, 
    show_experience, 
    show_projects, 
    create_experience,
    show_xml,
    show_json,
    show_xml_by_id,
    show_json_by_id,
)

app_name = 'main'

urlpatterns = [
    # Halaman HTML
    path('', show_main, name='show_main'),
    path('experience/', show_experience, name='show_experience'),
    path('projects/', show_projects, name='show_projects'),
    path('create-experience/', create_experience, name='create_experience'),

    # Data Delivery (XML & JSON)
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
]