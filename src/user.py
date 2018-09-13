import firebase_admin
from firebase_admin import credentials

class User(object):

    def __init__(self, display_name, email, password):
        try:
            firebaseUser = firebase_admin.auth.create_user(display_name, email, password)
            self.userId = firebaseUser.uid
            self.displayName = firebaseUser.display_name
            self.email = firebaseUser.email
            self.password = firebaseUser.password
        # TODO: Manejar excepciones
        except ValueError:
            raise ValueError
        except firebase_admin.auth.AuthError:
            raise firebase_admin.auth.AuthError



