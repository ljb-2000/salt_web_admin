from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'salt_web_admin.views.home', name='home'),
    # url(r'^salt_web_admin/', include('salt_web_admin.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','salt_web_admin_index.views.index'),
    url(r'^execute$','salt_web_admin_index.views.execute'),
    url(r'^getjobinfo$','salt_web_admin_index.views.getjobinfo'),
    url(r'^rebootha$','salt_web_admin_index.views.rebootha'),
    url(r'^rebootnginx$','salt_web_admin_index.views.rebootnginx'),
    url(r'^reloadnginx$','salt_web_admin_index.views.reloadnginx'),
    url(r'^testping$','salt_web_admin_index.views.testping'),
    url(r'^hafileupdate$','salt_web_admin_index.views.hafileupdate'),
    url(r'^nginxfileupdate$','salt_web_admin_index.views.nginxfileupdate'),
    url(r'^nginx_cache_url_withargs$','salt_web_admin_index.nginx_cache_purge.nginx_cache_url_withargs'),
    url(r'^result_check$','salt_web_admin_index.views.result_check'),
    url(r'^login/$','salt_web_admin_index.login.user_login'),
    url(r'^replacehaconf$','salt_web_admin_index.views.replacehaconf'),
    url(r'^replacenginxconf$','salt_web_admin_index.views.replacenginxconf'),
)
