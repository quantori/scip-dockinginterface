from DockingInterface import *

if __name__ == "__main__":
    docking = DockingInterface()
    docking.set_handler('qvina')
    docking.set_log_file('logfile.txt')
    docking.set_ligand('../ligands/00K_uff_E=531.34.pdbqt')
    #docking.set_ligand('../ligands/incorrect.pdbqt')
    docking.set_receptor('../2hnt.pdbqt')
    docking.set_center(17.3564, 1.5176, 12.9464)
    docking.set_size(25.0, 25.0, 25.0)
    docking.set_exhaustiveness(8)
    docking.docking()
    a = docking.get_result()
    for i in range(a.get_number_of_models()):
        print(a.get_ligand())
        print(a.get_receptor())
        print(a.get_values_by_index(i))
        print(a.get_model_by_index(i))

