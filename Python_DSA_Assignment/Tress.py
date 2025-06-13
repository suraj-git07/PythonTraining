"""Binary Tree implementation with level-wise creation and various traversals.

This module provides a BinaryTree class for creating and manipulating a binary tree.
It supports level-wise tree construction, various traversal methods (inorder, preorder,
postorder), views (right, left, top, bottom, alternate level), and maximum path sum
calculation. The tree is built interactively with user input and includes input validation.

Classes:
    TreeNode: Represents a single node in the binary tree.
    BinaryTree: Main class for binary tree operations and traversals.
"""

class TreeNode:
    """A single node in the binary tree.

    Attributes:
        value: The value stored in the node.
        left: Reference to the left child node.
        right: Reference to the right child node.
    """

    def __init__(self, value):
        """Initialize a TreeNode with a given value.

        Args:
            value: The value to store in the node.
        """
        self.value = value  # node value
        self.left = None    # left child reference
        self.right = None   # right child reference


class BinaryTree:
    """Binary tree with level-wise creation and various traversals.

    Provides methods to build a binary tree level by level and perform different
    types of traversals and views.

    Attributes:
        root: The root node of the binary tree.
    """

    def __init__(self):
        """Initialize an empty BinaryTree."""
        self.root = None

    def build_tree_levelwise(self):
        """Build a binary tree level by level using a queue.

        Prompts the user for node values and constructs the tree level-wise.
        Uses a queue to process nodes and add their children.

        Time Complexity: O(n) where n is the number of nodes, as each node is processed once.
        Space Complexity: O(w) where w is the maximum width of the tree (queue size).
        """
        # root value
        root_value = get_input("Enter root value: ")
        if root_value is None:
            print("Root cannot be null!")
            return

        self.root = TreeNode(root_value)
        print(f"Root {root_value} added")

        # queue - contains nodes that need children
        queue = [self.root]

        while queue:
            # Adding the child of ele (front of queue)
            current_parent = queue.pop(0)  # popping the first element
            print(f"\nAdding children for node {current_parent.value}")

            # Ask for left child
            left_value = get_input(f"Enter left child of {current_parent.value} (or 'q' to finish): ")
            if left_value == 'q':
                break
            if left_value is not None:
                current_parent.left = TreeNode(left_value)
                queue.append(current_parent.left)  # Add to queue for future processing
                print(f"Added {left_value} as left child of {current_parent.value}")
            else:
                print(f"Left child of {current_parent.value} is null")

            # Ask for right child
            right_value = get_input(f"Enter right child of {current_parent.value} (or 'q' to finish): ")
            if right_value == 'q':
                break
            if right_value is not None:
                current_parent.right = TreeNode(right_value)
                queue.append(current_parent.right)  # Add to queue for future processing
                print(f"Added {right_value} as right child of {current_parent.value}")
            else:
                print(f"Right child of {current_parent.value} is null")

        print("\nTree creation completed!")

    def inorder_traversal(self):
        """Perform an inorder traversal of the binary tree (Left -> Root -> Right).

        Returns:
            list: A list of node values in inorder traversal order.

        Time Complexity: O(n) where n is the number of nodes, visits each node once.
        Space Complexity: O(h) where h is the height of the tree, due to recursion stack.
        """
        result = []
        self._inorder_helper(self.root, result)
        return result

    def _inorder_helper(self, node, result):
        """Helper method for inorder traversal.

        Args:
            node: The current node being processed.
            result: List to store the traversal result.

        Time Complexity: O(n) where n is the number of nodes, each node processed once.
        Space Complexity: O(h) where h is the height of the tree, recursion stack depth.
        """
        if node is None:
            return

        self._inorder_helper(node.left, result)
        result.append(node.value)
        self._inorder_helper(node.right, result)

    def preorder_traversal(self):
        """Perform a preorder traversal of the binary tree (Root -> Left -> Right).

        Returns:
            list: A list of node values in preorder traversal order.

        Time Complexity: O(n) where n is the number of nodes, visits each node once.
        Space Complexity: O(h) where h is the height of the tree, due to recursion stack.
        """
        result = []
        self._preorder_helper(self.root, result)
        return result

    def _preorder_helper(self, node, result):
        """Helper method for preorder traversal.

        Args:
            node: The current node being processed.
            result: List to store the traversal result.

        Time Complexity: O(n) where n is the number of nodes, each node processed once.
        Space Complexity: O(h) where h is the height of the tree, recursion stack depth.
        """
        if node is None:
            return

        result.append(node.value)
        self._preorder_helper(node.left, result)
        self._preorder_helper(node.right, result)

    def postorder_traversal(self):
        """Perform a postorder traversal of the binary tree (Left -> Right -> Root).

        Returns:
            list: A list of node values in postorder traversal order.

        Time Complexity: O(n) where n is the number of nodes, visits each node once.
        Space Complexity: O(h) where h is the height of the tree, due to recursion stack.
        """
        result = []
        self._postorder_helper(self.root, result)
        return result

    def _postorder_helper(self, node, result):
        """Helper method for postorder traversal.

        Args:
            node: The current node being processed.
            result: List to store the traversal result.

        Time Complexity: O(n) where n is the number of nodes, each node processed once.
        Space Complexity: O(h) where h is the height of the tree, recursion stack depth.
        """
        if node is None:
            return

        self._postorder_helper(node.left, result)
        self._postorder_helper(node.right, result)
        result.append(node.value)

    def right_view(self):
        """Get the right view of the binary tree (rightmost node at each level).

        Returns:
            list: A list of node values representing the right view.

        Time Complexity: O(n) where n is the number of nodes, processes each node once.
        Space Complexity: O(w) where w is the maximum width of the tree (queue size).
        """
        if not self.root:
            return []

        result = []
        queue = [self.root]

        while queue:
            level_size = len(queue)
            for i in range(level_size):
                node = queue.pop(0)

                # Last node in current level
                if i == level_size - 1:
                    result.append(node.value)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

        return result

    def left_view(self):
        """Get the left view of the binary tree (leftmost node at each level).

        Returns:
            list: A list of node values representing the left view.

        Time Complexity: O(n) where n is the number of nodes, processes each node once.
        Space Complexity: O(w) where w is the maximum width of the tree (queue size).
        """
        if not self.root:
            return []

        result = []
        queue = [self.root]

        while queue:
            level_size = len(queue)
            for i in range(level_size):
                node = queue.pop(0)

                # First node in current level
                if i == 0:
                    result.append(node.value)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

        return result

    def top_view(self):
        """Get the top view of the binary tree (nodes visible from the top).

        Returns:
            list: A list of node values representing the top view, sorted by horizontal distance.

        Time Complexity: O(n) where n is the number of nodes, processes each node once.
        Space Complexity: O(w) where w is the maximum width of the tree (queue size + dictionary).
        """
        if not self.root:
            return []

        # Dictionary to store first node at each horizontal distance
        top_nodes = {}
        queue = [(self.root, 0)]  # (node, horizontal_distance)

        while queue:
            node, hd = queue.pop(0)

            # First node at this horizontal distance
            if hd not in top_nodes:
                top_nodes[hd] = node.value

            if node.left:
                queue.append((node.left, hd - 1))
            if node.right:
                queue.append((node.right, hd + 1))

        # Sort by horizontal distance and return values
        return [top_nodes[hd] for hd in sorted(top_nodes.keys())]

    def bottom_view(self):
        """Get the bottom view of the binary tree (nodes visible from the bottom).

        For each horizontal distance, the last node seen during level-order traversal is kept.

        Returns:
            list: A list of node values representing the bottom view, sorted by horizontal distance.

        Time Complexity: O(n) where n is the number of nodes, processes each node once.
        Space Complexity: O(w) where w is the maximum width of the tree (queue size + dictionary).
        """
        if not self.root:
            return []

        bottom_nodes = {}
        queue = [(self.root, 0)]  # (node, horizontal_distance)

        while queue:
            node, hd = queue.pop(0)

            # Always update the node at horizontal distance `hd`
            bottom_nodes[hd] = node.value

            if node.left:
                queue.append((node.left, hd - 1))
            if node.right:
                queue.append((node.right, hd + 1))

        # Return bottom view sorted by horizontal distance
        return [bottom_nodes[hd] for hd in sorted(bottom_nodes.keys())]

    def alternate_level_view(self):
        """Print nodes at alternate levels starting from the root (levels 0, 2, 4, ...).

        Time Complexity: O(n) where n is the number of nodes, processes each node once.
        Space Complexity: O(w) where w is the maximum width of the tree (queue size).
        """
        if not self.root:
            print("Empty tree")
            return

        queue = [self.root]
        level = 0

        while queue:
            level_size = len(queue)

            if level % 2 == 0:
                for i in range(level_size):
                    print(queue[i].value, end=" ")
                print()

            for _ in range(level_size):
                node = queue.pop(0)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            level += 1

    def max_path_sum(self):
        """Calculate the maximum path sum in the binary tree and its corresponding path.

        Returns:
            tuple: A tuple containing the maximum path sum and a list of node values in the path.

        Time Complexity: O(n) where n is the number of nodes, visits each node once.
        Space Complexity: O(h + k) where h is the height of the tree, k is the max length of best_path (up to n in worst case).
        """
        max_sum = float('-inf')  # depicts the negative infinity
        best_path = []  # for storing the best_path of that max_sum

        def dfs(node):
            if not node:
                return 0, []

            left_sum, left_path = dfs(node.left)
            right_sum, right_path = dfs(node.right)

            left_sum = max(0, left_sum)
            right_sum = max(0, right_sum)

            peak_sum = left_sum + node.value + right_sum

            nonlocal max_sum, best_path
            # here I am updating the nonlocal values, as this may be a possible answer
            if peak_sum > max_sum:
                max_sum = peak_sum
                peak_path = []
                if left_sum > 0:
                    peak_path.extend(left_path)
                peak_path.append(node.value)
                if right_sum > 0:
                    peak_path.extend(reversed(right_path))
                best_path = peak_path

            # Now logic of return came, can only return one side obviously
            # there is also a case where node is only positive but as we are already making sure our left_sum and right_sum become positive it is okay.
            if left_sum > right_sum:
                return node.value + left_sum, left_path + [node.value]
            else:
                return node.value + right_sum, [node.value] + right_path

        dfs(self.root)
        return max_sum, best_path

    def display(self):
        """Display the binary tree structure level by level using a queue.

        Prints each level of the tree, with 'null' for missing nodes.

        Time Complexity: O(n) where n is the number of nodes, processes each node once.
        Space Complexity: O(w) where w is the maximum width of the tree (queue size).
        """
        if not self.root:
            print("Empty tree")
            return

        queue = [self.root]

        while queue:
            level_size = len(queue)

            for _ in range(level_size):
                node = queue.pop(0)
                if node:
                    print(node.value, end=" ")
                    queue.append(node.left)
                    queue.append(node.right)
                else:
                    print("null", end=" ")

            print()  # New line after each level


