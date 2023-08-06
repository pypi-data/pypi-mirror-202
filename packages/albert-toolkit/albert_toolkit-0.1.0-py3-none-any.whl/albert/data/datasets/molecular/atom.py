from abc import ABC, abstractmethod

from rdkit import Chem
from rdkit.Chem.rdchem import Atom
from rdkit.Chem.rdchem import BondType as BT
from rdkit.Chem.rdchem import HybridizationType as HT


class AtomicAttributeCalculator(ABC):
    def __init__(self, data: Atom):
        self.data = data

    @abstractmethod
    def calculate(self):
        pass

    @abstractmethod
    def mask_value(self):
        raise NotImplementedError("mask_value needs to be implemented")

    @abstractmethod
    def embedding_input_dim(self):
        raise NotImplementedError("embedding_input_dim needs to be implemented")


class AtomType(AtomicAttributeCalculator):
    ATOM_LIST = list(range(1, 119))
    MASK_VALUE = len(ATOM_LIST)

    def calculate(self):
        return self.ATOM_LIST.index(self.data.GetAtomicNum())

    def mask_value(self):
        return self.MASK_VALUE

    def embedding_input_dim(self):
        return self.MASK_VALUE + 1


class AtomValence(AtomicAttributeCalculator):
    # Valence can vary from 0 to N so we do not need to
    # assign it as an index as we have been with other attributes

    def calculate(self):
        return self.data.GetImplicitValence() + self.data.GetExplicitValence()

    def mask_value(self):
        # When the atom is masked we want the molecule to still be physical
        # so we maintain the actual valence so the network learns to impute
        # a real atom instead of some fantasy hypervalent atom
        return self.calculate()

    def embedding_input_dim(self):
        # I am assuming the maximum valency is 10 -- anything more than this starts to get pretty crazy
        return 10


class AtomChirality(AtomicAttributeCalculator):
    CHIRALITY_LIST = [
        Chem.rdchem.ChiralType.CHI_UNSPECIFIED,
        Chem.rdchem.ChiralType.CHI_TETRAHEDRAL_CW,
        Chem.rdchem.ChiralType.CHI_TETRAHEDRAL_CCW,
        Chem.rdchem.ChiralType.CHI_OTHER,
    ]

    MASK_VALUE = 0

    def calculate(self):
        return self.CHIRALITY_LIST.index(self.data.GetChiralTag())

    def mask_value(self):
        return self.MASK_VALUE

    def embedding_input_dim(self):
        return 4


class AtomHybridization(AtomicAttributeCalculator):
    HYBRIDIZATION_LIST = [HT.S, HT.SP, HT.SP2, HT.SP3, HT.SP3D, HT.SP3D2, HT.OTHER]

    MASK_VALUE = len(HYBRIDIZATION_LIST)

    def calculate(self):
        return self.HYBRIDIZATION_LIST.index(self.data.GetHybridization())

    def mask_value(self):
        return self.MASK_VALUE

    def embedding_input_dim(self):
        return self.MASK_VALUE + 1


class AtomNHeavy(AtomicAttributeCalculator):
    # The degree of an atom is defined to be its number of directly-bonded neighbors.
    # The degree is independent of bond orders, but is dependent on whether H's are in the graph
    N_HEAVY_NEIGHBORS_LIST = [0, 1, 2, 3, 4, "MoreThanFour"]
    MASK_VALUE = len(N_HEAVY_NEIGHBORS_LIST)

    def calculate(self):
        return self.N_HEAVY_NEIGHBORS_LIST.index(self.data.GetDegree())

    def mask_value(self):
        return self.MASK_VALUE

    def embedding_input_dim(self):
        return self.MASK_VALUE + 1


class AtomAromaticity(AtomicAttributeCalculator):
    def calculate(self):
        return 1 if self.data.GetIsAromatic() else 0

    def mask_value(self):
        return self.calculate()

    def embedding_input_dim(self):
        return 2


class AtomCharge(AtomicAttributeCalculator):
    CHARGE_LIST = [-3, -2, -1, 0, 1, 2, 3, "Extreme"]
    MASK_VALUE = len(CHARGE_LIST)

    def calculate(self):
        return self.CHARGE_LIST.index(self.data.GetFormalCharge())

    def mask_value(self):
        return self.MASK_VALUE

    def embedding_input_dim(self):
        return self.MASK_VALUE + 1


class AtomInRing(AtomicAttributeCalculator):
    def calculate(self):
        return 1 if self.data.IsInRing() else 0

    def mask_value(self):
        return self.calculate()

    def embedding_input_dim(self):
        return 2


AtomicAttributeFunctions: dict[str, AtomicAttributeCalculator] = {
    "type": AtomType,
    "chirality": AtomChirality,
    "hybridization": AtomHybridization,
    "heavy_neighbors": AtomNHeavy,
    "aromaticity": AtomAromaticity,
    "charge": AtomCharge,
    "ring": AtomInRing,
    "valence": AtomValence,
}
