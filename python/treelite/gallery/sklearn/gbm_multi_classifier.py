# coding: utf-8
import treelite


class SKLGBMMultiClassifierMixin:
    @classmethod
    def process_model(cls, sklearn_model):
        # Check for init='zero'
        if sklearn_model.init != 'zero':
            raise Exception("Gradient boosted trees must be trained with "
                            "the option init='zero'")
        # Initialize treelite model builder
        # Set random_forest=False for gradient boosted trees
        # Set num_output_group for multiclass classification
        # Set pred_transform='softmax' to obtain probability predictions
        builder = treelite.ModelBuilder(num_feature=sklearn_model.n_features_,
                                        num_output_group=sklearn_model.n_classes_,
                                        random_forest=False,
                                        pred_transform='softmax')
        # Process [number of iterations] * [number of classes] trees
        for i in range(sklearn_model.n_estimators):
            for k in range(sklearn_model.n_classes_):
                builder.append(cls.process_tree(sklearn_model.estimators_[i][k].tree_,
                                                sklearn_model))

        return builder.commit()

    @classmethod
    def process_leaf_node(cls, treelite_tree, sklearn_tree, node_id, sklearn_model):
        leaf_value = sklearn_tree.value[node_id].squeeze()
        # Need to shrink each leaf output by the learning rate
        leaf_value *= sklearn_model.learning_rate
        # Initialize the leaf node with given node ID
        treelite_tree[node_id].set_leaf_node(leaf_value)
