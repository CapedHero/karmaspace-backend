from src.app_auth.models import User


def create_admin() -> None:
    admin = User(
        username="admin",
        email="admin@admin.admin",
        is_superuser=True,
        is_staff=True,
    )
    admin.set_password("admin")
    admin.save()


def create_user(username: str, email: str) -> User:
    return User.objects.create(username=username, email=email)
