"""Assignment 2: Trees for Treemap

=== CSC148 Winter 2019 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all sub-directories are:
Copyright (c) 2019 Bogdan Simion, David Liu, Diane Horton, Jacqueline Smith

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
from __future__ import annotations
import os
import math
from random import randint
from typing import List, Tuple, Optional


class TMTree:
    """A TreeMappableTree: a tree that is compatible with the treemap
    visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this asignment will involve you implementing new public
    *methods* for this interface.
    You should not add any new public methods other than those required by
    the client code.
    You can, however, freely add private methods as needed.

    === Public Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.

    === Private Attributes ===
    _colour:
        The RGB colour value of the root of this tree.
    _name:
        The root value of this tree, or None if this tree is empty.
    _subtrees:
        The subtrees of this tree.
    _parent_tree:
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.
    _expanded:
        Whether or not this tree is considered expanded for visualization.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.

    - _colour's elements are each in the range 0-255.

    - If _name is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.

    - if _parent_tree is not None, then self is in _parent_tree._subtrees

    - if _expanded is True, then _parent_tree._expanded is True
    - if _expanded is False, then _expanded is False for every tree
      in _subtrees
    - if _subtrees is empty, then _expanded is False
    """

    rect: Tuple[int, int, int, int]
    data_size: int
    _colour: Tuple[int, int, int]
    _name: Optional[str]
    _subtrees: List[TMTree]
    _parent_tree: Optional[TMTree]
    _expanded: bool

    def __init__(self, name: str, subtrees: List[TMTree],
                 data_size: int = 0) -> None:
        """Initialize a new TMTree with a random colour and the provided <name>.

        If <subtrees> is empty, use <data_size> to initialize this tree's
        data_size.

        If <subtrees> is not empty, ignore the parameter <data_size>,
        and calculate this tree's data_size instead.

        Set this tree as the parent for each of its subtrees.

        Precondition: if <name> is None, then <subtrees> is empty.
        """
        self.rect = (0, 0, 0, 0)
        self._name = name
        self._subtrees = subtrees[:]
        self._parent_tree = None
        self._expanded = False

        # You will change this in Task 5
        # if len(self._subtrees) > 0:
        #     self._expanded = True
        # else:
        #     self._expanded = False

        # TODO: (Task 1) Complete this initializer by doing two things:
        # 1. Initialize self._colour and self.data_size, according to the
        # docstring.
        # 2. Set this tree as the parent for each of its subtrees.
        self._colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.data_size = 0
        if name is None or len(self._subtrees) == 0:
            self.data_size = data_size
        else:
            size = 0
            for subtree in self._subtrees:
                size += subtree.data_size
                subtree._parent_tree = self
            self.data_size = size

    def is_empty(self) -> bool:
        """Return True iff this tree is empty.
        """
        return self._name is None

    def update_rectangles(self, rect: Tuple[int, int, int, int]) -> None:
        """Update the rectangles in this tree and its descendents using the
        treemap algorithm to fill the area defined by pygame rectangle <rect>.
        """
        # TODO: (Task 2) Complete the body of this method.
        # Read the handout carefully to help get started identifying base cases,
        # then write the outline of a recursive step.
        #
        # Programming tip: use "tuple unpacking assignment" to easily extract
        # elements of a rectangle, as follows.
        # x, y, width, height = rect
        if self.data_size == 0: # self is an empty folder
            pass
        elif len(self._subtrees) == 0: # self is a file
            self.rect = rect
        else: # self is a folder
            x, y, width, height = rect
            self.rect = rect
            for subtree in self._subtrees:
                percent = subtree.data_size / self.data_size
                if width > height:
                    new_width = width * percent
                    subtree.update_rectangles((int(x), int(y), int(new_width),
                                               int(height)))
                    x += new_width
                else:
                    new_height = height * percent
                    subtree.update_rectangles((int(x), int(y), int(width),
                                               int(new_height)))
                    y += new_height

    def get_rectangles(self) -> List[Tuple[Tuple[int, int, int, int],
                                           Tuple[int, int, int]]]:
        """Return a list with tuples for every leaf in the displayed-tree
        rooted at this tree. Each tuple consists of a tuple that defines the
        appropriate pygame rectangle to display for a leaf, and the colour
        to fill it with.
        """
        # TODO: (Task 2) Complete the body of this method.
        if self.data_size == 0:
            return []
        elif len(self._subtrees) == 0 or not self._expanded:
            return [(self.rect, self._colour)]
        else:
            return_list = []
            for subtree in self._subtrees:
                if len(subtree._subtrees) == 0:
                    return_list.append((subtree.rect, subtree._colour))
                else:
                    return_list.extend(subtree.get_rectangles())
            return return_list

    def get_tree_at_position(self, pos: Tuple[int, int]) -> Optional[TMTree]:
        """Return the leaf in the displayed-tree rooted at this tree whose
        rectangle contains position <pos>, or None if <pos> is outside of this
        tree's rectangle.

        If <pos> is on the shared edge between two rectangles, return the
        tree represented by the rectangle that is closer to the origin.
        """
        # TODO: (Task 3) Complete the body of this method
        x, y = pos
        if (self.rect[0] > x or self.rect[0] + self.rect[2] < x) or\
                (self.rect[1] > y or self.rect[1] + self.rect[3] < y):
            # pos out of bound
            return None
        return_obj = self
        if not self._expanded:
            return return_obj
        elif len(self._subtrees) == 1:
            return self._subtrees[0]
        else:
            for index in range(len(self._subtrees)-1):
                sub1 = self._subtrees[index].get_tree_at_position(pos)
                sub2 = self._subtrees[index+1].get_tree_at_position(pos)
                if sub1 and not sub2:
                    return_obj = sub1
                elif not sub1 and sub2:
                    return_obj = sub2
                elif sub1 and sub2:
                    sub1_dis = math.sqrt((sub1.rect[0]-x)**2
                                         + (sub1.rect[1]-y)**2)
                    sub2_dis = math.sqrt((sub2.rect[0]-x)**2
                                         + (sub2.rect[1]-y)**2)
                    if sub1_dis > sub2_dis:
                        return_obj = sub2
                    else:
                        return_obj = sub1
            return return_obj

    def update_data_sizes(self) -> int:
        """Update the data_size for this tree and its subtrees, based on the
        size of their leaves, and return the new size.

        If this tree is a leaf, return its size unchanged.
        """
        # TODO: (Task 4) Complete the body of this method.
        if len(self._subtrees) == 0:
            return self.data_size
        else:
            size = 0
            for subtree in self._subtrees:
                size += subtree.update_data_sizes()
            self.data_size = size
            return size

    def move(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, move this
        tree to be the last subtree of <destination>. Otherwise, do nothing.
        """
        # TODO: (Task 4) Complete the body of this method.
        # after moving files into folder A within folder B then try to expand
        # A folder, the content in folder A will not be selectable.
        if len(self._subtrees) == 0 and len(destination._subtrees) > 0:
            self._parent_tree._subtrees.remove(self)
            self._parent_tree.update_data_sizes()
            self._parent_tree = destination
            destination._subtrees.append(self)
            destination.update_data_sizes()
            self._expanded = False

    def change_size(self, factor: float) -> None:
        """Change the value of this tree's data_size attribute by <factor>.

        Always round up the amount to change, so that it's an int, and
        some change is made.

        Do nothing if this tree is not a leaf.
        """
        # TODO: (Task 4) Complete the body of this method
        if len(self._subtrees) > 0:
            pass
        else:
            if factor < 0:
                self.data_size = self.data_size \
                                 - math.ceil(self.data_size * abs(factor))
            else:
                self.data_size = self.data_size +\
                                 math.ceil(self.data_size * factor)

    # TODO: (Task 5) Write the methods expand, expand_all, collapse, and
    # TODO: collapse_all, and add the displayed-tree functionality to the
    # TODO: methods from Tasks 2 and 3
    def expand(self) -> None:
        """
        Changing the _expanded attribute to True for the current TMTree
        object.
        """
        self._expanded = True

    def expand_all(self) -> None:
        """
        Changing the _expanded attribute to True for the current TMTree
        object as well as its subtrees.
        """
        self.expand()
        for subtree in self._subtrees:
            subtree.expand_all()

    def collapse(self) -> None:
        """
        Changing the _expanded attribute to False for the current TMTree
        object.
        """
        self._parent_tree._expanded = False

    def collapse_all(self) -> None:
        """
        Changing the _expanded attribute to False for the current TMTree
        object as well as its subtrees.
        """
        for subtree in self._subtrees:
            subtree._expanded = False
        self._expanded = False
        if self._parent_tree:
            self._parent_tree.collapse_all()

    # Methods for the string representation
    def get_path_string(self, final_node: bool = True) -> str:
        """Return a string representing the path containing this tree
        and its ancestors, using the separator for this tree between each
        tree's name. If <final_node>, then add the suffix for the tree.
        """
        if self._parent_tree is None:
            path_str = self._name
            if final_node:
                path_str += self.get_suffix()
            return path_str
        else:
            path_str = (self._parent_tree.get_path_string(False) +
                        self.get_separator() + self._name)
            if final_node or len(self._subtrees) == 0:
                path_str += self.get_suffix()
            return path_str

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        raise NotImplementedError

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        raise NotImplementedError


