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


Add simpletickets urls to your main project urls.py file:

```python
urlpatterns = patterns('',
    ...
    url(r'^tickets/', include('simpletickets.urls')),
    )
```

---

## Module Config

There are some variables that can be set up in your settings file/s:
(The shown assigments are the default values)

**BASE_TEMPLATE** is the base template where the tickets will be shown, its assumend that will be a block named 'simpletickets'

```python
BASE_TEMPLATE = 'index.html'
```

**DELTA_CLOSE** is the timedelta and item changes irself from solved to closed

```python
DELTA_CLOSE = timedelta(hours=6)
```

**TICKET_ATTACHMENTS** is the folder where the ticket's attachments will be uploaded to

```python
TICKET_ATTACHMENTS = os.path.join(settings.MEDIA_ROOT, 'tickets')
```

Changes on the next variables can supose great changes on the templates, even when we have take in mind many cases; consider using your own templates if they dont perfectly fit.

**TICKET_TYPE** is the different kind of tickets, that is a category of tickets

```python
TICKET_TYPE = (
        (1, _(u'Inform about an error')),
        (2, _(u'Problem')),
        (8, _(u'Propose a sugestion')),
        (9, _(u'Others')),
        )
```

**TICKET_SEVERITY** is as guessed the severity of the ticket

```python
TICKET_SEVERITY = (
        (1, _(u'Critical')),
        (2, _(u'Very important')),
        (3, _(u'Important')),
        (4, _(u'Normal')),
        )
```

**TICKET_STATE**  is also as guessed the state of the ticket.

```python
TICKET_STATE = (
        (1, _(u'new')),
        (2, _(u'assigned')),
        (5, _(u'delayed')),
        (8, _(u'solved')),
        (9, _(u'closed')),
        )
```
