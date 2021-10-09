from dataclasses import dataclass

from src.karmaspace.models.unsplash_photo import UnsplashPhoto


@dataclass
class Photos:
    bowl_food: UnsplashPhoto
    english_flag: UnsplashPhoto
    family: UnsplashPhoto
    guitar: UnsplashPhoto
    library: UnsplashPhoto
    succulents: UnsplashPhoto
    sunflowers: UnsplashPhoto
    wooden_house: UnsplashPhoto


def create_unsplash_photos() -> Photos:
    bowl_food, _ = UnsplashPhoto.objects.get_or_create(
        id="kcA-c3f_3FE",
        regular_url="https://images.unsplash.com/photo-1546069901-ba9599a7e63c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyNTkxMDh8MHwxfGNvbGxlY3Rpb258MXxmbHYzSk96TklDa3x8fHx8Mnx8MTYzMzU1NDQ5Nw&ixlib=rb-1.2.1&q=80&w=1080",
        small_url="https://images.unsplash.com/photo-1546069901-ba9599a7e63c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyNTkxMDh8MHwxfGNvbGxlY3Rpb258MXxmbHYzSk96TklDa3x8fHx8Mnx8MTYzMzU1NDQ5Nw&ixlib=rb-1.2.1&q=80&w=400",
        author_name="Anh Nguyen",
        author_url="https://unsplash.com/@pwign",
    )

    english_flag, _ = UnsplashPhoto.objects.get_or_create(
        id="C713D7KSkaY",
        regular_url="https://images.unsplash.com/photo-1603989872628-7880d83bb581?crop=entropy&cs=tinysrgb"
        "&fit=max&fm=jpg&ixid=MnwyNTkxMDh8MHwxfGNvbGxlY3Rpb258MXxmbHYzSk96TklDa3x8fHx8Mnx8MTYzMzU1MDUwMg&ixlib=rb-1.2.1&q=80&w=1080",
        small_url="https://images.unsplash.com/photo-1603989872628-7880d83bb581?crop=entropy&cs=tinysrgb&fit=max&fm"
        "=jpg&ixid=MnwyNTkxMDh8MHwxfGNvbGxlY3Rpb258MXxmbHYzSk96TklDa3x8fHx8Mnx8MTYzMzU1MDUwMg&ixlib=rb-1.2.1"
        "&q=80&w=400",
        author_name="Sigmund",
        author_url="https://unsplash.com/@sigmund",
    )

    family, _ = UnsplashPhoto.objects.get_or_create(
        id="V3dHmb1MOXM",
        regular_url="https://images.unsplash.com/photo-1511895426328-dc8714191300?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyNTkxMDh8MHwxfHJhbmRvbXx8fHx8fHx8fDE2MzM3OTg3MjE&ixlib=rb-1.2.1&q=80&w=1080",
        small_url="https://images.unsplash.com/photo-1511895426328-dc8714191300?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyNTkxMDh8MHwxfHJhbmRvbXx8fHx8fHx8fDE2MzM3OTg3MjE&ixlib=rb-1.2.1&q=80&w=400",
        author_name="Tyler Nix",
        author_url="https://unsplash.com/@tylernixcreative",
    )

    guitar, _ = UnsplashPhoto.objects.get_or_create(
        id="bNKBFtg5vig",
        regular_url="https://images.unsplash.com/photo-1559304754-a042e039e5dd?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyNTkxMDh8MHwxfGNvbGxlY3Rpb258MXxmbHYzSk96TklDa3x8fHx8Mnx8MTYzMzU1NjcxNA&ixlib=rb-1.2.1&q=80&w=1080",
        small_url="https://images.unsplash.com/photo-1559304754-a042e039e5dd?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyNTkxMDh8MHwxfGNvbGxlY3Rpb258MXxmbHYzSk96TklDa3x8fHx8Mnx8MTYzMzU1NjcxNA&ixlib=rb-1.2.1&q=80&w=400",
        author_name="Maxime Favier",
        author_url="https://unsplash.com/@maximefavier",
    )

    library, _ = UnsplashPhoto.objects.get_or_create(
        id="2JIvboGLeho",
        regular_url="https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyNTkxMDh8MHwxfGNvbGxlY3Rpb258N3xmbHYzSk96TklDa3x8fHx8Mnx8MTYzMzU1NTkyNQ&ixlib=rb-1.2.1&q=80&w=1080",
        small_url="https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyNTkxMDh8MHwxfGNvbGxlY3Rpb258N3xmbHYzSk96TklDa3x8fHx8Mnx8MTYzMzU1NTkyNQ&ixlib=rb-1.2.1&q=80&w=400",
        author_name="Susan Q Yin",
        author_url="https://unsplash.com/@syinq",
    )

    sunflowers, _ = UnsplashPhoto.objects.get_or_create(
        id="79RuacUiXUI",
        defaults={
            "regular_url": "https://images.unsplash.com/photo-1552160793-cbaf3ebcba72?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyNTkxMDh8MHwxfGNvbGxlY3Rpb258MXxmbHYzSk96TklDa3x8fHx8Mnx8MTYzMzU0MjI4MA&ixlib=rb-1.2.1&q=80&w=1080",
            "small_url": "https://images.unsplash.com/photo-1552160793-cbaf3ebcba72?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyNTkxMDh8MHwxfGNvbGxlY3Rpb258MXxmbHYzSk96TklDa3x8fHx8Mnx8MTYzMzU0MjI4MA&ixlib=rb-1.2.1&q=80&w=400",
            "author_name": "Jordan Cormack",
            "author_url": "https://unsplash.com/@jordancormack",
        },
    )

    succulents, _ = UnsplashPhoto.objects.get_or_create(
        id="8mqOw4DBBSg",
        regular_url="https://images.unsplash.com/photo-1446071103084-c257b5f70672?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyNTkxMDh8MHwxfGNvbGxlY3Rpb258MnxmbHYzSk96TklDa3x8fHx8Mnx8MTYzMzU1MjgwMQ&ixlib=rb-1.2.1&q=80&w=1080",
        small_url="https://images.unsplash.com/photo-1446071103084-c257b5f70672?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyNTkxMDh8MHwxfGNvbGxlY3Rpb258MnxmbHYzSk96TklDa3x8fHx8Mnx8MTYzMzU1MjgwMQ&ixlib=rb-1.2.1&q=80&w=400",
        author_name="Annie Spratt",
        author_url="https://unsplash.com/@anniespratt",
    )

    wooden_house, _ = UnsplashPhoto.objects.get_or_create(
        id="tj2WkhP3D10",
        regular_url="https://images.unsplash.com/photo-1625592315827-259d633f9f3a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyNTkxMDh8MHwxfGNvbGxlY3Rpb258MXxmbHYzSk96TklDa3x8fHx8Mnx8MTYzMzU1NTA4MA&ixlib=rb-1.2.1&q=80&w=1080",
        small_url="https://images.unsplash.com/photo-1625592315827-259d633f9f3a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwyNTkxMDh8MHwxfGNvbGxlY3Rpb258MXxmbHYzSk96TklDa3x8fHx8Mnx8MTYzMzU1NTA4MA&ixlib=rb-1.2.1&q=80&w=400",
        author_name="Henri Lajarrige Lombard",
        author_url="https://unsplash.com/@henri0019",
    )

    return Photos(
        bowl_food,
        english_flag,
        family,
        guitar,
        library,
        succulents,
        sunflowers,
        wooden_house,
    )
