from rest_framework import serializers
from snippets.models import Snippet, SubSnip, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'snippets', 'subsnippets']

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    title = serializers.HyperlinkedIdentityField(view_name='snippet-title', format='html')

    class Meta:
        model = Snippet
        fields = ['url', 'id', 'highlight', 'owner', 'title', 'subsnippets']

class SubSnipSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='subsnip-highlight', format='html')

    class Meta:
        model = SubSnip
        fields = ['url', 'id', 'highlight', 'owner', 'snippet',
                'title', 'code', 'linenos', 'language', 'style']


