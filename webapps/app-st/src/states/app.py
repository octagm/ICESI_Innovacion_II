from typing import Callable, Any

import streamlit as st

from states.mappings import AppMap, map_session_state


@st.cache_data
def get_app_state_mapping() -> AppMap:
    return AppMap()


def init_app_state_mapping(fn: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if 'app' not in st.session_state:
            map_session_state(get_app_state_mapping())
            st.session_state['app'] = True

        return fn(*args, **kwargs)

    return wrapper
