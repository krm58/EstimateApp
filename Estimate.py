from __future__ import print_function
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.rst import RstDocument
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
from plyer import email
import string
import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from os.path import basename
from email.mime.application import MIMEApplication
import httplib2
import os
import base64
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from kivy.uix.popup import Popup
from kivy.uix.label import Label  
from kivy.uix.textinput import TextInput

try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags = None

class ToolListButton(ListItemButton):
	pass

class EmailInterface(BoxLayout, Screen):
	pass

class GoBack(Screen):
	pass

class ScreenManagement(ScreenManager):
	pass

def get_credentials():
		"""Gets valid user credentials from storage.

		If nothing has been stored, or if the stored credentials are invalid,
		the OAuth2 flow is completed to obtain the new credentials.

		Returns:
			Credentials, the obtained credential.
		"""
		SCOPES = 'https://mail.google.com/'
		CLIENT_SECRET_FILE = r'C:\Users\krm47\OneDrive\Documents\EdKivyApp\client_secret.json'
		APPLICATION_NAME = 'Acme Estimator'

		home_dir = os.path.expanduser('~')
		credential_dir = os.path.join(home_dir, '.credentials')
		if not os.path.exists(credential_dir):
			os.makedirs(credential_dir)
		credential_path = os.path.join(credential_dir,
									   'gmail-python-quickstart.json')

		store = Storage(credential_path)
		credentials = store.get()
		if not credentials or credentials.invalid:
			flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
			flow.user_agent = APPLICATION_NAME
			if flags:
				credentials = tools.run_flow(flow, store, flags)
			else: # Needed only for compatibility with Python 2.6
				credentials = tools.run(flow, store)
			print('Storing credentials to ' + credential_path)
		return credentials

class IntentButton(Button):
	email_recipient = StringProperty()
	email_sender = StringProperty()
	email_subject = StringProperty()
	email_text = StringProperty()
	email_filename = StringProperty()
	email_acme = StringProperty()
	email_supply = StringProperty()

	def send_email(self, name, *args):
		"""Send an email message.
		Args:
		service: Authorized Gmail API service instance.
		user_id: User's email address. The special value "me"
		can be used to indicate the authenticated user.
		message: Message to be sent.
		Returns: Sent Message.
		"""		
		credentials = get_credentials()
		http = credentials.authorize(httplib2.Http())
		service = discovery.build('gmail', 'v1', http=http)

		msg = MIMEMultipart()
		msg['From'] = self.email_recipient
		msg['To'] = self.email_sender #self.email_acme #, self.email_recipient
		msg['Subject'] = self.email_subject
		message = self.email_text
		msg.attach(MIMEText(message))
		
		name = name + '.docx'
		with open(name, "rb") as fil:
			part = MIMEApplication(
				fil.read(),
				Name=basename(name)
				)
			part['Content-Disposition'] = 'attachment; filename="%s"' % basename(name)
			msg.attach(part)
		raw = base64.urlsafe_b64encode(msg.as_bytes())
		raw = raw.decode()
		#body = {'raw': raw}
		body = {'raw': raw}
		message = (service.users().messages().send(userId="me", body=body).execute())

class ToolDB(BoxLayout, Screen):
	tool_text_input = ObjectProperty()
	tool_list = ObjectProperty()

	def submit_tool(self):
		# Get the tool's name from textInputs
		tool_name = self.tool_text_input.text
		#Add to ListView
		self.tool_list.adapter.data.extend([tool_name])
		#Reset the ListView
		self.tool_text_input.text = "" 
		self.tool_list._trigger_reset_populate()

	def delete_tool(self):
		# If a list item is selected
		if self.tool_list.adapter.selection:

			#Get the text from the item selected
			selection = self.tool_list.adapter.selection[0].text
			#Remove the matching item
			self.tool_list.adapter.data.remove(selection)
			#Reset the List View
			self.tool_list._trigger_reset_populate()

	def replace_tool(self):
		#If a list item is selected
		if self.tool_list.adapter.selection:
			#Get the text from the item selected
			selection = self.tool_list.adapter.selection[0].text
			#Remove the matching item
			self.tool_list.adapter.data.remove(selection)
			#Get the name of the tool from TextInputs
			tool_name = self.tool_text_input.text
			#Add the updated data to the list
			self.tool_list.adapter.data.extend([tool_name])
			#Reset the ListView
			self.tool_list._trigger_reset_populate()

	def save(self,name):
		toollist = str(self.tool_list.adapter.data)

		document = Document()
		my_image = document.add_picture('companylogo.png', width=Inches(1.0))
		last_paragraph = document.paragraphs[-1]
		last_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

		paragraph1 = document.add_paragraph()
		paragraph1.add_run('Materials List').bold = True
		paragraph1.alignment = WD_ALIGN_PARAGRAPH.CENTER

		for item in self.tool_list.adapter.data:
			paragraph2 = document.add_paragraph(style='ListBullet')
			paragraph2.add_run(str(item)).italic = True
		file = str(name) + '.docx'
		document.save(file)

# class Labor(BoxLayout, Screen):
# 	 def close_popup(self):
# 	 	self.dismiss

class NamePopup(BoxLayout, Button, Screen):
	filename_text_input = ObjectProperty()
	pass

class TimeorEstimate(BoxLayout, Button, Screen):
	pass

class PriceBook(BoxLayout, Button, Screen):
	pass

class TimeCard(BoxLayout, Button, Screen):
	pass

presentation = Builder.load_file("tooldb.kv")

class NamePopup(App):
	filename = StringProperty('')
	def build(self):
		return presentation
class TimeorEstimate(App):
	def build(self):
		return presentation
class ToolDBApp(App):
	def build(self):
		return presentation
# class LaborApp(App):
# 	def build(self):
# 		return presentation
class EmailApp(App):
	def build(self):
		return EmailInterface()

	def on_pause(self):
		return True

# if __name__ == "__main__":

TimeorEstimate().run()
NamePopup().run()
ToolDBApp().run()
EmailApp().run()
# LaborApp().run()
GoBack().run()