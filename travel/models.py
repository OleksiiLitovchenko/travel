from django.db import models


class TravelProject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def update_completed_status(self):
        places = self.places.all()
        self.is_completed = places.exists() and all(place.visited for place in places)
        self.save(update_fields=["is_completed"])

    def can_be_deleted(self):
        return not self.places.filter(visited=True).exists()

    def __str__(self):
        return self.name


class ProjectPlace(models.Model):
    project = models.ForeignKey(
        TravelProject,
        related_name="places",
        on_delete=models.CASCADE
    )
    external_id = models.IntegerField()
    title = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    visited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                fields=["project", "external_id"],
                name="unique_place_per_project"
            )
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.project.update_completed_status()

    def delete(self, *args, **kwargs):
        project = self.project
        super().delete(*args, **kwargs)
        project.update_completed_status()

    def __str__(self):
        return f"{self.project.name} - {self.title}"