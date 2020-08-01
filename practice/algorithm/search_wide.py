from collections import deque

graph = {}
graph["you"] = ["alice", "bob", "claire"]
graph["bob"] = ["anuj", "peggy"]
graph["alice"] = ["peggy"]
graph["claire"] = ["thom", "jonny"]
graph["anuj"] = []
graph["peggy"] = []
graph["thom"] = []
graph["jonny"] = []


def search(name):
    # 创建一个队列
    search_queue = deque()
    # 将你的邻居加入这个搜索队列当中
    search_queue += graph["you"]
    searched = []

    while search_queue:
        person = search_queue.popleft() #取出第一个人
        if not person in searched:
            if person_is_seller(person): #是否为芒果销售商
                print(person + " is a seller!")
                return True

            else:
                search_queue += graph[person] #不是，将这个人的朋友加入队列
                searched.append(person)

    return False #说明没有这个人

def person_is_seller(name):
    return name[-1] == 'm'

search("you")