from django.db import models
from django.conf import settings


class AnalysisHistory(models.Model):
    PLATFORM_CHOICES = [
        ("seo", "General SEO"),
        ("youtube", "YouTube"),
        ("instagram", "Instagram"),
        ("linkedin", "LinkedIn"),
        ("facebook", "Facebook"),
        ("twitter", "X / Twitter"),
        ("tiktok", "TikTok"),
        ("pinterest", "Pinterest"),
        ("grammar", "Grammar"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="analyses",
    )
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    input_text = models.TextField()
    result = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "analysis histories"

    def __str__(self):
        return f"{self.get_platform_display()} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
