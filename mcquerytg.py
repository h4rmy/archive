import logging, time
from datetime import datetime
from mcstatus import JavaServer
from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = 'tgapi'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    await message.reply("/srv [ip] [stat/plugins]")

@dp.message_handler(commands=['srv'])
async def server(message: types.Message):
    try:
        args = message.get_args().split()
        if args[1] == "stat":
            try:
                now = datetime.now()
                timelol = now.strftime("%H:%M:%S")
                timelol = str(timelol)
                print(f'[{timelol}] [@{message.from_user.username}] {message.from_user.first_name} {args}')
                srv = JavaServer.lookup(args[0])
                query = srv.query()
                host = srv.address.host
                status = srv.status()
                port = str(srv.address.port)
                latency = str(round(srv.ping(), 2))
                names = "\n- ".join(query.players.names)

                n = "\n"
                await message.answer(f'{host}:{port} [{status.players.online}/{status.players.max}]' + n +
                                     f'ping: {latency}ms' + n +
                                     f'players online:\n- {names}' + n +
                                     f'version: {query.software.version}' + n +
                                     f'brand: {query.software.brand}')
            except:
                await message.answer("не бумбум")
        elif args[1] == "plugins":
            try:
                now = datetime.now()
                timelol = now.strftime("%H:%M:%S")
                timelol = str(timelol)
                print(f'[{timelol}] [@{message.from_user.username}] {message.from_user.first_name} {args}')
                srv = JavaServer.lookup(args[0])
                query = srv.query()
                rawplugins = query.software.plugins
                plugins = [i.split()[0] for i in rawplugins]
                try:
                    plugins.sort()
                    return plugins
                finally:
                    plugins = "\n".join(plugins)
                    await message.answer(plugins)
            except:
                await message.answer("не бумбум")
    except IndexError:
        now = datetime.now()
        timelol = now.strftime("%H:%M:%S")
        timelol = str(timelol)
        print(f'[{timelol}] [@{message.from_user.username}] {message.from_user.first_name} {args}')
        await message.answer("no bitches?")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
