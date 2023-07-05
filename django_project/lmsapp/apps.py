from django.apps import AppConfig

# Sets the default primary key field and specifies the name of the app.
class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lmsapp'
