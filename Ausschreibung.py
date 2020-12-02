
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
#from selenium.webdriver.common.keys import Keys
#import time
from datetime import date, time
#from datetime import time
import smtplib

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://kultusministerium.hessen.de/ueber-uns/stellenangebote/stellenausschreibungen")
#print(driver.title)

#Um auf die Auswahl zu kommen, muss das iframe ausgewählt werden.
iframe = driver.find_element_by_class_name("hzd_iframe-processed")
driver.switch_to.frame(iframe)

#driver.implicitly_wait(5) # seconds
#Warte bis die Seite fertig geladen hat
try:
	element =WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.NAME, "practiceId"))
		)
except:
	driver.quit()

#Funktionsstelle auswaehlen
select_element = driver.find_element_by_name('practiceId')
select_object = Select(select_element)
select_object.select_by_visible_text('Funktionsstellenbesetzungsverfahren')

#submit button auswaehlen
submit_button = driver.find_element_by_name('choosePractice')
submit_button.click()

#nächste Seite laden
#driver.implicitly_wait(5) # seconds

try:
	element =WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.NAME, "personalOrganisationalUnitId"))
		)
except:
	driver.quit()

#Dienststelle auswählen
select_element = driver.find_element_by_name('personalOrganisationalUnitId')
select_object = Select(select_element)
select_object.select_by_visible_text('Schulamt Darmstadt-Dieburg')
select_object.select_by_visible_text('Schulamt Groß-Gerau u. Main-Taunus-Kreis')
select_object.select_by_visible_text('Schulamt Offenbach')

#Besoldung auswählen
select_element = driver.find_element_by_name('paymentId')
select_object = Select(select_element)
select_object.select_by_visible_text('A15')

#Button clicken
submit_button = driver.find_element_by_name('startChoice')
submit_button.click()

#Warten bis Resultate erscheinen
try:
	element =WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.CLASS_NAME, 'pbtable'))
		)
except:
	driver.quit()

row_count = len(driver.find_elements_by_xpath("/html/body/form/div/div[2]/div[6]/table/tbody/tr"))
col_count = len(driver.find_elements_by_xpath("/html/body/form/div/div[2]/div[6]/table/tbody/tr[3]/td"))

#print("Number of Rows", row_count)
#print("Number of Columns", col_count)

first_part='/html/body/form/div/div[2]/div[6]/table/tbody/tr['
second_part=']/td['
third_part=']'

#/html/body/form/div/div[2]/div[6]/table/tbody/tr[3]/td[1]

mailtext =""
#erst in der zweiten Zeile anfangen, erste Zeile ist Überschriften
#Columns die ersten beiden und letzte ist uninteressant
for n in range(3,row_count+1):
	mailtext = mailtext + "\n" + "\n" 
	for m in range(3,col_count):
		final_path = first_part + str(n) + second_part + str(m) + third_part
		#table_data = driver.find_element_by_xpath(final_path).text
		#print(table_data, end = " ")

		mailtext = mailtext + driver.find_element_by_xpath(final_path).text + " "

#print (bla)
driver.quit()

#mailtext = [str(buchstabe) for buchstabe in mailtext]

####Mailverschickung
subject = "Stellenausschreibungen vom " + str(date.today())
mail= smtplib.SMTP('smtp.web.de', 587)
mail.ehlo()
mail.starttls()
sender = "laksdjflkasjdf@web.de"
recipient = "salajsdfklajsdöfkjaskdljf@klasdfjaslködfj.de"
mail.login('alkösjdfklasjdf@web.de','lkjasdflökjasdkflj')
header='To:'+recipient+'\n'+'From:'+sender+'\n'+'subject:' + subject +'\n'
content=header+mailtext
mail.sendmail(sender,recipient,content.encode("utf-8"))
mail.close
