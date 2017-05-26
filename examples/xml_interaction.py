import xml.etree.ElementTree as ET

my_xml = ET.ElementTree()
my_xml._setroot(ET.Element("data"))
with open("../reviews_csatucu.txt", "r", encoding="utf-8") as read_file:
    content = read_file.readlines()
    i = 0
    try:
        while True:
            name = ET.Element("name")
            name.text = content[i]
            i += 1
            url = ET.Element("url")
            url.text = content[i]
            i += 1
            text =  ET.Element("text")
            text.text = content[i]
            i += 1
            stars = ET.Element("stars")
            stars.text = content[i]
            i += 2
            new_el = ET.Element("review")
            new_el.append(name)
            new_el.append(url)
            new_el.append(text)
            new_el.append(stars)
            my_xml.getroot().append(new_el)
    except IndexError:
        pass

my_xml.write("reviews_csatucu.xml", encoding="utf-8")
