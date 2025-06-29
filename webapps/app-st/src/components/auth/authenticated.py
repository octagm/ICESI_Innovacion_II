from typing import Callable, Any

import components.auth.login as login
from config import WEBAPP_AUTH_PROTECTED
from states.auth import get_is_authenticated


def authenticated(fn: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        is_authenticated = get_is_authenticated()
        if (is_authenticated is False) and WEBAPP_AUTH_PROTECTED:
            login.render()
            return

        return fn(*args, **kwargs)

    return wrapper
