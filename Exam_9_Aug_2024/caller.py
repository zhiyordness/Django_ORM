import os
from decimal import Decimal

import django
from django.db import transaction, models
from django.db.models import Q, F, Min, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import House, Dragon, Quest


def get_houses(search_string=None):

    houses = House.objects.all()

    if search_string:
        houses = houses.filter(Q(name__icontains=search_string) | Q(motto__icontains=search_string))

    if not search_string or search_string is None or len(houses) == 0:
        return f" No houses match your search."

    result = []
    for h in houses:
        result.append(f"House: {h.name}, wins: {h.wins}, motto: {h.motto if h.motto else 'N/A'}")

    return "\n".join(result)


def get_most_powerful_dragon():
    dragon = Dragon.objects.filter(is_healthy=True).order_by('-power', 'name').first()

    if not dragon:
        return "No relevant data."

    number_of_quests = dragon.quest_set.count()
    return f"The most powerful healthy dragon is {dragon.name} with a power level of {dragon.power:.1f}, breath type {dragon.breath}, and {dragon.wins} wins, coming from the house of {dragon.house}. Currently participating in {number_of_quests} quests."



def update_dragons_data():
    dragons = Dragon.objects.filter(is_healthy=False, power__gt=1.0)
    for dragon in dragons:
        dragon.power -= Decimal('0.1')
        dragon.is_healthy = True
        dragon.save()
    min_power = Dragon.objects.aggregate(Min('power'))['power__min']
    return f"The data for {len(dragons)} dragon/s has been changed. The minimum power level among all dragons is {min_power:.1f}"

def get_earliest_quest():
    earliest_quest = Quest.objects.order_by('start_time').first()
    if not earliest_quest:
        return "No relevant data."

    day = earliest_quest.start_time.day
    month = earliest_quest.start_time.month
    year = earliest_quest.start_time.year

    dragons = earliest_quest.dragons.order_by('-power', 'name')
    dragons_names = '*'.join([dragon.name for dragon in dragons])

    average_power = earliest_quest.dragons.aggregate(
        avg_power = Avg('power')
    )['avg_power'] or 0.0

    return (f"The earliest quest is: {earliest_quest.name}, code: {earliest_quest.code}, "
            f"start date: {day}.{month}.{year}, host: {earliest_quest.host}. "
            f"Dragons: {dragons_names}. "
            f"Average dragons power level: {average_power:.2f}.")


def announce_quest_winner(quest_code):

    if not quest_code or len(quest_code) != 4:
        return "No such quest."

    try:
        with transaction.atomic():

            quest = Quest.objects.select_related('host').prefetch_related(
                models.Prefetch(
                    'dragons',
                    queryset=Dragon.objects.select_related('house')
                )
            ).get(code=quest_code)

            # Check if quest has dragons
            if quest.dragons.count() == 0:
                quest_name = quest.name
                quest_reward = f"{quest.reward:.2f}"
                quest.delete()
                return f"The quest: {quest_name} had no participants and was removed. No wins awarded."

            # Get the most powerful dragon
            winning_dragon = quest.dragons.order_by('-power', 'name').first()

            # Update wins atomically to avoid race conditions
            Dragon.objects.filter(pk=winning_dragon.pk).update(
                wins=models.F('wins') + 1
            )
            House.objects.filter(pk=winning_dragon.house.pk).update(
                wins=models.F('wins') + 1
            )

            # Refresh objects to get updated win counts
            winning_dragon.refresh_from_db()
            winning_dragon.house.refresh_from_db()

            # Store values for response
            quest_name = quest.name
            dragon_name = winning_dragon.name
            house_name = winning_dragon.house.name
            dragon_wins = winning_dragon.wins
            house_wins = winning_dragon.house.wins
            quest_reward = f"{quest.reward:.2f}"

            # Delete the quest
            quest.delete()

            return (f"The quest: {quest_name} has been won by dragon {dragon_name} from house {house_name}. "
                    f"The number of wins has been updated as follows: {dragon_wins} total wins for the dragon "
                    f"and {house_wins} total wins for the house. The house was awarded with {quest_reward} coins.")

    except Quest.DoesNotExist:
        return "No such quest."
    except Exception as e:
        # Log the error in real application
        return "An error occurred while processing the quest winner."

print(announce_quest_winner("FaS#"))