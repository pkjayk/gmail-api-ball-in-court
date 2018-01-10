import os
import flask
import requests
import json

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

class Thread:

	def __init__(self):
		self.credentials = google.oauth2.credentials.Credentials(**flask.session['credentials'])
		self.client = googleapiclient.discovery.build('gmail', 'v1', credentials=self.credentials)


	def getThreads(self):
		threads = self.client.users().threads().list(userId='me', maxResults=3).execute()

		threads = threads.get('threads')

		emails = []

		for thread in threads:

			threadID = thread['id']
			tdata = self.client.users().threads().get(userId='me', id=thread['id']).execute()
			nmsgs = len(tdata['messages'])
			messages = tdata['messages']

			print(json.dumps(messages, indent=4, sort_keys=True))

			# get each individual message and grab it's headers
			for message in messages:
				headers = message['payload']['headers']

				# with each message get headers and append it's "From" value
				for header in headers:
					if header["name"] == "From":
						fromEmail = header["value"]
					if header["name"] == "To":
						toEmail = header["value"]
					if header["name"] == "Subject":
						emailSubject = header["value"]

				email = { "emailSubject": emailSubject, "toEmail": toEmail, "fromEmail": fromEmail, "threadID": threadID }

				emails.append(email)

		return emails

	def monitorThread(self, threadID):
		# set the thread to remember in memory (for now)
		flask.session['thread'] = threadID

		return threadID