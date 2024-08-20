from aiohttp import web
import asyncio
import jwt
import asynctnt

tarantool_conn = asynctnt.Connection(host='tarantool', port=3301)

SECRET_KEY = 'my_secret_key'

app = web.Application()
routes = web.RouteTableDef()

users = {
    'admin': 'presale'
}


def generate_token(username):
    """Генерация токена"""

    token = jwt.encode(
        {'username': username},
        SECRET_KEY,
        algorithm='HS256'
    )
    return token


def token_required(func):
    """Авторизация"""

    async def wrapper(request):
        token = request.headers.get('Authorization')
        if not token:
            return web.json_response({'message': 'The token is missing'}, status=401)

        try:
            token = token.split(' ')[1]
            jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except:
            return web.json_response({'message': 'The token is invalid'}, status=401)
        return await func(request)

    return wrapper


@routes.post('/api/login')
async def login(request):
    """Аутентификация"""

    auth_data = await request.json()
    username = auth_data.get('username')
    password = auth_data.get('password')

    if username in users and users[username] == password:
        token = generate_token(username)
        return web.json_response({'token': token})

    return web.json_response({'message': 'Invalid credentials'}, status=401)


@routes.post('/api/write')
@token_required
async def write_data(request):
    """Запись данных"""

    data = await request.json()
    data = data.get('data')

    if not data:
        return web.json_response({'message': 'No data'}, status=400)

    try:
        if not tarantool_conn.is_connected:
            await tarantool_conn.connect()

        tasks = [tarantool_conn.call('box.space.test:replace', [[key, value]]) for key, value in data.items()]
        await asyncio.gather(*tasks)
        return web.json_response({'status': 'success'})
    except Exception as e:
        return web.json_response({'message': f'Error: {e}'}, status=500)


@routes.post('/api/read')
@token_required
async def read_data(request):
    """Чтение данных"""

    keys = await request.json()
    keys = keys.get('keys')

    if not keys:
        return web.json_response({'message': 'No keys'}, status=400)

    try:
        if not tarantool_conn.is_connected:
            await tarantool_conn.connect()

        tasks = [tarantool_conn.call('box.space.test:get', [[key]]) for key in keys]
        results = await asyncio.gather(*tasks)
        result_dict = {key: val[0][1] if val else None for key, val in zip(keys, results)}
        return web.json_response({'data': result_dict})
    except Exception as e:
        return web.json_response({'message': f'Error: {e}'}, status=500)


app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=5005)
