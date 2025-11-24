from django.db import models

class BreathChoices(models.TextChoices):
    FIRE = "Fire", "Fire"
    ICE = "Ice", "Ice"
    LIGHTNING = "Lightning", "Lightning"
    UNKNOWN = "Unknown", "Unknown"