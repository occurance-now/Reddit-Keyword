import kivy
from kivy.app import App 
from kivy.uix.label import Label 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout 
from kivy.uix.textinput import TextInput 
from kivy.uix.button import Button 
from kivy.uix.widget import Widget 
from kivy.properties import ObjectProperty
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.config import Config
from kivy.lang import Builder 
from kivy.uix.screenmanager import ScreenManager, Screen 

import webbrowser
import praw

Config.set('input', 'mouse', 'mouse,disable_multitouch')#disable touch features

class MainWindow(Screen):
	url = ObjectProperty(None)
	keyword = ObjectProperty(None)
	subtitle = ObjectProperty(None)
	refcount = ObjectProperty(None)
	keyword_used = ObjectProperty(None)
	comment_amount = ObjectProperty(None)
	reload_limit = ObjectProperty(None)
	reload_limit_input = ObjectProperty(None)
	progress_bar = ObjectProperty(None)


	def btn(self):

		try:

			reddit = praw.Reddit(client_id='6BMBkfzv90xEeA', \
	                     client_secret='RawFzb39yXQ0gRVQnTh0PISR5fU', \
	                     user_agent='red-green', \
	                     username='redOrgreen94', \
	                     password='Hunter4real')

			submission = reddit.submission(url=(str(self.url.text)))
			self.sub_title = submission.title
			self.my_reload_limit = self.reload_limit.text

			submission.comments.replace_more(limit=(int(self.my_reload_limit)))

			self.sub_comments = submission.comments.list()
			self.progress_bar.max = (len(submission.comments.list()))


			self.my_keyword = [self.keyword.text]

			self.comment_count = 0 

			for comment in self.sub_comments:
				cbody = comment.body

				if any(keyword in cbody for keyword in self.my_keyword):
					self.comment_count += 1

			self.puopen()

		except:

			P.show_popup(self)

	
	def next(self, dt):

			if self.progress_bar.value < self.progress_bar.max:
				self.progress_bar.value += 2
			else:
				self.url.text = ''#clear
				self.keyword.text = ''#clear
				self.reload_limit.text = ''#clear
				self.subtitle.text = str(self.sub_title)
				self.refcount.text = str(self.comment_count)
				self.keyword_used.text = self.my_keyword[0]
				self.comment_amount.text = (str(len(self.sub_comments)))
				self.reload_limit_input.text = self.my_reload_limit
			
	def puopen(self):
		Clock.schedule_interval(self.next, 1/25)

	def call_wallstreetbets(self):
		WebCalls.open_wallstreetbets()

	def call_politics(self):
		WebCalls.open_politics()

	def call_worldnews(self):
		WebCalls.open_worldnews()



class SecondWindow(Screen):#instructions
	pass


class WebCalls():#webbroweser calls

	def open_wallstreetbets():
		webbrowser.open('https://www.reddit.com/r/wallstreetbets/')

	def open_politics():
		webbrowser.open('https://www.reddit.com/r/politics/')

	def open_worldnews():
		webbrowser.open('https://www.reddit.com/r/worldnews/')


class P(GridLayout):#popup 

	def show_popup(self):

		show = P()

		layout = GridLayout(cols = 1, padding = 10)

		popupLabel = Label(text = "You've entered an invalid input, please try again", size_hint = (.5, .9))
		closeButton = Button(text = 'Return to Main Page', size_hint = (.5, .1))

		layout.add_widget(popupLabel)
		layout.add_widget(closeButton)

		popup = Popup(title = 'Error Message', content=layout, auto_dismiss=False)
		closeButton.bind(on_press= popup.dismiss)

		popup.open()


class WindowManager(ScreenManager):
	pass


kv = Builder.load_file('reddit_keyword.kv')

class reddit_keywordMainApp(App):
	def build(self):
		return kv



if __name__ == '__main__':
	reddit_keywordMainApp().run()