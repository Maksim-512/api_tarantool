FROM tarantool/tarantool:latest

COPY . /usr/src/app
WORKDIR /usr/src/app

EXPOSE 3301

CMD ["tarantool", "init.lua"]
