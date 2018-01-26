from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
import time
import getpass
import traceback
import argparse
import sys

global parser
# Instantiate the parser
parser = argparse.ArgumentParser(description='Multipurpose bot for use with Grepolis')

# Specifies Chrome as the browser to use
parser.add_argument('-c', action='store_true', default=False, dest='useChrome',
                    help='Specifies Chrome as the browser to use')

# Specifies Firefox as the browser to use
parser.add_argument('-f', action='store_true', default=False, dest='useFirefox',
                    help='Specifies Firefox as the browser to use')

# Specifies your grepolis username
parser.add_argument('-u', dest='username',
                    help='Specifies your grepolis username')

#Specifies buildings to automatically upgrade
parser.add_argument('-b', type=int, nargs='*', dest='pref_buildings',
                    default=[],
                    help='Specifies buildings to automatically upgrade : 1 - Senate, 2 - Timber Camp, 3 - Farm, 4 - Quarry, 5 - Warehouse, 6 - Silver Mine, 7 - Barracks, 8 - Temple, 9 - Market, 10 - Harbour, 11 - Academy, 12 - City Wall, 13 - Cave',
                    )

def main():
	global args, world, time_village, driver, big_map_button, island_button, city_button, center_button, town_name_button, current_wood, current_stone, current_iron, current_population
	time_village = 0

	#Getting arguments
	args = parser.parse_args()

	#If both -c and -f arguments were used
	if args.useChrome and args.useFirefox:
		print("Error! Flags '-c' and '-f' can not be simultaneaously active!")
		sys.exit()

	#Getting browser to use
	if args.useChrome:
		option = "1"
	elif args.useFirefox:
		option = "2"
	else:
		option = input("Select browser: \n[1] Chrome\n[2] Firefox\nAnswer: ")

	#Getting credentials
	if args.username == None:
		username = input("\nGrepolis username: ")
	else:
		username = args.username

	password = getpass.getpass("Account password: ")

	world = input("\nSelect World: \n[1] Bassae\n[2] Doriscos\nAnswer: ")

	if world == "1":
		world = "BASSAE"
	else:
		world = "DORISCOS"

	#Getting buildings to automatically upgrade
	if args.pref_buildings == []:
		pref_buildings = [int(i) for i in ((input('\nSelect buildings to automatically upgrade:\n[0] None\n[1] Senate\n[2] Timber Camp\n[3] Farm\n[4] Quarry\n[5] Warehouse\n[6] Silver Mine\n[7] Barracks\n[8] Temple\n[9] Market\n[10] Harbour\n[11] Academy\n[12] City Wall\n[13] Cave\nEx: 11 3 1 (It will build Academy then Farm then Senate)\nAnswer: ')).split(" "))]
		pref_buildings.append(0)
	else:
		pref_buildings = args.pref_buildings
		pref_buildings.append(0)

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
	current_world = played_worlds_list.find_element_by_xpath('//div[contains(text(), "' + world + '" )]')
	current_world.click()
	time.sleep(2)

	#Getting the four buttons on top left
	big_map_button = driver.find_element_by_class_name('strategic_map')
	island_button = driver.find_element_by_class_name('island_view')
	city_button = driver.find_element_by_class_name('city_overview')
	center_button = driver.find_element_by_class_name('btn_jump_to_town')
	update_resources()

	# Getting the button to open city list
	town_name_button = driver.find_element_by_class_name('town_name')
	current_building = 0
	while True:
		try:
			resources_manager()
		except WebDriverException:
			traceback.print_exc()
		current_building = current_building + 1 if upgrade_building(pref_buildings[current_building]) else current_building
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
	global current_wood, current_stone, current_iron
	if index == 0:
		return False
	past_wood = current_wood
	past_stone = current_stone
	past_iron = current_iron
	buildings = ["main", "lumber", "farm", "stoner", "storage", "ironer", "barracks", "temple", "market", "docks", "academy", "wall", "hide"]
	print("Trying to build " + buildings[index-1])
	driver.execute_script("BuildingMain.buildBuilding('" + buildings[index-1] + "', 60);")
	time.sleep(1)
	update_resources()
	if past_iron > current_iron and past_wood > current_wood and past_stone > current_stone:
		print("Successfully built!")
		return True
	else:
		print("Coulnd't put build to construction queue...")
		return False

def close_windows():
	center_button.click()
	time.sleep(0.5)
	close_buttons = driver.find_elements(By.CSS_SELECTOR , "div.btn_wnd.close")
	for i in range(len(close_buttons)):
		try:
			#The foremost window is the last element of the array
			close_buttons = driver.find_elements(By.CSS_SELECTOR , "div.btn_wnd.close")
			b_close = close_buttons[len(close_buttons) - (i + 1)]
			b_close.click()
			time.sleep(1)
		except WebDriverException:
			pass

def elementExists(mode, str):
	try:
		if mode == 0:
			driver.find_element_by_class_name(str)
		elif mode == 1:
			driver.find_element_by_id(str)
	except NoSuchElementException:
		return False
	return True

# Switches between cities and call get_resources() for each one
def resources_manager():
	close_windows()
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
		time.sleep(2)
		get_resources()
		town_name_button.click()
		time.sleep(2)
	town_name_button.click()

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
			warehouse_not_full = True
			for i in range(n_villages):
				list_owned_villages = driver.find_elements(By.CSS_SELECTOR , "a.owned.farm_town")

				#If village is on the selected city's island
				if list_owned_villages[i].get_attribute("data-same_island") == "true":
					same_island_villages += 1

					#If previous attempts did not reveal the popup saying warehouse is full
					if warehouse_not_full:
						list_owned_villages[i].click()
						time.sleep(2)
						card_claim_resources = driver.find_element_by_class_name('card_click_area')

						#Get villages lowest waiting time
						container_time = driver.find_element_by_class_name('action_time')
						tmp_time_village = int(container_time.text[:-1]) * 60

						if time_village == 0 or time_village > tmp_time_village:
							time_village = tmp_time_village

						#Try to collect resources
						try:

							#If popup that indicates resouces ready to collect does not appear next to village icon, then say 0 resources were collected
							if not elementExists(1, str(list_owned_villages[i].get_attribute("id")) + "_claim"):
								print("Claimed 0 resources from village " + str(driver.find_element_by_class_name('village_name').text) + ", cooldown was in effect")

							else:
								card_claim_resources.click()
								time.sleep(2)

								#If popup appears about wasting resources, then warehouse is full and no further resources can be collected
								#This could be done via simply breaking the loop if warehous is full but we wouldn't know the true value of same_island_villages
								if elementExists(0, 'confirmation'):
									close_windows()
									print('Warehouse capacity overflowed in current city!')
									warehouse_not_full = False

								#If all is normal, proceed as planned
								else:
									print("Claimed " + str(driver.find_element_by_class_name('action_count').text) + " resources from village " + str(driver.find_element_by_class_name('village_name').text))
									successful += 1

						except WebDriverException:
							pass
					close_windows()
					time.sleep(1)

			print("Claimed resources from " + str(successful) + " of " + str(same_island_villages) + " villages.\n")
			break
		except WebDriverException:
			tries += 1
	update_resources()

if __name__ == "__main__":
	main()
