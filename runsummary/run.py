#!/usr/bin/env python3

import datetime
import logging
import logging.config
import os
import subprocess
import time
import yaml

import csv_writer
import epics_getter
import hddaq_getter

logger = logging.getLogger(__name__)

#______________________________________________________________________________
def make_magnet_param():
  comment_info = hddaq_getter.comment_info()
  epics_getter.set_comment_info(comment_info)
  epics_getter.make_magnet_param()

#______________________________________________________________________________
def run(offset=1):
  try:
    csv_writer.make_title(force=True)
    while True:
      make_magnet_param()
      comment_info = hddaq_getter.comment_info()
      recorder_info = hddaq_getter.recorder_info()
      logger.debug(f'comment_info : {comment_info}')
      logger.debug(f'recorder_info : {recorder_info}')
      epics_getter.set_comment_info(comment_info)
      epics_getter.read_all()
      for n in range(offset, offset + 10000):
        if csv_writer.is_listed(n):
          continue
        if n not in comment_info:
          continue
        logger.debug(f'run{n:05d}')
        c = comment_info[n]
        values = list()
        if 'StopTime' in c:
          values.append(n)
          values.append(c['StartTime'])
          values.append(c['StopTime'])
          values.append(c['ElapsedTime'])
          values.append(c['Title'])
          if n in recorder_info:
            r = recorder_info[n]
            values.append(r['EventNumber'])
            values.append('ON')
            values.append(r['Bytes'])
          else:
            values.append('')
            values.append('OFF')
            values.append('')
          # t = hddaq_getter.trigger(n)
          logger.debug(f'{c}')
          if datetime.datetime.now() - c['StopTimeDT'] < datetime.timedelta(hours=4, minutes=30):
            continue
          t = epics_getter.trigger_info(n)
          logger.debug(f'{t}')
          # values.append(t[0])
          s = hddaq_getter.scaler(n)
          logger.debug(f'{s}')
          if s is False:
            continue
          values.extend(s)
          e = epics_getter.epics_info(n)
          values.extend(e)
          values.extend(t)
          csv_writer.write(values)
      # break
      time.sleep(2)
      #     # values.append(f'{year}/{date} {hms}')
      #     # values.append()
  except KeyboardInterrupt:
    pass

if __name__ == '__main__':
  top_dir = os.path.dirname(os.path.abspath(__file__))
  log_conf = os.path.join(top_dir, 'logging_config.yml')
  with open(log_conf, 'r') as f:
    logging.config.dictConfig(yaml.safe_load(f))
#  make_magnet_param()
  run(74000)

  # epics_getter.get(70183, 'K18MAG:D4:FLD')
  # hddaq_getter.event_number(70183)
  # hddaq_getter.comment_info()
  # #hddaq_getter.recorder_info()
  # logger.info(hddaq_getter.trigger())
