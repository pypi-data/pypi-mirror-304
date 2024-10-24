__package__ = 'plugins_pkg.pip'

import sys
from pathlib import Path
from typing import List
from pydantic import InstanceOf, Field, model_validator


import django
import django.db.backends.sqlite3.base
from django.db.backends.sqlite3.base import Database as django_sqlite3     # type: ignore[import-type]
from pydantic_pkgr import BinProvider, BinName, BinaryOverrides, SemVer

from archivebox import VERSION

from abx.archivebox.base_binary import BaseBinary, BaseBinProvider, env, apt, brew

from archivebox.misc.logging import hint

from .binproviders import LIB_PIP_BINPROVIDER, VENV_PIP_BINPROVIDER, SYS_PIP_BINPROVIDER

###################### Config ##########################



class ArchiveboxBinary(BaseBinary):
    name: BinName = 'archivebox'

    binproviders_supported: List[InstanceOf[BinProvider]] = [VENV_PIP_BINPROVIDER, SYS_PIP_BINPROVIDER, apt, brew, env]
    overrides: BinaryOverrides = {
        VENV_PIP_BINPROVIDER.name:  {'packages': [], 'version': VERSION},
        SYS_PIP_BINPROVIDER.name:   {'packages': [], 'version': VERSION},
        apt.name:                   {'packages': [], 'version': VERSION},
        brew.name:                  {'packages': [], 'version': VERSION},
    }
    
    # @validate_call
    def install(self, **kwargs):
        return self.load()                  # obviously it's already installed if we are running this ;)
    
    # @validate_call
    def load_or_install(self, **kwargs):
        return self.load()                  # obviously it's already installed if we are running this ;)

ARCHIVEBOX_BINARY = ArchiveboxBinary()


class PythonBinary(BaseBinary):
    name: BinName = 'python'

    binproviders_supported: List[InstanceOf[BinProvider]] = [VENV_PIP_BINPROVIDER, SYS_PIP_BINPROVIDER, apt, brew, env]
    overrides: BinaryOverrides = {
        SYS_PIP_BINPROVIDER.name: {
            'abspath': sys.executable,
            'version': '{}.{}.{}'.format(*sys.version_info[:3]),
        },
    }
    
    # @validate_call
    def install(self, **kwargs):
        return self.load()                  # obviously it's already installed if we are running this ;)
    
    # @validate_call
    def load_or_install(self, **kwargs):
        return self.load()                  # obviously it's already installed if we are running this ;)

PYTHON_BINARY = PythonBinary()


LOADED_SQLITE_PATH = Path(django.db.backends.sqlite3.base.__file__)
LOADED_SQLITE_VERSION = SemVer(django_sqlite3.version)
LOADED_SQLITE_FROM_VENV = str(LOADED_SQLITE_PATH.absolute().resolve()).startswith(str(VENV_PIP_BINPROVIDER.pip_venv.absolute().resolve()))

class SqliteBinary(BaseBinary):
    name: BinName = 'sqlite'
    binproviders_supported: List[InstanceOf[BaseBinProvider]] = Field(default=[VENV_PIP_BINPROVIDER, SYS_PIP_BINPROVIDER])
    overrides: BinaryOverrides = {
        VENV_PIP_BINPROVIDER.name: {
            "abspath": LOADED_SQLITE_PATH if LOADED_SQLITE_FROM_VENV else None,
            "version": LOADED_SQLITE_VERSION if LOADED_SQLITE_FROM_VENV else None,
        },
        SYS_PIP_BINPROVIDER.name: {
            "abspath": LOADED_SQLITE_PATH if not LOADED_SQLITE_FROM_VENV else None,
            "version": LOADED_SQLITE_VERSION if not LOADED_SQLITE_FROM_VENV else None,
        },
    }
    
    @model_validator(mode='after')
    def validate_json_extension_is_available(self):
        # Check to make sure JSON extension is available in our Sqlite3 instance
        try:
            cursor = django_sqlite3.connect(':memory:').cursor()
            cursor.execute('SELECT JSON(\'{"a": "b"}\')')
        except django_sqlite3.OperationalError as exc:
            print(f'[red][X] Your SQLite3 version is missing the required JSON1 extension: {exc}[/red]')
            hint([
                'Upgrade your Python version or install the extension manually:',
                'https://code.djangoproject.com/wiki/JSON1Extension'
            ])
        return self
    
    # @validate_call
    def install(self, **kwargs):
        return self.load()                  # obviously it's already installed if we are running this ;)
    
    # @validate_call
    def load_or_install(self, **kwargs):
        return self.load()                  # obviously it's already installed if we are running this ;)

SQLITE_BINARY = SqliteBinary()


LOADED_DJANGO_PATH = Path(django.__file__)
LOADED_DJANGO_VERSION = SemVer(django.VERSION[:3])
LOADED_DJANGO_FROM_VENV = str(LOADED_DJANGO_PATH.absolute().resolve()).startswith(str(VENV_PIP_BINPROVIDER.pip_venv and VENV_PIP_BINPROVIDER.pip_venv.absolute().resolve()))

class DjangoBinary(BaseBinary):
    name: BinName = 'django'

    binproviders_supported: List[InstanceOf[BaseBinProvider]] = Field(default=[VENV_PIP_BINPROVIDER, SYS_PIP_BINPROVIDER])
    overrides: BinaryOverrides = {
        VENV_PIP_BINPROVIDER.name: {
            "abspath": LOADED_DJANGO_PATH if LOADED_DJANGO_FROM_VENV else None,
            "version": LOADED_DJANGO_VERSION if LOADED_DJANGO_FROM_VENV else None,
        },
        SYS_PIP_BINPROVIDER.name: {
            "abspath": LOADED_DJANGO_PATH if not LOADED_DJANGO_FROM_VENV else None,
            "version": LOADED_DJANGO_VERSION if not LOADED_DJANGO_FROM_VENV else None,
        },
    }
    
    # @validate_call
    def install(self, **kwargs):
        return self.load()                  # obviously it's already installed if we are running this ;)
    
    # @validate_call
    def load_or_install(self, **kwargs):
        return self.load()                  # obviously it's already installed if we are running this ;)

DJANGO_BINARY = DjangoBinary()

class PipBinary(BaseBinary):
    name: BinName = "pip"
    binproviders_supported: List[InstanceOf[BinProvider]] = [LIB_PIP_BINPROVIDER, VENV_PIP_BINPROVIDER, SYS_PIP_BINPROVIDER, apt, brew, env]

    # @validate_call
    def install(self, **kwargs):
        return self.load()                  # obviously it's already installed if we are running this ;)
    
    # @validate_call
    def load_or_install(self, **kwargs):
        return self.load()                  # obviously it's already installed if we are running this ;)

PIP_BINARY = PipBinary()


class PipxBinary(BaseBinary):
    name: BinName = "pipx"
    binproviders_supported: List[InstanceOf[BinProvider]] = [LIB_PIP_BINPROVIDER, VENV_PIP_BINPROVIDER, SYS_PIP_BINPROVIDER, apt, brew, env]

PIPX_BINARY = PipxBinary()
