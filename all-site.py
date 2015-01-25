# -*- coding: utf-8 -*-

import eventbullet.site.connpass as connpass


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
    "ansible"
]

for tag in tags:
    connpass.notify(tag)