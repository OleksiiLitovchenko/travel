from rest_framework import serializers
from .models import TravelProject, ProjectPlace
from .services import fetch_artwork


class ProjectPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPlace
        fields = ["id", "external_id", "title", "notes", "visited"]
        read_only_fields = ["id", "title"]


class ProjectPlaceCreateSerializer(serializers.Serializer):
    external_id = serializers.IntegerField()
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate_external_id(self, value):
        artwork = fetch_artwork(value)
        if not artwork:
            raise serializers.ValidationError("Place not found in Art Institute API.")
        return value



class TravelProjectSerializer(serializers.ModelSerializer):
    places = ProjectPlaceSerializer(many=True, read_only=True)

    class Meta:
        model = TravelProject
        fields = [
            "id", "name", "description", "start_date",
            "is_completed", "places", "created_at"
        ]
        read_only_fields = ["id", "is_completed", "created_at"]



class TravelProjectCreateSerializer(serializers.ModelSerializer):
    places = ProjectPlaceCreateSerializer(many=True, required=False)

    class Meta:
        model = TravelProject
        fields = ["id", "name", "description", "start_date", "places"]

    def validate_places(self, places):
        if len(places) > 10:
            raise serializers.ValidationError("Maximum 10 places allowed.")
        external_ids = [p["external_id"] for p in places]
        if len(external_ids) != len(set(external_ids)):
            raise serializers.ValidationError("Duplicate external_id values are not allowed.")
        return places

    def create(self, validated_data):
        places_data = validated_data.pop("places", [])
        project = TravelProject.objects.create(**validated_data)

        for place_data in places_data:
            artwork = fetch_artwork(place_data["external_id"])
            ProjectPlace.objects.create(
                project=project,
                external_id=artwork["external_id"],
                title=artwork["title"],
                notes=place_data.get("notes", "")
            )

        project.update_completed_status()
        return project

class ProjectPlaceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPlace
        fields = ["notes", "visited"]