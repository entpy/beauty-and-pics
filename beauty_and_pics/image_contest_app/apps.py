from django.apps import AppConfig

class imageContestAppConfig(AppConfig):

    name = 'image_contest_app'

    def ready(self):
        # import signal handlers
        import image_contest_app.signals
