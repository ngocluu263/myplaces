'''
Created on May 28, 2013

@author: ivan
'''

from django.conf.urls import patterns, include, url
from django.conf.urls import *
import views
from django.views.generic import TemplateView, ListView
from models import PlacesGroup
from django.contrib.auth.decorators import login_required, permission_required
import format

from rest2backbone.resources import IndexedRouter
from resources import PlacesViewSet, GroupsViewSet, AddressesViewSet, GeocodeReverse, Geocode
from rest2backbone.views import restApi
from rest2backbone.forms import FormFactory
from myplaces.explaces import ExportView

router=IndexedRouter(trailing_slash=False)
router.register('place',PlacesViewSet )
router.register('group', GroupsViewSet )
router.register('address', AddressesViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mapy.views.home', name='home'),
    url(r'^api/', include(router.urls)),
    url(r'^api/geocode/?$', Geocode.as_view() ),
    url(r'^api/geocode/reverse/?$', GeocodeReverse.as_view() ),
    url(r'^import/(?P<step>\d+)/?$', 
        permission_required('myplaces.import_placesgroup', raise_exception=True)(views.upload_places), name='upload-places'),
    url(r'^map/?/(?P<group_id>\d+)/?(?P<place_id>\d+)?/?$', TemplateView.as_view(template_name='map.html')),
   
    url(r'^geojson/group/(?P<group_id>\d+)/?', views.group_geojson),
    url(r'^geojson/group/voronoi/(?P<group_id>\d+)/?', views.group_voronoi_geojson),
    
    url(r'^js-restAPI/?$', restApi.as_view(), {'router': router, 'url_prefix':'/mp/api'}, name='js-api'),   
    url(r'^/?$', TemplateView.as_view(template_name='home.html'), {'forms': FormFactory(router), 'formats':format.index()}, name='home'),
    url(r'^info/about/?$', TemplateView.as_view(template_name='info/about.html')),
    url(r'^info/contribute/?$', TemplateView.as_view(template_name='info/contribute.html')),  
    url(r'^info/terms/?$', TemplateView.as_view(template_name='info/terms.html')),
    url(r'^info/contact/?$', TemplateView.as_view(template_name='info/contact.html')),
    url(r'^export/group/(?P<group>\d+)/(?P<fmt>[^/]+)/?', ExportView.as_view()),
                   
    
    
)