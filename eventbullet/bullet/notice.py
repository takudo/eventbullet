# -*- coding: utf-8 -*-

from pushbullet import PushBullet

pb = PushBullet(api_key)

success, push = pb.push_note("This is the title", "This is the body")