import argparse
import codecs
import sys

from . import log, setup_logger
from .auth import parse_authentication
from .confluence_api import create_confluence_api
from .confluence import ConfluencePageManager
from .constants import DEFAULT_CONFLUENCE_API_VERSION


def main():
    parser = argparse.ArgumentParser(description='Dumps Confluence page in storage format')
    parser.add_argument('page_id', type=str, help='Configuration file')
    parser.add_argument('-u', '--url', type=str, help='Confluence Url')
    auth_group = parser.add_mutually_exclusive_group(required=True)
    auth_group.add_argument('-a', '--auth', type=str, help='Base64 encoded user:password string')
    auth_group.add_argument('-U', '--user', type=str, help='Username (prompt password)')
    parser.add_argument('-o', '--output', type=str, help='Output file|stdout|stderr', default='stdout')
    parser.add_argument('-v', '--verbose', action='count')

    args = parser.parse_args()

    auth = parse_authentication(args.auth, args.user)
    setup_logger(args.verbose)

    confluence_api = create_confluence_api(DEFAULT_CONFLUENCE_API_VERSION, args.url, auth)
    page_manager = ConfluencePageManager(confluence_api)
    page = page_manager.load(args.page_id)

    if args.output.lower() == 'stdout':
        f = sys.stdout
    elif args.output.lower() == 'stderr':
        f = sys.stderr
    else:
        f = codecs.open(args.output, 'w', encoding='utf-8')

    with f:
        f.write(page.body)

    log.info('Complete!')


if __name__ == '__main__':
    main()
