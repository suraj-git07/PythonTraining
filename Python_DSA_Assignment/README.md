# 📂 Python_DSA_Assignment

## 🧾 Overview
This repository is part of a larger project containing multiple assignment folders for Data Structures and Algorithms coursework. It includes `Tress.py`, a Python implementation of a **binary tree data structure**, to demonstrate proficiency in tree-based algorithms and interactive program design.

---

## 📄 Contents

### `Tress.py`
Implements a binary tree with:

- **`TreeNode` Class**  
  Defines a node with:
  - `value`: The node's data (integer).
  - `left`: Reference to the left child node.
  - `right`: Reference to the right child node.

- **`BinaryTree` Class**  
  Provides methods for:
  - **Level-wise tree construction**: Builds the tree using a queue-based approach.
  - **Traversals**: Inorder (Left-Root-Right), Preorder (Root-Left-Right), Postorder (Left-Right-Root).
  - **Views**:
    - Right view: Rightmost node at each level.
    - Left view: Leftmost node at each level.
    - Top view: Nodes visible from above.
    - Bottom view: Nodes visible from below.
    - Alternate level view: Nodes at even levels (0, 2, 4, ...).
  - **Maximum Path Sum**: Calculates the maximum sum of any path in the tree, returning the sum and path nodes.

- **Interactive Menu-Driven Interface**  
  Allows users to:
  - Build the tree by inputting node values.
  - Display the tree structure level by level.
  - View all traversals and views.
  - Compute the maximum path sum.
  - Exit the program.

- **Input Validation**  
  - Accepts integers in the range `[-10000, 10000]`.
  - Supports special keywords: `'null'` for empty nodes, `'q'` to quit input.
  - Includes robust error handling for invalid inputs.

- **Complexity Analysis**  
  - Each method includes comments detailing time and space complexity (e.g., O(n) time for traversals, O(w) space for queue-based methods, where `n` is the number of nodes and `w` is the maximum tree width).

---