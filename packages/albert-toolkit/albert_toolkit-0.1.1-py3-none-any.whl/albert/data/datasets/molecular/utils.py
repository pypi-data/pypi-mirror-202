from torch_geometric.data import Batch


def graph_collate_fn(graphs):
    # Use default collate to stack individual samples into a batch
    batch = Batch.from_data_list(graphs)

    return batch
