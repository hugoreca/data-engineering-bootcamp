import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


FORKS_URL = 'https://github.com/hugoreca/data-engineering-bootcamp/network/members'

# Browser setup
options = Options()
options.binary_location = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
driver_path = r'C:\Development\chromedriver.exe'
driver = webdriver.Chrome(options=options, executable_path=driver_path)

# Login to github
sign_in_url = 'https://github.com/login'
driver.get(sign_in_url)
user = os.environ['user']
user_text_box_fill = driver.find_element_by_css_selector('#login_field').send_keys(user)
pwd = os.environ['pwd']
pwd_text_box_fill = driver.find_element_by_css_selector('#password').send_keys(pwd)
# Click on sign in button
driver.find_element_by_css_selector('#login > div.auth-form-body.mt-3 > form > div > input.btn.btn-primary.btn-block.js-sign-in-button').click()

# Repo scraping
driver.get(FORKS_URL)
repos = driver.find_elements_by_link_text('data-engineering-bootcamp')

# Looping through the links, ignoring the first two because (the first is mine, and the second is the original Wizeline repo

even_count = 0
even_list = []
links = [repo.get_attribute('href') for repo in repos][2:]

for link in links:
    driver.get(link)
    github_message = driver.find_element_by_css_selector('#repo-content-pjax-container > div > div.gutter-condensed.gutter-lg.flex-column.flex-md-row.d-flex > div.flex-shrink-0.col-12.col-md-9.mb-4.mb-md-0 > div.d-sm-flex.Box.mb-3.Box-body.color-bg-secondary > div.d-flex.flex-auto').text
    coder_profile = driver.find_element_by_css_selector('#repository-container-header > div.d-flex.mb-3.px-3.px-md-4.px-lg-5 > div > h1 > span.author.flex-self-stretch > a').text
    if github_message == 'This branch is even with wizelineacademy:main.':
        even_count += 1
        even_list.append(coder_profile)
    # Switch back to repos page
    driver.get(FORKS_URL)

driver.close()
print(f'The number of people that didnt complete the challenge is {even_count}')
print(f'The "names" of those who didnt complete the challenge are:')
for name in even_list:
    print(name)
