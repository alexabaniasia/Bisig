from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

User = get_user_model()


def register_view(request):
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""
        confirm_password = request.POST.get("confirm_password") or ""

        def fail(message):
            return render(request, "register/register.html", {
                "error": message,
                "username": username,
            })

        if not username:
            return fail("Please enter a username.")
        if password != confirm_password:
            return fail("Passwords do not match.")
        if User.objects.filter(username=username).exists():
            return fail("Username already exists.")
        try:
            validate_password(password, user=User(username=username))
        except ValidationError as e:
            return fail(" ".join(e.messages))

        User.objects.create_user(username=username, password=password)
        return redirect("login:login")
    return render(request, "register/register.html")