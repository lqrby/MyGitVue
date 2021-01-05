'''
version: V2.0
Author: 学海无涯任我游
Date: 2020-12-02 11:22:35
LastEditors: 学海无涯任我游
LastEditTime: 2020-12-17 11:34:47
'''

def on_spawning_complete(user_count):
    self.update_state(STATE_RUNNING)
    if environment.reset_stats:
        logger.info("Resetting stats\n")
        self.stats.reset_all()

self.environment.events.spawning_complete.add_listener(on_spawning_complete)






def on_hatch_complete(user_count):
    self.state = STATE_RUNNING
    if self.options.reset_stats:
        logger.info("Resetting stats\n")
        self.stats.reset_all()
events.hatch_complete += on_hatch_complete