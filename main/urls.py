from django.urls import path
from main.views import (
    show_main, 
    show_experience, 
    show_projects, 
    create_experience,
    create_project,
    edit_project,
    delete_project,
    edit_experience,
    delete_experience,
    toggle_star,
    toggle_experience_star,
    register,
    login_user,
    logout_user,
    show_xml,
    show_json,
    show_xml_by_id,
    show_json_by_id,
    show_project_xml,
    show_project_json,
    get_projects_json,
    show_project_xml_by_id,
    show_project_json_by_id,
)

app_name = 'main'

urlpatterns = [
    # Halaman HTML
    path('', show_main, name='show_main'),
    path('experience/', show_experience, name='show_experience'),
    path('projects/', show_projects, name='show_projects'),
    
    # Autentikasi
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),

    # Form Experience & Star
    path('create-experience/', create_experience, name='create_experience'),
    path('edit-experience/<str:id>/', edit_experience, name='edit_experience'),
    path('delete-experience/<str:id>/', delete_experience, name='delete_experience'),
    path('experience/star/<str:id>/', toggle_experience_star, name='toggle_experience_star'),

    # Form Project & Star
    path('create-project/', create_project, name='create_project'),
    path('edit-project/<str:id>/', edit_project, name='edit_project'),
    path('delete-project/<str:id>/', delete_project, name='delete_project'),
    path('projects/star/<str:id>/', toggle_star, name='toggle_star'),

    # Data Delivery (XML & JSON)
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),

    # Data Delivery Project (XML & JSON)
    path('projects/xml/', show_project_xml, name='show_project_xml'),
    path('projects/json/', get_projects_json, name='get_projects_json'),
    path('projects/json/legacy/', get_projects_json, name='show_project_json'),
    path('projects/xml/<str:id>/', show_project_xml_by_id, name='show_project_xml_by_id'),
    path('projects/json/<str:id>/', show_project_json_by_id, name='show_project_json_by_id'),
]