from django.contrib.auth import get_user_model, login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect, render

User = get_user_model()


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home:home")

    if request.method == "POST":
        values = {
            "username": (request.POST.get("username") or "").strip(),
            "full_name": (request.POST.get("full_name") or "").strip(),
            "barangay": (request.POST.get("barangay") or "").strip(),
            "email": (request.POST.get("email") or "").strip(),
        }
        password = request.POST.get("password") or ""
        confirm_password = request.POST.get("confirm_password") or ""

        def fail(message):
            return render(request, "register/register.html", {"error": message, "values": values})

        if not values["full_name"]:
            return fail("Please enter your full name.")
        if not values["barangay"]:
            return fail("Please enter your barangay.")
        if not values["username"]:
            return fail("Please enter a username.")
        if values["email"]:
            try:
                validate_email(values["email"])
            except ValidationError:
                return fail("Please enter a valid email address, or leave it blank.")
        if password != confirm_password:
            return fail("Passwords do not match.")
        if User.objects.filter(username__iexact=values["username"]).exists():
            return fail("Username already exists.")
        try:
            validate_password(password, user=User(username=values["username"]))
        except ValidationError as e:
            return fail(" ".join(e.messages))

        user = User.objects.create_user(
            username=values["username"],
            password=password,
            email=values["email"],
            full_name=values["full_name"],
            barangay=values["barangay"],
        )
        login(request, user)
        return redirect("home:home")

    return render(request, "register/register.html", {"values": {}})
