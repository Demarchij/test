### THIS DOC CONTAINS NOTES ABOUT OUR IMPLEMENTATION AND TESTING INSTRUCTIONS

Note: Our "models" container automatically runs django migrations during startup. This assumes that a cs4501 database has been created and is empty.
Note: Our docker containers (web, models, exp) run on ports 8000, 8001, and 8002, respectively.

## Test commands. Enter the following in your terminal after running 'docker-compose up':
# create some users
curl --data "username=Aaron&phone=111&email=a@a.com&password=pw" localhost:8001/api/v1/users/create
curl --data "username=Barry&phone=222&email=b@b.com&password=pw" localhost:8001/api/v1/users/create
curl --data "username=Candace&phone=333&email=c@c.com&password=pw" localhost:8001/api/v1/users/create
curl --data "username=Danny&phone=444&email=d@d.com&password=pw" localhost:8001/api/v1/users/create
curl --data "username=Eduardo&phone=555&email=e@e.com&password=pw" localhost:8001/api/v1/users/create
curl --data "username=Frederick&phone=666&email=f@f.com&password=pw" localhost:8001/api/v1/users/create
curl --data "username=Gaster&phone=777&email=g@g.com&password=pw" localhost:8001/api/v1/users/create
curl --data "username=Henry&phone=888&email=h@h.com&password=pw" localhost:8001/api/v1/users/create
curl --data "username=Isaac&phone=999&email=i@i.com&password=pw" localhost:8001/api/v1/users/create

# create some items
curl --data "owner=Aaron&title=Aaron's item&description=Some item belonging to Aaron&filename=http://i.imgur.com/D0eiXFU.jpg&size=0&tags=cute&tags=animal&category=unlisted" localhost:8001/api/v1/items/create
curl --data "owner=Barry&title=Barry's item&description=Some item belonging to Barry&filename=http://i.imgur.com/sKqLHyW.jpg&size=0&tags=cute&tags=animal&category=unlisted" localhost:8001/api/v1/items/create
curl --data "owner=Candace&title=Candace's item&description=Some item belonging to Candace&filename=http://i.imgur.com/yLf2ZsF.gif&size=0&tags=funny&category=unlisted" localhost:8001/api/v1/items/create
curl --data "owner=Danny&title=Danny's item&description=Some item belonging to Danny&filename=http://i.imgur.com/xZoPEC0.jpg&size=0&tags=animal&tags=cute&category=unlisted" localhost:8001/api/v1/items/create
curl --data "owner=Eduardo&title=Eduardo's item&description=Some item belonging to Eduardo&filename=http://i.imgur.com/PzHJEdp.jpg&size=0&tags=animal&tags=cute&category=unlisted" localhost:8001/api/v1/items/create
curl --data "owner=Frederick&title=Frederick's item&description=Some item belonging to Frederick&filename=http://i.imgur.com/A4Bf97G.png&size=0&tags=animal&category=unlisted" localhost:8001/api/v1/items/create
curl --data "owner=Gaster&title=Gaster's item&description=Some item belonging to Gaster&filename=http://i.imgur.com/5cXrc8n.jpg&size=0&tags=weird&category=unlisted" localhost:8001/api/v1/items/create
curl --data "owner=Henry&title=Henry's item&description=Some item belonging to Henry&filename=http://i.imgur.com/Fst3Sau.png&size=0&tags=math&category=unlisted" localhost:8001/api/v1/items/create
curl --data "owner=Isaac&title=Isaac's item&description=Some item belonging to Isaac&filename=http://i.imgur.com/ASnZ5Xc.png&size=0&tags=nature&category=unlisted" localhost:8001/api/v1/items/create

# Our two pages are hosted at localhost:8000 and localhost:8000/list
Visiting these on some web browser should take you to our Bootstrap'd app.

# The former is the homepage and displays the last 6 items created
# The latter simply lists every single item (in no particular order)
# Some item details are omitted from the display boxes. 
# Many functions are not implemented (searches, clicking on items, ratings, comments, etc.)




