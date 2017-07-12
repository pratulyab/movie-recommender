from django.conf.urls import url, include
from .views import search, movie

urlpatterns = [
		url(r'^home/$', home, name='home'),
#		url(r'^logout/$', logout, name='logout'),
		url(r'^edit_account/$', edit_account, name='edit_account'),
		url(r'^activate/(?P<user_hashid>[a-zA-Z0-9]{13,})/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),
		url(r'^reset_password/(?P<user_hashid>[a-zA-Z0-9]{13,})/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', reset_password, name='reset_password'),
		url(r'^forgot_password/$', forgot_password, name='forgot_password'),
		url(r'^social_profile/$', social_profile, name='social_profile'),
		url(r'pwd_activate/(?P<user_hashid>[a-zA-Z0-9]{13,})/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', set_usable_password_activation, name='usable_pwd_activation'),
]
