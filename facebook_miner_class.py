from selenium import webdriver
import time
from pyvirtualdisplay import Display


class WebGetter:
    def __init__(self):
        self.browser = webdriver.Firefox()

    def login_facebook(self, login=None, password=None):
        if login is None or password is None:
            with open(".login.txt", "r") as file_login:
                login = file_login.readline().strip()
                password = file_login.readline().strip()
        self.browser.get('https://www.facebook.com')

        login_css = self.browser.find_element_by_id('email')
        password_css = self.browser.find_element_by_id('pass')
        button = self.browser.find_element_by_id('u_0_q')

        login_css.send_keys(login)
        password_css.send_keys(password)
        button.click()
        time.sleep(3)
        print("Current_url %s" % self.browser.current_url)
        print("Logged in...")

    def friends_scrapper(self, pg_id):
        url = "%s/friends" % self.link_editor(pg_id)
        self.browser.get(url)
        time.sleep(1.5)
        while len(self.browser.find_elements_by_css_selector("img._359.img")) == 1:
            # Scroll down to bottom
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("Scrolled to the bottom...")
        blocks = self.browser.find_elements_by_xpath("//div[@data-testid='friend_list_item']")
        ids_list = list()
        for block in blocks:
            try:
                link = block.find_element_by_css_selector('div.fsl.fwb.fcb a')
                name = link.text
                link = link.get_attribute("href")
            except Exception as e:
                self.add_error(e)
                name = ""
                link = ""
            ids_list.append(name)
            ids_list.append(link)
        return ids_list

    @staticmethod
    def link_editor(line):
        if "profile.php?id=" in line:
            line = "https://www.facebook.com/" + line[40:line.find("&") + 1]
        else:
            line = line[:line.find("?fref=") + 1]
        return line

    @staticmethod
    def add_error(content):
        with open("error.log", "w") as error_log_file:
            error_time = "Error time :: %s" % (time.strftime("%a, %d %b %Y %H:%M:%S",
                                                             time.localtime()))
            error_log_file.write("\n%s\n%s\n" % (error_time, content))

    def close_browser(self):
        self.browser.quit()

    def write_file(self, content, file_name="result.txt"):
        with open(file_name, "w") as file_write:
            for sent in content:
                file_write.write("%s\n" % sent)

display = Display(visible=0, size=(800, 600))
display.start()
inst = WebGetter()
time_ = time.time()
inst.login_facebook()
try:
    with open("./data/interested.txt", "r", encoding="utf-8") as file_read:
        cont = file_read.readlines()
        for i in range(len(cont) // 2):
            print("Current profile index is %s" % str(i))
            inst.write_file(inst.friends_scrapper(cont[i * 2 + 1].strip()), file_name="./db_interested/%s.txt" % cont[i * 2].strip())
finally:
    inst.close_browser()
    display.stop()
print(time.time() - time_)
