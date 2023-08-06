from abc import ABC, abstractmethod

from rdkit import Chem
from rdkit.Chem.rdchem import Bond
from rdkit.Chem.rdchem import BondType as BT


class BondAttributeCalculator(ABC):
    def __init__(self, data: Bond):
        self.data = data

    @abstractmethod
    def calculate(self):
        pass

    @abstractmethod
    def embedding_input_dim(self):
        raise NotImplementedError(
            "you need to implement the embedding_input_dim function"
        )


class BondType(BondAttributeCalculator):
    BOND_TYPES = [BT.SINGLE, BT.DOUBLE, BT.TRIPLE, BT.AROMATIC]

    def calculate(self):
        return self.BOND_TYPES.index(self.data.GetBondType())

    def embedding_input_dim(self):
        return len(self.BOND_TYPES) + 1


class BondDir(BondAttributeCalculator):
    BOND_DIRS = [
        Chem.rdchem.BondDir.NONE,
        Chem.rdchem.BondDir.ENDUPRIGHT,
        Chem.rdchem.BondDir.ENDDOWNRIGHT,
    ]

    def calculate(self):
        return self.BOND_DIRS.index(self.data.GetBondDir())

    def embedding_input_dim(self):
        return len(self.BOND_DIRS) + 1


class ConjugatedBond(BondAttributeCalculator):
    def calculate(self):
        return 1 if self.data.GetIsConjugated() else 0

    def embedding_input_dim(self):
        return 2


class BondInRing(BondAttributeCalculator):
    def calculate(self):
        return 1 if self.data.IsInRing() else 0

    def embedding_input_dim(self):
        return 2


BondAttributeFunctions = {
    "type": BondType,
    "dir": BondDir,
    "conjugated": ConjugatedBond,
    "ring": BondInRing,
}
