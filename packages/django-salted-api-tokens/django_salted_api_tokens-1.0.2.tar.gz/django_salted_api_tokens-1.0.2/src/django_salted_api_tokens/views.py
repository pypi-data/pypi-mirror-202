from ksuid import ksuid
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import ApiToken
from .serializers import TokenResponseSerializer
from .settings import (DSAT_HASHLIB_ALGO, DSAT_MAX_TOKENS_PER_USER,
                       DSAT_TOKEN_LENGTH)
from .utils import gen_token, hashed_secret


class CreateApiToken(ObtainAuthToken):
    """
    Create API access token for user.
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        n_user_tokens = ApiToken.objects.filter(user=user).count()
        if n_user_tokens >= DSAT_MAX_TOKENS_PER_USER:
            raise ValidationError('Maximum tokens limit reached for user')
        token_id, user_token = f'{ksuid()}', gen_token(n_chars=DSAT_TOKEN_LENGTH)
        db_token, created = ApiToken.objects.get_or_create(
            user=user,
            token_id=token_id,
            token=hashed_secret(secret=user_token, algo=DSAT_HASHLIB_ALGO),
        )
        token_resp = TokenResponseSerializer(
            {'token_id': db_token.token_id, 'token': user_token}
        ).data
        return Response(token_resp)
