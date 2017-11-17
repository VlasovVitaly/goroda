from django.contrib.auth import views as auth_views


logout_then_login = auth_views.logout_then_login


class login(auth_views.LoginView):
    template_name = 'login.html'
