import streamlit as st


from domain.user import User
from states import AuthState
from states.mappings import get_app_state_mapping


class UnauthenticatedException(Exception):
    pass


def get_auth_state() -> AuthState:
    asm = get_app_state_mapping()
    value = st.session_state[asm.auth]
    return AuthState(**value)


def get_jwt() -> str:
    auth = get_auth_state()
    if auth.is_authenticated:
        return auth.jwt
    else:
        raise UnauthenticatedException()


def get_is_authenticated() -> bool:
    auth = get_auth_state()
    return auth.is_authenticated


def get_user() -> User:
    auth = get_auth_state()
    if auth.is_authenticated:
        return auth.user
    else:
        raise UnauthenticatedException()


def set_auth(state: AuthState) -> None:
    asm = get_app_state_mapping()
    st.session_state[asm.auth] = state.model_dump()
