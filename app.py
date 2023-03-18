from request import Request,scope_to_request
from response import ASGIResponse
import os
from pathlib import Path
import mimetypes



async def not_found(request):
    content = "Page not found."
    headers = [("Content-Type", "text/plain")]
    return ASGIResponse(content, status=404, headers=headers) 

async def http_handler(urlpattern,request,response):
        #response = response
        response = urlpattern.get(request.path,not_found)
        return await response(request) 
        
async def process_middleware(middlewares,request,response):
    req,res = request,response    
    for middleware in middlewares:
        return  await middleware(request,response)
    return (req,res)    

                    
            

class AsgiApplication:
    urlpattern = {}
    middlewares = []

    def __init__(self,urlpattern={},middlewares = []):
        self.urlpattern = urlpattern
        self.middlewares = middlewares


    def add_route(self,path,func):
        self.urlpattern[str(path)] = func

    def add_middleware(self,middleware):
        self.middlewares.append(middleware)

    
    async def __call__(self,scope, receive, send):
        assert scope['type'] == 'http'
        request = await scope_to_request(scope,receive)
        response = ASGIResponse()
        response = await http_handler(self.urlpattern, request,response)
        _,response = await process_middleware(self.middlewares, request,response)
        await response(scope, receive, send)

