def app(environ, start_response):
    status = '200 OK'
    headers = [('Content-Type', 'text/plain')]
    start_response(status, headers)

    data = environ['QUERY_STRING'].split('&')
    body = '\n'.join(data).encode('utf-8')

    return [body]
