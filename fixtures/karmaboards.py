from dataclasses import dataclass
from datetime import datetime

from dateutil.relativedelta import relativedelta
from pytz import timezone

from fixtures.constants import USER_1_ID
from src.app_auth.models import User
from src.karmaspace.models import Karma, KarmaBoard


today = datetime.now(timezone("Europe/Warsaw"))
yesterday = today - relativedelta(days=1)
two_days_ago = today - relativedelta(days=2)
four_days_ago = today - relativedelta(days=4)
ten_days_ago = today - relativedelta(days=10)
two_months_ago = today - relativedelta(months=2)

user_1 = User.objects.get(id=USER_1_ID)


@dataclass
class KarmaData:
    name: str
    value: int
    created_at: datetime


def _create_karma_fixture(karmaboard, karma_data: KarmaData) -> None:
    karma = Karma.objects.create(
        karmaboard=karmaboard,
        name=karma_data.name,
        value=karma_data.value,
    )
    karma.created_at = karma_data.created_at
    karma.save()


###################################
# KarmaBoard 1 - Obowiązki domowe #
###################################

karmaboard_1 = KarmaBoard.objects.create(
    owner=user_1,
    name="Obowiązki domowe",
)

karmas_data = [
    KarmaData(name="Odkurzanie góry", value=3, created_at=today),
    KarmaData(name="Zmywanie garów", value=4, created_at=yesterday),
    KarmaData(name="Wynoszenie pudeł i śmieci", value=11, created_at=yesterday),
    KarmaData(name="Mycie luster", value=-10, created_at=two_days_ago),
    KarmaData(name="Nadanie paczek", value=5, created_at=four_days_ago),
    KarmaData(name="Naprawa cokołu", value=15, created_at=ten_days_ago),
    KarmaData(name="Pomalowanie barierki", value=-11, created_at=two_months_ago),
]

for karma_data_ in karmas_data:
    _create_karma_fixture(karmaboard_1, karma_data_)


###################################
# KarmaBoard 2 - Obowiązki domowe #
###################################

karmaboard_2 = KarmaBoard.objects.create(
    owner=user_1,
    name="Rośliny i ogród",
)

karmas_data = [
    KarmaData(name="Podlewanie monstery i fikusa", value=3, created_at=today),
    KarmaData(name="Przesadzenie Palmy Areka", value=4, created_at=yesterday),
    KarmaData(name="Kupno i przywiezienie ziemi z Sansevierą", value=11, created_at=yesterday),
]

for karma_data_ in karmas_data:
    _create_karma_fixture(karmaboard_2, karma_data_)

#####################################
# KarmaBoard 3 - KarmaSpace startup #
#####################################

karmaboard_3 = KarmaBoard.objects.create(
    owner=user_1,
    name="KarmaSpace startup",
)

karmas_data = [
    KarmaData(name="Rozwinięcie mapy myśli (Core)", value=3, created_at=today),
    KarmaData(
        name="Znalezienie potencjalnych motywów dla KarmaBoardów",
        value=4,
        created_at=yesterday,
    ),
    KarmaData(name="3h programowania FE + BE", value=11, created_at=yesterday),
]

for karma_data_ in karmas_data:
    _create_karma_fixture(karmaboard_3, karma_data_)
