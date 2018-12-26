from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
    
  
   
    
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^bott/$', views.bott, name='bott'),
    url(r'^bott1/$', views.bott1, name='bott1'),
    url(r'^dashbord/$', views.dashbord, name='dashbord'),
    url(r'^edit/$', views.edit_profile, name='edit_profile'),
    url(r'^profile/$', views.view_profile, name='view_profile'),
    url(r'^contact/$', views.ContactUsView.as_view(), {}, 'contactus'),
    url(r'^success/$', views.success, name='success'),
    url(r'^about/$', views.about, name='about'),
     
  
   
  
    

]