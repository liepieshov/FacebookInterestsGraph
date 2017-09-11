import json

file_name = "data.json"
with open(file_name, "r", encoding="utf-8") as file_read:
    data = json.loads(file_read.read(), encoding="utf-8")
# print(data["nodes"][0])
# 25781.25
y = -25000
#print(data["nodes"][0])
#print(data["edges"])
z = 0
y2 = -25000
counter = 0
counter2 = 0
for index in range(len(data["nodes"])):
    if "Mode" in data["nodes"][index]["attributes"]\
            and data["nodes"][index]["attributes"]["Mode"] == '1':
        if data["nodes"][index]["y"] < z:
            z = data["nodes"][index]["y"]
            print(z)
        data["nodes"][index]["x"] = 5000000
        #print("OK")
        radius = data["nodes"][index]["size"] * 1000
        y += max(radius + 10, 150)
        data["nodes"][index]["y"] = y
        y += max(radius + 10, 150)
        counter2 += 1
    elif "Mode" in data["nodes"][index]["attributes"]\
            and data["nodes"][index]["attributes"]["Mode"] == '0':
        # print(data["nodes"][index]["y"])
        data["nodes"][index]["x"] = 0
        # print("OK")
        radius = data["nodes"][index]["size"] * 1000
        y2 += max(radius + 10, 150)
        data["nodes"][index]["y"] = y
        y2 += max(radius + 10, 150)
        counter += 1
z3 = -25000
zm = -25000

for index in range(len(data["nodes"])):
    if "Mode" in data["nodes"][index]["attributes"]\
            and data["nodes"][index]["attributes"]["Mode"] == '0':
        # print(data["nodes"][index]["y"])
        data["nodes"][index]["x"] = y // 2
        data["nodes"][index]["y"] = zm
        zm += y // counter

    else:
        z3 += y // counter2
        data["nodes"][index]["y"] = z3
        z3 += y // counter2


file_name2 = "third_chart.json"
with open(file_name2, "w", encoding="utf-8") as file_w:
    json.dump(data, file_w, ensure_ascii=False)
