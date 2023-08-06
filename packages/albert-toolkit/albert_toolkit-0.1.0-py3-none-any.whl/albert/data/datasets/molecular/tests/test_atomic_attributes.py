import pytest
import torch
from rdkit import Chem
from albert.data.datasets.molecular.graph import AtomicAttributes, BondAttributes


@pytest.mark.parametrize(
    "attributes, expected_shape, expected_values, expected_mask",
    [
        (
            [
                "type",
                "chirality",
                "heavy_neighbors",
                "aromaticity",
                "ring",
                "charge",
                "hybridization",
                "valence",
            ],
            (11, 8),
            [
                [5, 0, 1, 0, 0, 3, 3, 4],
                [5, 0, 3, 1, 1, 3, 2, 4],
                [5, 0, 2, 1, 1, 3, 2, 4],
                [5, 0, 3, 1, 1, 3, 2, 4],
                [5, 0, 2, 0, 0, 3, 3, 4],
                [5, 2, 3, 0, 0, 3, 3, 4],
                [8, 0, 1, 0, 0, 3, 3, 1],
                [16, 0, 1, 0, 0, 3, 3, 1],
                [5, 0, 2, 1, 1, 3, 2, 4],
                [5, 0, 2, 1, 1, 3, 2, 4],
                [5, 0, 2, 1, 1, 3, 2, 4],
            ],
            [
                [118, 0, 6, 0, 0, 8, 7, 4],
                [118, 0, 6, 1, 1, 8, 7, 4],
                [118, 0, 6, 1, 1, 8, 7, 4],
                [118, 0, 6, 1, 1, 8, 7, 4],
                [118, 0, 6, 0, 0, 8, 7, 4],
                [118, 0, 6, 0, 0, 8, 7, 4],
                [118, 0, 6, 0, 0, 8, 7, 1],
                [118, 0, 6, 0, 0, 8, 7, 1],
                [118, 0, 6, 1, 1, 8, 7, 4],
                [118, 0, 6, 1, 1, 8, 7, 4],
                [118, 0, 6, 1, 1, 8, 7, 4],
            ],
        ),
    ],
)
def test_atomic_attributes(attributes, expected_shape, expected_values, expected_mask):
    # Create a test molecule
    mol = Chem.MolFromSmiles("Cc1cc(C[C@H](F)Cl)ccc1")

    # Create an instance of the AtomicAttributes class
    calculator = AtomicAttributes(attributes)

    # Calculate the attributes for the test molecule
    result, mask = calculator(mol)

    # TODO : Test the Mask Tensor

    # Check that the result is a torch tensor with the expected shape
    assert isinstance(result, torch.Tensor)
    assert result.shape == expected_shape
    assert isinstance(mask, torch.Tensor)

    # Check that the attribute values are correct for the test molecule
    for i, expected_row in enumerate(expected_values):
        for j, expected_value in enumerate(expected_row):
            assert result[i, j] == expected_value

    # Check that the mask values are correct for the test molecule
    for i, expected_row in enumerate(expected_mask):
        for j, expected_value in enumerate(expected_row):
            assert mask[i, j] == expected_value


@pytest.mark.parametrize(
    "attributes, expected_shape, expected_attr_values, expected_edge_index_values",
    [
        (
            [
                "type",
                "dir",
                "conjugated",
                "ring",
            ],
            (22, 4),
            [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [3, 0, 1, 1],
                [3, 0, 1, 1],
                [3, 0, 1, 1],
                [3, 0, 1, 1],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [3, 0, 1, 1],
                [3, 0, 1, 1],
                [3, 0, 1, 1],
                [3, 0, 1, 1],
                [3, 0, 1, 1],
                [3, 0, 1, 1],
                [3, 0, 1, 1],
                [3, 0, 1, 1],
            ],
            [
                [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 5, 7, 3, 8, 8, 9, 9, 10, 10, 1],
                [1, 0, 2, 1, 3, 2, 4, 3, 5, 4, 6, 5, 7, 5, 8, 3, 9, 8, 10, 9, 1, 10],
            ],
        ),
    ],
)
def test_bond_attributes(
    attributes, expected_shape, expected_attr_values, expected_edge_index_values
):
    # Create a test molecule
    mol = Chem.MolFromSmiles("Cc1cc(C[C@H](F)Cl)ccc1")

    # Create an instance of the AtomicAttributes class
    calculator = BondAttributes(attributes)

    # Calculate the attributes for the test molecule
    edge_index, edge_attr = calculator(mol)

    # Check that the result is a torch tensor with the expected shape
    assert isinstance(edge_attr, torch.Tensor)
    assert edge_attr.shape == expected_shape

    # Check that the attribute values are correct for the test molecule
    for i, expected_row in enumerate(expected_attr_values):
        for j, expected_value in enumerate(expected_row):
            assert edge_attr[i, j] == expected_value

    for i, expected_row in enumerate(expected_edge_index_values):
        for j, expected_value in enumerate(expected_row):
            assert edge_index[i, j] == expected_value
