from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import TravelProject, ProjectPlace
from .serializers import (
    TravelProjectSerializer,
    TravelProjectCreateSerializer,
    ProjectPlaceSerializer,
    ProjectPlaceCreateSerializer,
    ProjectPlaceUpdateSerializer,
)
from .services import fetch_artwork


class TravelProjectViewSet(viewsets.ModelViewSet):
    queryset = TravelProject.objects.all().order_by("-created_at")

    def get_serializer_class(self):
        if self.action == "create":
            return TravelProjectCreateSerializer
        return TravelProjectSerializer

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        if project.places.filter(visited=True).exists():
            return Response(
                {"detail": "Cannot delete project with visited places."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["get", "post"], url_path="places")
    def places(self, request, pk=None):
        project = self.get_object()

        if request.method == "GET":
            serializer = ProjectPlaceSerializer(project.places.all(), many=True)
            return Response(serializer.data)

        serializer = ProjectPlaceCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if project.places.count() >= 10:
            raise ValidationError({"detail": "Maximum 10 places allowed in a project."})

        external_id = serializer.validated_data["external_id"]

        if project.places.filter(external_id=external_id).exists():
            raise ValidationError({"detail": "This place already exists in the project."})

        artwork = fetch_artwork(external_id)
        place = ProjectPlace.objects.create(
            project=project,
            external_id=artwork["external_id"],
            title=artwork["title"],
            notes=serializer.validated_data.get("notes", "")
        )
        return Response(ProjectPlaceSerializer(place).data, status=status.HTTP_201_CREATED)

class ProjectPlaceViewSet(viewsets.GenericViewSet):
    queryset = ProjectPlace.objects.all()

    def retrieve(self, request, pk=None):
        place = self.get_object()
        return Response(ProjectPlaceSerializer(place).data)

    def partial_update(self, request, pk=None):
        place = self.get_object()
        serializer = ProjectPlaceUpdateSerializer(place, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        place.project.update_completed_status()
        return Response(ProjectPlaceSerializer(place).data)