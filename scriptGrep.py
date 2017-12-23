from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import getpass
import traceback

def main():
	global time_village, driver, big_map_button, island_button, city_button, center_button, current_wood, current_stone, current_iron, current_population
	time_village = 0

	#Getting browser to use
	option = input("Select browser: \n[1] Chrome\n[2] Firefox\nAnswer: ")

	#Getting credentials
	username = input("\nGrepolis username: ")
	password = getpass.getpass("Account password: ")
	
	#Getting building to automatically upgrade
	pref_building = int(input('\nSelect building to automatically upgrade:\n[0] None\n[1] Senate\n[2] Timber Camp\n[3] Farm\n[4] Quarry\n[5] Warehouse\n[6] Silver Mine\n[7] Barracks\n[8] Temple\n[9] Market\n[10] Harbour\n[11] Academy\n[12] City Wall\n[13] Cave\nAnswer: '))

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
	big_map_button = driver.find_element_by_class_name('strategic_map')
	island_button = driver.find_element_by_class_name('island_view')
	city_button = driver.find_element_by_class_name('city_overview')
	center_button = driver.find_element_by_class_name('btn_jump_to_town')
	update_resources()

	# Getting the button to open city list
	global town_name_button
	town_name_button = driver.find_element_by_class_name('town_name')

	while True:
		upgrade_building(pref_building)
		try:
			resources_manager()
		except WebDriverException:
			traceback.print_exc()
		print("\nSleeping " + str(time_village/60) + " minutes")
		time.sleep(time_village)
	print("Stopped script!")


def update_resources():
	global current_wood, current_stone, current_iron, current_population
	current_wood = int((driver.find_element(By.CSS_SELECTOR , ".indicator.wood > .amount")).text)
	current_stone = int((driver.find_element(By.CSS_SELECTOR , ".indicator.stone > .amount")).text)
	current_iron = int((driver.find_element(By.CSS_SELECTOR , ".indicator.iron > .amount")).text)
	current_population = int((driver.find_element(By.CSS_SELECTOR , ".indicator.population > .amount")).text)

def upgrade_building(index):
	if index == 0:
		return
	buildings = ["main", "lumber", "farm", "stoner", "storage", "ironer", "barracks", "temple", "market", "docks", "academy", "wall", "hide"]
	driver.execute_script("BuildingMain.buildBuilding('" + buildings[index-1] + "', 60);")
	time.sleep(1)

def close_windows():
	center_button.click()
	time.sleep(0.5)
	close_buttons = driver.find_elements(By.CSS_SELECTOR , "div.btn_wnd.close")
	for b_close in close_buttons:
		try:
			b_close.click()
		except WebDriverException:
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
		time.sleep(2)

# Collect resources from all villages in the island of a given city
def get_resources():
	global time_village

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
				
					#Get villages lowest waiting time
					container_time = driver.find_element_by_class_name('action_time')
					tmp_time_village = int(container_time.text[:-1]) * 60

					if time_village == 0:
						container_time = driver.find_element_by_class_name('action_time')
						time_village = int(container_time.text[:-1]) * 60

					elif time_village < tmp_time_village:
						time_village = tmp_time_village

					try:
						card_claim_resources.click()
						print("Claimed " + str(driver.find_element_by_class_name('action_count').text) + " resources from village " + str(driver.find_element_by_class_name('village_name').text))
						successful += 1
					except WebDriverException:
						pass
					close_windows()
					time.sleep(1)
			
			print("Claimed resources from " + str(successful) + " of " + str(same_island_villages) + " villages.")
			break
		except WebDriverException:
			tries += 1
<<<<<<< HEAD
	update_resources()
=======
>>>>>>> 9b692752b85467d3387d73fb8b2f188a29cd78ef

if __name__ == "__main__":
	main()