def get_input(input_instruction):
    """Get and validate integer input from the user.

    Args:
        input_instruction: The prompt to display to the user.

    Returns:
        int or None or str: The integer value entered, None for 'null', or 'q' to quit.

    Time Complexity: O(1) for each input operation.
    Space Complexity: O(1) for storing input value.
    """
    while True:
        try:
            value = input(input_instruction).strip()  # strip for removing the leading and trailing whitespaces
            if value.lower() == 'q':
                return 'q'
            if value.lower() == 'null':
                return None
            num = int(value)
            if -10000 <= num <= 10000:
                return num
            print("Value must be between -10000 and 10000")
        except ValueError:
            print("Enter a valid number, 'null', or 'q' to quit")


def main():
    """Main program for interactive binary tree creation and operations.

    Provides a menu to create a tree, display its structure, show traversals,
    calculate the maximum path sum, or exit.

    Time Complexity: O(n) for tree operations, dominated by traversal or build operations.
    Space Complexity: O(w) or O(h) depending on operation, where w is max width and h is height.
    """
    print("=== Binary Tree Builder ===")
    tree = BinaryTree()

    while True:
        print("\n1. Create tree (level-wise)")
        print("2. Display tree structure")
        print("3. Show traversals")
        print("4. Bonus Question ( Max Path Sum )")
        print("5. Exit")

        choice = input("Choose (1-5): ").strip()

        if choice == '1':
            # Create tree level-wise
            tree = BinaryTree()
            tree.build_tree_levelwise()

        elif choice == '2':
            # Display tree structure
            if not tree.root:
                print("No tree created yet!")
                continue
            tree.display()

        elif choice == '3':
            # Show all traversals
            if not tree.root:
                print("No tree created yet!")
                continue

            print("\n=== Tree Traversals ===")
            print(f"Inorder: {tree.inorder_traversal()}")
            print(f"Preorder: {tree.preorder_traversal()}")
            print(f"Postorder: {tree.postorder_traversal()}")
            print(f"Right View: {tree.right_view()}")
            print(f"Left View: {tree.left_view()}")
            print(f"Top View: {tree.top_view()}")
            print(f"Bottom View: {tree.bottom_view()}")
            print(f"Alternate Level View:")
            tree.alternate_level_view()

        elif choice == '4':
            print("======= BONUS Question++++++")
            print(f"Max Path Sum :{tree.max_path_sum()}")

        elif choice == '5':
            # Exit
            print("Goodbye!")
            break

        else:
            print("Invalid choice!")


# execute the main func
if __name__ == "__main__":
    main()