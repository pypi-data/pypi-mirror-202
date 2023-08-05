from __future__ import unicode_literals, absolute_import
'''
 Copyright 2013-2019 Cofense, Inc.  All rights reserved.

 This software is provided by PhishMe, Inc. ("Cofense") on an "as is" basis and any express or implied warranties,
 including but not limited to the implied warranties of merchantability and fitness for a particular purpose, are
 disclaimed in all aspects.  In no event will Cofense be liable for any direct, indirect, special, incidental or
 consequential damages relating to the use of this software, even if advised of the possibility of such damage. Use of
 this software is pursuant to, and permitted only in accordance with, the agreement between you and Cofense.
'''

import asyncio
import argparse
import datetime
import sys
import os
from importlib import import_module
import json
import logging

from jinja2 import Environment, PackageLoader

from cofense_intelligence.outputs.JsonFileOutput import JsonFileOutput
from cofense_intelligence.outputs.TextFileOutput import TextFileOutput
from cofense_intelligence.outputs.CsvFileOutput import CsvFileOutput
from cofense_intelligence.outputs.CefFileOutput import CefFileOutput
from cofense_intelligence.outputs.StixFileOutput import StixFileOutput
from cofense_intelligence.outputs.Stix2FileOutput import Stix2FileOutput
from cofense_intelligence.outputs.HttpOutput import HttpOutput
from cofense_intelligence.outputs.SyslogOutput import SyslogOutput
from cofense_intelligence.core import CFIntelSync
from cofense_intelligence.api import IntelligenceAPI


def valid_date(date):
    try:
        return datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise argparse.ArgumentError('Not a valid date: {}'.format(date))


def valid_token(token):
    if len(token) != 32 and not isinstance(token, str):
        raise argparse.ArgumentError('Invalid authentication token. Ensure it is the correct user or password token')
    return token


def valid_name(integration_name):
    if not integration_name.isidentifier():
        raise RuntimeError('Invalid name, must be a valid python identifier See: https://docs.python.org/3.3/reference/lexical_analysis.html#identifiers')
    try:
        import_module(integration_name)
    except ImportError:
        pass
    else:
        raise RuntimeError('Name conflicts with the name of an existing Python package')

    return True


def setup_logger(args):
    if args.log_file == 'stdout':
        logging.basicConfig()
    else:
        logging.basicConfig(filename=args.log_file)

    logger = logging.getLogger()

    if args.log_level == 'info':
        logger.setLevel(logging.INFO)
    elif args.log_level == 'debug':
        logger.setLevel(logging.DEBUG)
    elif args.log_level == 'crit':
        logger.setLevel(logging.CRITICAL)
    elif args.log_level == 'warn':
        logger.setLevel(logging.WARN)

    return logger


def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args) # , **kwargs)
    return wrapped


@background
def run_for_format(arguments, style):
    logger = setup_logger(arguments)
    integrations = {'json': JsonFileOutput,
                    'cef': CefFileOutput,
                    'csv': CsvFileOutput,
                    'stix': StixFileOutput,
                    'stix2': Stix2FileOutput,
                    'list': TextFileOutput,
                    'http': HttpOutput,
                    'syslog': SyslogOutput}

    fmt = ensure_format(arguments, style)

    integration = integrations[style]

    config = {'CF_USER': arguments.username,
              'CF_PASS': arguments.password,
              'INTEL_FORMAT': fmt,
              'THREAT_TYPE': arguments.intel_type,
              'BASE_DIR': arguments.base_dir,
              'INTEGRATION': integration,
              'POSITION_FILE': f'{style}.pos',
              'ARGS': arguments}

    if arguments.proxy:
        logger.debug('Adding proxy data')
        proxy_config = {'PROXY_URL': arguments.proxy_addr}
        if arguments.proxy_user or arguments.proxy_pass:
            logger.debug('Adding proxy authentication data')
            proxy_config['PROXY_AUTH'] = True
            proxy_config['PROXY_USER'] = arguments.proxy_user
            proxy_config['PROXY_PASS'] = arguments.proxy_pass
        logger.debug('Updating the config with proxy data')
        config.update(proxy_config)

    if arguments.begin_date:
        logger.debug('Setting INIT_DATE')
        config['INIT_DATE'] = int(arguments.begin_date.timestamp())
        logger.debug('INIT_DATE set to {}'.format(config['INIT_DATE']))

    logger.debug('Creating the cofense handler')
    cf_handler = CFIntelSync(**config)

    logger.info(f'Running the {integration} integration...')
    cf_handler.run()
    logger.info(f'Integration {integration} complete.')


