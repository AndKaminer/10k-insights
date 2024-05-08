# Flask Things
This section will go over all of the flask-y bits of the app.

## SocketIO
This project uses SocketIO to send information back and forth between the server and client.
Doing just about anything in this project requires that you interact with it.
Here are some things you will need it for:

### Working with Language Models
Since language models take a lot of time to give an answer, you need to give the client
a loading page while the language model responds. To do this, you will need to make a SocketIO
event. Look at 'chart-event' or 'claude-event' in the main __init__.py file for reference.

### Working with Charts
Since retrieving data for charting may also take a long time (thanks SEC), you will also probably
need a loading page. For reference, check out the events noted in the above section.

### The Testing Event
One helpful SocketIO event is the testing event, which allows you to test how your SocketIO setup
is working. It just waits a bit then serves you some sample text, but you can modify how you like.
Just check out 'test-event'.

## The Stock Route
Most of the website's functionality goes through the stock route (just look for the function of
the same name. It's a big one.) On a get request, the route gives the user options for what they
would like to do with certain data over certain timeframes. On a post request, the route
detects which form is filled out and then, depending on the form, serves the appropriate template.
If you want to add functionality to the app, it is very likely going to be by adding another form
to the page which serves another template.

## Extra Data Wrangling Functions
There are a couple of extra functions at the end of the file that, ideally, should be in a separate
module. These are pretty much one-offs, so changing them shouldn't break a bunch of stuff across
the site (only the things that call them directly).
