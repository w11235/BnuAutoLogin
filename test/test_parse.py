import execjs

ctx = execjs.compile(open('base64.js').read()+open('test.js').read())
# ctx = ctx.compile()
# print(ctx.call('add', 1, 2))
print(ctx.call('encode', 'test'))
