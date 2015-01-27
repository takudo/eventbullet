# -*- coding: utf-8 -*-

from eventbullet.db.events import Event

import eventbullet.site.connpass as connpass
import eventbullet.site.doorkeeper as doorkeeper
import eventbullet.site.atnd as atnd


tags = [
    # language
    "java",
    "scala",
    "php",
    "javascript",
    "python",
    # cloud
    "aws",
    "gcp",
    # VM
    "docker",
    "vagrant",
    # provisioning
    "chef",
    "puppet",
    "ansible",
    "hadoop",
    # Work
    u"フリーランス",
    # DB
    "mysql",
    "oracle",
    "postgresql",
    "sql",
    "html"
]

# for tag in tags:
#     connpass.notify(tag)

# doorkeeper.notify(tags)

atnd.reload(tags)

evs = Event.get_not_notified_events()

for ev in evs:
    ev.notify()
