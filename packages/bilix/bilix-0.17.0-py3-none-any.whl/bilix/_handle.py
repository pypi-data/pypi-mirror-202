import asyncio
import functools
import inspect
from typing import Callable, Union, Dict

from bilix.exception import HandleError
from bilix.log import logger


class Handler:
    _registered: Dict[str, Callable] = {}

    @classmethod
    def check(cls, name: str, handle_func: Callable):
        if name in cls._registered:
            raise HandleError(f"Handler name: {name} all ready exists")
        sig = inspect.signature(handle_func)
        if len(sig.parameters) != 1:
            raise HandleError("Handler func should only have one cli_kwargs parameter")

    @staticmethod
    def kwargs_filter(obj: Union[type, Callable], cli_kwargs: dict):
        """

        :param obj:
        :param cli_kwargs:
        :return:
        """
        sig = inspect.signature(obj)
        obj_require = set(sig.parameters.keys())

        def check(k):
            if k in obj_require:
                p = sig.parameters[k]
                # check type hint
                try:
                    if p.annotation is inspect.Signature.empty or \
                            isinstance(cli_kwargs[k], p.annotation):
                        return True
                    else:
                        logger.debug(f"kwarg {k}:{cli_kwargs[k]} has been drop due to type hint missmatch")
                        return False
                except TypeError:  # https://peps.python.org/pep-0604/#isinstance-and-issubclass
                    # lower than 3.10, Union
                    # TypeError: Subscripted generics cannot be used with class and instance checks
                    return True
            return False

        kwargs = {k: cli_kwargs[k] for k in filter(check, cli_kwargs)}
        return kwargs

    @classmethod
    def register(cls, name: str):
        def decorator(handle_func: Callable):
            cls.check(name, handle_func)

            @functools.wraps(handle_func)
            def wrapped(cli_kwargs):
                if (res := handle_func(cli_kwargs)) is None:
                    return
                executor, cor = res
                if inspect.isclass(executor):  # handle func return class instead of instance
                    kwargs = cls.kwargs_filter(executor, cli_kwargs)
                    executor = executor(**kwargs)
                    logger.debug(f"auto assemble {executor} by {kwargs}")
                if inspect.iscoroutinefunction(cor):  # handle func return async function instead of coroutine
                    sig = inspect.signature(cor)
                    kwargs = cls.kwargs_filter(cor, cli_kwargs)
                    cors = []
                    for key in cli_kwargs['keys']:
                        if 'self' in sig.parameters:  # coroutine function has not bound to instance
                            cors.append(cor(executor, key, **kwargs))  # bound executor to self
                        else:
                            cors.append(cor(key, **kwargs))
                        logger.debug(f"auto assemble {cor} by {kwargs}")
                    cor = asyncio.gather(*cors)
                return executor, cor

            cls._registered[name] = wrapped
            return wrapped

        return decorator

    @classmethod
    def assign(cls, cli_kwargs: dict):
        for name, handle_func in cls._registered.items():
            if name == 'bilibili':
                continue
            if (res := handle_func(cli_kwargs)) is not None:
                logger.debug(f"Assign to {name}")
                return res
        # since bilix is originally designed for bilibili, finally use bilibili handler
        return cls._registered['bilibili'](cli_kwargs)
