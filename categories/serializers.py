from rest_framework import serializers
from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    kind = serializers.CharField(read_only=True)

    class Meta:
        model = Category
        fields = (
            "pk",
            "name",
            "kind",
        )
