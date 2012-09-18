# -*- encoding: utf-8 -*-

import os
import os.path
import re
import logging
from contextlib import closing
from gzip import GzipFile
from cStringIO import StringIO
from datetime import datetime

from boto.s3.connection import S3Connection


class Fetcher(object):

    __RE_DATE__ = re.compile('([0-9]{4}\-[0-9]{2}\-[0-9]{2})', re.I)

    def __init__(self, env, log_prefix, logger=None):
        super(Fetcher, self).__init__()
        self.env = env
        self.log_prefix = log_prefix
        self.logger = logger

        if not self.logger:
            self.logger = logging.getLogger(
                type(self).__module__ + '.' + type(self).__name__)

    def fetch(self):
        conn = self.connection
        bucket = conn.lookup(self.log_bucket)

        for key in bucket.list(prefix=self.log_prefix):
            date = self.__RE_DATE__.findall(key.name)[0]
            if not self.filter_date(date):
                continue

            cag = key.get_contents_as_string()
            self.logger.info('date: %s, log: %s' % (date, key.name))

            with closing(StringIO(cag)) as ins:
                with GzipFile(fileobj=ins) as gz:
                    log_name = '%s.log' % (date)
                    log_file = os.path.join(self.fetch_storage, log_name)
                    with open(log_file, 'a+') as f:
                        f.write('\n'.join(gz.read().splitlines()[2:]))

    def filter_date(self, date):
        date = datetime.strptime(date, '%Y-%m-%d')

        def filter_before(cond, target):
            if cond:
                return target <= datetime.strptime(cond, '%Y-%m-%d')
            return True

        def filter_after(cond, target):
            if cond:
                return target >= datetime.strptime(cond, '%Y-%m-%d')
            return True

        return filter_before(self.env.before, date)\
               and filter_after(self.env.after, date)

    @property
    def connection(self):
        return S3Connection(
            self.aws_key,
            self.aws_secret,
            host=self.aws_region)

    @property
    def aws_key(self):
        return self.env.access_key

    @property
    def aws_secret(self):
        return self.env.secret_key

    @property
    def log_bucket(self):
        return self.env.bucket_name

    @property
    def aws_region(self):
        return self.env.s3_region

    @property
    def fetch_storage(self):
        storage_name = self.env.storage
        if not os.path.exists(storage_name):
            os.mkdir(storage_name)

        return os.path.abspath(storage_name)
