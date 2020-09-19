from django.apps import AppConfig

class HospitalAuthConfig(AppConfig):
    name = 'hospital_auth'

    def ready(self):
        import hospital_auth.signals