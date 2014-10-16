from authsys.models import User


class UserFactory():

    DEFAULT_PASSWORD = "test"

    @classmethod
    def create(self, **kwargs):
        user = User(**kwargs)
        user.username = user.username or ('username %s' % User.objects.count())
        user.email = user.email or ("username%s@test.com"
                                    % User.objects.count())
        user.password = UserFactory.DEFAULT_PASSWORD
        user = User.objects.create_user(user.username,
                                        user.email,
                                        user.password)
        UserFactory.setAllWithKwArgs(user, **kwargs)

        user.save()
        return user

    @classmethod
    def setAllWithKwArgs(self, user,  **kwargs):
        for key, value in kwargs.items():
            setattr(user, key, value)
