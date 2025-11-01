from django.db import models


class MealTypeChoices(models.TextChoices):
    BREAKFAST =  'Breakfast', 'Breakfast'
    LUNCH =  'Lunch', 'Lunch'
    DINNER =  'Dinner', 'Dinner'
    SNACK =  'Snack', 'Snack'

class DungeonDifficultyChoices(models.TextChoices):
    EASY =  'Easy', 'Easy'
    MEDIUM =  'Medium', 'Medium'
    HARD =  'Hard', 'Hard'

class WorkoutTypeChoices(models.TextChoices):
    CARDIO =  'Cardio', 'Cardio'
    STRENGTH =  'Strength', 'Strength'
    YOGA =  'Yoga', 'Yoga'
    CROSSFIT =  'CrossFit', 'CrossFit'
    CALISTHENICS =  'Calisthenics', 'Calisthenics'

class Brands(models.TextChoices):
    ASUS = 'Asus', 'Asus'
    ACER = 'Acer', 'Acer'
    APPLE = 'Apple', 'Apple'
    LENOVO = 'Lenovo', 'Lenovo'
    DELL = 'Dell', 'Dell'

class OS(models.TextChoices):
    WINDOWS = 'Windows', 'Windows'
    MACOS = 'MacOS', 'MacOS'
    CHROMEOS = 'ChromeOS', 'ChromeOS'
    LINUX = 'Linux', 'Linux'

