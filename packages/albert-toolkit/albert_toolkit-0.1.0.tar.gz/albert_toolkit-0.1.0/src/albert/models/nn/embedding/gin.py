# Imported From MolCLR Project Under the MIT License

import torch
from torch import nn
import torch.nn.functional as F

from torch_geometric.nn import MessagePassing
from torch_geometric.utils import add_self_loops
from torch_geometric.nn import global_add_pool, global_mean_pool, global_max_pool

import lightning as L

num_atom_type = 119  # including the extra mask tokens
num_chirality_tag = 3

num_bond_type = 5  # including aromatic and self-loop edge
num_bond_direction = 3


class GINEConv(MessagePassing):
    def __init__(self, edge_attr_info: dict, emb_dim: int):
        super(GINEConv, self).__init__()
        self.mlp = nn.Sequential(
            nn.Linear(emb_dim, 2 * emb_dim), nn.ReLU(), nn.Linear(2 * emb_dim, emb_dim)
        )

        edge_emb_layers = []
        for x in edge_attr_info:
            edge_emb_layers.append(nn.Embedding(x[1], emb_dim))
            nn.init.xavier_uniform_(edge_emb_layers[-1].weight.data)

        self.edge_embedding_modules = nn.ModuleList(edge_emb_layers)

    def forward(self, x, edge_index, edge_attr):
        # add self loops in the edge space
        edge_index = add_self_loops(edge_index, num_nodes=x.size(0))[0]

        # add features corresponding to self-loop edges.
        self_loop_attr = torch.zeros(x.size(0), edge_attr.shape[1])
        self_loop_attr[:, 0] = 4  # bond type for self-loop edge
        self_loop_attr = self_loop_attr.to(edge_attr.device).to(edge_attr.dtype)
        edge_attr = torch.cat((edge_attr, self_loop_attr), dim=0)

        edge_embeddings = None
        for i, emb_layer in enumerate(self.edge_embedding_modules):
            if edge_embeddings is None:
                edge_embeddings = emb_layer.forward(edge_attr[:, i])
            else:
                edge_embeddings = edge_embeddings + emb_layer.forward(edge_attr[:, i])

        return self.propagate(edge_index, x=x, edge_attr=edge_embeddings)

    def message(self, x_j, edge_attr):
        return x_j + edge_attr

    def update(self, aggr_out):
        return self.mlp(aggr_out)


class GINet(nn.Module):
    """
    Args:
        num_layer (int): the number of GNN layers
        emb_dim (int): dimensionality of embeddings
        max_pool_layer (int): the layer from which we use max pool rather than add pool for neighbor aggregation
        drop_ratio (float): dropout rate
    Output:
        node representations
    """

    def __init__(
        self,
        num_layer=5,
        emb_dim=300,
        feat_dim=256,
        drop_ratio=0,
        pool="mean",
        atom_attr_info=None,
        edge_attr_info=None,
    ):
        super(GINet, self).__init__()
        self.num_layer = num_layer
        self.emb_dim = emb_dim
        self.feat_dim = feat_dim
        self.drop_ratio = drop_ratio
        self.pool_type = pool

        if (atom_attr_info is not None) and (edge_attr_info is not None):
            self.initialize_network(atom_attr_info, edge_attr_info)
        else:
            self.atom_attr_info = atom_attr_info
            self.edge_attr_info = edge_attr_info
            self.ready = False

    def initialize_network(self, atom_attr_info, edge_attr_info):
        self.atom_attr_info = atom_attr_info
        self.edge_attr_info = edge_attr_info

        atomic_emb_layers = []
        for x in atom_attr_info:
            print(f"Found Atomic Feature `{x[0]}` with input dim `{x[1]}`")
            atomic_emb_layers.append(nn.Embedding(x[1], self.emb_dim))
            nn.init.xavier_uniform_(atomic_emb_layers[-1].weight.data)

        self.atomic_embedding_modules = nn.ModuleList(atomic_emb_layers)

        # List of MLPs
        for x in edge_attr_info:
            print(f"Found Bond Feature {x[0]} with input dim {x[1]}")
        self.gnns = nn.ModuleList()
        for layer in range(self.num_layer):
            self.gnns.append(GINEConv(self.edge_attr_info, self.emb_dim))

        # List of batchnorms
        self.batch_norms = nn.ModuleList()
        for layer in range(self.num_layer):
            self.batch_norms.append(nn.BatchNorm1d(self.emb_dim))

        if self.pool_type == "mean":
            self.pool = global_mean_pool
        elif self.pool_type == "max":
            self.pool = global_max_pool
        elif self.pool_type == "add":
            self.pool = global_add_pool

        self.feat_lin = nn.Linear(self.emb_dim, self.feat_dim)

        self.out_lin = nn.Sequential(
            nn.Linear(self.feat_dim, self.feat_dim),
            nn.ReLU(inplace=True),
            nn.Linear(self.feat_dim, self.feat_dim // 2),
        )

        self.ready = True

    def forward(self, data):
        assert self.ready, "You need to run initialize_network before calling forward"

        x = data.x
        edge_index = data.edge_index
        edge_attr = data.edge_attr

        h = None
        for i, emb_layer in enumerate(self.atomic_embedding_modules):
            if h is None:
                h = emb_layer.forward(x[:, i])
            else:
                h = h + emb_layer.forward(x[:, i])

        for layer in range(self.num_layer):
            h = self.gnns[layer](h, edge_index, edge_attr)
            h = self.batch_norms[layer](h)
            if layer == self.num_layer - 1:
                h = F.dropout(h, self.drop_ratio, training=self.training)
            else:
                h = F.dropout(F.relu(h), self.drop_ratio, training=self.training)

        h = self.pool(h, data.batch)
        h = self.feat_lin(h)
        out = self.out_lin(h)

        return h, out

    def __getstate__(self):
        return {
            "num_layer": self.num_layer,
            "emb_dim": self.emb_dim,
            "feat_dim": self.feat_dim,
            "drop_ratio": self.drop_ratio,
            "pool": self.pool_type,
            "state_dict": self.state_dict(),
            "edge_attr_info": self.edge_attr_info
            if self.edge_attr_info is not None
            else None,
            "atom_attr_info": self.atom_attr_info
            if self.atom_attr_info is not None
            else None,
        }

    def __setstate__(self, state):
        state_dict = state["state_dict"]
        del state["state_dict"]
        self.__init__(**state)
        self.load_state_dict(state_dict)
