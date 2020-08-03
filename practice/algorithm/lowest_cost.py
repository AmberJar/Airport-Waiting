graph = {}
graph["you"] = {"alice", "bob", "claire"}

graph["start"] = {}
graph["start"]["a"] = 6
graph["start"]["b"] = 2

print(graph["start"].keys())
print(graph["start"]["a"])
print(graph["start"]["b"])

graph["a"] = {}
graph["a"]["fin"] = 1
graph["b"] = {}
graph["b"]["a"] = 3
graph["b"]["fin"] = 5
graph["fin"] = {}

infinity = float("inf")
costs = {}
costs["a"] = 6
costs["b"] = 2
costs["fin"] = infinity

parents = {}
parents["a"] = "start"
parents["b"] = "start"
parents["fin"] = None

processed = []

def find_lowest_cost_node(costs):
    lowest_cost = float("inf")
    lowest_cost_node = None

    for node in costs:   #便利所有节点
        cost = costs(node)
        if cost < lowest_cost and node not in processed: #如果开销更低且未处理过
            lowest_cost = cost
            lowest_cost_node = node

    return lowest_cost_node


node = find_lowest_cost_node(costs) #再未处理的节点中找出开销最小的节点

while node is not None:    #处理所有节点后结束
    cost = costs[node]
    neighbors = graph[node]
    for n in neighbors.keys(): #遍历当前节点的邻居
        new_cost = cost + neighbors[n]
        if cost[n] > new_cost:  #如果经当前节点前往该邻居更近
            cost[n] = new_cost     #就前往该邻居
            parents[n] = node   #同时将该邻居的父节点设置为当前节点

    processed.append(node)      #将当前节点标记为已处理
    node = find_lowest_cost_node(costs)     #找出接下来要处理的节点并循环