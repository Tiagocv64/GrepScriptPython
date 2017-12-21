from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import getpass

username = input("Username no grepolis: ")
password = getpass.getpass("Password da conta: ")
print("Opening Chrome...")

opts = webdriver.ChromeOptions()
opts.add_argument("--start-maximized")
driver = webdriver.Chrome(chrome_options=opts)
driver.get("https://pt47.grepolis.com/")
username_form = driver.find_element_by_id('login_userid')
username_form.clear()
username_form.send_keys(username)
pass_form = driver.find_element_by_id('login_password')
pass_form.clear()
pass_form.send_keys(password)
submit_button = driver.find_element_by_id('login_Login')
submit_button.click()
time.sleep(2)
#page to select world

played_worlds_list = driver.find_element_by_class_name('world_name')
current_world = played_worlds_list.find_element_by_xpath('//div[contains(text(), "BASSAE")]')
current_world.click()
time.sleep(2)

#page of city
island_button = driver.find_element_by_class_name('pointer')
center_button = driver.find_element_by_class_name('btn_jump_to_town')
island_button.click()
center_button.click()
time.sleep(2)

#page of islands
list_owned_villages = driver.find_elements(By.CSS_SELECTOR , "a.owned.farm_town")
n_villages = len(list_owned_villages)
q = 0
t = 0
while q < 50 and t < 100:
	try:
		driver.execute_script("BuildingMain.buildBuilding('main', 25);")
		time.sleep(2)
		driver.execute_script("BuildingMain.buildBuilding('farm', 40);")
		for i in range(n_villages):
			list_owned_villages = driver.find_elements(By.CSS_SELECTOR , "a.owned.farm_town")
			list_owned_villages[i].click()
			time.sleep(2)
			claim_resources = driver.find_element_by_class_name('card_click_area')
			try: 
				claim_resources.click() 
				print("Claimed resources!")
			except:
				print("Could not get resources from this village")
			close_buttons = driver.find_elements(By.CSS_SELECTOR , "div.btn_wnd.close");
			for b_close in close_buttons:
				try: 
					b_close.click()
				except:
					print("Couldn't close window!")
			time.sleep(1)
		print("Slepping for 5 minutes")
		time.sleep(300)
		print("Starting again...")
		island_button.click()
		center_button.click()
		q += 1
		t = 0
	except:
		print("Something went wrong, starting over!")
		t += 1
print("Stopped script!")
