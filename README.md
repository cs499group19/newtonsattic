# Newton's Attic Class Management Solution

This is the repository for our senior design project, [Newton's Attic Class Management Solution](https://cs499classmgmtsln.wordpress.com/). 

Since we are using the Django web programming framework, there is a fair amount of generated code. In order to properly evalutate our code, to date, one would want to look in the following directories and files (all paths are relative the to project root):

  * scheduling
  * scheduling/admin.py      -- Settings for Django Admin
  * scheduling/models.py     -- Model definitions for Scheduling back-end.
  * scheduling/view.py       -- Controller definitions for Scheduling back-end.
  * scheduling/templates     -- View definitions for Scheduling UI.
  * scheduling/templatetags  -- Helper functions to be used in the views.

At the time of this writing, the `scheduling` directory contains files relating to the backend of the scheduling module. The `models.py` file will be of particular interest here. It contains the definitions that underlay the core functionality of this module. The `scheduling/templates` directory contains code that pertains to the UI of the scheduling module.
