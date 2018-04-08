from queue import Queue

from nginx_parser.tail import FileTail
from nginx_parser.nginx import NginxSummary


def main():
    shared_queue = Queue()
    file_tailer = FileTail('/var/log/nginx/access.log', shared_queue)
    nginx_summary = NginxSummary('/var/log/stats.log', shared_queue)

    nginx_summary.start()
    file_tailer.start()


if __name__ == '__main__':
    main()
