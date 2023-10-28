from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
import smtplib
import re

import smtplib
import base64
from google.oauth2.credentials import Credentials
import google.auth.transport.requests

class SignupScreen(Screen):
    message = StringProperty('')

    def send_verification_email(self, email):
        try:
            with open("token.pkl", "rb") as token_file:
                credentials = pickle.load(token_file)

            # Refresh the token if it's expired
            request = google.auth.transport.requests.Request()
            credentials.refresh(request)

            # Set up the SMTP server and port
            smtp_server = "smtp.gmail.com"
            port = 587

            # Create the SMTP session
            server = smtplib.SMTP(smtp_server, port)
            server.starttls()
            
            # Use the OAuth2 token to authenticate
            auth_string = 'user={0}\1auth=Bearer {1}\1\1'.format(credentials.username, credentials.token)
            server.docmd('AUTH', 'XOAUTH2 ' + base64.b64encode(auth_string.encode()).decode())

            # Email content
            sender_email = credentials.username
            subject = "Email Verification for Your App"
            body = "Hello, \n\nPlease verify your email by clicking the link below:\n[verification_link_here]"
            message = f"Subject: {subject}\n\n{body}"

            # Sending the email
            server.sendmail(sender_email, email, message)
            server.quit()

        except Exception as e:
            print(e)  # Printing the exception for debugging purposes
            self.message = "Failed to send the verification email. Please try again."



class SignupApp(App):

    def sign_up(self, email, username, password):
        screen = self.root

        # Check if email ends with @gmu.edu
        if not re.match(r"[^@]+@gmu\.edu", email):
            screen.message = "Please enter a valid GMU email."
            return

        # Check username and password length as a basic validation
        if len(username) < 4:
            screen.message = "Username should be at least 4 characters."
            return

        if len(password) < 6:
            screen.message = "Password should be at least 6 characters."
            return

        # Send verification email
        screen.send_verification_email(email)

        # Update message
        screen.message = "Verification email sent! Check your inbox."

    def build(self):
        return SignupScreen()


if __name__ == "__main__":
    SignupApp().run()
