from pydantic import BaseModel
from flask_login import UserMixin
from auth.schemas import UserProfile
import auth.auth as auth  # Import all to avoid circular imports


class UserAuthenticated(UserMixin):

    def __init__(
        self,
        id=None,
    ):
        self.id = id
        self.get_user_profile()

    def get_user_profile(self):
        _auth_response = auth.controlplane_auth(self.id)
        self.user_profile = _auth_response.user_profile


class AuthResponse(BaseModel):
    status: bool
    user_profile: UserProfile
