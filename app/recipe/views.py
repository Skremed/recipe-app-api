from rest_framework import viewsets, mixins, generics, views, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404

from core.models import Tag, Ingredient, Recipe

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



class TagViewSet(RecipeAttributeViewSet, mixins.DestroyModelMixin):
    """Manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return self.serializer_class

        return self.serializer_class

    def retrieve(self, request, pk=None):
        queryset = Tag.objects.all()
        tag = get_object_or_404(queryset, pk=pk)
        serializer = serializers.TagSerializer(tag)
        return Response(serializer.data)


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

class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)
