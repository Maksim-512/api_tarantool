box.cfg {
    listen = 3301,
    log_level = 5,
}

box.schema.space.create('test', {if_not_exists = true})
box.space.test:format({
    {name = 'key', type = 'string'},
    {name = 'value', type = 'any'},
})
box.space.test:create_index('primary', {
    parts = {'key'},
    if_not_exists = true
})


require('console').start()

