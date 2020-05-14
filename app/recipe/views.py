from rest_framework import viewsets, mixins, generics,views, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from django.shortcuts import render
from core.models import Tag, Ingredient

from recipe import serializers

class RecipeAttributeViewSet(viewsets.GenericViewSet,
                             mixins.ListModelMixin,
                             mixins.CreateModelMixin):
    """Base viewset for user owened recipe attribute"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class TagViewSet(RecipeAttributeViewSet):
    """Manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(RecipeAttributeViewSet, views.APIView):
    """Manage ingredients in the Database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    @api_view(('GET','DELETE'))
    def show_one_ing(self, pk):
        item = Ingredient.objects.filter(pk=pk).first()
        if self.method == 'GET':
            serializer = serializers.IngredientSerializer(item)
            return Response(serializer.data)
        elif self.method == 'DELETE':
            Ingredient.objects.filter(pk=pk).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
