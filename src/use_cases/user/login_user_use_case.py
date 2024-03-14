from flask import flash
from flask_login import login_user

from ...utils.password_hasher import PasswordHash
from ...forms.login_form import LoginForm
from ...repositories.user_repository import UserRepository


class LoginUserUseCase():

    def __init__(self, form: LoginForm, repository: UserRepository, pwd_hasher: PasswordHash):
        self.__repository = repository
        self.__form = form
        self.__pwd_hasher = pwd_hasher

    def attempt_login_user(self):
        username = self.__form.username.data
        password = self.__form.password.data

        valid_credentials = self.verify_credentials(username, password)

        if valid_credentials:
            user = self.__repository.get_user_by_username(username)
            login_user(user)
            return True

        return False

    def verify_credentials(self, username, password):
        user_exists = self.__repository.exists_user_with_field(
            "username", username)
        if user_exists:
            database_password = self.__repository\
                .get_user_password_by_username(username)

            pwd_is_correct = self.__pwd_hasher\
                .check_password(password, database_password)

            if not pwd_is_correct:
                flash("Senha incorreta", "error")

            return pwd_is_correct

        flash("Usuário não encontrado", "error")
        return False

   