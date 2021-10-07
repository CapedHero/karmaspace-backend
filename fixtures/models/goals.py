from src.karmaspace.models import Goal, KarmaBoard


def create_goals(karmaboard: KarmaBoard) -> None:
    Goal.objects.create(
        karmaboard=karmaboard,
        owner=karmaboard.owner,
        timeframe=Goal.Timeframe.DAILY,
        target_value=10,
    )
