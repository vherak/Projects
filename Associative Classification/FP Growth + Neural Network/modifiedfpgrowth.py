""" Original code is from pyfpgrowth library, but added my own method here which is get_classification_association_rules.
This new addition generates CARs
"""
import itertools


class FPNode(object):
    """
    A node in the FP tree.
    """

    def __init__(self, value, count, parent):
        """
        Create the node.
        """
        self.value = value
        self.count = count
        self.parent = parent
        self.link = None
        self.children = []

    def has_child(self, value):
        """
        Check if node has a particular child node.
        """
        for node in self.children:
            if node.value == value:
                return True

        return False

    def get_child(self, value):
        """
        Return a child node with a particular value.
        """
        for node in self.children:
            if node.value == value:
                return node

        return None

    def add_child(self, value):
        """
        Add a node as a child node.
        """
        child = FPNode(value, 1, self)
        self.children.append(child)
        return child


class FPTree(object):
    """
    A frequent pattern tree.
    """

    def __init__(self, transactions, threshold, root_value, root_count):
        """
        Initialize the tree.
        """
        self.frequent = self.find_frequent_items(transactions, threshold)
        self.headers = self.build_header_table(self.frequent)
        self.root = self.build_fptree(
            transactions, root_value,
            root_count, self.frequent, self.headers)

    @staticmethod
    def find_frequent_items(transactions, threshold):
        """
        Create a dictionary of items with occurrences above the threshold.
        """
        items = {}

        for transaction in transactions:
            for item in transaction:
                if item in items:
                    items[item] += 1
                else:
                    items[item] = 1

        for key in list(items.keys()):
            if items[key] < threshold:
                del items[key]

        return items

    @staticmethod
    def build_header_table(frequent):
        """
        Build the header table.
        """
        headers = {}
        for key in frequent.keys():
            headers[key] = None

        return headers

    def build_fptree(self, transactions, root_value,
                     root_count, frequent, headers):
        """
        Build the FP tree and return the root node.
        """
        root = FPNode(root_value, root_count, None)

        for transaction in transactions:
            sorted_items = [x for x in transaction if x in frequent]
            sorted_items.sort(key=lambda x: frequent[x], reverse=True)
            if len(sorted_items) > 0:
                self.insert_tree(sorted_items, root, headers)

        return root

    def insert_tree(self, items, node, headers):
        """
        Recursively grow FP tree.
        """
        first = items[0]
        child = node.get_child(first)
        if child is not None:
            child.count += 1
        else:
            # Add new child.
            child = node.add_child(first)

            # Link it to header structure.
            if headers[first] is None:
                headers[first] = child
            else:
                current = headers[first]
                while current.link is not None:
                    current = current.link
                current.link = child

        # Call function recursively.
        remaining_items = items[1:]
        if len(remaining_items) > 0:
            self.insert_tree(remaining_items, child, headers)

    def tree_has_single_path(self, node):
        """
        If there is a single path in the tree,
        return True, else return False.
        """
        num_children = len(node.children)
        if num_children > 1:
            return False
        elif num_children == 0:
            return True
        else:
            return True and self.tree_has_single_path(node.children[0])

    def mine_patterns(self, threshold):
        """
        Mine the constructed FP tree for frequent patterns.
        """
        if self.tree_has_single_path(self.root):
            return self.generate_pattern_list()
        else:
            return self.zip_patterns(self.mine_sub_trees(threshold))

    def zip_patterns(self, patterns):
        """
        Append suffix to patterns in dictionary if
        we are in a conditional FP tree.
        """
        suffix = self.root.value

        if suffix is not None:
            # We are in a conditional tree.
            new_patterns = {}
            for key in patterns.keys():
                new_patterns[tuple(sorted(list(key) + [suffix]))] = patterns[key]

            return new_patterns

        return patterns

    def generate_pattern_list(self):
        """
        Generate a list of patterns with support counts.
        """
        patterns = {}
        items = self.frequent.keys()

        # If we are in a conditional tree,
        # the suffix is a pattern on its own.
        if self.root.value is None:
            suffix_value = []
        else:
            suffix_value = [self.root.value]
            patterns[tuple(suffix_value)] = self.root.count

        for i in range(1, len(items) + 1):
            for subset in itertools.combinations(items, i):
                pattern = tuple(sorted(list(subset) + suffix_value))
                patterns[pattern] = \
                    min([self.frequent[x] for x in subset])

        return patterns

    def mine_sub_trees(self, threshold):
        """
        Generate subtrees and mine them for patterns.
        """
        patterns = {}
        mining_order = sorted(self.frequent.keys(),
                              key=lambda x: self.frequent[x])

        # Get items in tree in reverse order of occurrences.
        for item in mining_order:
            suffixes = []
            conditional_tree_input = []
            node = self.headers[item]

            # Follow node links to get a list of
            # all occurrences of a certain item.
            while node is not None:
                suffixes.append(node)
                node = node.link

            # For each occurrence of the item,
            # trace the path back to the root node.
            for suffix in suffixes:
                frequency = suffix.count
                path = []
                parent = suffix.parent

                while parent.parent is not None:
                    path.append(parent.value)
                    parent = parent.parent

                for i in range(frequency):
                    conditional_tree_input.append(path)

            # Now we have the input for a subtree,
            # so construct it and grab the patterns.
            subtree = FPTree(conditional_tree_input, threshold,
                             item, self.frequent[item])
            subtree_patterns = subtree.mine_patterns(threshold)

            # Insert subtree patterns into main patterns dictionary.
            for pattern in subtree_patterns.keys():
                if pattern in patterns:
                    patterns[pattern] += subtree_patterns[pattern]
                else:
                    patterns[pattern] = subtree_patterns[pattern]

        return patterns


