from arrays import Array, DynamicArray


class Edge:
    """
    A simple Edge for Graph of class GraphNetworkADT
    """
    def __init__(self, name="Name Surname", user_id="ID"):
        """
        Initialising class with DynamicArray friends_list; strings name and id
        :param name: str, user name
        :param user_id: str, link to the user's page
        """
        self.name = name
        self.id = user_id
        self.friends_list = DynamicArray()

    def __eq__(self, other):
        """
        Checks the equality of self and other
        :param other: dict of type: {"name": "text", "id": "text"}
        :return: True if the names and the ids are in common, otherwise: False
        """
        return (self.name == other["name"]) and (self.id == other["id"])


class GraphNetworkADT:
    """
    Class representing connections between users of one group in FaceBook
    """
    def __init__(self, max_size):
        """
        Initialising class with int size=0 and array edges_list of size max_size
        :param max_size: the size of edges_list
        """
        self.size = 0
        self.edges_list = Array(max_size)

    def add(self, name, user_id):
        """
        Adds new Edge to the edges_list by name and link
        :param name: str, name of the user
        :param user_id: str, link to the user's page
        :return: None
        """
        self.edges_list[self.size] = Edge(name, user_id)
        self.size += 1

    def __contains__(self, item):
        """
        Checks if the item is in the edges_list

        :param item: dictionary of type {"name": "text", "id": "text"}
        :return: The element(instance of Edge) if the element is in the list, otherwise: None
        """
        # Parsing the edges_list by index
        for index in range(self.size):
            if self.edges_list[index] == item:
                return self.edges_list[index]

    @staticmethod
    def create_instance(data_file="../data/next_sec.txt"):
        """
        Creates the instance of GraphNetworkADT with data of Edges from data_file

        :param data_file: the name of the file
        :return: instance of GraphNetworkADT
        """
        with open(data_file, "r", encoding="utf-8") as source_file:
            # Reading all lines from the file
            content = source_file.readlines()

            # Creating new instance with half size array
            length_data = len(content) // 2
            inst = GraphNetworkADT(length_data)
            # Filling the array with the data from opened file
            for row in range(length_data):
                inst.add(content[2 * row], content[2 * row + 1])

        return inst

    def manage_friends(self):
        """
        Reading from files names by Edge.name of edges_list
        and filling the arrays of each user's nodes
        :return: None
        """
        for index in range(self.size):
            # getting the name of single user
            name = self.edges_list[index].name
            # opening the data file of this user
            with open("%s.txt" % name, "r", encoding="utf-8") as file_read:
                # reading the whole content of the file as a list of strings
                cont = file_read.readlines()
                # parsing content of the file by index
                for edge_index in range(len(cont) // 2):
                    # getting the name of the user
                    u_name = cont[edge_index * 2].strip()
                    # getting the link to the user's page
                    u_id = cont[edge_index * 2 + 1].strip()
                    # putting link and name to the dict
                    u_dict = {
                        "name": u_name,
                        "id": u_id
                    }
                    # saving connection between users
                    user_instance = u_dict in self
                    if user_instance:
                        self.edges_list[index].friends_list.append(user_instance)


class Graph:
    def __init__(self):
        self.nodes = DynamicArray()

    def __getitem__(self, item):
        return self.nodes[item]