def ensure_format(args, format):
    if format == 'http':
        if not args.http_format:
            fmt = 'json'
        else:
            fmt = args.http_format
    elif format == 'cef' or format == 'syslog':
        fmt = 'cef'
    elif format == 'stix':
        fmt = 'stix'
    else:
        fmt = 'json'
    return fmt


def run_integration(args):
    if not args.formats:
        args.formats = ['json']

    loop = asyncio.get_event_loop()                                                # Have a new event loop
    looper = asyncio.gather(*[run_for_format(args, x) for x in args.formats])
    loop.run_until_complete(looper)


def execute():
    parser = argparse.ArgumentParser(description='Cofense Intelligence API Tool')

    subparsers = parser.add_subparsers()

    # Set up Run parsing
    run_parser = subparsers.add_parser('run',
                                       help='run Cofense Intelligence Integration')
    run_parser.add_argument('--username', '-u',
                            default=os.environ.get('COFENSE_USER'),
                            type=valid_token,
                            help='Cofense API username token, if not provided will use COFENSE_USER environment variable')
    run_parser.add_argument('--password', '-p',
                            default=os.environ.get('COFENSE_PASSWORD'),
                            type=valid_token,
                            help='Cofense API password token, if not provided will use COFENSE_PASSWORD environment variable')
    run_parser.add_argument('-f', '--formats', choices=['json', 'cef', 'stix', 'stix2', 'list', 'csv', 'http', 'syslog'], action='append', help='File output format')
    run_parser.add_argument('-d', '--begin-date', type=valid_date, help='Integration begin date')
    run_parser.add_argument('--intel-type', choices=['malware', 'phish', 'all'], default='malware', help='ThreatReport Intelligence type (default Malware)')
    run_parser.add_argument('--log-level', choices=['debug', 'info', 'warn', 'error', 'crit'], help='Logging level set', default='info')
    run_parser.add_argument('--log-file', help='Log file to write to', default='stdout')
    run_parser.add_argument('--proxy', action='store_true', help='Use proxy for api requests')
    run_parser.add_argument('--proxy-addr', help='Set proxy address, if using different plain and ssl proxies specify ssl proxy')
    run_parser.add_argument('--proxy-user', help='Proxy username')
    run_parser.add_argument('--proxy-pass', help='Proxy password')
    run_parser.add_argument('--base-dir', default=os.getcwd(), help='Base directory to run from')
    run_parser.add_argument('--http-url', help='The full URL to send data to')
    run_parser.add_argument('--http-format', choices=['json', 'cef', 'stix', 'stix2'], help='The format to send to the http server')
    run_parser.add_argument('--http-method', default='POST', help='The http method to use when sending to the web server')
    run_parser.add_argument('--http-proxy', help='Optional proxy for http requests')
    run_parser.add_argument('--http-proxy-username', help='Optional proxy username for the http output')
    run_parser.add_argument('--http-proxy-password', help='Optional proxy password for the http output')
    run_parser.add_argument('--http-basic-auth-user', help='Optional basic auth username for the http output')
    run_parser.add_argument('--http-basic-auth-pass', help='Optional basic auth password for the http output')
    run_parser.add_argument('--http-header', action='append', help='Additional headers for the http output. '
                                                                   'Use the format key:value')

    run_parser.add_argument('--http-splunk-sourcetype',
                            help="Optionally set the sourcetyp when sending to a Splunk HTTP Event Collector")
    run_parser.add_argument('--http-splunk-token',
                            help='Auth token for data being sent to a splunk HTTP Event Collector. '
                                 'See http://dev.splunk.com/view/event-collector/SP-CAAAE7F')

    run_parser.add_argument('--syslog-host', help='Address to send syslog messages to', default='127.0.0.1')
    run_parser.add_argument('--syslog-port', help='Port to send syslog messages to', default=514, type=int)
    run_parser.add_argument('--syslog-level', help='Syslog level', default=5, type=int)
    run_parser.add_argument('--syslog-facility', help='Syslog facility', default=3, type=int)
    run_parser.add_argument('--syslog-protocol',
                            help='Use TCP or UDP to send the syslog messages',
                            choices=['TCP', 'UDP'],
                            default='UDP')

    run_parser.set_defaults(func=run_integration)

    # set up create_integration parsing
    create_parser = subparsers.add_parser('create', help='create custom Cofense Integration')
    create_parser.add_argument('name', help='Integration name')
    create_parser.add_argument('--target', default=os.getcwd(), help='Target directory for integration module')
    create_parser.set_defaults(func=create_integration)

    # Search parsing
    search_parser = subparsers.add_parser('search', help='search for Cofense Threat Intelligence reports. Output will be Threat ID, Threat Type and Brand or Malware Family')
    search_parser.add_argument('params', nargs='*', help='Search key value params (formatted key=value). See https://threathq.com/docs/rest_api_reference.html#threat for available params')
    search_parser.add_argument('--username', '-u',
                            default=os.environ.get('COFENSE_USER'),
                            type=valid_token,
                            help='Cofense API username token, if not provided will use COFENSE_USER environment variable')
    search_parser.add_argument('--password', '-p',
                            default=os.environ.get('COFENSE_PASSWORD'),
                            type=valid_token,
                            help='Cofense API password token, if not provided will use COFENSE_PASSWORD environment variable')
    search_parser.add_argument('-v', '--verbose', action='store_true', help='Output the full json of the threat report')
    search_parser.add_argument('-f', '--file', action='store_true', help='Output full json of each threat report to a file in a "results" directory')

    search_parser.set_defaults(func=search)

    if len(sys.argv) == 1:
        parser.print_help()
        parser.error('Missing action')
        sys.exit(1)

    args = parser.parse_args()

    args.func(args)


