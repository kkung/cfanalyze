import os
import os.path
import glob


class CloudFrontLog(object):

    def __init__(self, name):
        super(CloudFrontLog, self).__init__()
        self.name = name

    def __iter__(self):
        with open(self.name) as f:
            for entry in f:
                yield entry.split('\t')


class Analyzer(object):

    def __init__(self, env):
        super(Analyzer, self).__init__()
        self.env = env

    def run(self):
        logs = glob.glob('%s/%s' % (self.fetch_storage, '*.log'))
        for log in logs:
            for entry in CloudFrontLog(log):
                self.map(entry)

        return self.reduce()

    def map(self, entry):
        raise NotImplementedError

    def reduce(self):
        raise NotImplementedError

    @property
    def fetch_storage(self):
        return os.path.abspath(self.env.storage)


class RefererAnalyzer(Analyzer):

    def __init__(self, env):
        super(RefererAnalyzer, self).__init__(env=env)
        self.referer = dict()

    def map(self, entry):
        self.referer[entry[9]] = self.referer.get(entry[9], 0) + 1

    def reduce(self):
        return sorted(self.referer.items(), key=lambda x: x[1], reverse=True)


class ContentTrafficAnalyzer(Analyzer):

    def __init__(self, env):
        super(ContentTrafficAnalyzer, self).__init__(env=env)
        self.entries = dict()
        self.total_count = 0
        self.total_traffic = 0

    def map(self, entry):
        bytes = int(entry[3])
        method = entry[5]
        content = entry[7]
        status = entry[8]

        if method == 'GET' and status in ('200', '304'):
            row = self.entries.get(content, None)
            if not row:
                self.entries[content] = (bytes, 1)
            else:
                self.entries[content] = (row[0] + bytes, row[1] + 1)

            self.total_count = self.total_count + 1
            self.total_traffic = self.total_traffic + bytes

    def reduce(self):
        return sorted(
            self.entries.items(),
            key=lambda x: x[1][1],
            reverse=True)
