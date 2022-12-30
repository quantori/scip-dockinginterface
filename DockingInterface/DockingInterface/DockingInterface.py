# coding=utf-8
import ctypes
import traceback
from .lib import LibPathResolver, DOCKING_LIBRARY_PATH
from .util import MoleculeResult, DockingResult, Molecule, DockingException, RdockResult

_qvina = None
_smina = None
_vina = None
_rdock = None


def _get_rdock(libpath):
    global _rdock
    if _rdock is None:
        _rdock = ctypes.CDLL(libpath)
    return _rdock


def _get_qvina(libpath):
    global _qvina
    if _qvina is None:
        _qvina = ctypes.CDLL(libpath)
    return _qvina


def _get_smina(libpath):
    global _smina
    if _smina is None:
        _smina = ctypes.CDLL(libpath)
    return _smina


def _get_vina(libpath):
    global _vina
    if _vina is None:
        _vina = ctypes.CDLL(libpath)
    return _vina


class DockingInterface:
    def __init__(self):
        self._lib = None
        self._ligand = None
        self._config = None
        self._receptor = None
        self._rdocksys = None
        self._rdockprm = None
        self._rdockroot = None
        self._rdockhome = None
        self._nruns = 1
        self._seed = None
        self._output = None
        self._vinaDynamicLib = None
        self._qvinaDynamicLib = None
        self._sminaDynamicLib = None
        self._rdockDynamicLib = None
        self._argv = None
        self._argc = None
        self._log = None
        self._center_x = None
        self._center_y = None
        self._center_z = None
        self._size_x = None
        self._size_y = None
        self._size_z = None
        self._exhaustiveness = None
        self._docking_result = None
        self._result = DockingResult()
        self._scoring = None
        self._autobox = None
        self._buffer = None

    def crash(self):
        if self._lib == 'smina':
            self._sminaDynamicLib.crash()
        elif self._lib == 'vina':
            self._vinaDynamicLib.crash()
        elif self._lib == 'qvina':
            self._qvinaDynamicLib.crash()


    def _create_arg(self):
        if self._qvinaDynamicLib is None and self._vinaDynamicLib is None and self._sminaDynamicLib is None and \
                self._rdockDynamicLib is None:
            raise DockingException(lib_error=True)

        if self._ligand is None and self._buffer is None:
            raise DockingException(no_file='Ligand')

        if self._lib == "rdock":
            self._argv = ["", "-i", self._ligand, "-o", f"{self._ligand}_out",
                          "-p", self._rdockprm, "-r", self._rdocksys, "-n", self._nruns]
        else:

            if self._receptor is None:
                raise DockingException(no_file='Receptor')

            if self._config is not None:
                self._argv = ["", "--receptor", self._receptor, "--config", self._config]
            elif self._autobox and self._lib == "smina":
                self._argv = ["", "--receptor", self._receptor, "--autobox_ligand", self._autobox]
            elif self._lib != "rdock":
                if self._size_x is None or self._size_y is None or self._size_x is None:
                    raise DockingException(size=True)
                if self._center_x is None or self._center_y is None or self._center_z is None:
                    raise DockingException(center=True)
                self._argv = ["", "--receptor", self._receptor,
                              "--center_x", self._center_x, "--center_y", self._center_y, "--center_z", self._center_z,
                              "--size_x", self._size_x, "--size_y", self._size_y, "--size_z", self._size_z]

            if self._ligand:
                self._argv.append("--ligand")
                self._argv.append(self._ligand)

            if self._output:
                self._argv.append("--out")
                self._argv.append(self._output)

            if self._scoring and self._lib == "smina":
                self._argv.append("--scoring")
                self._argv.append(self._scoring)

            if self._buffer:
                self._argv.append("--buffer")
                self._argv.append(self._buffer)

            if self._seed:
                self._argv.append("--seed")
                self._argv.append(self._seed)

            if self._log:
                self._argv.append("--log")
                self._argv.append(self._log)

            if self._exhaustiveness:
                self._argv.append("--exhaustiveness")
                self._argv.append(self._exhaustiveness)



        self._argc = len(self._argv)
        tmp_arg = (ctypes.POINTER(ctypes.c_char) * (len(self._argv)))()
        for i, arg in enumerate(self._argv):
            arg = str(arg)
            enc_arg = arg.encode('utf-8')
            tmp_arg[i] = ctypes.create_string_buffer(enc_arg)
        self._argv = ctypes.cast(tmp_arg, ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))

    def set_handler(self, libname):
        """
       Installs a handler
        :param libname: 'smina' or 'qvina' or 'vina'
        """
        self._lib = libname
        resolver = LibPathResolver(*DOCKING_LIBRARY_PATH)
        libpath = resolver.get_lib(libname)
        if libpath is not None:
            if self._lib == 'qvina':
                self._qvinaDynamicLib = _get_qvina(str(libpath))
            elif self._lib == 'smina':
                self._sminaDynamicLib = _get_smina(str(libpath))
            elif self._lib == 'vina':
                self._vinaDynamicLib = _get_vina(str(libpath))
            elif self._lib == "rdock":
                self._rdockDynamicLib = _get_rdock(str(libpath))

    def set_scoring_function(self, scoring):
        self._scoring = scoring

    def set_buffer_ligand(self, buffer):
        self._buffer = buffer

    def set_autobox_ligand(self, autobox):
        self._autobox = autobox

    def set_ligand(self, ligand):
        """
        Sets the path to the ligand
        :param ligand: "/set/your/path.pdbqt"
        """
        self._ligand = ligand

    def set_center(self, center_x, center_y, center_z):
        self._center_x = str(center_x)
        self._center_y = str(center_y)
        self._center_z = str(center_z)

    def set_size(self, size_x, size_y, size_z):
        self._size_x = str(size_x)
        self._size_y = str(size_y)
        self._size_z = str(size_z)

    def set_exhaustiveness(self, exhaustiveness):
        self._exhaustiveness = str(exhaustiveness)

    def set_log_file(self, log):
        self._log = log

    def set_receptor(self, receptor):
        """
        Sets the path to the receptor
        :param receptor: "/set/your/path.pdbqt"
        """
        self._receptor = receptor

    def set_rdockprm(self, rdockprm):
        self._rdockprm = rdockprm

    def set_rdocksys(self, rdocksys):
        self._rdocksys = rdocksys

    def set_rdockroot(self, rdockroot):
        self._rdockroot = rdockroot
        
    def set_rdockhome(self, rdockhome):
        self._rdockhome = rdockhome
        
    def set_nruns(self, n):
        self._nruns = n

    def _free_mem(self):
        if self._lib == 'vina':
            self._vinaDynamicLib.freemem(self._docking_result)
        elif self._lib == 'qvina':
            self._qvinaDynamicLib.freemem(self._docking_result)
        elif self._lib == 'smina':
            self._sminaDynamicLib.freemem(self._docking_result)
        elif self._lib == 'rdock':
            self._rdockDynamicLib.freemem(self._docking_result)

    def set_config(self, config):
        """
       Sets the path to the config
        :param config: "/set/your/path.txt"
        """
        self._config = config

    def set_seed(self, seed):
        self._seed = str(seed)

    def set_output(self, output):
        self._output = output

    def docking(self):
        """
        Checks all the necessary parameters of the docking and launches it
        """
        self._create_arg()

        if self._lib == 'vina':
            self._vinaDynamicLib.runVina.restype = ctypes.POINTER(Molecule)
            self._docking_result = self._vinaDynamicLib.runVina(self._argc, self._argv)
        elif self._lib == 'qvina':
            self._qvinaDynamicLib.runQvina.restype = ctypes.POINTER(Molecule)
            self._docking_result = self._qvinaDynamicLib.runQvina(self._argc, self._argv)
        elif self._lib == 'smina':
            self._sminaDynamicLib.runSmina.restype = ctypes.POINTER(Molecule)
            self._docking_result = self._sminaDynamicLib.runSmina(self._argc, self._argv)
        elif self._lib == 'rdock':
            self._rdockDynamicLib.runRdock.restype = ctypes.POINTER(RdockResult)
            self._docking_result = self._rdockDynamicLib.runRdock(ctypes.create_string_buffer(self._rdockroot.encode('utf-8')), ctypes.create_string_buffer(self._rdockhome.encode('utf-8')), self._argc, self._argv)

        if self._lib != "rdock":
            if self._docking_result.contents.count == -1 and self._docking_result.contents.pdbqtFormatData[0]:
                message = self._docking_result.contents.pdbqtFormatData[0]
                self._free_mem()
                raise DockingException(handler_error=self._lib,
                                       error_message=message)
            elif self._docking_result.contents.count == -1:
                self._free_mem()
                raise DockingException(handler_error=self._lib)
            else:
                self._result.set_path(self._ligand, self._receptor)
                for i in range(self._docking_result.contents.count):
                    self._result.append(MoleculeResult(self._docking_result.contents.resArray[i][0],
                                                       self._docking_result.contents.resArray[i][1],
                                                       self._docking_result.contents.resArray[i][2],
                                                       self._docking_result.contents.resArray[i][3],
                                                       self._docking_result.contents.pdbqtFormatData[i]))
                self._free_mem()

        else:
            if self._docking_result.contents.error != 0:
                raise DockingException(handler_error=1,
                                       error_message=self._docking_result.contents.errorMessage)
            tmp = self._docking_result.contents.data.decode('utf-8')
            res = tmp.split("ITERATION")
            scores = []
            for i in range(1, len(res)):
                res[i] = res[i].split(" ", 1)

            for i in res[1:]:
                scores.append(float(i[0]))
                ind = scores.index(min(scores))

                
            self._result = [res[0].strip(), float(res[ind+1][0]), res[ind+1][1]]

    def get_result(self):
        return self._result
