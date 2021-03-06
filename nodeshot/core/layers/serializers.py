from django.conf import settings
from rest_framework import serializers, pagination
from rest_framework_gis import serializers as geoserializers

from .models import Layer

from nodeshot.core.base.serializers import GeoJSONPaginationSerializer
from nodeshot.core.nodes.models import Node,StatusIcon
from nodeshot.core.nodes.serializers import NodeListSerializer


__all__ = [
    'LayerDetailSerializer',
    'LayerListSerializer',
    'LayerNodeListSerializer',
    'GeoLayerListSerializer',
    'CustomNodeListSerializer',
    'PaginatedLayerListSerializer',
    'PaginatedGeojsonLayerListSerializer',
    'LayerStatusIconSerializer',
    'StatusIconSerializer',
]


class LayerListSerializer(geoserializers.GeoModelSerializer):
    """
    Layer list
    """
    details = serializers.HyperlinkedIdentityField(view_name='api_layer_detail', slug_field='slug')
    nodes = serializers.HyperlinkedIdentityField(view_name='api_layer_nodes_list', slug_field='slug')
    geojson = serializers.HyperlinkedIdentityField(view_name='api_layer_nodes_geojson', slug_field='slug')
    
    class Meta:
        model = Layer

        fields= (
            'id', 'slug', 'name', 'center', 'area',
            'details', 'nodes', 'geojson'
        )


class PaginatedLayerListSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = LayerListSerializer

class PaginatedGeojsonLayerListSerializer(GeoJSONPaginationSerializer):
    class Meta:
        object_serializer_class = LayerListSerializer

class GeoLayerListSerializer(geoserializers.GeoFeatureModelSerializer, LayerListSerializer):
    class Meta:
        model = Layer
        geo_field = 'area'

        fields= ('id', 'name', 'slug')
        
        
class LayerDetailSerializer(LayerListSerializer):
    """
    Layer details
    """
    
    class Meta:
        model = Layer
        fields = ('name', 'center', 'area', 'zoom', 'is_external',
                  'description', 'text', 'organization', 'website', 'nodes', 'geojson')
        

class CustomNodeListSerializer(NodeListSerializer):
    
    class Meta:
        model = Node
        fields = [
            'name', 'slug', 'user',
            'geometry', 'elev', 'address', 'description',
            'updated', 'added', 'details'
        ]
        read_only_fields = ['added', 'updated']
        geo_field = 'geometry'


class LayerNodeListSerializer(LayerDetailSerializer):
    """
    Nodes of a Layer
    """
    
    class Meta:
        model = Layer

        fields = ('name', 'description', 'text', 'organization', 'website')
        
        
class StatusIconSerializer(serializers.ModelSerializer):
    status = serializers.Field(source='status')
    class Meta:
        model = StatusIcon
        fields = ('status','background_color',)
        

class LayerStatusIconSerializer(serializers.ModelSerializer):
    """
    Layer details
    """
    status_icons = StatusIconSerializer(source='statusicon_set')
    
    class Meta:
        model = Layer
        fields = ('slug', 'status_icons')
