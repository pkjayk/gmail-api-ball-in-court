import os
import flask
import requests

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
			tdata = self.client.users().threads().get(userId='me', id=thread['id']).execute()
			nmsgs = len(tdata['messages'])
			messages = tdata['messages']

			# get each individual message and grab it's headers
			for message in messages:
				headers = message['payload']['headers']

				# with each message get headers and append it's "From" value
				for header in headers:
					if header["name"] == "From":
						fromEmail = header["value"]
					if header["name"] == "To":
						toEmail = header["value"]

				email = { "To Email": toEmail, "From Email": fromEmail }

				emails.append(email)

		return emails