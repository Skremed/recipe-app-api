from rest_framework import viewsets, mixins, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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


class IngredientViewSet(RecipeAttributeViewSet):
    """Manage ingredients in the Database"""
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    # def delete(self, request):
    #     print(request.data[0]['name'])
    #     object = Ingredient.get_object(request.data[0]['name'])
    #     object.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
