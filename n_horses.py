"""
Question: In a race with n horses, how many possible outcomes are there
if ties are allowed?

Solution: Consider the possible outcomes for a race with 1 horse, named A.
Horse A must finish; there is only one outcome, which we call [[A]].

Add a new horse, B. B can either finish before A, with A, or after A.
The solutions, then, are given as [[B], [A]], [[B, A]], and [[A], [B]].

Notice the size of these solutions. For example, [[B], [A]] is of size
2; there was a first place and a second place. [[B, A]] is of size 1;
there is only first place. 

Let us define the size of solution to be the number of unique finishing
positions there are; for example, [[A, B], [C]] has a 1st and 2nd place,
and is of size 2.

We are interested in how many solutions are added when a new horse is
introduced. Notice that when adding a new horse to a solution of size n,
there are n+1 places to put the new horse; it can tie with any of the 
positions (yielding a new solution of size n), it can go between any two 
positions (yielding solutions of size n+1), or it can beat or lose to every 
other position (yielding solutions of size n+1). We can say that a solution 
of size 1 yields 3 solutions, of sizes [2, 1, 2]. A solution of size 2 
yields 5 solutions, of sizes [3, 2, 3, 2, 3]. A solution of size n yields 
n+1 solutions, of sizes [n+1, n, n+1, n, n+1, n, ... n+1].

The code below simulates this, with each `Node` representing a solution of
size `name`.

Note: this game becomes very difficult to play with more than 9 or 10 horses.
"""


class Node:
    def __init__(self, name: int):
        self.name = name

    def spawn(self) -> list:
        """Create a list of new solutions (Nodes) from a given node

        Example: Node(2) -> [Node(2), Node(2), Node(3), Node(3), Node(3)]
        """
        out = list()
        for i in range(self.name):
            out.append(Node(self.name))
        for i in range(self.name + 1):
            out.append(Node(self.name + 1))
        return out


solutions = {}
solutions[1] = [Node(name=1)]

for i in range(2, 9):
    solutions[i] = []
    for element in solutions[i - 1]:
        solutions[i].extend(element.spawn())
    print(f"If there are {i} horses, there are {len(solutions[i])} possible solutions")
