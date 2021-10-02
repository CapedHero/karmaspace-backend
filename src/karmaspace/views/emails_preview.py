from django.shortcuts import render


def preview_follow_up_after_joining_email_view(request):
    return render(
        request=request,
        template_name="emails/follow_up_after_joining.html",
    )


def preview_thank_you_for_joining_email_view(request):
    return render(
        request=request,
        template_name="emails/thank_you_for_joining.html",
    )
