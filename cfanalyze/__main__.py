#!/usr/bin/env python

import optparse
import os
import sys
import logging

from .fetch import Fetcher
from .analyze import RefererAnalyzer, ContentTrafficAnalyzer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


def main():
    parser = optparse.OptionParser(usage='usage: %prog [options] log_prefix')
    parser.add_option('-a', '--access-key',
                      dest='access_key',
                      help='S3 Access Key',
                      default=os.environ.get('AWS_ACCESS_KEY', None))
    parser.add_option('-k', '--secret-key',
                      dest='secret_key',
                      help='S3 Secret Key',
                      default=os.environ.get('AWS_SECRET_KEY', None))
    parser.add_option('-b', '--bucket-name',
                      dest='bucket_name',
                      help='Log bucket name')
    parser.add_option('-r', '--region',
                      dest='s3_region',
                      help='S3 Region',
                      default='s3-ap-northeast-1.amazonaws.com')
    parser.add_option('-s', '--storage',
                      dest='storage',
                      default='cflogs',
                      help='Directory used by log analyzer')
    parser.add_option('-t', '--type',
                      dest='analyze_type',
                      help='Analyze type: referer, content_traffic',
                      choices=['referer', 'content_traffic'],
                      default='referer')
    parser.add_option('--skip-fetch',
                      dest='skip_fetch',
                      action='store_true')
    parser.add_option('--before',
                      dest='before',
                      help='Log before %Y-%m-%d')
    parser.add_option('--after',
                      dest='after',
                      help='Log after %Y-%m-%d')

    options, args = parser.parse_args()

    if len(args) != 1:
        parser.print_help()
        return 1

    if not options.skip_fetch:
        fetcher = Fetcher(options, args[0], logger=logger)
        fetcher.fetch()

    if options.analyze_type == 'referer':
        for r, c in RefererAnalyzer(options).run():
            print '%d\t%s' % (c, r)
    elif options.analyze_type == 'content_traffic':
        analyzer = ContentTrafficAnalyzer(options)

        print '{0:80} {1:>10} {2:>10}'.format('URL', 'Bytes(MB)', 'Hit')
        for url, c in analyzer.run():
            print '{0:80} {1:>10.4} {2:>10}'.format(
                url,
                c[0] / 1024 / 1024.0,
                c[1])

        print 'Grand Total:\nHit: {0:,}\nBytes(MB): {1:,}\n'.format(
            analyzer.total_count,
            analyzer.total_traffic / 1024 / 1024)

    return 0

if __name__ == '__main__':
    sys.exit(main())
