from response import ASGIResponse

async def middleware1(request,response):
    print('REQUEST  : '+ request.path)
    #response = ASGIResponse(status=401,content='UNAUTHOREZIDE')
    return(request,response)


async def middleware2(request,response):
    print('REQUEST2  : '+ request.path)
    return(request,response)


async def middleware3(request,response):
    print('REQUEST3  : '+ request.path)
    
    print('M3 :'+response.content)
    return(request,response)   

  

