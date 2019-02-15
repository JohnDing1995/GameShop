from django.db import models
# Create your models here.
from django.utils.datetime_safe import datetime

from JSGameStore import settings


class Game(models.Model):
    game_name = models.TextField(primary_key=True)
    developer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    copies_sold = models.IntegerField()
    price = models.FloatField()
    url = models.URLField(default='http://webcourse.cs.hut.fi/example_game.html')
    category = models.CharField(default='No category', max_length=256)
    CATEGORY_CHOICES=(('No category', 'No category'),
                      ('Action', 'Action'),
                      ('Adventure', 'Adventure'),
                      ('Arcade', 'Arcade'),
                      ('Music', 'Music'),
                      ('Platform', 'Platform'),
                      ('Racing', 'Racing'))


class Purchase(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        name="user",
        on_delete=models.CASCADE
    )
    pid = models.TextField(primary_key=True)
    ref = models.TextField()
    result = models.BooleanField()
    checksum = models.TextField()
    amount = models.FloatField(default=0.0)
    time = models.DateTimeField(auto_now_add=True, blank=True)
    game_state = models.CharField(max_length=255, default="")

class Score(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        name="user",
        on_delete=models.CASCADE,
    )
    game = models.ForeignKey(
        Game,
        name="game",
        on_delete=models.CASCADE
    )
    score = models.FloatField()
    time = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        unique_together = ("user", "game")

class GameState(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        name="user",
        on_delete=models.CASCADE,
    )
    game = models.ForeignKey(
        Game,
        name="game",
        on_delete=models.CASCADE
    )
    time = models.DateTimeField(default=datetime.now, blank=True)
    game_state = models.CharField(max_length=255, default="")

    class Meta:
        unique_together = ("user", "game")
