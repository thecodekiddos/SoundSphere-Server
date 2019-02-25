from flask import flash
from flask_login import current_user, login_user
from sqlalchemy.orm.exc import NoResultFound
from flask_dance import OAuth1ConsumerBlueprint
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from ..database.db import OAuth, db, User
import os

# api = Namespace('discogs', description="Discogs endpoints")

discogs_blueprint = OAuth1ConsumerBlueprint("discogs", __name__,
                                            client_key=os.environ['DISCOGS_KEY'],
                                            client_secret=os.environ["DISCOGS_SECRET"],
                                            signature_method="HMAC-SHA1",
                                            base_url="https://api.discogs.com",
                                            request_token_url="https://api.discogs.com/oauth/request_token",
                                            access_token_url="https://api.discogs.com/oauth/access_token",
                                            authorization_url="https://www.discogs.com/oauth/authorize",
                                            redirect_url="http://localhost:5000/home",
                                            backend=SQLAlchemyBackend(OAuth, db.session, user=current_user)
                                            )


@oauth_authorized.connect_via(discogs_blueprint)
def discogs_logged_in(discogs_blueprint, token):
    if not token:
        flash("Failed to log in", category="error")
        return False

    resp = discogs_blueprint.session.get("account/verify_credientials.json")
    if not resp.ok:
        msg = "Failed to fetch user info"
        flash(msg, category="error")
        return False

    discogs_info = resp.json()
    user_id = str(discogs_info["id"])

    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(
        provider=discogs_blueprint.name,
        provider_user_id=user_id,
    )
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(
            provider=discogs_blueprint.name,
            provider_user_id=user_id,
            token=token,
        )

    if oauth.user:
        login_user(oauth.user)
        flash("Successfully signed in.")

    else:
        # Create a new local user account for this user
        user = User(
            name=discogs_info["username"],
        )
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # Log in the new local user account
        login_user(user)
        flash("Successfully signed in.")

    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False


# notify on OAuth provider error
@oauth_error.connect_via(discogs_blueprint)
def discogs_error(discogs_blueprint, message, response):
    msg = (
        "OAuth error from {name}! "
        "error={error} description={description}"
    ).format(
        name=discogs_blueprint.name,
        error=message,
        description=response,
    )
    flash(msg, category="error")
    return False
