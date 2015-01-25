# eventbullet

eventbullte is newer event push notification tool with [pushbullet](https://www.pushbullet.com/).

## requirements

* peewee
* pyquery
* pushbullet.py

And make pushbullet account.

## installment

```
$ sudo pip install peewee pyquery pushbullet.py
```

'pyquery' requires 'libxml' libraries.
If you find errors, then you install libxml libraries(ex: libxslt, libxml-python), when pip install pyquery.


Git clone this repository.

```
$ git clone https://github.com/takudo/eventbullet.git
$ cd eventbullet
```

Make config file.

```-
$ cp app.cfg.template app.cfg
$ cat app.cfg
[pushbullet]
api_key: [api_key from https://www.pushbullet.com/account]
title: #from#~#to_time# #title#
message: #url#
```

replace api_key from your [pushbullet account page](https://www.pushbullet.com/account)

Edit your interesting keywords.

```
$ vi all-site.py
```

You can edit `tags` variable, then you can get the event's info that match you.

## Executing

```
$ python example.py
```

## TODO

* Paging site