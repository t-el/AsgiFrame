import uvicorn
from app import AsgiApplication
from response import ASGIResponse
from middlewares import middleware1,middleware2,middleware3

async def my_view(request):
    content = "Hello, world!"
    headers = [("Content-Type", "text/plain")]
    return ASGIResponse(content, status=200, headers=headers)

async def index(request):
    name = request.query_params.get('q',"world")
    content = f"Hello, {name}"
    headers = [("Content-Type", "text/plain")]
    return ASGIResponse(content, status=200, headers=headers)



app = AsgiApplication(urlpattern = {"/hello":my_view}, middlewares=[middleware1,middleware2])
app.add_route('/',index)
app.add_middleware(middleware3)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)