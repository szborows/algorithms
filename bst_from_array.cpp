#include <algorithm>
#include <initializer_list>
#include <iostream>
#include <memory>
#include <vector>

#include <gtest/gtest.h>

using namespace std;


template <typename T> struct Node {
    explicit Node(T const& data) : data(data) { }
    unique_ptr<Node<T>> left, right;
    T data;
};

unique_ptr<Node<int>> buildTreeImpl(vector<int> const& array, int start, int end) {
    if (end - start < 1) {
      return nullptr;
    }

    int mid = start + ((end - start) / 2);
    unique_ptr<Node<int>> node = unique_ptr<Node<int>>(new Node<int>(array[mid]));
    node->left = buildTreeImpl(array, start, mid - 1);
    node->right = buildTreeImpl(array, mid + 1, end);

    return node;
}

unique_ptr<Node<int>> buildTree(vector<int> & array) {
    sort(array.begin(), array.end());
    array.erase(unique(array.begin(), array.end()), array.end());
    return buildTreeImpl(array, 0, array.size() - 1);
}

template <typename T> bool testBst(Node<T> * node, T low = numeric_limits<T>::min(), T high = numeric_limits<T>::max()) {
    if (nullptr == node) return true;
    return (node->data > low && node->data < high)
        ? testBst(node->left.get(), low, node->data) && testBst(node->right.get(), node->data, high)
        : false;
}

template <typename T> int height(Node<T> * node) {
    return node ? 1 + max(height(node->left.get()), height(node->right.get())) : 0;
}

template <typename T> bool testBalanced(Node<T> * node) {
    if (nullptr == node) return true;
    return (abs(height(node->left.get()) - height(node->right.get())) <= 1)
           && testBalanced(node->left.get())
           && testBalanced(node->right.get());
}

void testArray(vector<int> & v) {
    unique_ptr<Node<int>> t = buildTree(v);
    ASSERT_TRUE(testBst(t.get())) << "Not a BST!";
    ASSERT_TRUE(testBalanced(t.get())) << "Not balanced!";
}

void testArrays(initializer_list<vector<int>> const& arrays) {
    for (vector<int> const& array: arrays) {
        vector<int> v = array;
        testArray(v);
    }
}

TEST(BstFromArray, FixedSamples) {
    testArrays({
            {1},
            {1, 0},
            {1, 2, 3},
            {1, 2, 10, 4},
            {10, 0, 8, 2, 1},
            {10, 0, 8, 2, 1, 77},
            {10, 8, 6, 4, 2, 0, 1},
            {10, 8, 6, 4, 2, 0, 1, 9},
            {10, 8, 6, 4, 2, 0, 1, 9, 7},
            {10, 9, 8, 7, 6, 5, 4, 3, 2, 1},
            {10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 11},
            {10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 11, 12},
            {10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 11, 12, 13},
            {10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 11, 12, 13, 14},
            {10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 11, 12, 13, 14, 15},
            {10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 11, 12, 13, 14, 15, 16},
            {10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 11, 12, 13, 14, 15, 16, 17},
            {10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 11, 12, 13, 14, 15, 16, 17, 18},
            {10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 11, 12, 13, 14, 15, 16, 17, 18, 19},
            {10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20},
    });
}

TEST(BstFromArray, BigAndSorted) {
    vector<int> v(10000);
    iota(v.begin(), v.end(), 0);
    testArray(v);
}

TEST(BstFromArray, Random) {
    vector<int> v;
    int const rounds = 5000;
    for (int i = 0; i < rounds; ++i) {
        v = vector<int>(10000);
        generate(v.begin(), v.end(), rand);
        testArray(v);
    }

}

int main(int ac, char ** av) {
    ::testing::InitGoogleTest(&ac, av);
    return RUN_ALL_TESTS();
}


/// Optional code to dump tree in DOT format.
template <typename T> void dumpNode(Node<T> * node) {
    cout << "\t" << node->data << endl;

    if (node->left) {
        cout << "\t" << node->data << " -> " << node->left->data << endl;
        dumpNode(node->left.get());
    }
    if (node->right) {
        cout << "\t" << node->data << " -> " << node->right->data << endl;
        dumpNode(node->right.get());
    }
}

template <typename T> void dumpTree(Node<T> * root) {
    cout << "digraph T {" << endl;
    dumpNode(root);
    cout << "}" << endl;
}
