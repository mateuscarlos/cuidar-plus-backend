"""Transactional Decorator - Ensures database transaction boundaries."""
from functools import wraps
from typing import Callable, Any

from sqlalchemy.orm import Session


def transactional(func: Callable) -> Callable:
    """
    Decorator to wrap a function in a database transaction.
    
    The function must receive a Session object as the first argument.
    
    Usage:
        @transactional
        def my_function(session: Session, arg1, arg2):
            # This will be executed in a transaction
            pass
    """
    @wraps(func)
    def wrapper(session: Session, *args: Any, **kwargs: Any) -> Any:
        try:
            result = func(session, *args, **kwargs)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise e
    
    return wrapper
