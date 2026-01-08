from django.db import models

class Report(models.Model):
    name = models.CharField(max_length=100)
    generated_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        'accounts.User',  # or admin user
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return f"{self.name} - {self.generated_at}"
