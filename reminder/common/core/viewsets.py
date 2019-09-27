from rachel.views import ViewSet
from oauth2_provider.models import AccessToken


class APIView(ViewSet):
    def _set_client_credentials_user(self):
        if isinstance(self.request.auth, AccessToken):
            self.request.user = self.request.auth.application.user
            self.request.auth = self.request.user
