from dataclasses import dataclass
from datetime import datetime
from typing import List

from dateutil.relativedelta import relativedelta
from pytz import timezone

from fixtures.models.karmaboards import KarmaBoards
from src.karmaspace.models import Karma, KarmaBoard


@dataclass
class KarmaData:
    name: str
    value: int
    created_at: datetime
    duration_in_m: int = 0
    is_task: bool = False
    note: str = ""


def create_karmas(karmaboards: KarmaBoards) -> None:
    today = datetime.now(timezone("Europe/Warsaw"))
    yesterday = today - relativedelta(days=1)
    two_days_ago = today - relativedelta(days=2)
    three_days_ago = today - relativedelta(days=3)
    four_days_ago = today - relativedelta(days=4)
    five_days_ago = today - relativedelta(days=5)
    six_days_ago = today - relativedelta(days=6)
    seven_days_ago = today - relativedelta(days=7)
    eight_days_ago = today - relativedelta(days=8)
    ten_days_ago = today - relativedelta(days=10)
    twelve_days_ago = today - relativedelta(days=12)
    fourteen_days_ago = today - relativedelta(days=14)
    two_months_ago = today - relativedelta(months=2)

    _create_karmas(
        karmaboard=karmaboards.duties_and_leasure,
        karma_data_collection=[
            KarmaData(
                name="Porządki w szafie i spakowanie nienoszonych rzeczy",
                value=3,
                created_at=today,
                is_task=True,
            ),
            KarmaData(
                name="Odrabianie lekcji z polskiego i matematyki",
                value=4,
                duration_in_m=60,
                note=(
                    "<p>Trzeba znaleźć dodatkowe materiały do geometrii.</p>"
                    "<p>Może jakieś <strong>tablice dydaktyczne</strong> na ścianę?</p>"
                ),
                created_at=today,
            ),
            KarmaData(
                name="Granie na tablecie",
                value=-3,
                duration_in_m=45,
                created_at=yesterday,
            ),
            KarmaData(
                name="Przygotowanie się do klasówki z hiszpańskiego",
                value=6,
                duration_in_m=90,
                created_at=yesterday,
            ),
            KarmaData(name="Wieczorne spotkanie z koleżankami", value=-5, created_at=two_days_ago),
            KarmaData(
                name="Wspólna nauka programowania w Pythonie",
                value=4,
                duration_in_m=60,
                created_at=two_days_ago,
            ),
            KarmaData(
                name="Pomaganie dziadkom w ogródku",
                value=10,
                duration_in_m=150,
                created_at=three_days_ago,
            ),
            KarmaData(
                name="Zajęcia na basenie",
                value=6,
                duration_in_m=60,
                created_at=three_days_ago,
            ),
            KarmaData(
                name="Oglądanie filmików na YouTubie",
                value=-4,
                duration_in_m=60,
                created_at=three_days_ago,
            ),
            KarmaData(
                name="Czytanie lektury",
                value=10,
                duration_in_m=120,
                created_at=four_days_ago,
            ),
            KarmaData(
                name="Pisanie referatu na historię (z małą pomocą 😉)",
                value=4,
                duration_in_m=60,
                created_at=ten_days_ago,
            ),
            KarmaData(
                name="Czytanie lektury",
                value=10,
                duration_in_m=120,
                created_at=two_months_ago,
            ),
            KarmaData(
                name="Seriale na Netflixie",
                value=-6,
                duration_in_m=90,
                created_at=two_months_ago,
            ),
        ],
    )

    _create_karmas(
        karmaboard=karmaboards.house_chores,
        karma_data_collection=[
            KarmaData(
                name="Duże zakupy spożywcze w markecie",
                value=6,
                is_task=True,
                note=(
                    "<p>Pamiętać o:</p>"
                    "<ul>"
                    "<li><p>oliwie</p></li>"
                    "<li><p><strong>totolotku</strong></p></li>"
                    "</ul>"
                ),
                created_at=today,
            ),
            KarmaData(name="Odkurzanie wszystkich pokojów", value=3, created_at=today),
            KarmaData(
                name="Mycie luster",
                value=3,
                note="<p>Nowy płyn do mycia szyb jest fantasyczny : D</p>",
                created_at=today,
            ),
            KarmaData(name="Wynoszenie pudeł i śmieci", value=2, created_at=yesterday),
            KarmaData(name="Zmywanie garnków", value=1, created_at=two_days_ago),
            KarmaData(name="Nadanie paczek", value=3, created_at=four_days_ago),
            KarmaData(name="Naprawa cokołu w kuchni", value=5, created_at=ten_days_ago),
            KarmaData(name="Pomalowanie barierki na balkonie", value=5, created_at=two_months_ago),
        ],
    )

    _create_karmas(
        karmaboard=karmaboards.fitness_and_health,
        karma_data_collection=[
            KarmaData(
                name="Wziąć udział w biegu na 15 km",
                value=30,
                created_at=today,
                is_task=True,
            ),
            KarmaData(
                name="Trening na siłowni",
                value=15,
                note=(
                    "<p>Trzeba przychodzić <strong>przed 11:00</strong>, "
                    "bo potem są już tłumy.</p>"
                ),
                created_at=today,
            ),
            KarmaData(name="Dzień bez mięsa", value=10, created_at=today),
            KarmaData(
                name="Pizza pepperoni na grubym cieście i wino",
                value=-10,
                created_at=yesterday,
            ),
            KarmaData(name="Zjedzenie całej czekolady!", value=-5, created_at=two_days_ago),
            KarmaData(
                name="Wyjście ze znajomymi do knajpy, czyli alkohol i snacki",
                value=-20,
                created_at=three_days_ago,
            ),
            KarmaData(name="Bieganie 5 km", value=5, created_at=three_days_ago),
            KarmaData(
                name="Zrobienie domowych obiadów na trzy dni",
                value=15,
                created_at=five_days_ago,
            ),
            KarmaData(name="Trening na siłowni", value=15, created_at=five_days_ago),
            KarmaData(name="Cheat meal, burgery i lody", value=-10, created_at=six_days_ago),
            KarmaData(name="Bieganie 10 km", value=10, created_at=eight_days_ago),
            KarmaData(
                name="Impreza w domu, czyli alkohol i chipsy",
                value=-25,
                created_at=ten_days_ago,
            ),
            KarmaData(name="Siatkówka z ludźmi z pracy", value=20, created_at=twelve_days_ago),
            KarmaData(name="Krótki trening na siłowni", value=10, created_at=two_months_ago),
        ],
    )

    _create_karmas(
        karmaboard=karmaboards.personal_growth,
        karma_data_collection=[
            KarmaData(
                name="Poczytać ambitną książkę",
                value=8,
                duration_in_m=120,
                created_at=today,
                is_task=True,
                note=(
                    "<ul>"
                    "<li><p><strong>"
                    '"Sapiens. Od zwierząt do bogów" Yuvala?'
                    "</strong></p></li>"
                    "<li><p>"
                    'A może "Pułapki myślenia" Kahnemana?'
                    "</p></li>"
                    "</ul>"
                ),
            ),
            KarmaData(
                name="Poszukiwanie dobrego bloga o marketingu online",
                value=3,
                duration_in_m=45,
                created_at=yesterday,
            ),
            KarmaData(
                name="Granie na konsoli",
                value=-8,
                duration_in_m=120,
                created_at=yesterday,
            ),
            KarmaData(
                name="Seriale na Netflixie",
                value=-10,
                duration_in_m=150,
                created_at=two_days_ago,
            ),
            KarmaData(
                name="Czytanie książki po angielsku (King)",
                value=4,
                duration_in_m=60,
                created_at=two_days_ago,
            ),
            KarmaData(
                name='Słuchanie audiobooka "7 nawyków skutecznego działania"',
                value=3,
                duration_in_m=45,
                created_at=three_days_ago,
            ),
            KarmaData(
                name="Trening na siłowni",
                value=4,
                duration_in_m=60,
                created_at=three_days_ago,
            ),
            KarmaData(
                name='Obejrzenie 2x odcinków "Planeta Ziemia"',
                value=6,
                duration_in_m=90,
                created_at=four_days_ago,
            ),
            KarmaData(
                name="Zaktualizowanie CV i profilu na LinkedIn",
                value=4,
                duration_in_m=60,
                created_at=four_days_ago,
            ),
            KarmaData(
                name='Słuchanie audiobooka "7 nawyków skutecznego działania"',
                value=3,
                duration_in_m=45,
                created_at=seven_days_ago,
            ),
            KarmaData(
                name="Zajęcia z jogi",
                value=4,
                duration_in_m=60,
                created_at=ten_days_ago,
            ),
            KarmaData(
                name="Pójścia do kina na najnowszego Bonda",
                value=-10,
                duration_in_m=150,
                created_at=ten_days_ago,
            ),
            KarmaData(
                name="Basen",
                value=5,
                duration_in_m=75,
                created_at=twelve_days_ago,
            ),
            KarmaData(
                name="Zdanie egzaminu z angielskiego na poziom C1",
                value=20,
                created_at=fourteen_days_ago,
            ),
            KarmaData(
                name="Wyjście do teatru",
                value=12,
                duration_in_m=180,
                created_at=two_months_ago,
            ),
        ],
    )

    _create_karmas(
        karmaboard=karmaboards.plants,
        karma_data_collection=[
            KarmaData(name="Przyciąć wawrzyn i bukszpan", value=3, created_at=today, is_task=True),
            KarmaData(
                name="Podlewanie Monstery i Fikusa",
                value=1,
                note=(
                    "<p>Monstera w końcu <strong>zaczęła rosnąć</strong>! Faktycznie "
                    "potrzebowała więcej światła.</p>"
                ),
                created_at=today,
            ),
            KarmaData(name="Przesadzenie Palmy Areka", value=3, created_at=yesterday),
            KarmaData(
                name="Kupno i przywiezienie Strelicji oraz ziemi do roślin",
                value=5,
                created_at=yesterday,
            ),
            KarmaData(name="Podlewanie Sukulentów", value=1, created_at=four_days_ago),
            KarmaData(name="Walka z ćmą bukszpanową!", value=3, created_at=ten_days_ago),
            KarmaData(
                name="Podlewanie i nawożenie roślin na balkonie",
                value=2,
                created_at=two_months_ago,
            ),
        ],
    )

    _create_karmas(
        karmaboard=karmaboards.learning_english,
        karma_data_collection=[
            KarmaData(
                name="Znalezienie kursu online na poziom C1",
                value=4,
                created_at=today,
                is_task=True,
            ),
            KarmaData(name="Powtarzanie słówek", value=1, created_at=today),
            KarmaData(
                name='Czytanie "Miasteczka Salem" Kinga w oryginale',
                value=3,
                duration_in_m=45,
                note=(
                    "<p>Może następną książką po angielsku wziąć w "
                    "<strong>ebooku</strong>? Na komputerze będzie łatwiej "
                    "sprawdzać i zapisywać nowe słówka.</p>"
                ),
                created_at=yesterday,
            ),
            KarmaData(
                name="Lekcja indywidualna z Johnem",
                value=5,
                duration_in_m=60,
                created_at=yesterday,
            ),
            KarmaData(name="Powtarzanie słówek", value=1, created_at=two_days_ago),
            KarmaData(
                name="Oglądanie materiału na YouTubie o idiomach",
                value=2,
                duration_in_m=30,
                created_at=four_days_ago,
            ),
            KarmaData(name="Powtarzanie słówek", value=1, created_at=four_days_ago),
            KarmaData(
                name='Czytanie "Miasteczka Salem" Kinga w oryginale',
                value=8,
                duration_in_m=120,
                created_at=five_days_ago,
            ),
            KarmaData(name="Powtarzanie słówek", value=1, created_at=ten_days_ago),
            KarmaData(
                name="Robienie ćwiczeń z gramatyki",
                value=3,
                duration_in_m=45,
                created_at=two_months_ago,
            ),
        ],
    )

    _create_karmas(
        karmaboard=karmaboards.learning_guitar,
        karma_data_collection=[
            KarmaData(
                name="Wymienić struny i wyregulować gitarę",
                value=4,
                created_at=today,
                is_task=True,
            ),
            KarmaData(
                name="Ćwiczenie zadanego materiału",
                value=2,
                duration_in_m=30,
                created_at=today,
            ),
            KarmaData(
                name="Ćwiczenie zadanego materiału",
                value=1,
                duration_in_m=15,
                created_at=yesterday,
            ),
            KarmaData(
                name="Oglądanie filmiku o skalach muzycznych na YouTube",
                value=3,
                duration_in_m=45,
                note=(
                    "<p>Link: "
                    '<a href="https://www.youtube.com/watch?v=bw8oUp9geuY" '
                    'rel="noopener noreferrer nofollow">'
                    "Brandon D'eon - Wrong way VS Right way to play scales"
                    "</a>"
                    "</p>"
                ),
                created_at=yesterday,
            ),
            KarmaData(
                name="Lekcja z Mariuszem",
                value=6,
                duration_in_m=60,
                created_at=three_days_ago,
            ),
            KarmaData(
                name="Ćwiczenie zadanego materiału",
                value=4,
                duration_in_m=60,
                created_at=four_days_ago,
            ),
            KarmaData(
                name="Jam session u Roberta",
                value=12,
                duration_in_m=120,
                created_at=five_days_ago,
            ),
            KarmaData(
                name="Nauka budowy akordów z podręcznikiem",
                value=3,
                duration_in_m=45,
                created_at=six_days_ago,
            ),
            KarmaData(
                name="Ćwiczenie zadanego materiału",
                value=2,
                duration_in_m=30,
                created_at=ten_days_ago,
            ),
            KarmaData(
                name="Ćwiczenie zadanego materiału",
                value=2,
                duration_in_m=30,
                created_at=two_months_ago,
            ),
        ],
    )

    _create_karmas(
        karmaboard=karmaboards.reading_books,
        karma_data_collection=[
            KarmaData(
                name='"Gambit królowej" - Walter Tevis',
                value=8,
                created_at=today,
                is_task=True,
                note=(
                    "<p>"
                    "Hm, a może najpierw obejrzeć serial na "
                    "<a "
                    'href="https://www.netflix.com/title/80234304" '
                    'rel="noopener noreferrer nofollow"'
                    ">"
                    "Netflixie"
                    "</a>"
                    "?"
                    "</p>"
                ),
            ),
            KarmaData(name='"Pieśń o Achillesie" - Madeline Miller', value=8, created_at=today),
            KarmaData(
                name='"Diuna" - Frank Herbert',
                value=16,
                created_at=today - relativedelta(days=6),
            ),
            KarmaData(
                name='"Sapiens. Od zwierząt do bogów" - Yuval Noah Harari',
                value=20,
                created_at=today - relativedelta(days=12),
            ),
            KarmaData(
                name='"Nowy wspaniały świat" - Aldous Huxley',
                value=10,
                created_at=today - relativedelta(days=20),
            ),
            KarmaData(
                name='"Sto lat samotności" - Gabriel García Márquez',
                value=10,
                created_at=today - relativedelta(days=24),
            ),
            KarmaData(
                name='"Pan Lodowego Ogrodu - księga 1" - Jarosław Grzędowicz',
                value=12,
                created_at=today - relativedelta(days=30),
            ),
            KarmaData(
                name='"Kocia kołyska" - Kurt Vonnegut',
                value=8,
                created_at=today - relativedelta(days=36),
            ),
            KarmaData(
                name='"Cień wiatru" - Carlos Ruiz Zafón',
                value=10,
                created_at=today - relativedelta(days=42),
            ),
            KarmaData(
                name='"Solaris" - Stanisław Lem',
                value=7,
                created_at=today - relativedelta(days=50),
            ),
            KarmaData(
                name='"Pułapki myślenia. O myśleniu szybkim i wolnym" - Daniel Kahneman',
                value=20,
                created_at=today - relativedelta(days=60),
            ),
            KarmaData(
                name='"Portret Doriana Graya" - Oscar Wilde',
                value=7,
                created_at=today - relativedelta(days=70),
            ),
        ],
    )

    _create_karmas(
        karmaboard=karmaboards.family_relations,
        karma_data_collection=[
            KarmaData(name="Odwiedzić ciocię Anię", value=4, created_at=yesterday, is_task=True),
            KarmaData(
                name="Telefon do babci",
                value=1,
                duration_in_m=15,
                note=(
                    "<p>"
                    "Pamiętać, żeby następnym razem zapytać się o "
                    "<strong>zdjęcia mamy z dzieciństwa</strong>."
                    "</p>"
                ),
                created_at=yesterday,
            ),
            KarmaData(name="Wspólna kolacja z rodzicami", value=8, created_at=two_days_ago),
            KarmaData(name="Pomoc dziadkom w sadzie", value=5, created_at=four_days_ago),
            KarmaData(name="Rozmowa z mamą", value=5, duration_in_m=75, created_at=ten_days_ago),
            KarmaData(
                name="Telefon do babci i dziadka",
                value=2,
                duration_in_m=30,
                created_at=two_months_ago,
            ),
        ],
    )


def _create_karmas(karmaboard: KarmaBoard, karma_data_collection: List[KarmaData]) -> None:
    for karma_data in karma_data_collection:
        karma = Karma.objects.create(
            karmaboard=karmaboard,
            name=karma_data.name,
            value=karma_data.value,
            duration_in_m=karma_data.duration_in_m,
            is_task=karma_data.is_task,
            note=karma_data.note,
        )
        karma.created_at = karma_data.created_at
        karma.save()
