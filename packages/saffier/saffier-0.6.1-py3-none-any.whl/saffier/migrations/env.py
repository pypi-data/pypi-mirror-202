import os
import sys
import typing
from dataclasses import dataclass
from importlib import import_module
from pathlib import Path

from rich.console import Console

from saffier.exceptions import EnvironmentError
from saffier.migrations.constants import SAFFIER_DISCOVER_APP

console = Console()


@dataclass
class Scaffold:
    """
    Simple Application scaffold that holds the
    information about the app and the path to
    the same app.
    """

    path: str
    app: typing.Any


@dataclass
class MigrationEnv:
    """
    Loads an arbitraty application into the object
    and returns the App.
    """

    path: typing.Optional[str] = None
    app: typing.Optional[typing.Any] = None

    def load_from_env(
        self, path: typing.Optional[str] = None, enable_logging: bool = True
    ) -> "MigrationEnv":
        """
        Loads the environment variables into the scaffold.
        """
        # Adds the current path where the command is being invoked
        # To the system path
        command_path = str(Path().cwd())
        if command_path not in sys.path:
            sys.path.append(command_path)
        try:
            import dotenv

            dotenv.load_dotenv()
        except ImportError:
            ...

        _path = os.getenv(SAFFIER_DISCOVER_APP) if not path else path
        _app = self.find_app(path=_path, enable_logging=enable_logging)

        return MigrationEnv(path=_app.path, app=_app.app)

    def import_app_from_string(cls, path: typing.Optional[str] = None) -> Scaffold:
        if path is None:
            raise EnvironmentError(
                detail="Path cannot be None. Set env `SAFFIER_DEFAULT_APP` or use `--app` instead."
            )
        module_str_path, app_name = path.split(":")
        module = import_module(module_str_path)
        app = getattr(module, app_name)
        return Scaffold(path=path, app=app)

    def find_app(self, path: typing.Optional[str], enable_logging: bool = True) -> Scaffold:
        """
        Loads the application based on the path provided via env var.
        """
        if enable_logging:
            console.print(f"[bright_blue]Loading application: [bright_green]{path}")
        return self.import_app_from_string(path)
