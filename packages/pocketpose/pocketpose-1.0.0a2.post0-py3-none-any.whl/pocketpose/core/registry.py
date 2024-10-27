from typing import Callable, Optional, Type, Union


class Registry:
    """A registry to map strings to classes or functions.

    Registered object could be built from registry. Meanwhile, registered
    functions could be called from registry.

    Args:
        name (str): Registry name.

    Example:
        >>> # define a registry
        >>> MODELS = Registry('models')
        >>> # registry the `MoveNet` to `MODELS`
        >>> @MODELS.register_module()
        >>> class MoveNet:
        >>>     def __init__(self, *args, **kwargs):
        >>>         pass
        >>> # build model from `MODELS`
        >>> movenet = MODELS.build('MoveNet', *args, **kwargs)
    """

    def __init__(self, name: str):
        self.name = name
        self._module_dict = {}

    def register_module(
        self,
        name: Optional[str] = None,
        force: bool = False,
        module: Optional[Type] = None,
    ) -> Union[type, Callable]:
        """Register a module.

        A record will be added to ``self._module_dict``, whose key is the class
        name or the specified name, and value is the class itself.
        It can be used as a decorator or a normal function.

        Args:
            name (str, optional): The module name to be registered. If not
                specified, the class name will be used.
            force (bool): Whether to override an existing class with the same
                name. Defaults to False.
            module (type, optional): Module class or function to be registered.
                Defaults to None.
        """
        if not isinstance(force, bool):
            raise TypeError(f"force must be a boolean, but got {type(force)}")

        # raise the error ahead of time
        if not (name is None or isinstance(name, str)):
            raise TypeError(
                "name must be None or an instance of str, " f"but got {type(name)}"
            )

        def _register_module(module, module_name=name, force=force):
            if not callable(module):
                raise TypeError(f"module must be Callable, but got {type(module)}")

            if module_name is None:
                module_name = module.__name__

            if not force and module_name in self._module_dict:
                existed_module = self._module_dict[module_name]
                raise KeyError(
                    f"{name} is already registered in {self.name} "
                    f"at {existed_module.__module__}"
                )
            self._module_dict[module_name] = module
            return module

        return _register_module

    def get(self, name):
        """Get the class corresponding to the name.

        Args:
            name (str): The name of the class.

        Returns:
            The corresponding class.

        Raises:
            ValueError: If the name is not registered in the registry.
        """
        if name not in self._module_dict:
            raise ValueError(f"{name} is not registered in the {self.name} registry")

        return self._module_dict.get(name)

    def build(self, name, *args, **kwargs):
        """Build a class using the name.

        Args:
            name (str): The name of the class.
            *args: The arguments to pass to the class constructor
            **kwargs: The keyword arguments to pass to the class constructor.

        Returns:
            The built class.

        Raises:
            ValueError: If the name is not registered in the registry.
        """
        cls = self.get(name)
        return cls(*args, **kwargs)

    def list(self):
        """List all the registered names."""
        return list(sorted(self._module_dict.keys()))

    def __len__(self):
        return len(self._module_dict)

    def __getitem__(self, name):
        return self.get(name)

    def __contains__(self, name):
        return name in self._module_dict


def build_from_cfg(cfg, registry, default_args=None):
    """Build a class from the config.

    Args:
        cfg (dict): The config.
        registry (Registry): The registry to look up the class.
        default_args (dict): The default arguments to the class.

    Returns:
        The built class.
    """
    if not isinstance(cfg, dict):
        raise TypeError(f"cfg must be a dict, but got {type(cfg)}")

    if "name" not in cfg:
        raise KeyError(f"cfg must contain the key 'name'")

    name = cfg.pop("name")
    cls = registry.get(name)
    if default_args is not None:
        for k, v in default_args.items():
            cfg.setdefault(k, v)

    return cls(**cfg)
