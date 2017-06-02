from .arrays import Array, DynamicArray


class Node:
    """
    A simple Node (representing a single connection between two users)
    for Graph of class GraphNetworkADT
    """
    def __init__(self, *elements):
        """
        Taking two arguments from elemnts and saves it into items Array
        :param elements: instances of Edge class
        """
        self.items = Array(2)
        self.items[0] = elements[0]
        self.items[1] = elements[1]

    def __eq__(self, other):
        """
        Checks the equality of Nodes
        :param other: instance of class Node or Tuple or List of instances of class Edge
        :return: return True if other Node is equal to this Node
        """
        if isinstance(other, Node):
            if (self.items[0] == other.items[0]
                and self.items[1] == other.items[1])\
                or (self.items[1] == other.items[0]
                    and self.items[0] == other.items[1]):
                return True
            return False
        else:
            if (self.items[0] == other[0]
                and self.items[1] == other[1])\
                or (self.items[1] == other[0]
                    and self.items[0] == other[1]):
                return True
            return False


class Edge:
    """
    A simple Edge (representing a single user) for Graph of class GraphNetworkADT
    """
    def __init__(self, name="Name Surname", user_id="ID"):
        """
        Initialising class with strings name and id
        :param name: str, user name
        :param user_id: str, link to the user's page
        """
        self.name = name
        self.id = user_id
        # self.friends_list = DynamicArray()

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
        Initialising class with int size=0; 
        array edges_list of size max_size;
        dynamic array nodes_list
        :param max_size: the size of edges_list
        """
        self.size = 0
        self.edges_list = Array(max_size)
        self.nodes_list = DynamicArray()

    def add_node(self, name, user_id):
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
        if isinstance(item, Node):
            for index in range(len(self.nodes_list)):
                if self.nodes_list[index] == item:
                    return True
        else:
            for index in range(self.size):
                if self.edges_list[index] == item:
                    # Returning the instance of class Edge
                    return True
        return False

    @staticmethod
    def create_instance(data_file="../data/will_go_lst.txt"):
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
                u_name = content[2 * row].strip()
                u_url = content[2 * row + 1].strip()
                if u_name and u_url:
                    inst.add_node(u_name, u_url)

        return inst

    def manage_friends(self):
        """
        Reading from files names by Edge.name of edges_list
        and filling the arrays of each user's nodes
        :return: None
        """
        c = 0
        for index in range(self.size):
            c += 1
            print(c)
            # getting the instance of single user
            inst = self.edges_list[index]
            # opening the data file of this user
            with open("./db/%s.txt" % inst.name, "r", encoding="utf-8") as file_read:
                # reading the whole content of the file as a list of strings
                cont = file_read.readlines()
                # parsing content of the file by index
                for edge_index in range(len(cont) // 2):
                    # getting the name of the user
                    u_name = cont[edge_index * 2].strip()
                    # getting the link to the user's page
                    u_id = GraphNetworkADT.link_editor(cont[edge_index * 2 + 1].strip())
                    # putting link and name to the dict
                    u_dict = {
                        "name": u_name,
                        "id": u_id
                    }
                    # saving connection between users as a Node in the node_list
                    if u_dict in self:
                        user_instance = self.find_edge(u_dict)
                        self.nodes_list.append(Node(user_instance, inst))

    def find_edge(self, item):
        for index in range(len(self.edges_list)):
            if self.edges_list[index] == item:
                return self.edges_list[index]
        return False

    @staticmethod
    def link_editor(line):
        if "profile.php?id=" in line:
            line = "https://www.facebook.com/" + line[40:line.find("&") + 1]
        else:
            line = line[:line.find("?fref=") + 1]
        return line

    def gephi_write(self, files={"nodes": "nodes.csv", "edges": "edges.csv"}):
        """
        Writes to csv files in gephi format
        :param files: the dictionary of the file-names
        :return: None
        """
        with open(files["edges"], "w", encoding="utf-8") as file:
            file.write("ID,Label,Urls\n")
            for index in range(self.size):
                file.write("%s,%s,%s\n" % (
                    id(self.edges_list[index]),
                    self.edges_list[index].name,
                    self.edges_list[index].id
                ))
        with open(files["nodes"], "w", encoding="utf-8") as file:
            file.write("Source,Target\n")
            for index in range(len(self.nodes_list)):
                file.write("%s,%s\n" % (
                    id(self.nodes_list[index].items[0]),
                    id(self.nodes_list[index].items[1])
                ))
