import http.server
import socketserver
import threading


class ThreadedHTTPHandler(http.server.SimpleHTTPRequestHandler):
    """
    Custom handler to process GET requests in separate threads.
    """

    def do_GET(self) -> None:
        """
        Handles GET request, sends a text message after a simulated delay.
        :return: nothing
        """
        thread_name = threading.current_thread().name
        print(f"{thread_name}: Received request for {self.path}")

        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()

        response_message = f"Hello from thread: {thread_name}\nRequest path: {self.path}"
        self.wfile.write(response_message.encode("utf-8"))
        print(f"{thread_name}: Finished responding to {self.path}")


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """
    This class combines HTTPServer with ThreadingMixIn to handle each request in a new thread.
    """
    pass


def run_server(port: int = 8080) -> None:
    """
    Starts the threaded HTTP server on the specified port.
    :param port: Port number to listen on
    :return: nothing
    """
    server_address = ('', port)
    httpd = ThreadedHTTPServer(server_address, ThreadedHTTPHandler)
    print(f"http://localhost:{port}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server shutdown.")
        httpd.shutdown()


if __name__ == '__main__':
    run_server()
