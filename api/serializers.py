# from rest_framework import serializers
# from recipes.models import Ingredient, Purchase
# from rest_framework.validators import UniqueTogetherValidator
#
#
# class IngredientsListSerializer(serializers.ModelSerializer):
#     title = serializers.CharField(source='name')
#     dimension = serializers.CharField(source='unit')
#
#     class Meta:
#         model = Ingredient
#         fields = ('title', 'dimension')
#
#
# class PurchaseSerializer(serializers.ModelSerializer):
#     user = serializers.HiddenField(
#         default=serializers.CurrentUserDefault()
#     )
#     class Meta:
#         model = Purchase
#         fields = ('user', 'recipe')
#         read_only_fields = ('user', )
#         validator = [
#             UniqueTogetherValidator(
#                 queryset=Purchase.objects.all(),
#                 fields=fields
#             )
#         ]
#
