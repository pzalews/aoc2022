
from __future__ import annotations

import argparse
from copy import deepcopy
import os.path

import pytest
from collections import deque
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Node:
    data = None
    next = None
    previous = None
    moved = False

    def __init__(self, data):
        self.data = data
        self.next = None
        self.previous = None

    def __repr__(self):
        return str(self.data)


class LinkedList:
    # head
    def __repr__(self):
        node = self.head
        nodes = []
        if node is None:
            return ""
        nodes.append(str(node.data))
        node = node.next
        while node is not None and node is not self.head:
            nodes.append(str(node.data))
            node = node.next
        nodes.append("None")
        return " -> ".join(nodes)

    def get_list(self):
        node = self.head
        nodes = []
        if node is None:
            return []
        nodes.append(node)
        node = node.next
        while node is not None and node is not self.head:
            nodes.append(node)
            node = node.next
        return nodes

    def __init__(self, nodes=None):
        self.head = None
        if nodes is not None:
            node = Node(data=nodes.pop(0))
            self.head = node
            for elem in nodes:
                node.next = Node(data=elem)
                node.next.previous = node
                node = node.next
            node.next = self.head
            self.head.previous = node

    def head_to_zero(self):
        for n in self.get_list():
            if n.data == 0:
                self.head = n
                break

    def __iter__(self):
        node = self.head
        while node is not None and node.previous != self.head:
            yield node
            node = node.next

    # def add_last(self, node):
    #     if self.head is None:
    #         self.head = node
    #         return
    #     for current_node in self:
    #         pass
    #     current_node.next = node
    #     node.previous = current_node

    def move(self, node):
        if self.head is None:
            raise Exception("Empty")
        if node.data > 0:
            for _ in range(0, node.data):
                if self.head == node:
                    self.head = node.previous
                np = node.previous
                nn = node.next
                nnn = nn.next
                np.next = nn
                nn.previous = np
                nn.next = node
                node.previous = nn
                node.next = nnn
                nnn.previous = node
        if node.data < 0:
            for _ in range(0, node.data, -1):
                if self.head == node:
                    self.head = node.next
                nn = node.next
                np = node.previous
                npp = np.previous
                npp.next = node
                node.previous = npp
                node.next = np
                np.previous = node
                np.next = nn
                nn.previous = np

    def return_indexes(self, arr):
        m = max(arr)
        odp = []
        n = self.head
        for a in range(0, m+2):
            if a in arr and n is not None:
                odp.append(n.data)
            n = n.next
        return odp
 

def compute(s: str) -> int:

    orginal = s.splitlines()
    orginal = [int(x) for x in orginal]
    # print(orginal)
    ll = LinkedList(orginal)
    # print(ll)
    for node in ll.get_list():
        ll.move(node)
    ll.head_to_zero()
    print(ll)
    k = ll.return_indexes([1000, 2000, 3000])
    print(k)
    return sum(k)


INPUT_S = '''\
1
2
-3
3
-2
0
4
'''
EXPECTED = 4+-3+2


@ pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),


)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def testLL():
    ll = LinkedList([0, 1, 2, 3])
    a = 0
    for n in ll:
        assert n.data == a
        a += 1
    node = ll.head
    ll.move(node)
    odp = [0, 1, 2, 3]
    a = 0
    for n in ll:
        assert n.data == odp[a]
        a += 1
    ll.move(node.next)
    odp = [0, 2, 1, 3]
    a = 0
    for n in ll:
        assert n.data == odp[a]
        a += 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
