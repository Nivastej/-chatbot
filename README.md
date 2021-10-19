# -chatbot

#|||||||||||||||||||||||||||||||||||||||||||||||||||||||#
#
#--- Notes ---#
#
#


#====================================#
# Database close and open statements #
#====================================#

# The Database closed and opened comments are for easy identification of when we can
# access the database and to ensure we're properly closing connections
# after opening them. Sometimes they are at the far left, sometimes they are indented
# when they are indented it is because they have been closed or opened within an "if" meaning
# that code in other if statements is not affected. At the points where the database is closed
# or opened for every eventuality, the open or closed statement is pushed to the far left
# messages about whether the database is open or closed are also included within the functions
# but they rely on those connections being set up before the functions are called so if you change
# something and that breaks, that could be the cause

#====================================#
#     App code and location code     #
#====================================#

# Wherever you see this, even if it is in a function, it is only needed to help us keep track
# of what is going on in print statements. I've added it in as a variable so that each time
# we start a new process we change the location code. If two different parts of code call exactly
# the fame function we'll know if one of them is causing an error or whether it is the function itself
# because the print statement will help us keep track of where the information is coming from


#====================================#
#              Functions             #
#====================================#

# Anything of the format "bunch_of_words(thing_1, thing_2, thing_3, etc.)" is a function
# to execute them, you just write them out and replace thing_1 etc. with the information you want
# them to use, to create them you write "def" then write out the function using placeholders for the data
# wherever you find a function in this code and don't know what it does, scroll to the synchronous functions
# section at the bottom where it will be explained


#====================================#
#               return               #
#====================================#

# When we write "return" that's the end of the process, if you haven't got that, the code will keep
# going down the list, if it is within an "if" condition it'll jump out of the if and keep running unless
# there is no more code that it meets the conditions for


#====================================#
#               Contexts             #
#====================================#

# Don't confuse the contexts we RECEIVE from API.AI with the contexts we SEND to API.AI

# Slack token and challenge management resource: https://github.com/slackapi/Slack-Python-Onboarding-Tutorial


#====================================#
#         Deduplication section      #
#====================================#

# Slack is quite prone to sending event notifications more than once, particularly
# if our application takes a little while longer to respond. One solution is to
# pay money for faster processing, another is to move the response up as high as possible
# in the code so we respond as quickly as possible, a third is to run through some Deduplication
# when we get these messages and discount the repeated calls.

# The risk here is that the user might legitimately send us two identical responses
# within a short time frame, perhaps, for example, if they are responding to a few messages with "yes"
# . The solution here is to carefully manage the amount of time we're ignoring (a minute should hopefully
# cover Slack resent responses without discounting many repeated messages) and to control the times when users might send a
# duplicate response by using buttons in Slack. Some chat bots use buttons to help control the full conversational
# flow but relying purely on buttons does devolve the conversation into essentially a pretty linear website journey


#====================================#
#                 Tokens             #
#====================================#

# This program uses a combination of user tokens and bot tokens, user tokens give us permission to post wherever that user can
# bot tokens give us permission to post wherever that bot has been allowed. In this application that difference in freedom
# to roam doesn't particularly change the functionality but it does allow us to show how we'd deal with each.


#====================================#
#                 Celery             #
#====================================#

# Celery on Heroku resources (the former is a good resource for understanding but clashes with our database so this
# program implements the latter): https://blog.miguelgrinberg.com/post/using-celery-with-flask
# and https://devcenter.heroku.com/articles/celery-heroku

#
#
#--- End of notes ---#
