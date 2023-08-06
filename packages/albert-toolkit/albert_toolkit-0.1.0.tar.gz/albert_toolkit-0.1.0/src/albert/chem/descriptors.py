from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import AllChem


def get_descriptors_from_smiles(smiles: str) -> dict:
    return get_descriptors_from_mol(Chem.MolFromSmiles(smiles))


def get_descriptors_from_mol(mol):
    descriptors = {}
    for descriptor_name, descriptor_function in Descriptors.descList:
        try:
            descriptor_value = descriptor_function(mol)
            descriptors[descriptor_name] = descriptor_value
        except:
            pass
    return descriptors


def is_hydrophobic(atom):
    hydrophobic_elements = ["C", "F", "I", "Br", "Cl", "P"]
    return atom.GetSymbol() in hydrophobic_elements


def get_hydrophobe_length_from_smiles(smiles: str):
    return get_hydrophobe_length_from_mol(Chem.MolFromSmiles(smiles))


def get_hydrophobe_length_from_mol(mol):
    max_hydrophobe_length = 0

    for atom in mol.GetAtoms():
        if is_hydrophobic(atom):
            visited_atoms = set()
            stack = [(atom, 0)]
            while stack:
                current_atom, current_length = stack.pop()
                current_atom_idx = current_atom.GetIdx()
                if current_atom_idx not in visited_atoms:
                    visited_atoms.add(current_atom_idx)
                    if current_length > max_hydrophobe_length:
                        max_hydrophobe_length = current_length
                    for neighbor in current_atom.GetNeighbors():
                        if is_hydrophobic(neighbor):
                            stack.append((neighbor, current_length + 1))

    return max_hydrophobe_length


def count_repeating_units_smiles(molecule_smiles, smarts_pattern):
    return count_repeating_units(Chem.MolFromSmiles(molecule_smiles), smarts_pattern)


def count_repeating_units(molecule, smarts_pattern):
    """
    Count the number of repeating units within a molecule based on a substructure (SMARTS pattern).

    Args:
    molecule (rdkit.Chem.Mol): The molecule to analyze.
    smarts_pattern (str): The SMARTS pattern representing the repeating unit.

    Returns:
    int: The number of repeating units in the molecule.
    """
    substructure = Chem.MolFromSmarts(smarts_pattern)
    matches = molecule.GetSubstructMatches(substructure)
    return len(matches)
