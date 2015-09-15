# simpletickets

This is a django module to manage ticketing between the users and the staff.
In a simple, easy and usefull way.

---

## Module Set Up

Add "simpletickets" to your installed apps:

```python
INSTALLED_APPS = (
    ...
    'simpletickets',
    )
```


Add simpletickets urls on one of your urls.py files:

```python
urlpatterns = patterns('',
    ...
    url(r'^simpletickets/', include('simpletickets.urls')),
    )
```

---

## Module Config

There are some variables that can be set up in your settings file/s:
(The shown assigments are the default values)

**BASE_TEMPLATE** is the base template where the tickets will be shown, there you __should have a template block named 'simpletickets'__

```python
BASE_TEMPLATE = 'index.html'
```

**TICKET_REST_API** boolean to select if you want a REST api, this feature uses django-restframework. so if activated you will need to install and set it up accordingly.

**DELTA_CLOSE** is the timedelta lapse between the moment the ticket is marked as solved by an staff member until it changes to closed without the owner reopening it.

Once the item is closed it can not be reopened again, the user has to create a new ticket for more support.

```python
DELTA_CLOSE = timedelta(hours=6)
```

**TICKET_ATTACHMENTS** is the folder where the ticket's attachments will be uploaded to

```python
TICKET_ATTACHMENTS = os.path.join(settings.MEDIA_ROOT, 'tickets')
```

The next 3 configuration variables are the most commonly changed in the module, i have left some digits in the tuples empty by purpose, maybe this setup can work for 80% of the sites out there, but im sure you can fill up the voids with you special needs, feel free to do that in those blank spaces.

Of course you can override the whole thing with you special needs, in that case you will have to fix all the now broken logic passed to the templates and create the templates themselves.

Ok straigt to the variables.

**TICKET_TYPE** is the different kind of tickets, im sure it will vary a lot from site to site, feel free to configurate the spaces between the 1, 2 and 8, 9

```python
TICKET_TYPE = (
        (1, _(u'Inform about an error')),
        (2, _(u'Problem')),
        ..
        (8, _(u'Propose a sugestion')),
        (9, _(u'Others')),
        )
```

**TICKET_SEVERITY** is as guessed the severity of the ticket from lowest priority to the higuest ones

```python
TICKET_SEVERITY = (
        (1, _(u'Low')),
        (2, _(u'Normal')),
        ..
        (5, _(u'important')),  # can be changed
        ..
        (8, _(u'very important')),
        (9, _(u'Critical')),
        )
```

**TICKET_STATE**

In this case it is the different states the ticket can have:
Only the owner can create tickets, and will be marked as new (and red hued in the template).
Once a staff member opens the ticket its asigned (brown hued) to himself, now the staff can leave it as asigned to himself, scale asigning it to other staff member or go straight to solve the problem and marking it as in progress (blue hued).
'in progress' is all the time between the staff member commences working on it untill its completly solved.
Once solved (greyed out) unless the owner reopens it, it will be finaly marked as closed until the DELTA_CLOSE passes.

```python
TICKET_STATE = (
        (1, _(u'new')),
        (2, _(u'assigned')),
        ..
        (5, _(u'in progress')),  # can be changed
        ..
        (8, _(u'solved')),
        (9, _(u'closed')),
        )
```

The ticket monitor is a supervision feature, there you can see all and every change the model object has sufered since created until finaly been closed.

The next two variables config if you want the staff or the owner to be able to download this file for every ticket in their lists.

```python
TICKET_MNTR_STAFF = True
TICKET_MNTR_OWNER = False
```

The next 5 variables config if you want the different boxes (main taskbar or the statistic) to be shown for staff and/or owner. If you are using your own templates simply ignore them.

```python
MAIN_TASKBAR = True
```

```python
STATISTIC_TIMES_STAFF = True
STATISTIC_NUMBERS_STAFF = True
```

```python
STATISTIC_TIMES_OWNER = True
STATISTIC_NUMBERS_OWNER = True
```
