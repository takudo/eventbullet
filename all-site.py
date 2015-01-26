# -*- coding: utf-8 -*-

import eventbullet.site.connpass as connpass
import eventbullet.site.doorkeeper as doorkeeper


tags = [
    # language
    "scala",
    "java",
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
    u"フリーランス"

]

# for tag in tags:
#     connpass.notify(tag)

doorkeeper.notify(tags)