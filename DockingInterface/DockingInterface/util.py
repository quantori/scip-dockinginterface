from ctypes import Structure, POINTER, c_char, c_int, c_double, cast, c_char_p
import traceback
import sys



class MoleculeResult:
    def __init__(self, i, affinity, rmsd_l_b, rmsd_u_b, pdbqtFormatData):
        self._ind = int(i)
        self._affinity = affinity
        self._rmsd_l_b = rmsd_l_b
        self._rmsd_u_b = rmsd_u_b
        self._pdbqtFormatData = self._conv(pdbqtFormatData)

    def get_values(self):
        return [self._ind, self._affinity, self._rmsd_l_b, self._rmsd_u_b]

    def get_pdb_data(self):
        return self._pdbqtFormatData

    def get_all(self):
        return [self._ind, self._affinity, self._rmsd_l_b, self._rmsd_u_b, self._pdbqtFormatData]

    def _conv(self, data):
        data = data.replace(b"\r", b"\n")
        data = data.replace(b"\n\n", b"\n")
        return data.decode('utf-8')


class DockingResult:
    def __init__(self):
        self._data = []
        self._ligand_path = None
        self._receptor_path = None

    def set_path(self, ligand_path, receptor_path):
        self._ligand_path = ligand_path
        self._receptor_path = receptor_path

    def get_ligand(self):
        return self._ligand_path

    def get_receptor(self):
        return self._receptor_path

    def append(self, data):
        self._data.append(data)

    def get_all_data(self):
        return [i.get_all() for i in self._data]

    def get_values_by_index(self, i):
        return self._data[i].get_values()

    def get_model_by_index(self, i):
        return self._data[i].get_pdb_data()

    def get_all_by_index(self, i):
        return self._data[i].get_all()

    def get_all_values(self):
        return [i.get_values() for i in self._data]

    def get_number_of_models(self):
        return len(self._data)


class Molecule(Structure):
    _fields_ = ("pdbqtFormatData", POINTER(c_char_p)), \
               ("resArray", POINTER(POINTER(c_double))), \
               ("count", c_int), \
               ("len", POINTER(c_int))

class RdockResult(Structure):
    _fields_ = ("errorMessage", c_char_p), \
               ("data", c_char_p), \
               ("error", c_int)


class DockingException(Exception):
    def __init__(self, handler_error=None, error_message=None, file_error=None, no_file=None, size=None, lib_error=None, center=None):
        if error_message is not None:
            self.__error_message = error_message.decode("utf-8")
        self.__handler_error = handler_error
        self.__size = size
        self.__center = center
        self.__lib_error = lib_error
        self.__no_file = no_file
        self.__file_error = file_error

    def __str__(self):
        self._exc()
        if self.__lib_error:
            return "\nNot found dynamic lib. Stop\n"
        if self.__center:
            return "\nProblem with some center. Skip docking\n"
        if self.__size:
            return "\nProblem with some size. Skip docking\n"
        if self.__handler_error and self.__error_message:
            return "{}".format(self.__error_message)
        elif self.__handler_error:
            return "some Error"
    def _exc(self):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback, limit=5)


