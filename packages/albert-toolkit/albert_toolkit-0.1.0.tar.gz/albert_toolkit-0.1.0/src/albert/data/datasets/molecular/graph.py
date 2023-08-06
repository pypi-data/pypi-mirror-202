import csv
import math
import os
import random
import time
from copy import deepcopy

import networkx as nx
import numpy as np
import rdkit
import torch
import torch.nn.functional as F
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.rdchem import BondType as BT
from rdkit.Chem.rdchem import HybridizationType as HT

from torch.utils.data.sampler import SubsetRandomSampler
from torch_geometric.data import Data, DataLoader, Dataset
from torch_scatter import scatter

from albert.data.datasets.molecular.atom import AtomicAttributeFunctions, AtomType
from albert.data.datasets.molecular.bond import BondAttributeFunctions


def _read_smiles(data_path):
    smiles_data = []
    with open(data_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for i, row in enumerate(csv_reader):
            smiles = row[-1]
            smiles_data.append(smiles)
    return smiles_data


class AtomicAttributes:
    def __init__(self, attributes: list[str] | None) -> None:
        self.attributes = attributes if attributes is not None else []

    def get_attr_info(self):
        all_info = []
        for attr in self.attributes:
            if attr in AtomicAttributeFunctions:
                aaf = AtomicAttributeFunctions[attr](None)
                all_info.append((attr, aaf.embedding_input_dim()))
            else:
                raise ValueError(f"Attribute {attr} is not supported")

        return all_info

    def __call__(self, mol: Chem.rdchem.Mol) -> torch.Tensor:
        attrs = {}
        masks = {}

        for attr in self.attributes:
            attrs[attr] = []
            masks[attr] = []

        # For each atom we need to calculate its attributes
        # and add them to the attributes for the entire molecule
        # When we are building atomic properties we need to add in all the explicit
        # H atoms so that the valencey calculation is correct
        for atom in mol.GetAtoms():
            for attr in self.attributes:
                if attr in AtomicAttributeFunctions:
                    # For this specific attribute we need to calculate its value
                    # for this atom and add it to the list for this attribute
                    attribute_function = AtomicAttributeFunctions[attr](atom)
                    attrs[attr].append(attribute_function.calculate())
                    masks[attr].append(attribute_function.mask_value())
                else:
                    raise ValueError(f"Attribute {attr} is not supported")

        attr_tensors = [
            torch.tensor(attr, dtype=torch.long).view(-1, 1) for attr in attrs.values()
        ]

        mask_tensors = [
            torch.tensor(attr, dtype=torch.long).view(-1, 1) for attr in masks.values()
        ]

        return torch.cat(attr_tensors, dim=-1), torch.cat(mask_tensors, dim=-1)


class BondAttributes:
    def __init__(self, attributes: list[str] | None) -> None:
        self.attributes = attributes if attributes is not None else []

    def get_attr_info(self):
        all_info = []

        for attr in self.attributes:
            if attr in BondAttributeFunctions:
                baf = BondAttributeFunctions[attr](None)
                all_info.append((attr, baf.embedding_input_dim()))
            else:
                raise ValueError(f"{attr} is not a supported Bond attribute")
            
        return all_info

    def __call__(self, mol: Chem.rdchem.Mol) -> torch.Tensor:
        attrs = {}

        for attr in self.attributes:
            attrs[attr] = []

        # For each bond we need to calculate its attributes
        # and add them to the attributes for the entire molecule
        row, col, edge_feat = [], [], []
        for bond in mol.GetBonds():
            start, end = bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()
            row += [start, end]
            col += [end, start]
            for _ in range(2):
                esubfeat = []
                for attr in self.attributes:
                    if attr in BondAttributeFunctions:
                        # For this specific attribute we need to calculate its value
                        # for this bond and add it to the list for this attribute
                        esubfeat.append(BondAttributeFunctions[attr](bond).calculate())
                    else:
                        raise ValueError(f"Bond Attribute {attr} is not supported")
                edge_feat.append(esubfeat)

        edge_index = torch.tensor([row, col], dtype=torch.long)
        edge_attr = torch.tensor(np.array(edge_feat), dtype=torch.long)

        return edge_index, edge_attr


class MolecularGraph:
    def __init__(
        self,
        smiles: str | None = None,
        mol: Chem.rdchem.Mol | None = None,
        atomic_attributes: list[str] | None = None,
        bond_attributes: list[str] | None = None,
        allowed_augmentations: list[str] | None = None,
    ) -> None:
        if smiles is not None and mol is not None:
            raise ValueError("Only one of `smiles` or `mol` should be provided")

        if mol is not None:
            self.mol = deepcopy(mol)

        if smiles is not None:
            self.set_smiles(smiles)

        if self.mol is None:
            raise ValueError("`smiles` or `mol` must be provided")

        self.atomic_attributes = atomic_attributes
        self.bond_attributes = bond_attributes
        self.allowed_augmentations = allowed_augmentations
        self.base_graph = None

    def set_smiles(self, smiles: str) -> None:
        if smiles != "":
            self.smiles = smiles
            self.mol = Chem.MolFromSmiles(self.smiles)

    def set_mol(self, mol: Chem.rdchem.Mol) -> None:
        self.mol = mol

    def generate_base_graph(self):
        self.N = self.mol.GetNumAtoms()
        self.M = self.mol.GetNumBonds()

        # Compute all the atomic attributes
        self.x, self.x_masks = AtomicAttributes(self.atomic_attributes)(self.mol)

        self.edge_index, self.edge_attr = BondAttributes(self.bond_attributes)(self.mol)

        self.base_graph = Data(
            x=self.x, edge_index=self.edge_index, edge_attr=self.edge_attr
        )

    def generate_augmented_variant(self):
        # TODO: add allowed augmentations and figure out
        # how we will apply them to the base graph
        # Can this even be done in a sequential manner
        # or do we have to build up a special composite augmentation
        # for each possible combination of augmentations?

        # random mask a subgraph of the molecule
        num_mask_nodes = max([1, math.floor(0.25 * self.N)])
        num_mask_edges = max([0, math.floor(0.25 * self.M)])
        mask_nodes_i = random.sample(list(range(self.N)), num_mask_nodes)
        mask_edges_i_single = random.sample(list(range(self.M)), num_mask_edges)
        mask_edges_i = [2 * i for i in mask_edges_i_single] + [
            2 * i + 1 for i in mask_edges_i_single
        ]

        x_i = deepcopy(self.x)
        x_mask_i = deepcopy(self.x_masks)
        for atom_idx in mask_nodes_i:
            x_i[atom_idx, :] = x_mask_i[atom_idx, :]
        edge_index_i = torch.zeros((2, 2 * (self.M - num_mask_edges)), dtype=torch.long)
        edge_attr_i = torch.zeros(
            (2 * (self.M - num_mask_edges), len(self.bond_attributes)), dtype=torch.long
        )
        count = 0
        for bond_idx in range(2 * self.M):
            if bond_idx not in mask_edges_i:
                edge_index_i[:, count] = self.edge_index[:, bond_idx]
                edge_attr_i[count, :] = self.edge_attr[bond_idx, :]
                count += 1
        return Data(x=x_i, edge_index=edge_index_i, edge_attr=edge_attr_i)

    def construct_tensors(
        self, num_variants: int = 2, augment_all: bool = False
    ) -> list[Data]:
        assert self.mol is not None, "No Molecule has been defined"

        if self.base_graph is None:
            self.generate_base_graph()

        graphs: list[Data] = []

        # If the user wants all augmented variants then we generate
        # only augmented versions
        if augment_all:
            for i in range(num_variants):
                graphs.append(self.generate_augmented_variant())
        else:
            # Otherwise the first variant we return is the base
            # unaugmented variant
            graphs.append(self.base_graph)
            for i in range(num_variants - 1):
                graphs.append(self.generate_augmented_variant())

        return graphs


class MolecularStructureDataset(Dataset):
    def __init__(
        self,
        num_variants_per_mol: int = 2,
        atomic_attributes: list[str] | None = None,
        bond_attributes: list[str] | None = None,
        allowed_augmentations: list[str] | None = None,
        augment_all_variants: bool = False,
    ):
        self.atomic_attributes = atomic_attributes
        self.bond_attributes = bond_attributes
        self.allowed_augmentations = allowed_augmentations
        self.num_variants_per_mol = num_variants_per_mol
        self.augment_all_variants = augment_all_variants

        assert (
            self.atomic_attributes is not None
        ), "you must specify at least one atomic attribute so that each atomic node has at least a single label"

    def get_atomic_attr_info(self):
        return AtomicAttributes(self.atomic_attributes).get_attr_info()

    def get_bond_attr_info(self):
        return BondAttributes(self.bond_attributes).get_attr_info()


class MoleculeSMILESDataset(MolecularStructureDataset):
    def __init__(
        self,
        num_variants_per_mol: int = 2,
        smiles_file_path: str | None = None,
        smiles_strings: list[str] | None = None,
        atomic_attributes: list[str] | None = None,
        bond_attributes: list[str] | None = None,
        allowed_augmentations: list[str] | None = None,
        augment_all_variants: bool = False,
        **kwargs,
    ):
        super().__init__(
            num_variants_per_mol,
            atomic_attributes,
            bond_attributes,
            allowed_augmentations,
            augment_all_variants,
        )
        self.smiles_strings = []
        if smiles_file_path is not None:
            self.smiles_strings.extend(_read_smiles(smiles_file_path))

        if smiles_strings is not None:
            self.smiles_strings.extend(smiles_strings)

        if len(self.smiles_strings) < 1:
            raise ValueError(
                "No smiles Strings were passed in, we have no data to build the dataset on"
            )

    def __len__(self) -> int:
        return len(self.smiles_strings)

    def __getitem__(self, idx: int) -> list[Data]:
        assert idx < len(
            self.smiles_strings
        ), "the index passed to the dataset is out of bounds"

        smiles_str: str = self.smiles_strings[idx]

        # Build the MolecularGraph for this SMILES string
        graph = MolecularGraph(
            smiles_str,
            None,
            atomic_attributes=self.atomic_attributes,
            bond_attributes=self.bond_attributes,
            allowed_augmentations=self.allowed_augmentations,
        )

        return graph.construct_tensors(
            num_variants=self.num_variants_per_mol,
            augment_all=self.augment_all_variants,
        )


class MoleculeDataset(Dataset):
    def __init__(self, data_path):
        super(Dataset, self).__init__()
        self.smiles_data = _read_smiles(data_path)

    def __getitem__(self, index):
        mol = Chem.MolFromSmiles(self.smiles_data[index])
        # mol = Chem.AddHs(mol)

        N = mol.GetNumAtoms()
        M = mol.GetNumBonds()

        type_idx = []
        chirality_idx = []
        atomic_number = []
        # aromatic = []
        # sp, sp2, sp3, sp3d = [], [], [], []
        # num_hs = []
        for atom in mol.GetAtoms():
            type_idx.append(ATOM_LIST.index(atom.GetAtomicNum()))
            chirality_idx.append(CHIRALITY_LIST.index(atom.GetChiralTag()))
            atomic_number.append(atom.GetAtomicNum())
            # aromatic.append(1 if atom.GetIsAromatic() else 0)
            # hybridization = atom.GetHybridization()
            # sp.append(1 if hybridization == HybridizationType.SP else 0)
            # sp2.append(1 if hybridization == HybridizationType.SP2 else 0)
            # sp3.append(1 if hybridization == HybridizationType.SP3 else 0)
            # sp3d.append(1 if hybridization == HybridizationType.SP3D else 0)

        # z = torch.tensor(atomic_number, dtype=torch.long)
        x1 = torch.tensor(type_idx, dtype=torch.long).view(-1, 1)
        x2 = torch.tensor(chirality_idx, dtype=torch.long).view(-1, 1)
        x = torch.cat([x1, x2], dim=-1)
        # x2 = torch.tensor([atomic_number, aromatic, sp, sp2, sp3, sp3d, num_hs],
        #                     dtype=torch.float).t().contiguous()
        # x = torch.cat([x1.to(torch.float), x2], dim=-1)

        row, col, edge_feat = [], [], []
        for bond in mol.GetBonds():
            start, end = bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()
            row += [start, end]
            col += [end, start]
            # edge_type += 2 * [MOL_BONDS[bond.GetBondType()]]
            edge_feat.append(
                [
                    BOND_LIST.index(bond.GetBondType()),
                    BONDDIR_LIST.index(bond.GetBondDir()),
                ]
            )
            edge_feat.append(
                [
                    BOND_LIST.index(bond.GetBondType()),
                    BONDDIR_LIST.index(bond.GetBondDir()),
                ]
            )

        edge_index = torch.tensor([row, col], dtype=torch.long)
        edge_attr = torch.tensor(np.array(edge_feat), dtype=torch.long)

        # random mask a subgraph of the molecule
        num_mask_nodes = max([1, math.floor(0.25 * N)])
        num_mask_edges = max([0, math.floor(0.25 * M)])
        mask_nodes_i = random.sample(list(range(N)), num_mask_nodes)
        mask_nodes_j = random.sample(list(range(N)), num_mask_nodes)
        mask_edges_i_single = random.sample(list(range(M)), num_mask_edges)
        mask_edges_j_single = random.sample(list(range(M)), num_mask_edges)
        mask_edges_i = [2 * i for i in mask_edges_i_single] + [
            2 * i + 1 for i in mask_edges_i_single
        ]
        mask_edges_j = [2 * i for i in mask_edges_j_single] + [
            2 * i + 1 for i in mask_edges_j_single
        ]

        x_i = deepcopy(x)
        for atom_idx in mask_nodes_i:
            x_i[atom_idx, :] = torch.tensor([len(ATOM_LIST), 0])
        edge_index_i = torch.zeros((2, 2 * (M - num_mask_edges)), dtype=torch.long)
        edge_attr_i = torch.zeros((2 * (M - num_mask_edges), 2), dtype=torch.long)
        count = 0
        for bond_idx in range(2 * M):
            if bond_idx not in mask_edges_i:
                edge_index_i[:, count] = edge_index[:, bond_idx]
                edge_attr_i[count, :] = edge_attr[bond_idx, :]
                count += 1
        data_i = Data(x=x_i, edge_index=edge_index_i, edge_attr=edge_attr_i)

        x_j = deepcopy(x)
        for atom_idx in mask_nodes_j:
            x_j[atom_idx, :] = torch.tensor([len(ATOM_LIST), 0])
        edge_index_j = torch.zeros((2, 2 * (M - num_mask_edges)), dtype=torch.long)
        edge_attr_j = torch.zeros((2 * (M - num_mask_edges), 2), dtype=torch.long)
        count = 0
        for bond_idx in range(2 * M):
            if bond_idx not in mask_edges_j:
                edge_index_j[:, count] = edge_index[:, bond_idx]
                edge_attr_j[count, :] = edge_attr[bond_idx, :]
                count += 1
        data_j = Data(x=x_j, edge_index=edge_index_j, edge_attr=edge_attr_j)

        return data_i, data_j

    def __len__(self):
        return len(self.smiles_data)


class MoleculeDatasetWrapper(object):
    def __init__(self, batch_size, num_workers, valid_size, data_path):
        super(object, self).__init__()
        self.data_path = data_path
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.valid_size = valid_size

    def get_data_loaders(self):
        train_dataset = MoleculeDataset(data_path=self.data_path)
        train_loader, valid_loader = self.get_train_validation_data_loaders(
            train_dataset
        )
        return train_loader, valid_loader

    def get_train_validation_data_loaders(self, train_dataset):
        # obtain training indices that will be used for validation
        num_train = len(train_dataset)
        indices = list(range(num_train))
        np.random.shuffle(indices)

        split = int(np.floor(self.valid_size * num_train))
        train_idx, valid_idx = indices[split:], indices[:split]

        # define samplers for obtaining training and validation batches
        train_sampler = SubsetRandomSampler(train_idx)
        valid_sampler = SubsetRandomSampler(valid_idx)

        train_loader = DataLoader(
            train_dataset,
            batch_size=self.batch_size,
            sampler=train_sampler,
            num_workers=self.num_workers,
            drop_last=True,
        )

        valid_loader = DataLoader(
            train_dataset,
            batch_size=self.batch_size,
            sampler=valid_sampler,
            num_workers=self.num_workers,
            drop_last=True,
        )

        return train_loader, valid_loader
