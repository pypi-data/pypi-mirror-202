from inspect import isclass

from .abstract_modifier import AbstractModifier
from .smart_open_modifier import SmartOpenModifier


# def modifier_factory(*modifiers):
#     """
#     Build a chain of instantiated modifiers so the :method:`apply` from the super class
#     `AbstractModifier` can be called once for a :class:`DataConnector` subclass object.
#
#     return a subclass of EngineTypeModifier
#     @param modifiers (list of str):
#     """
#     if len(modifiers) != 1:
#         raise NotImplementedError("Current supports a single engine type modifier")
#
#     raise NotImplementedError("TODO - I am here")
#
#
# def apply_modifier(connector, *modifiers):
#     """
#     maybe??
#     """
#     pass


class ConnectorModifiersPluginsRegistry:
    """
    A modifier adds capabilities to a connector, for example, transparent compression.
    """

    def __init__(self):
        self.registered_modifiers = []  # list of classes, not instances - publicly readable
        self.reset()

    def reset(self):
        "set registered connectors to just those that are built in"
        self.registered_modifiers = [
            SmartOpenModifier,
        ]

    def register_connector(self, modifier_cls):
        """
        Add a private modifier to the dataset connection discovery process.
        @param modifier_cls ():
        """
        if not isclass(connector_cls) or not issubclass(connector_cls, AbstractModifier):
            msg = "'connector_cls' should be a class (not object) and subclass of DataConnector"
            raise TypeError(msg)

        # MAYBE - a mechanism to specify the position/priority of the class
        self.registered_connectors.append(connector_cls)


# global registry
connector_modifiers_registry = None
