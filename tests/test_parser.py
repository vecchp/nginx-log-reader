import pytest
from collections import defaultdict

from nginx_parser.nginx import parse_log_entry, LogEntry, build_summary

sample_entries = [
    (
        '10.10.180.161 - 50.112.166.232, 192.33.28.238 - - - [02/Aug/2015:15:56:14 +0000]  https https https "GET /our-products HTTP/1.1" 200 35967 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36"',
        LogEntry(route='/our-products', status_code='200')
    ),
    (
        '50.112.166.232 - 50.112.166.232, 192.33.28.238, 50.112.166.232,127.0.0.1 - - - [02/Aug/2015:15:56:14 +0000]  http https,http https,http "GET /api/v1/user HTTP/1.1" 200 3350 "https://release.dollarshaveclub.com/our-products" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36"',
        LogEntry(route='/api/v1/user', status_code='200')

    ),
    (
        '66.249.67.54 - 66.249.67.54, 192.33.28.238, 66.249.67.54,127.0.0.1 - - - [03/Aug/2015:14:23:08 +0000]  http https,http https,http "GET /post-shave HTTP/1.1" 301 131 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"',
        LogEntry(route='/post-shave', status_code='301')
    ),
    (
        '10.10.180.40 - 66.249.67.123, 192.33.28.238 - - - [03/Aug/2015:08:34:48 +0000]  http http http "GET / HTTP/1.1" 403 135 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"',
        LogEntry(route='/', status_code='403')
    ),
    (
        '10.10.180.40 - 222.186.21.41 - - - [03/Aug/2015:15:05:12 +0000]  http http http "GET /manager/html HTTP/1.1" 404 564 "-" "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)"',
        LogEntry(route='/manager/html', status_code='404')
    )
]


@pytest.mark.parametrize("log_entry,expected", sample_entries)
def test_parse_line(log_entry, expected):
    parsed_entry = parse_log_entry(log_entry)
    assert parsed_entry == expected


metric_samples = [
    (
        [
            LogEntry(route='/manager/html', status_code='200')
        ],
        {
            '20x': 1
        }
    ),
    (
        [
            LogEntry(route='/manager/html', status_code='200'),
            LogEntry(route='/logout', status_code='500'),
            LogEntry(route='/manager/html', status_code='301'),
            LogEntry(route='/manager/html', status_code='500'),
            LogEntry(route='/api/users', status_code='200'),
            LogEntry(route='/logout', status_code='500'),
            LogEntry(route='/logout', status_code='500')
        ],
        {
            '20x': 2,
            '30x': 1,
            '50x': 4,
            '/manager/html': 1,
            '/logout': 3,
        }
    )

]


@pytest.mark.parametrize("metrics,expected", metric_samples)
def test_build_summary(metrics, expected):
    metric_summary = defaultdict(int)
    for metric in metrics:
        build_summary(metric, metric_summary)

    assert (metric_summary == expected)
