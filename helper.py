import os
from flask import redirect, render_template, request, session
from functools import wraps

# Check what kind of user is logged in...?

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function