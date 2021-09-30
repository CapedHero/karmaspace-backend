from tempfile import NamedTemporaryFile

from django.contrib.auth import login
from django.core.files import File

import requests
from loguru import logger
from social_core.pipeline.partial import partial


def login_with_social_auth(strategy, backend, user=None, *args, **kwargs):
    if user is None:
        return

    if backend.name == "facebook":
        auth_backend = "social_core.backends.facebook.FacebookOAuth2"
    elif backend.name == "google-openidconnect":
        auth_backend = "social_core.backends.google_openidconnect.GoogleOpenIdConnect"
    else:
        raise RuntimeError(
            f"Unhandled Social Auth backend! "
            f"backend.name={backend.name} "
            f"type(backend)={type(backend)}"
        )

    login(strategy.request, user, auth_backend)


def save_avatar(backend, user, response, is_new=False, *args, **kwargs):
    if user is None or not is_new:
        return

    if backend.name == "facebook":
        user_picture_url = f"https://graph.facebook.com/{response['id']}/picture"
        user_picture_params = {"type": "large", "access_token": response["access_token"]}
    elif backend.name == "google-openidconnect":
        user_picture_url = response.get("picture")
        user_picture_params = {}
    else:
        return

    try:
        user_picture_response = requests.get(user_picture_url, params=user_picture_params)
        user_picture_response.raise_for_status()
        _, file_suffix = user_picture_response.headers["Content-Type"].split("/")
    except (requests.HTTPError, KeyError, IndexError):
        logger.exception(f"Failed downloading social auth image. backend={backend.name}")
        return

    img_temp = NamedTemporaryFile()
    img_temp.write(user_picture_response.content)
    img_temp.flush()
    user.avatar.save(f"{user.username}.{file_suffix}", File(img_temp))


@partial
def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    """
    Handle cases of users that do not have or do not share emails.

    This pipeline is for future reference in case we want to handle cases, when
    users do not share their email with us.

    Source:
        https://github.com/python-social-auth/social-examples/blob/master/example-common/pipeline.py#L4-L16

    Partial pipeline:
        https://python-social-auth.readthedocs.io/en/latest/pipeline.html?highlight=partial#partial-pipeline

    If we decide to eventually use this partial pipeline, we will have to
    add email validation:
        https://python-social-auth.readthedocs.io/en/latest/pipeline.html?highlight=partial#email-validation
    """
    if kwargs.get("ajax") or user and user.email:
        return
    elif is_new and not details.get("email"):
        email = strategy.request_data().get("email")
        if email:
            details["email"] = email
        else:
            current_partial = kwargs.get("current_partial")
            return strategy.redirect("/email?partial_token={0}".format(current_partial.token))
