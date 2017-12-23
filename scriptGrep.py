from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import getpass

def main():

	#Getting browser to use
	option = input("Select browser: \n[1] Chrome\n[2] Firefox\nAnswer: ")

	#Getting credentials
	username = input("\nGrepolis username: ")
	password = getpass.getpass("Account password: ")

	global driver

	#Set browser to Chrome and initialize driver
	if option == "1":
		print("\nOpening Chrome...")
		opts = webdriver.ChromeOptions()
		opts.add_argument("--start-maximized")
		driver = webdriver.Chrome(chrome_options=opts)

	#Set browser to Firefox and initialize driver
	elif option == "2":
		print("\nOpening Firefox...")
		opts = webdriver.FirefoxProfile()
		driver = webdriver.Firefox(firefox_profile=opts)
		driver.maximize_window()

	#Opening browser in Grepolis page
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
	time.sleep(4)

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

	# Getting the button to open city list
	global town_name_button
	town_name_button = driver.find_element_by_class_name('town_name')

	while True:
		resources_manager()
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

# Switches between cities and call get_resources() for each one
def resources_manager():
	island_button.click()
	time.sleep(1)
	town_name_button.click()
	time.sleep(2)
	n_cities = len(driver.find_elements(By.CSS_SELECTOR , "div.town_group_town"))
	list_of_cities = driver.find_elements(By.CSS_SELECTOR , "div.town_group_town")
	
	for i in range(n_cities):
		list_of_cities = driver.find_elements(By.CSS_SELECTOR , "div.town_group_town")
		list_of_cities[i].click()
		time.sleep(2)
		center_button.click()
		get_resources()
		town_name_button.click()
		time.sleep(10)

# Collect resources from all villages in the island of a given city
def get_resources():
	print("\nStarting to collect resources for city " + str(driver.find_element_by_class_name('town_name').text))
	n_villages = len(driver.find_elements(By.CSS_SELECTOR , "a.owned.farm_town"))
	tries = 0
	while tries < 30:
		try:
			successful = 0
			same_island_villages = 0
			for i in range(n_villages):
				list_owned_villages = driver.find_elements(By.CSS_SELECTOR , "a.owned.farm_town")
				if list_owned_villages[i].get_attribute("data-same_island") == "true":
					same_island_villages += 1
					list_owned_villages[i].click()
					time.sleep(2)
					card_claim_resources = driver.find_element_by_class_name('card_click_area')
					try:
						card_claim_resources.click()
						print("Claimed " + str(driver.find_element_by_class_name('action_count').text) + " resources from village " + str(driver.find_element_by_class_name('village_name').text))
						successful += 1
					except:
						pass
					close_windows()
					time.sleep(1)
			print("Claimed resources from " + str(successful) + " of " + str(same_island_villages) + " villages.")
			break
		except:
			tries += 1

if __name__ == "__main__":
	main()
