"""litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import authentication.views
import feed.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.login_page, name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('signup', authentication.views.signup_page, name='signup'),
    path('feed/', feed.views.feed, name='home'),
    path('create_ticket/', feed.views.create_ticket, name='create_ticket'),
    path('create_review/', feed.views.create_review, name='create_review'),
    path('follow-users/', feed.views.follow_users, name='follow_users'),
    path('review/<int:review_id>/', feed.views.review_snippet, name='review_snippet'),
    path('ticket/<int:ticket_id>/', feed.views.ticket_snippet, name='ticket_snippet'),
    path('create_review_to_ticket/<int:ticket_id>/', feed.views.create_review_to_ticket, name='create_review_to_ticket'),
    path('posts/', feed.views.my_posts, name='my_posts'),
    path('edit_review/<int:review_id>/', feed.views.edit_review, name='edit_review'),
    path('delete_review/<int:review_id>/', feed.views.delete_review, name='delete_review'),
    path('edit_ticket/<int:ticket_id>/', feed.views.edit_ticket, name='edit_ticket'),
    path('delete_ticket/<int:ticket_id>/', feed.views.delete_ticket, name='delete_ticket'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

