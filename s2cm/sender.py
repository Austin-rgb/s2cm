import requests as req


class SCMSender:
    def __init__(self, server_url, sender_session):
        self.session = req.sessions.Session()
        # session_cookie = req.sessions.cookies.create_cookie('sender_session',sender_session)
        # self.session.cookies.set_cookie(session_cookie)
        self.server_url = server_url

    def send(self, username, message):
        """
        send a message to a user identified by the username
        """
        self.session.post(
            f"{self.server_url}/send", data=dict(username=username, message=message)
        )

    def set_hs(self, username, session):
        """
        set the http cookie for a user,
        the user can then be able to receive messages sent to this username after submitting this http cookie to the server
        """
        self.session.post(
            f"{self.server_url}/set_username",
            data=dict(username=username, session=session),
        )
        print(f"posted; username:{username},session:{session}")
