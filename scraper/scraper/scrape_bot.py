import http.server
import socketserver
from urllib.parse import parse_qs

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scraper.spiders.imdb_spider import ImdbSpider


def main():
    PORT = 8000

    class MyHttpRequestHandler(http.server.BaseHTTPRequestHandler):
        def _set_headers(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        def do_GET(self):
            self._set_headers()
            with open('index.html', 'rb') as in_:
                self.wfile.write(in_.read())

        def do_POST(self):
            data = self.rfile.read().decode('utf-8')

            data = parse_qs(data, keep_blank_values=True)

            project_settings = get_project_settings()
            project_settings.set('user_config', data)
            process = CrawlerProcess(settings=project_settings)

            process.crawl(ImdbSpider)
            process.start()


    Handler = MyHttpRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Http Server Serving at port", PORT)
        httpd.serve_forever()


if __name__ == '__main__':
    main()
