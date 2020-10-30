class Vertex:
    def __init__(self, name=None):
        self.name = name  # name can be any type, is not required
        self.neighbors = []  # list of Vertices

    def __repr__(self):
        return str(self.name)


class Graph:
    """Class to represent a graph. Containts Node objects, and dict
    of connections between nodes
    """

    def __init__(self, vertices: list, edges: list, directed: bool = False, name=None, start=None):
        """Args:
            name: An optional name for the graph
            vertices: A list of names for the vertices to create
            edges: a list of edges to draw, given as a list of tuples of names
                Example: [(v1, v2), (v2, v3)...]
            start: The name of a starting vertex for traversals and searches.
                If none specified, use the first vertex in the list.
        """
        self.name = name
        self.vertices = {}  # {name : Vertex} pairs
        self.directed = directed

        # Populate vertices
        for name in vertices:
            self.vertices[name] = Vertex(name=name)

        # Create edges
        for edge in edges:
            self.vertices[edge[0]].neighbors.append(self.vertices[edge[1]])
            if not directed:
                self.vertices[edge[1]].neighbors.append(self.vertices[edge[0]])

        # Designate a default starting node for searches
        self.start = self.vertices[start] if start else self.vertices[vertices[0]]

    def find_euler_path(self, show: bool = True, debug: bool = False) -> bool:
        """An implementation of Fleury's Algorithm to find the Euler path.

        References used:
            https://www.geeksforgeeks.org/fleurys-algorithm-for-printing-eulerian-path/
            (note, this page includes a python implementation; I did not look at it)
        """
        # If the graph is directed this won't work...
        if self.directed:
            return False  # It isn't necessarily impossible, but this method won't work

        # Check if there is one at all
        odd_degrees: int = 0
        odd_vertex = None
        for vertex in self.vertices.values():
            if debug: print(f"{vertex} has {len(vertex.neighbors)} neighbors")
            if len(vertex.neighbors) % 2 == 1: 
                odd_degrees += 1
                odd_vertex = vertex
        
        if debug: print(f"This graph has {odd_degrees} vertices with odd degree")
        
        if not (odd_degrees == 0 or odd_degrees == 2):  # No path exists
            if show: print("No path exists")
            return False

        if not show:  # A path exists, but we don't want to see it
            return True
        
        # Helper functions!
        def is_bridge(v: Vertex) -> bool:
            """Helper to determine if the edge to a vertex is the only edge to that vertex"""
            return len(v.neighbors) == 1
        
        def travel(start: Vertex) -> Vertex:
            """Travel from one vertex to another, removing the edge connecting them.

            Return:
                Vertex: The vertex we will travel to
            """
            end = None
            for neighbor in start.neighbors:
                if (not end) and (not is_bridge(neighbor)):
                    if debug: 
                        print(f"Traveling from {start} to {neighbor} ...")
                    end = neighbor

            # There is only one edge left out of start; we must follow it
            if not end:
                end = start.neighbors[0]

            start.neighbors.remove(end)
            end.neighbors.remove(start)
            return end
            
        # Find the path
        curr: Vertex = odd_vertex if odd_vertex else self.start
        path = ""
        while len(curr.neighbors) > 0:
            path += f"({curr.name} -> "
            curr = travel(curr)
            path += f"{curr.name}), "

        path += "end"
        print(path)

        return True

            
    def __repr__(self) -> str:
        out = "*********************************************\n"
        out += f"Graph name: {self.name}\n"
        for vertex in self.vertices.values():
            out += f"Vertex: {vertex.name}; Neighbors: ["
            for neighbor in vertex.neighbors:
                out += f"{neighbor.name}, "
            out += "]\n"

        out += "*********************************************"
        return out


if __name__ == "__main__":
    g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (2, 3)], directed=False)
    print(g)
    g.find_euler_path()

    h = Graph(
        name="K5",
        vertices=[1, 2, 3, 4, 5], 
        edges=[(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)], 
        directed=False
        )
    print(h)
    h.find_euler_path()

    # Demo that this works for multigraphs as well
    i = Graph(
        name="Konigsburg", 
        vertices=[1, 2, 3, 4], 
        edges=[(1, 2), (1, 2), (1, 3), (1, 3), (1, 4), (2, 4), (3, 4)], 
        directed=False
        )
    print(i)
    i.find_euler_path()
