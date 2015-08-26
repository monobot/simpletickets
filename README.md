# simpletickets

This is a django module to manage ticketing between the users and the staff.
In a simple, easy and usefull way.

---

## Module Set Up

Add "simpletickets" to your installed apps:

`INSTALLED_APPS = (
    ...
    'simpletickets',
    )`


Add simpletickets urls to your main project urls.py file:

`urlpatterns = patterns('',
    ...
    url(r'^tickets/', include('simpletickets.urls')),
    )`

---

## Module Config

There are some variables that can be set up in your settings file/s:
(The shown assigments are the default values)

**BASE_TEMPLATE** is the base template where the tickets will be shown, its assumend that will be a block named 'blocktickets'

`BASE_TEMPLATE = 'index.html'`

**TICKET_ATTACHMENTS** is the folder where the ticket's attachments will be uploaded to

`TICKET_ATTACHMENTS = os.path.join(settings.MEDIA_ROOT, 'tickets')`

**TICKET_TYPE** is the different kind of tickets, that is a category of tickets

`TICKET_TYPE = (
        (1, _(u'Inform about an error')),
        (2, _(u'Problem')),
        (3, _(u'Propose a sugestion')),
        (4, _(u'Others')),
        )`

**TICKET_SEVERITY** is as guessed the severity of the ticket

`TICKET_SEVERITY = (
        (1, _(u'Critical')),
        (2, _(u'Very important')),
        (3, _(u'Important')),
        (4, _(u'Normal')),
        )`

**TICKET_STATE**  is also as guessed the state of the ticket.

`TICKET_STATE = (
        (1, _(u'new')),
        (2, _(u'assigned')),
        (3, _(u'solved')),
        (4, _(u'closed')),
        )`
