class ASGIResponse:
   
    
    def __init__(self, content="", status=200, headers=[("Content-Type", "application/json")]):
        self.content = content
        self.status = status
        self.headers = headers

    async def __call__(self, scope, receive, send):
        headers = [(key.encode(), value.encode()) for key, value in self.headers]
        await send({
            "type": "http.response.start",
            "status": self.status,
            "headers": headers,
        })
        await send({
            "type": "http.response.body",
            "body": self.content.encode(),
        })

