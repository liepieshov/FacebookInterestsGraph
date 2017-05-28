from os import listdir
from os.path import isfile, join


onlyfiles = [f for f in listdir("./db") if isfile(join("./db", f))]


def open_file(file_name):
    cont = list()
    with open(file_name, "r", encoding="utf-8") as file:
        pre_content = file.readlines()
    for index in range(len(pre_content) // 2):
        user_name = pre_content[index * 2].strip()
        user_link = pre_content[index * 2 + 1].strip()
        if user_link and user_name:
            cont.append((user_name, user_link))
    return cont


file_names = open_file("./data/will_go_lst.txt")
# print(len(file_names))
counter = 0
with open("./data/ready_data.txt", "w", encoding="utf-8") as file_w:
    for u_name, u_link in file_names:
        if u_name+".txt" in onlyfiles:
            file_w.write("%s\n%s\n" % (u_name, u_link))
            counter += 1

# print(len(file_names))
print(counter)
