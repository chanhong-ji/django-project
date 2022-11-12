from rest_framework import serializers
from experiences.models import Perk


class PerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"
