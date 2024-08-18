import dataplane.dataplane as dp
import logging
import auth.models as auth_models  # Import all to avoid circular imports
from auth.schemas import UserProfile


def controlplane_auth(app_token: str) -> auth_models.AuthResponse:

    _auth_response = auth_models.AuthResponse(status=False, user_profile={})
    try:
        _auth_response = dp.dataplane_login(app_token)
        _auth_response = auth_models.AuthResponse(**_auth_response)
    except Exception as e:
        _auth_response = auth_models.AuthResponse(
            status=False, user_profile=UserProfile()
        )
        # logging.error(f"Failed logging in to dataplane {e}")

    return _auth_response
