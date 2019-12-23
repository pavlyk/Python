# from selenium import webdriver
 
# driver = webdriver.Chrome('C:/Users/kozlov_pa/Downloads/chromedriver_win32___/chromedriver')
# search_string = "real python"
# driver.get("https://www.google.com/search?q={}".format(search_string)) 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('C:/Users/kozlov_pa/Downloads/chromedriver_win32___/chromedriver')
# driver = webdriver.Firefox()
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
elem.send_keys("hello world")
elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()