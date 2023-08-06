"""IndieAuth client."""

import web

# XXX from twilio.base.exceptions import TwilioException, TwilioRestException
# XXX from twilio.jwt.access_token import AccessToken
# XXX from twilio.jwt.access_token.grants import ChatGrant, VideoGrant
# XXX from twilio.rest import Client

app = web.application(__name__, prefix="live")
# XXX twilio_account_sid = app.cfg.get("TWILIO_ACCOUNT_SID")
# XXX twilio_api_key_sid = app.cfg.get("TWILIO_API_KEY_SID")
# XXX twilio_api_key_secret = app.cfg.get("TWILIO_API_KEY_SECRET")
# XXX try:
# XXX     twilio_client = Client(
# XXX         twilio_api_key_sid, twilio_api_key_secret, twilio_account_sid
# XXX     )
# XXX except TwilioException:
# XXX     twilio_client = None


# XXX def get_chatroom(name):
# XXX     """Return a room, creating one if necessary."""
# XXX     for conversation in twilio_client.conversations.conversations.stream():
# XXX         if conversation.friendly_name == name:
# XXX             return conversation
# XXX     return twilio_client.conversations.conversations.create(friendly_name=name)


@app.control("")
class Live:
    """"""

    def get(self):
        """"""
        return app.view.index()


@app.control("stream")
class Stream:
    """"""

    def get(self):
        """"""
        return app.view.stream()


@app.control("chat")
class Chat:
    """Chat with guests."""

    def get(self):
        """Return a chat room."""
        # if not web.tx.user.session:
        #     raise web.SeeOther("/sign-in")
        return app.view.chat()

    def post(self):
        """Sign user in to chat."""
        username = web.form("username").username
        # XXX conversation = get_chatroom("MyRoom")
        # XXX try:
        # XXX     conversation.participants.create(identity=username)
        # XXX except TwilioRestException as exc:
        # XXX     # do not error if the user is already in the conversation
        # XXX     if exc.status != 409:
        # XXX         raise
        # XXX token = AccessToken(
        # XXX     twilio_account_sid,
        # XXX     twilio_api_key_sid,
        # XXX     twilio_api_key_secret,
        # XXX     identity=username,
        # XXX )
        # XXX token.add_grant(VideoGrant(room="MyRoom"))
        # XXX token.add_grant(ChatGrant(service_sid=conversation.chat_service_sid))
        # XXX return {"token": token.to_jwt(), "conversation_sid": conversation.sid}
