from __future__ import annotations

import logging
from datetime import datetime as dt

import jwt
from flask import Blueprint

import ckan.model as model
import ckan.plugins as p
from ckan.plugins import toolkit as tk

import ckanext.let_me_in.utils as lmi_utils
from ckanext.let_me_in.interfaces import ILetMeIn

log = logging.getLogger(__name__)
lmi = Blueprint("lmi", __name__)


@lmi.route("/lmi/<token>")
def login_with_token(token):
    try:
        token = jwt.decode(token, lmi_utils.get_secret(False), algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        tk.h.flash_error(tk._("The login link has expired. Please request a new one."))
        return tk.h.redirect_to("user.login")
    except jwt.DecodeError:
        tk.h.flash_error(tk._("Invalid login link."))
        return tk.h.redirect_to("user.login")

    user = lmi_utils.get_user(token["user_id"])

    if not user:
        tk.h.flash_error(tk._("Invalid login link."))
        return tk.h.redirect_to("user.login")

    context = {}

    for plugin in p.PluginImplementations(ILetMeIn):
        user = plugin.manage_user(user, context)

    if user.state != model.State.ACTIVE:
        tk.h.flash_error(tk._("User is not active. Can't login"))
        return tk.h.redirect_to("user.login")

    if user.last_active and user.last_active > dt.fromtimestamp(token["created_at"]):
        tk.h.flash_error(
            tk._("You have tried to use a one-time login link that has expired.")
        )
        return tk.h.redirect_to("user.login")

    for plugin in p.PluginImplementations(ILetMeIn):
        plugin.before_otl_login(user, context)

    tk.login_user(user)

    for plugin in p.PluginImplementations(ILetMeIn):
        plugin.after_otl_login(user, context)

    return tk.h.redirect_to("user.me")
