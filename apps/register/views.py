from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

User = get_user_model()

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "register/register.html", {
                "error": "Passwords do not match.",
                "username": username,
            })
        if User.objects.filter(username=username).exists():
            return render(request, "register/register.html", {
                "error": "Username already exists.",
                "username": username,
            })
        User.objects.create_user(username=username, password=password)
        return redirect("login:login")
    return render(request, "register/register.html")