def find_frequent_patterns(transactions, support_threshold):
    """
    Given a set of transactions, find the patterns in it
    over the specified support threshold.
    """
    # the input into find_frequent_patterns :
    #   a) transactions :- training data
    #   b) support threshold :- number of items in your transactions that satisfies the frequent itemset
    tree = FPTree(transactions, support_threshold, None, None)
    return tree.mine_patterns(support_threshold)


def generate_association_rules(patterns, confidence_threshold):
    """
    Given a set of frequent itemsets, return a dict
    of association rules in the form
    {(left): ((right), confidence)}
    """
    # the input into generate_association_rules :
    #   a) patterns :- from above
    #   b) confidence_threshold :- the minimum threshold
    rules = {}
    for itemset in patterns.keys():
        upper_support = patterns[itemset]

        for i in range(1, len(itemset)):
            for antecedent in itertools.combinations(itemset, i):
                antecedent = tuple(sorted(antecedent))
                consequent = tuple(sorted(set(itemset) - set(antecedent)))

                if antecedent in patterns:
                    lower_support = patterns[antecedent]
                    confidence = float(upper_support) / lower_support

                    if confidence >= confidence_threshold:
                        rules[antecedent] = (consequent, confidence)

    return rules

def get_classification_association_rules(training_data, class_label, support_threshold, confidence_threshold):
    """ This function generates Classification Association Rules (CARs) using fp-growth algorithm.

    Args:
        training_data (list): A list of transactions
        class_label (list): A list of the class labels of our target in the transaction
        support_threshold (int): The minimum support threshold for generating the frequent patterns
        confidence_threshold (int): The minimum confidence threshold for the CARs

    Returns:
        dict: A dictionary containing all the Classification Association Rules (CARs)
    """
    patterns = find_frequent_patterns(training_data, support_threshold)

    total = len(training_data)
    CARs = {}
    for itemset in patterns.keys():
        upper_support = patterns[itemset]

        for i in range(1, len(itemset)):
            for antecedent in itertools.combinations(itemset, i):
                antecedent = tuple(sorted(antecedent))
                consequent = tuple(sorted(set(itemset) - set(antecedent)))

                if len(consequent) == 1 and consequent[0] in class_label:
                    if antecedent in patterns:
                        lower_support = patterns[antecedent]
                        confidence = float(upper_support) / lower_support
                        support = upper_support/total
                        if confidence >= confidence_threshold:
                            CARs[antecedent] = (consequent, confidence,support)
    return CARs

if __name__ == "__main__":
    # library imports
    from datapreprocess import preprocess_data

    # dataset imports
    breast_cancer = preprocess_data("breast-cancer.data", missing_value_symbol='?')
    # primary_tumour = preprocess_data("primary-tumor.csv")
    balance_scale = preprocess_data("balance-scale.data")
    car = preprocess_data("car.data")

    breast_cancer_class_label = ['Feature 0 : no-recurrence-events', 'Feature 0 : recurrence-events']
    # primary_tumour_class_label = ['Feature 0 : 1', 'Feature 0 : 2', 'Feature 0 : 3', 'Feature 0 : 4', 'Feature 0 : 5', 'Feature 0 : 6', 'Feature 0 : 7', 'Feature 0 : 8', 'Feature 0 : 9', 'Feature 0 : 10', 'Feature 0 : 11', 'Feature 0 : 12', 'Feature 0 : 13', 'Feature 0 : 14', 'Feature 0 : 15', 'Feature 0 : 16', 'Feature 0 : 17', 'Feature 0 : 18', 'Feature 0 : 19', 'Feature 0 : 20', 'Feature 0 : 21', 'Feature 0 : 22',]
    balance_scale_class_label = ['Feature 0 : R', 'Feature 0 : L']
    car_class_label = ['Feature 6 : unacc', 'Feature 6 : acc']

    breast_cancer_rules = get_classification_association_rules(breast_cancer, breast_cancer_class_label, 10, 0.8)
    print(len(breast_cancer_rules))
    # primary_tumour_rules = get_classification_association_rules(primary_tumour, primary_tumour_class_label, 10, 0.5)
    # print(len(primary_tumour_rules))
    balance_scale_rules = get_classification_association_rules(balance_scale, balance_scale_class_label, 20, 0.8)
    print(len(balance_scale_rules))
    car_rules = get_classification_association_rules(car, car_class_label, 30, 0.8)
    print(len(car_rules))

    for rule in breast_cancer_rules:
        consequent, confidence,support = breast_cancer_rules.get(rule)
        print(rule, "=>", consequent, "[", confidence, support,"]")

    # for rule in primary_tumour_rules:
    #     consequent, confidence = primary_tumour_rules.get(rule)
    #     print(rule, "=>", consequent, "[", confidence, "]")

    # for rule in balance_scale_rules:
    #     consequent, confidence,support = balance_scale_rules.get(rule)
    #     print(rule, "=>", consequent, "[", confidence, support,"]")
    #
    # for rule in car_rules:
    #     consequent, confidence,support = car_rules.get(rule)
    #     print(rule, "=>", consequent, "[", confidence, support,"]")

