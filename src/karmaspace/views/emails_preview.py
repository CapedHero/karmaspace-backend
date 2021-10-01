from django.shortcuts import render


def preview_thank_you_for_joining_email_view(request):
    return render(
        request=request,
        template_name="emails/thank_you_for_joining.html",
    )
