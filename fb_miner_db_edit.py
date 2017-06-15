from selenium import webdriver
import time
from pyvirtualdisplay import Display
from facebook_network_graph.facebook_network_graph import NetworkGraph
import sys


class WebGetter:
    """
    Class that helps to scrap the data from facebook
    """
    display = Display(visible=0, size=(800, 600))

    def __init__(self, db_file_name="wgdb.db", clear=True):
        """Creates the new FireFox session and connects to the database.
        Depending on clear arg could clear the database."""
        self.browser = webdriver.Firefox()
        self.db = NetworkGraph(db_file_name)
        if clear:
            self.db.clear()

    def login_facebook(self, login=None, password=None):
        """
        Performs the login event to facebook
        """
        if login is None or password is None:
            with open(".login.txt", "r") as file_login:
                login = file_login.readline().strip()
                password = file_login.readline().strip()
        self.browser.get('https://www.facebook.com')

        login_css = self.browser.find_element_by_id('email')
        password_css = self.browser.find_element_by_id('pass')
        button = self.browser.find_element_by_id('login_form')

        login_css.send_keys(login)
        password_css.send_keys(password)
        button.submit()
        time.sleep(3)
        print("Current_url %s" % self.browser.current_url)
        print("Logged in...")

    def friends_scrapper(self, name, url):
        """Scrapes the friends data from the page named by name and situated
        by url on facebook and writes it to database"""
        pg_id = self.link_editor(url)
        name = name.strip()

        user = self.db.add_node(name=name, facebook_id=pg_id)
        try:
            for uname, uid in self._friends_scrapper(pg_id):
                new_user = self.db.add_node(name=uname, facebook_id=uid)
                self.db.add_edge(user, new_user)
        except Exception as e:
            print(e)
            # self.add_error(e)

    def likes_scrapper(self, name, url):
        """Scrapes the likes data from the page named by name and situated
        by url on facebook and writes it to database"""
        pg_id = self.link_editor(url)
        name = name.strip()

        user = self.db.add_node(name=name, facebook_id=pg_id)
        try:
            for uname, uid in self._likes_scrapper(pg_id):
                like_page = self.db.add_like_page(name=uname, facebook_id=uid)
                self.db.add_like_edge(user, like_page)
        except Exception as e:
            print(e)
            sys.stdout.flush()
            # self.add_error(e)

    def _likes_scrapper(self, user_id):
        """Helper method for likes_scrapper"""
        url = "https://www.facebook.com/%s/likes" % self.link_editor(user_id)

        self.browser.get(url)
        time.sleep(1.5)
        print(self.browser.current_url)
        limit = 1500
        curr_count = 0
        while len(self.browser.find_elements_by_css_selector("img._359.img")) == 1 and curr_count <= limit:
            # Scroll down to bottom
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            curr_count += 1
        print("Scrolled to the bottom...")

        blocks = self.browser.find_elements_by_css_selector(".fsl.fwb.fcb")
        print(len(blocks))
        sys.stdout.flush()
        for block in blocks:
            try:
                name = block.find_element_by_css_selector("a").text.strip()
                link = block.find_element_by_css_selector("a").get_attribute("href").strip()
                # print(name, link)
            except Exception as e:
                print(e)
                sys.stdout.flush()
                name = None
                continue
            if name:
                yield name, self.link_editor(link)

    def _friends_scrapper(self, pg_id):
        """Helper function for friends scrapper funct"""
        url = "https://www.facebook.com/%s/friends" % self.link_editor(pg_id)

        self.browser.get(url)
        time.sleep(1.5)
        limit = 1500
        current_counter = 0
        while len(self.browser.find_elements_by_css_selector("img._359.img")) == 1 and current_counter <= limit:
            # Scroll down to bottom
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            current_counter += 1
        print("Scrolled to the bottom...")

        blocks = self.browser.find_elements_by_xpath("//div[@data-testid='friend_list_item']")

        for block in blocks:
            try:
                link = block.find_element_by_css_selector('div.fsl.fwb.fcb a')
                name = link.text.strip()
                link = link.get_attribute("href").strip()
            except Exception as e:
                self.add_error(e)
                continue
            if name:
                yield name, self.link_editor(link)

    def link_editor(self, link):
        """
        Returns the only id from the url line
        """
        return self.db.id_from_url(link)

    @staticmethod
    def add_error(content):
        """Writes the error to the error log"""
        with open("error.log", "w") as error_log_file:
            error_time = "Error time :: %s" % (time.strftime("%a, %d %b %Y %H:%M:%S",
                                                             time.localtime()))
            error_log_file.write("\n%s\n%s\n" % (error_time, content))

    def close_browser(self):
        """Closes the session"""
        self.browser.quit()

    @staticmethod
    def write_file(content, file_name="result.txt"):
        """Writes content to the file_name file"""
        with open(file_name, "w") as file_write:
            for sent in content:
                file_write.write("%s\n" % sent)


def read_file(file_name):
    """
    Reads the file which contains the name of the user followed by the url to its
    page on facebook and returns the list of this data
    """
    data = list()
    with open(file_name, "r", encoding="utf-8") as rfile:
        cont = rfile.readlines()
        length = len(cont) // 2
        for index in range(length):
            name = cont[index * 2].strip()
            fb_id = cont[index * 2 + 1].strip()
            if name:
                data.append((name, fb_id))
    return data

if __name__ == "__main__":
    # Starting invisible display
    time.sleep(15)
    WebGetter.display.start()

    # Starting a new browser
    inst = WebGetter(db_file_name="data/will_go_lst.db", clear=False)
    # st = int(input("Write"))
    # en = int(input("Write"))
    # try:
    inst.login_facebook()
    # inst.db.add_node(name="Kostya Liepieshov", facebook_id="Inkognita.n1")
    user_parsed_index = 0
    list_of_users = inst.db.get_nodes().all()
    start_p = int(input("W: "))
    finish_p = int(input("W: "))
    for user in list_of_users:
        if user_parsed_index >= start_p and user_parsed_index <= finish_p and user.facebook_id != "jarko.korol":
            print("Current profile id %d, name = %s, id = %s" % (user_parsed_index, user.name, user.facebook_id))
            sys.stdout.flush()
            inst.likes_scrapper(user.name, user.facebook_id)
        user_parsed_index += 1
    # except Exception as e:
    #    print("Got" + str(e))
    #    sys.stdout.flush()
    # Closing the browser
    inst.close_browser()

    # Stopping the display
    WebGetter.display.stop()