def create_integration(args):
    print('creating integration: ' + args.name)

    valid_name(args.name)
    camel_case_name = ''.join(char for char in args.name.title() if char != '_')

    target_dir = args.target

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    env = Environment(loader=PackageLoader('cofense_intelligence', 'templates'))
    template = env.get_template('integration_template.py-ptl')
    output_file = template.render(integration_name=args.name, camel_case_name=camel_case_name)

    with open(args.name + '.py', 'w') as outfile:
        outfile.write(output_file)


def search(args):
    params = {}

    for pair in args.params:
        try:
            key, value = pair.split('=', 1)
        except ValueError:
            raise RuntimeError('Parameter [{}] could not be unpacked. Ensure params are passed as key=value pairs'.format(pair))

        params[key] = value

    auth = (args.username, args.password)

    api_handler = IntelligenceAPI(auth=auth)

    threat_reports = api_handler.threat_search(**params)

    if not args.verbose or not args.file:
        print("Threat ID | Threat Type | Malware Family / Brand")

    for report in threat_reports:
        if not args.verbose or not args.file:
            print_summary(report)
        if args.verbose:
            print_full(report)
        if args.file:
            write_to_file(report)


def print_summary(report):
    threat_id = report.threat_id
    threat_type = report.threat_type

    if threat_type == 'MALWARE':
        desc = report.malware_families
    else:
        desc = report.brands

    print(threat_id, ' | ', 'threat_type', ' | ', desc)


def print_full(report):
   print(report.json)


def write_to_file(report):
    results_dir = os.path.join(os.getcwd(), 'reports')
    results_file = os.path.join(results_dir, str(report.threat_id) + '.json')

    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    with open(results_file, 'w') as report_file:
        json.dump(report.json, report_file)


if __name__ == '__main__':
    execute()
