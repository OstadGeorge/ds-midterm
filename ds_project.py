#!bin/python

"""
:title: data structure course midterm project
:author: Mohammad Ali Heydari
:date: 2-Dec-2020
"""


class CursorSpace:
    def __init__(self, cap=1000):
        self._cap = cap
        self._size = cap
        self._down = [None] * self._size
        self._next = [None] * self._size
        self._avail = 0
        self._heads = []

        for i in range(self._size - 1):
            self._next[i] = i + 1

    def add_head(self, idx):
        self._heads.append(idx)

    def allocate(self):
        if self._avail is None:
            raise Exception("out of space")
        idx = self._avail
        self._avail = self._next[idx]
        self._cap -= 1
        self._next[idx] = None
        self._down[idx] = None
        return idx

    def free(self, idx):
        if self._avail is None:
            self._avail = idx
            self._next[idx] = None
            self._down[idx] = None
        else:
            temp = self._avail
            self._avail = idx
            self._next[idx] = temp
            self._down[idx] = None
        self._cap += 1

    def garbage_collection(self, detail=False):
        mark = set()
        new_mark = set(self._heads)
        while len(new_mark) > 0:
            if detail:
                print(new_mark)
            mark = mark.union(new_mark)
            new_mark.clear()
            for i in range(self._size):
                if i in mark and self._next[i] is not None and self._next[i] not in mark:
                    new_mark.add(self._next[i])
                if i in mark and self._down[i] is not None and self._down[i] not in mark:
                    new_mark.add(self._down[i])
        cnt = 0
        for i in range(self._size):
            if i in mark:
                continue
            self.free(i)
            cnt += 1
        if detail:
            print("{} units of block can allocate :)))".format(cnt))

    def set_down(self, down_idx, idx):
        self._down[idx] = down_idx

    def get_down(self, idx):
        return self._down[idx]

    def set_next(self, next_idx, idx):
        self._next[idx] = next_idx

    def get_next(self, idx):
        return self._next[idx]

    def is_full(self):
        return self._cap == 0


class List:
    def __init__(self, space: CursorSpace):
        self._space = space
        self._head = space.allocate()
        self._space.add_head(self._head)

    def print(self, recursive=False):
        if recursive:
            self._print_recursive(self._head, 0)
            print()
        else:
            self._print_none_recursive()

    def _print_recursive(self, node, d):
        if self._space.get_down(node) is not None:
            print("(", end="")
            self._print_recursive(self._space.get_down(node), d + 1)
        if self._space.get_next(node) is None:
            if d != 0:
                print(")", end="")
        else:
            print("*", end="")
            self._print_recursive(self._space.get_next(node), d)

    def _print_none_recursive(self):
        node = [self._head, 0]
        ret = ""
        stk = [node]
        while len(stk):
            node = stk[-1]
            stk.pop(-1)
            if self._space.get_down(node[0]) is not None:
                ret += "("
                if self._space.get_next(node[0]) is not None:
                    stk.append([self._space.get_next(node[0]), node[1]])
                stk.append([self._space.get_down(node[0]), node[1] + 1])
            elif self._space.get_next(node[0]) is not None:
                ret += "*"
                stk.append([self._space.get_next(node[0]), node[1]])
            else:
                ret += ")"

        ret += ")"
        print(ret)

    def get_head(self):
        return self._head

    def delete_node(self, node):
        self._space.set_down(None, node)

    def make_child(self, node, lst):
        self._space.set_down(self._space.get_down(lst.get_head()), node)

    def build(self, expr, detail=False):
        self._build(self._head, expr, 0, detail)
        if detail:
            print("\n=======BUILD ENDED=======")

    def _build(self, par, expr, expr_idx, detail=False):
        while expr_idx < len(expr):
            if expr[expr_idx] == "*":
                if detail:
                    print("right", end=" ")
                new_node = self._space.allocate()
                self._space.set_next(new_node, par)
                expr_idx += 1
                par = new_node

            if expr[expr_idx] == "(":
                if detail:
                    print("down", end=" ")
                new_node = self._space.allocate()
                self._space.set_down(new_node, par)
                expr_idx = self._build(new_node, expr, expr_idx + 1, detail)

            elif expr[expr_idx] == ")":
                if detail:
                    print("up", end=" ")
                return expr_idx + 1


space = CursorSpace(cap=1000)
lst = List(space)

# First Command #
lst.build("((***)*)", detail=True)
lst.build("((***)****(*))", detail=True)
lst.build("(((((**))**))(*****(*)(*)))", detail=True)
lst.build("((((((((**((((***(****)))**)*)*****)))))))*)", detail=True)
print("\n")


# Second Command #
lst2 = List(space)
lst2.build("((*)*)", detail=False)

lst3 = List(space)
lst3.build("(**(*)*)", detail=False)

# Third Command #
lst2.make_child(space.get_down(lst2.get_head()), lst3)


# Third Command #
lst4 = List(space)
lst4.build("((**)*)")
lst4.delete_node(space.get_down(lst4.get_head()))

# Forth Command #
lst.build("((***)****(*))", detail=False)
print("## RECURSIVE PRINT ##")
lst.print(recursive=True)
print("## NON RECURSIVE PRINT ##")
lst.print(recursive=False)
print("\n")

# Fifth Command #
space.garbage_collection(detail=False)
space.garbage_collection(detail=True)
lst.delete_node(space.get_down(lst.get_head()))
print("\n")
space.garbage_collection(detail=True)
