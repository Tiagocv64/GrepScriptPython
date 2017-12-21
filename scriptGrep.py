from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import getpass

def main():
	#Getting credentials
	username = input("Username no grepolis: ")
	password = getpass.getpass("Password da conta: ")

	#Opening browser in Grepolis page
	print("Opening Chrome...")
	opts = webdriver.ChromeOptions()
	opts.add_argument("--start-maximized")
	global driver
	driver = webdriver.Chrome(chrome_options=opts)
	driver.get("https://pt47.grepolis.com/")

	#Entering credentials to page
	username_form = driver.find_element_by_id('login_userid')
	username_form.clear()
	username_form.send_keys(username)
	pass_form = driver.find_element_by_id('login_password')
	pass_form.clear()
	pass_form.send_keys(password)
	submit_button = driver.find_element_by_id('login_Login')
	submit_button.click()
	time.sleep(2)

	#Selecting world BASSAE in world selection
	played_worlds_list = driver.find_element_by_class_name('world_name')
	current_world = played_worlds_list.find_element_by_xpath('//div[contains(text(), "BASSAE")]')
	current_world.click()
	time.sleep(2)

	#Getting the four buttons on top left
	global big_map_button, island_button, city_button, center_button
	big_map_button = driver.find_element_by_class_name('strategic_map')
	island_button = driver.find_element_by_class_name('island_view')
	city_button = driver.find_element_by_class_name('city_overview')
	center_button = driver.find_element_by_class_name('btn_jump_to_town')

	while True:
		get_resources()
		time.sleep(300)
	print("Stopped script!")

def upgrade_building(building):
	driver.execute_script("BuildingMain.buildBuilding('" + building + "', 60);")
	time.sleep(1)

def close_windows():
	center_button.click()
	time.sleep(0.5)
	close_buttons = driver.find_elements(By.CSS_SELECTOR , "div.btn_wnd.close")
	for b_close in close_buttons:
		try:
			b_close.click()
		except:
			pass

def get_resources():
	island_button.click()
	center_button.click()
	time.sleep(1)
	n_villages = len(driver.find_elements(By.CSS_SELECTOR , "a.owned.farm_town"))
	trys = 0
	while trys < 30:
		try:
			successful = 0
			for i in range(n_villages):
				list_owned_villages = driver.find_elements(By.CSS_SELECTOR , "a.owned.farm_town")
				list_owned_villages[i].click()
				time.sleep(2)
				card_claim_resources = driver.find_element_by_class_name('card_click_area')
				try:
					card_claim_resources.click()
					successful += 1
				except:
					pass
				close_windows()
				time.sleep(1)
			print("Claimed resources from " + str(successful) + " of " + str(n_villages) + " villages.")
			break
		except:
			trys += 1

if __name__ == "__main__":
	main()
