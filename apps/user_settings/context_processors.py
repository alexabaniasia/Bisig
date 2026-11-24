from .models import UserSettings


def user_preferences(request):
    dark_mode = False
    if request.user.is_authenticated:
        dark_mode = (
            UserSettings.objects.filter(user=request.user)
            .values_list("dark_mode", flat=True)
            .first()
        ) or False
    return {"dark_mode": dark_mode}