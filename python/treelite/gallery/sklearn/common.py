# coding: utf-8
import treelite


class SKLConverterBase:
    @classmethod
    def process_tree(cls, sklearn_tree, sklearn_model):
        treelite_tree = treelite.ModelBuilder.Tree()
        # Node #0 is always root for scikit-learn decision trees
        treelite_tree[0].set_root()

        # Iterate over each node: node ID ranges from 0 to [node_count]-1
        for node_id in range(sklearn_tree.node_count):
            cls.process_node(treelite_tree, sklearn_tree, node_id, sklearn_model)

        return treelite_tree

    @classmethod
    def process_node(cls, treelite_tree, sklearn_tree, node_id, sklearn_model):
        if sklearn_tree.children_left[node_id] == -1:  # leaf node
            cls.process_leaf_node(treelite_tree, sklearn_tree, node_id, sklearn_model)
        else:  # test node
            cls.process_test_node(treelite_tree, sklearn_tree, node_id, sklearn_model)

    @classmethod
    def process_test_node(cls, treelite_tree, sklearn_tree, node_id, sklearn_model):
        # Initialize the test node with given node ID
        treelite_tree[node_id].set_numerical_test_node(
            feature_id=sklearn_tree.feature[node_id],
            opname='<=',
            threshold=sklearn_tree.threshold[node_id],
            default_left=True,
            left_child_key=sklearn_tree.children_left[node_id],
            right_child_key=sklearn_tree.children_right[node_id])

    @classmethod
    def process_leaf_node(cls, treelite_tree, sklearn_tree, node_id, sklearn_model):
        raise NotImplementedError()   # implemented by mixin
