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

Git clone this repository.

```
$ git clone https://github.com/takudo/eventbullet.git
$ cd eventbullet
```

Make config file.

```
$ cp app.cfg.template app.cfg
$ cat app.cfg
[pushbullet]
api_key: [api_key from https://www.pushbullet.com/account]
title: #from#~#to_time# #title#
message: #url#
```

replace api_key from your [pushbullet account page](https://www.pushbullet.com/account)

## Executing

```
$ python example.py
```

## TODO

* Paging site