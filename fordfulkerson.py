class Graph:
    def __init__(self):
        self.graph = []
        self.ROW = 0

    def add_edge(self, u, v, capacity):
        max_node = max(u, v)
        if max_node >= self.ROW:
            self.ROW = max_node + 1
            for i in range(len(self.graph)):
                self.graph[i] += [0] * (self.ROW - len(self.graph[i]))
            self.graph += [[0] * self.ROW] * (self.ROW - len(self.graph))

        self.graph[u][v] = capacity

    def BFS(self, s, t, parent):
        visited = [False] * self.ROW
        queue = []
        queue.append(s)
        visited[s] = True

        while queue:
            u = queue.pop(0)
            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u

        return True if visited[t] else False

    def ford_fulkerson(self, source, sink):
        parent = [-1] * self.ROW
        max_flow = 0

        while self.BFS(source, sink, parent):
            path_flow = float("inf")
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            max_flow += path_flow

            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

        return max_flow

    def min_cut(self, source, sink):
        visited = [False] * self.ROW
        self.DFS(source, visited)
        min_cut = []

        for i in range(self.ROW):
            for j in range(self.ROW):
                if visited[i] and not visited[j] and self.graph[i][j]:
                    min_cut.append((i, j))

        return min_cut

    def DFS(self, source, visited):
        visited[source] = True
        for i in range(self.ROW):
            if self.graph[source][i] and not visited[i]:
                self.DFS(i, visited)

    def print_min_cut_graph(self, min_cut):
        min_cut_graph = [[0] * self.ROW for _ in range(self.ROW)]
        for u, v in min_cut:
            min_cut_graph[u][v] = self.graph[u][v]

        print("Minimum Cut Graph:")
        for row in min_cut_graph:
            print(row)


g = Graph()

# Taking input for the graph
while True:
    edge_input = input("Enter edge and capacity (u v capacity), or type 'done' to finish: ")
    if edge_input.lower() == 'done':
        break
    try:
        u, v, capacity = map(int, edge_input.split())
        g.add_edge(u, v, capacity)
    except ValueError:
        print("Invalid input format. Please enter integers for u, v, and capacity.")

source = int(input("Enter source node: "))
sink = int(input("Enter sink node: "))

max_flow = g.ford_fulkerson(source, sink)
print("Max Flow:", max_flow)

min_cut = g.min_cut(source, sink)
g.print_min_cut_graph(min_cut)
