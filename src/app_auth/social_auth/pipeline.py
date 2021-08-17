import logging
from tempfile import NamedTemporaryFile

from django.contrib.auth import login
from django.core.files import File

import requests
from social_core.pipeline.partial import partial


logger = logging.getLogger("main")


def login_with_social_auth(strategy, backend, user=None, *args, **kwargs):
    if user is None:
        return

    if backend.name == "facebook":
        auth_backend = "social_core.backends.facebook.FacebookOAuth2"
    else:
        raise RuntimeError("Unhandled Social Auth backend!")

    login(strategy.request, user, auth_backend)


def save_avatar(backend, user, response, is_new=False, *args, **kwargs):
    if user is None:
        return

    if backend.name == "facebook" and is_new:
        user_picture_url = f"https://graph.facebook.com/{response['id']}/picture"
        user_picture_params = {"type": "large", "access_token": response["access_token"]}

        try:
            user_picture_response = requests.get(user_picture_url, params=user_picture_params)
            user_picture_response.raise_for_status()
        except requests.HTTPError:
            logger.exception("Failed downloading Facebook image.")
            return
        else:
            img_temp = NamedTemporaryFile()
            img_temp.write(user_picture_response.content)
            img_temp.flush()
            user.avatar.save(f"{user.username}.jpg", File(img_temp))


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
