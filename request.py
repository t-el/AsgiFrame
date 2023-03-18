from urllib.parse import unquote

class Request:
    def __init__(self, method: str, path: str, headers: dict, query_params: dict, body: bytes):
        self.method = method
        self.path = path
        self.headers = headers
        self.query_params = query_params
        self.body = body
    

    def __str__(self):
        return self.method+":"+self.path



def get_params(query_string):
        query_params = {}
        for pair in query_string.split("&"):
            if not pair:
                continue
            key_value = pair.split("=", 1)
            key = unquote(key_value[0])
            value = unquote(key_value[1]) if len(key_value) > 1 else ""
            query_params[key] = value
        
        return query_params  


async def scope_to_request(scope,receive) -> Request:

    method = scope["method"]
    path = scope["path"]
    #raw_path = unquote(scope["raw_path"].decode()) 
    headers = {}
    for name, value in scope.get("headers", []):
        headers[name.decode()] = value.decode()
        
    query_params = get_params(scope['query_string'].decode())
    
    body = b""
    more_body = True
    while more_body:
        message = await receive()
        body += message.get("body", b"")
        more_body = message.get("more_body", False)
    

    return Request(method, path, headers, query_params, body)
