# src/restackio/ai/__init__.py
__path__ = __import__('pkgutil').extend_path(__path__, __name__)

from .restack import Restack

__all__ = ["Restack"]
