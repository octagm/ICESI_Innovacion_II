import streamlit as st


from domain.user import User
from states import AuthState
from states.app import get_app_state_mapping


class UnauthenticatedException(Exception):
    pass


def get_jwt() -> str:
    asm = get_app_state_mapping()
    auth = st.session_state[asm.auth]
    if auth.is_authenticated:
        return auth.jwt
    else:
        raise UnauthenticatedException()


def get_is_authenticated() -> bool:
    asm = get_app_state_mapping()
    return st.session_state[asm.auth].is_authenticated


def get_user() -> User:
    asm = get_app_state_mapping()
    auth = st.session_state[asm.auth]
    if auth.is_authenticated:
        return auth.user
    else:
        raise UnauthenticatedException()


def set_auth(state: AuthState) -> None:
    asm = get_app_state_mapping()
    st.session_state[asm.auth] = state
