class TreeNode:
    """A single node in the binary tree"""
    
    def __init__(self, value):
        self.value = value # node value
        self.left = None   # left child refrence
        self.right = None  # right child refrence


class BinaryTree:
    """Binary tree with level-wise creation and diff traversals"""
    
    def __init__(self):
        self.root = None
    
    def build_tree_levelwise(self):
        """Build tree level by level using queue"""
        # Time Complexity: O(n) where n is number of nodes, as we process each node once
        # Space Complexity: O(w) where w is maximum width of the tree (queue size)
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
        """Inorder: Left -> Root -> Right"""
        # Time Complexity: O(n) where n is number of nodes, visits each node once
        # Space Complexity: O(h) where h is height of tree, due to recursion stack
        result = []
        self._inorder_helper(self.root, result)
        return result
    
    def _inorder_helper(self, node, result):
        """Helper method for inorder traversal"""
        # Time Complexity: O(n) - each node processed once
        # Space Complexity: O(h) - recursion stack depth equals tree height
        if node is None:
            return
        
        self._inorder_helper(node.left, result)
        result.append(node.value)
        self._inorder_helper(node.right, result)
    
    def preorder_traversal(self):
        """Preorder: Root -> Left -> Right"""
        # Time Complexity: O(n) where n is number of nodes, visits each node once
        # Space Complexity: O(h) where h is height of tree, due to recursion stack
        result = []
        self._preorder_helper(self.root, result)
        return result
    
    def _preorder_helper(self, node, result):
        """Helper method for preorder traversal"""
        # Time Complexity: O(n) - each node processed once
        # Space Complexity: O(h) - recursion stack depth equals tree height
        if node is None:
            return
        
        result.append(node.value)
        self._preorder_helper(node.left, result)
        self._preorder_helper(node.right, result)
    
    def postorder_traversal(self):
        """Postorder: Left -> Right -> Root"""
        # Time Complexity: O(n) where n is number of nodes, visits each node once
        # Space Complexity: O(h) where h is height of tree, due to recursion stack
        result = []
        self._postorder_helper(self.root, result)
        return result
    
    def _postorder_helper(self, node, result):
        """Helper method for postorder traversal"""
        # Time Complexity: O(n) - each node processed once
        # Space Complexity: O(h) - recursion stack depth equals tree height
        if node is None:
            return
        
        self._postorder_helper(node.left, result)
        self._postorder_helper(node.right, result)
        result.append(node.value)
    
    def right_view(self):
        """Right view: rightmost node at each level"""
        # Time Complexity: O(n) where n is number of nodes, processes each node once
        # Space Complexity: O(w) where w is maximum width of tree (queue size)
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
        """Left view: leftmost node at each level"""
        # Time Complexity: O(n) where n is number of nodes, processes each node once
        # Space Complexity: O(w) where w is maximum width of tree (queue size)
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
        """Top view: nodes visible from top"""
        # Time Complexity: O(n) where n is number of nodes, processes each node once
        # Space Complexity: O(w) where w is maximum width of tree (queue size + dictionary)
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
        """
        Bottom view: nodes visible from bottom.
        For each horizontal distance (hd), the last node seen during level-order traversal is kept.
        """
        # Time Complexity: O(n) where n is number of nodes, processes each node once
        # Space Complexity: O(w) where w is maximum width of tree (queue size + dictionary)
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
        """
        Prints nodes at alternate levels starting from root (level 0, 2, 4, ...).
        """
        # Time Complexity: O(n) where n is number of nodes, processes each node once
        # Space Complexity: O(w) where w is maximum width of tree (queue size)
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
        """
        Maximum path sum in binary tree, returning sum and path values.
        """
        # Time Complexity: O(n) where n is number of nodes, visits each node once
        # Space Complexity: O(h + k) where h is height of tree, due to recursion stack, k is max length of best_path → could be up to n in worst case
        max_sum = float('-inf') # depits the negative infinity
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
            #here I am updating the nonlocal values , as this may a  possible ans
            if peak_sum > max_sum:
                max_sum = peak_sum
                peak_path = []
                if left_sum > 0:
                    peak_path.extend(left_path)
                peak_path.append(node.value)
                if right_sum > 0:
                    peak_path.extend(reversed(right_path))
                best_path = peak_path
        
            # Now logic of return came , can only return one side obv 
            # there is also a case where node is only +ive but as we are already making sure the our left_sum and right_sum become +ive it is okay.
            if left_sum > right_sum:
                return node.value + left_sum,  left_path + [node.value] 
            else:
                return node.value + right_sum, [node.value] + right_path
    
        dfs(self.root)
        return max_sum, best_path
    
    def display(self):
        """
        Directly print the tree level by level using a list as a queue.
        """
        # Time Complexity: O(n) where n is number of nodes, processes each node once
        # Space Complexity: O(w) where w is maximum width of tree (queue size)
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
    """Get integer input from user"""
    # Time Complexity: O(1) for each input operation
    # Space Complexity: O(1) for storing input value
    while True:
        try:
            value = input(input_instruction).strip() #strip for removing the leading and trailing whitespaces
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
    """Main program - level-wise tree builder with traversals"""
    # Time Complexity: O(n) for tree operations, dominated by traversal or build operations
    # Space Complexity: O(w) or O(h) depending on operation, where w is max width and h is height
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