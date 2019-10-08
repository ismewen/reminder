from django.conf import settings


def discover_views():
    for mod in settings.INSTALLED_APPS:
        print(mod)
        if str(mod).startswith("modules"):
            print(mod)
            try:
                __import__(mod + ".views")
            except Exception as e:
                raise e
                print("import error", e)

