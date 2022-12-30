import os

from pathlib import Path
from platform import system, machine


LIBRARY_NAMES = dict(
    qvina = dict(
        darwin = 'libqvinaDynamic.dylib',
        linux = 'libqvinaDynamic.so',
        windows = 'libqvinaDynamic.dll'
    ),
    smina = dict(
        darwin = 'libsminaDynamic.dylib',
        linux = 'libsminaDynamic.so',
        windows = 'libsminaDynamic.dll'
    ),
    vina = dict(
        darwin = 'libvinaDynamic.dylib',
        linux = 'libvinaDynamic.so',
        windows = 'libvinaDynamic.dll'
    ),
    rdock = dict(
        darwin = 'libRbt.dylib',
        linux = 'libRbt.so',
        windows = 'libRbt.dll'
    )
)


LIBRARY_PATHS = dict(
    aarch64 = [
        'C_Dynamic_Libs/Linux/arm64',
        'C_Dynamic_Libs/macOS/arm64',
        'C_Dynamic_Libs/win32/arm64'
    ],
    amd64 = [
        'C_Dynamic_Libs/win32/AMD64'
    ],
    arm64 = [
        'C_Dynamic_Libs/Linux/arm64',
        'C_Dynamic_Libs/macOS/arm64',
        'C_Dynamic_Libs/win32/arm64'
    ],
    x86_64 = [
        'C_Dynamic_Libs/Linux/x86_64',
        'C_Dynamic_Libs/macOS/x86_64',
        'C_Dynamic_Libs/win32/x86_64'
    ]
)

LIBRARY_PATH_PREFIX = Path(__file__).parent 
LIBRARY_PATH_SEPARATOR = ':'


DOCKING_LIBRARY_PATH = tuple(
    filter(None, os.getenv('DOCKING_LIBRARY_PATH', '').split(LIBRARY_PATH_SEPARATOR))
)

class LibPathResolver(object):

    def __init__(self, *search_paths):
        paths = search_paths
        if len(search_paths) < 1:
            paths = LIBRARY_PATHS.get(machine().lower(), [])
        paths = map(lambda x: Path(x), paths)

        self._spath = list() 
        for path in paths:
            if path.is_absolute():
                self._spath.append(path)
            else:
                self._spath.append(LIBRARY_PATH_PREFIX.joinpath(path))

    def get_lib(self, libname) -> Path:
        '''
        Try to find out a file with given name and return its name if ... 
        '''
        try:
            platform_libs = LIBRARY_NAMES[libname]
        except KeyError:
            raise ValueError(
                "The library '{}' is not supported by docking interface".format(libname)
            )

        try:
            lib_file = platform_libs[system().lower()]
        except KeyError:
            raise NotImplementedError(
                "The docking interface has no support the '{}' library for '{}' platform".format(
                    libname,
                    system()
                )
            )

        return self._discover_library(lib_file)

    @property
    def spaths(self) -> list():
        return self._spath

    def _discover_library(self, name):
        lib = None
        for folder in self._spath:
            candidate = folder.joinpath(name)
            if candidate.is_file():
                lib = candidate
                break
        return lib
