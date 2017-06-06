from selenium import webdriver
import time
from pyvirtualdisplay import Display
from facebook_network_graph.facebook_network_graph import NetworkGraph


class WebGetter:
    """
    Class that helps to scrap the data from facebook
    """
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
        button = self.browser.find_element_by_id('u_0_q')

        login_css.send_keys(login)
        password_css.send_keys(password)
        button.click()
        time.sleep(3)
        print("Current_url %s" % self.browser.current_url)
        print("Logged in...")

    def friends_scrapper(self, name, pg_id):
        """Scrappes the friends data from the page named by name and situated
        by pg_id on facebook and writes it to database"""
        pg_id = self.link_editor(pg_id)
        name = name.strip()

        user = self.db.add_node(name=name, facebook_id=pg_id)
        try:
            for name, pg_id in self._friends_scrapper(pg_id):
                new_user = self.db.add_node(name=name, facebook_id=pg_id)
                self.db.add_edge(user, new_user)
        except Exception as e:
            self.add_error(e)

    def _friends_scrapper(self, pg_id):
        """Helper function for friends scrapper funct"""
        url = "https://www.facebook.com/%s/friends" % self.link_editor(pg_id)

        self.browser.get(url)
        time.sleep(1.5)

        while len(self.browser.find_elements_by_css_selector("img._359.img")) == 1:
            # Scroll down to bottom
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
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


def read_perform(input_file, wgInst):
    """
    Perform reading the information from the fb pages of users stored
    in input_file using instance of class WebGetter as the second positional arg
    """
    i = 0
    for name, fb_id in read_file(input_file):
        print("Current profile index is %s" % str(i))
        wgInst.friends_scrapper(fb_id)
        i += 1


if __name__ == "__main__":
    display = Display(visible=0, size=(800, 600))
    display.start()
    inst = WebGetter()
    time_ = time.time()
    inst.login_facebook()
    try:
        read_perform("./data/interested.txt", inst)
    finally:
        inst.close_browser()
        display.stop()
    print(time.time() - time_)
