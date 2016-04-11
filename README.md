# Newton's Attic Class Management Solution

This is the repository for our senior design project, [Newton's Attic Class Management Solution](https://cs499classmgmtsln.wordpress.com/). 

Since we are using the Django web programming framework, there is a fair amount of generated code. In order to properly evalutate our code, to date, one would want to look in the following directories and files (all paths are relative the to project root):

  * scheduling
  * scheduling/templates

At the time of this writing, the `scheduling` directory contains files relating to the backend of the scheduling module. The `models.py` file will be of particular interest here. It contains the definitions that underlay the core functionality of this module. The `scheduling/templates` directory contains code that pertains to the UI of the scheduling module. Currently, it does not interact with the backend and is just a proof of concept. The next step here is to fully integrate this interface with the backend so that it can work with test data from our database.

As of right now, those are the main components of our project's code that are worth looking at. Of course, this will change as time goes on and we get closer to the end of the semester.
