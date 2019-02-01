[initial version of the project.]

To run the server execute
1.cd SmartOrder ( outer directory containing manage.py)
2.
execute this :    python manage.py runserver 0.0.0.0:8000


------------------:Fixing Known bugs:-------------------
For Unix/Linux if server time is wrong then to change it:
1.Goto SmartOrder/settings.py
2.Change TIME_ZONE = None
3.Change USE_TZ = False
4.Restart the server

it worked for me...hope it works for you to.
