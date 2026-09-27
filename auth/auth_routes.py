from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from database.db import db
from database.models import User


# ---------------------------------------------------
# Blueprint
# ---------------------------------------------------

auth_bp = Blueprint(
    "auth",
    __name__
)


# ---------------------------------------------------
# Register Route
# ---------------------------------------------------

@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Check Existing User
        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash(
                "Email already exists",
                "danger"
            )

            return redirect(
                url_for("auth.register")
            )

        # Hash Password
        hashed_password = generate_password_hash(
            password
        )

        # Create User
        new_user = User(

            username=username,
            email=email,
            password=hashed_password

        )

        db.session.add(new_user)
        db.session.commit()

        flash(
            "Registration successful. Please login.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "register.html"
    )


# ---------------------------------------------------
# Login Route
# ---------------------------------------------------

@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    from flask_login import current_user
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user, remember=True)

            return redirect(
                url_for("home")
            )

        flash(
            "Invalid email or password",
            "danger"
        )

    return render_template(
        "login.html"
    )


# ---------------------------------------------------
# Logout Route
# ---------------------------------------------------

@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Logged out successfully",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )