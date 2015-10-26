from selenium import webdriver

browser = webdriver.Chrome('C:\Program Files\chromedriver\chromedriver')
browser.get('http://localhost:8000')

assert 'Django' in browser.title