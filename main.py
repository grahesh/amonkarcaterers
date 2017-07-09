# Copyright 2012 Digital Inspiration
# http://www.labnol.org/

import os
import sys
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.api import mail


##reload(sys)
##sys.setdefaultencoding("utf-8")

class MainHandler(webapp.RequestHandler):
  def get (self, q):
    if q is None:
      q = 'index.html'

    path = os.path.join (os.path.dirname (__file__), q)
    self.response.headers ['Content-Type'] = 'text/html'
    self.response.out.write (template.render (path, {}))

  def post(self,q):
    # takes input from user
        userMail=self.request.get("contact_email")
        name=self.request.get("contact_name")
        userMessage=self.request.get("contact_message")
        message=mail.EmailMessage(sender="goaweddingexpo.in: Contact Us<admin@goaweddingexpo.in>",subject="Contact")

        # not tested
        if not mail.is_email_valid(userMail):
            self.response.out.write("Wrong email! Check again!")

        message.to=userMail
        message.body="""Thank you!
	       You have entered following information:
	       Your mail: %s
	       Name: %s
	       Message: %s
         \nThank You For Contacting Goa Wedding Expo.""" %(userMail,name,userMessage)
        message.send()
        # self.response.out.write("Message sent to user!")

        contact_message=mail.EmailMessage(sender="admin@goaweddingexpo.in",subject="Contact")
        contact_message.to="contact@goaweddingexpo.in"
        contact_message.body="""The Following person contacted:
         Mail: %s
         Name: %s
         Message: %s""" %(userMail,name,userMessage)
        contact_message.send()
        # self.response.out.write("Message sent to goa wedding expo admin!")

        self.response.out.write("sent")


def main ():
  application = webapp.WSGIApplication ([('/(.*html)?', MainHandler)], debug=True)
  util.run_wsgi_app (application)

if __name__ == '__main__':
  main ()
