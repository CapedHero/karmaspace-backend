from django.shortcuts import render


def preview_passphrase_email_view(request):
    return render(
        request=request,
        template_name="emails/passphrase.html",
        context={"passphrase": "dummy-passphrase-foo-bar"},
    )
