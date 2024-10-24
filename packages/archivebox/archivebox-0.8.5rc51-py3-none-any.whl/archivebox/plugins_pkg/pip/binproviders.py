__package__ = 'plugins_pkg.pip'

import os
import sys
import site
from pathlib import Path
from typing import Optional

from pydantic_pkgr import PipProvider, BinName, BinProviderName

from archivebox.config import CONSTANTS

from abx.archivebox.base_binary import BaseBinProvider


###################### Config ##########################

class SystemPipBinProvider(PipProvider, BaseBinProvider):
    name: BinProviderName = "sys_pip"
    INSTALLER_BIN: BinName = "pip"
    
    pip_venv: Optional[Path] = None        # global pip scope
    
    def on_install(self, bin_name: str, **kwargs):
        # never modify system pip packages
        return 'refusing to install packages globally with system pip, use a venv instead'

class SystemPipxBinProvider(PipProvider, BaseBinProvider):
    name: BinProviderName = "pipx"
    INSTALLER_BIN: BinName = "pipx"
    
    pip_venv: Optional[Path] = None        # global pipx scope


IS_INSIDE_VENV = sys.prefix != sys.base_prefix

class VenvPipBinProvider(PipProvider, BaseBinProvider):
    name: BinProviderName = "venv_pip"
    INSTALLER_BIN: BinName = "pip"

    pip_venv: Optional[Path] = Path(sys.prefix if IS_INSIDE_VENV else os.environ.get("VIRTUAL_ENV", '/tmp/NotInsideAVenv/lib'))
    
    def setup(self):
        """never attempt to create a venv here, this is just used to detect if we are inside an existing one"""
        return None
    

class LibPipBinProvider(PipProvider, BaseBinProvider):
    name: BinProviderName = "lib_pip"
    INSTALLER_BIN: BinName = "pip"
    
    pip_venv: Optional[Path] = CONSTANTS.DEFAULT_LIB_DIR / 'pip' / 'venv'
    
    def setup(self) -> None:
        # update paths from config if they arent the default
        from archivebox.config.common import STORAGE_CONFIG
        if STORAGE_CONFIG.LIB_DIR != CONSTANTS.DEFAULT_LIB_DIR:
            self.pip_venv = STORAGE_CONFIG.LIB_DIR / 'pip' / 'venv'
            
        super().setup()

SYS_PIP_BINPROVIDER = SystemPipBinProvider()
PIPX_PIP_BINPROVIDER = SystemPipxBinProvider()
VENV_PIP_BINPROVIDER = VenvPipBinProvider()
LIB_PIP_BINPROVIDER = LibPipBinProvider()
pip = LIB_PIP_BINPROVIDER

# ensure python libraries are importable from these locations (if archivebox wasnt executed from one of these then they wont already be in sys.path)
assert VENV_PIP_BINPROVIDER.pip_venv is not None
assert LIB_PIP_BINPROVIDER.pip_venv is not None

major, minor, patch = sys.version_info[:3]
site_packages_dir = f'lib/python{major}.{minor}/site-packages'

LIB_SITE_PACKAGES = (LIB_PIP_BINPROVIDER.pip_venv / site_packages_dir,)
VENV_SITE_PACKAGES = (VENV_PIP_BINPROVIDER.pip_venv / site_packages_dir,)
USER_SITE_PACKAGES = site.getusersitepackages()
SYS_SITE_PACKAGES = site.getsitepackages()

ALL_SITE_PACKAGES = (
    *LIB_SITE_PACKAGES,
    *VENV_SITE_PACKAGES,
    *USER_SITE_PACKAGES,
    *SYS_SITE_PACKAGES,
)
for site_packages_dir in ALL_SITE_PACKAGES:
    if site_packages_dir not in sys.path:
        sys.path.append(str(site_packages_dir))
