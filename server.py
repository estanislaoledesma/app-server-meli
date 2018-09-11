from src.hello import app

import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

'''
user = auth.get_user(uid)
user = auth.get_user_by_email(email)
print('Successfully fetched user data: {0}'.format(user.uid))

user = auth.create_user(
	uid='examplid',
    email='user@example.com',
    email_verified=False,
    phone_number='+15555550100',
    password='secretPassword',
    display_name='John Doe',
    photo_url='http://www.example.com/12345678/photo.png',
    disabled=False)
print('Sucessfully created new user: {0}'.format(user.uid))

'''

if __name__ == "__main__":
	cred = credentials.Certificate('docs/meli-4620b-firebase-adminsdk-8c1z7-a8c5799e31.json')
	default_app = firebase_admin.initialize_app(cred)
	app.run()