class FileSystemTree(TMTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _name attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/Diane/csc148/assignments'

    The data_size attribute for regular files is simply the size of the file,
    as reported by os.path.getsize.
    """

    def __init__(self, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.

        """
        # Remember that you should recursively go through the file system
        # and create new FileSystemTree objects for each file and folder
        # encountered.
        #
        # Also remember to make good use of the superclass constructor!
        # TODO: (Task 1) Implement the initializer
        if os.path.isfile(path) or len(os.listdir(path)) == 0:
            # this path directs to a file
            TMTree.__init__(self, os.path.basename(path), [],
                            os.path.getsize(path))
        else:  # this path directs to a folder
            subtrees = []
            total_size = 0
            for subtr in os.listdir(path):
                sub_path = os.path.join(path, subtr)
                if os.path.basename(sub_path) != '.DS_Store':
                    sub = FileSystemTree(sub_path)
                    total_size += sub.data_size
                    subtrees.append(sub)
                TMTree.__init__(self, os.path.basename(path), subtrees,
                                total_size)

    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return os.sep

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """
        if len(self._subtrees) == 0:
            return ' (file)'
        else:
            return ' (folder)'


if __name__ == '__main__':
    '''task 1 tests'''
    # temp = FileSystemTree('/Users/yehuang/Desktop/csc148/assignments/a2//
    # example-directory/workshop/prep')
    # for s in temp._subtrees:
    #     print(s._name)
    #     print(s.get_suffix())
    #     print(s._data_size)
    # print(temp._data_size)

    '''task 2 tests'''
    # ssub1 = TMTree('ssub1', [], 2)
    # ssub2 = TMTree('ssub2', [], 8)
    # sub1 = TMTree('sub1', [ssub1, ssub2], 10)
    # sub2 = TMTree('sub2', [], 25)
    # sub3 = TMTree('sub3', [], 15)
    # temp = TMTree('root', [sub1, sub2, sub3], 50)
    # temp.update_rectangles((0, 0, 200, 100))
    # # update_rectangle test
    # print(temp.rect)
    # for s in temp._subtrees:
    #     print(s.rect)
    # print('sub1: ' + str(sub1.rect))
    # # get_rectangle test
    # print(temp.get_rectangles())

    '''task 3 tests'''
    # sub0 = TMTree('sub0', [], 10)
    # sub1 = TMTree('sub1', [], 10)
    # sub2 = TMTree('sub2', [], 20)
    # sub3 = TMTree('sub3', [], 10)
    # temp = TMTree('root', [sub0, sub1, sub2, sub3], 50)
    # temp.update_rectangles((0, 0, 200, 100))
    # loc = temp.get_tree_at_position((0, 0))
    # print(loc._name)

    '''task 4 tests'''
    # ssub1 = TMTree('ssub1', [], 2)
    # ssub2 = TMTree('ssub2', [], 8)
    # sub1 = TMTree('sub1', [ssub1, ssub2], 10)
    # sub2 = TMTree('sub2', [], 25)
    # sub3 = TMTree('sub3', [], 15)
    # temp = TMTree('root', [sub1, sub2, sub3], 50)
    # ssub1.move(temp)
    # print('sub1 subtrees: ' + str(sub1._subtrees))
    # print('sub1 data size: ' + str(sub1._data_size))
    # print('temp subtrees: ' + str(sub3._subtrees))
    # print('temp data size: ' + str(sub3._data_size))
    # print(temp.update_data_sizes())
    # sub1.change_size(1.00001)
    # print(sub1._data_size)
    # print(temp._data_size)

    '''task 5 tests'''
    # task 5's features have been tested in the treemap visulization :)

    '''sample test'''
    # EXAMPLE_PATH = os.path.join('example-directory', 'workshop')
    # tree = FileSystemTree(EXAMPLE_PATH)
    # _sort_subtrees(tree)
    #
    # tree.update_rectangles((0, 0, 200, 100))
    # rects = tree.get_rectangles()

    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'math', 'random', 'os', '__future__'
        ]
    })
