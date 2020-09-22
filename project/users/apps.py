from django.apps import AppConfig

class HospitalAuthConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals