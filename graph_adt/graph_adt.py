from arrays import Array, DynamicArray


class Node:
    def __init__(self, name="Name Surname", user_id="Linked", items=list()):
        self.name = name
        self.id = user_id
        self.size = len(items)
        self.items = Array(self.size or 1)
        for index in range(self.size):
            self.items[index] = items[index]


class Friend:
    def __init__(self, name="Name Surname", user_id="ID"):
        self.name = name
        self.id = user_id
        self.friend_list = DynamicArray()

    def __eq__(self, other):
        return (self.name == other["name"]) and (self.id == other["id"])


class UsersList:
    def __init__(self, max_size):
        self.size = 0
        self.items = Array(max_size)

    def add(self, name, user_id):
        self.items[self.size] = Friend(name, user_id)
        self.size += 1

    def __contains__(self, item):
        for i in range(self.size):
            if self.items[i] == item:
                return self.items[i]
        return False

    @staticmethod
    def reads_from_file(file_name="../data/next_sec.txt"):

        with open(file_name, "r", encoding="utf-8") as source_file:
            content = source_file.readlines()
            length = len(content) // 2
            result = UsersList(length)
            for i in range(length):
                result.add(content[2 * i], content[2 * i + 1])
        return result


class Graph:
    def __init__(self, max_size):
        self.size = 0
        self.nodes = Array(max_size)

    def __setitem__(self, key, value):
        self.nodes[key] = value

    def __getitem__(self, item):
        return self.nodes[item]
a = UsersList.reads_from_file()
print(a.items[0].name)