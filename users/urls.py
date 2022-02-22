from django.urls import path
from . import views 

urlpatterns = [
    # USER PATTERNS
    path('', views.index),
    path('register', views.register),
    path('new_user', views.new_user),
    path('login', views.login),
    path('profile', views.profile),
    path('profile/<int:user_id>/update', views.update_user),
    path('success', views.success),
    path('logout', views.logout),
    
    path('dashboard', views.dashboard),
    path('ticket_form', views.ticket_form),
    path('create_ticket', views.create_ticket),
    path('ticket/<int:ticket_id>/edit', views.edit_ticket),
    path('ticket/<int:ticket_id>/update', views.update_ticket),
    path('ticket/<int:ticket_id>/delete', views.delete_ticket),
    path('add_comment/<int:ticket_id>/', views.add_comment),
    path('comment/<int:comment_id>/delete', views.delete_comment),
    
]
