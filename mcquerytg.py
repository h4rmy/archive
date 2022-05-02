import logging, requests, json
import socket
from datetime import datetime
from mcstatus import JavaServer
from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = 'tgapi'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
whitelist = [555091019, 328508967, 615744908]
            #h4rmy      crinny      slamerr
            
@dp.message_handler(commands=['id'])
async def welcome(message: types.Message):
    now = datetime.now()
    timelol = now.strftime("%H:%M:%S")
    timelol = str(timelol)
    print(f'[{timelol}] [@{message.from_user.username}] {message.from_user.first_name} id: [{str(message.chat.id)}')
    await message.reply("<code>" + str(message.chat.id) + "</code>", parse_mode="HTML")

@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    now = datetime.now()
    timelol = now.strftime("%H:%M:%S")
    timelol = str(timelol)
    print(f'[{timelol}] [@{message.from_user.username}] {message.from_user.first_name} started the bot')
    await message.reply("/srv [ip/host]\n/q [ip/host] [stat/plugins]\n/id\n/owner")

@dp.message_handler(lambda message: message.chat.id not in whitelist)
async def checker(message):
    now = datetime.now()
    timelol = now.strftime("%H:%M:%S")
    timelol = str(timelol)
    print(f'[{timelol}] [@{message.from_user.username}] {message.from_user.first_name} access denied')
    await message.answer_photo("https://github.com/h4rmy/filehosting/blob/main/2.png?raw=true")

@dp.message_handler(commands=['owner'])
async def welcome(message: types.Message):
    now = datetime.now()
    timelol = now.strftime("%H:%M:%S")
    timelol = str(timelol)
    print(f'[{timelol}] [@{message.from_user.username}] {message.from_user.first_name} /owner')
    await message.reply("<b>@h4rmy</b>", parse_mode="HTML")

@dp.message_handler(commands=['srv'])
async def server(message: types.Message):
    args = message.get_args().split()
    now = datetime.now()
    timelol = now.strftime("%H:%M:%S")
    timelol = str(timelol)
    print(f'[{timelol}] [@{message.from_user.username}] {message.from_user.first_name} /srv {args}')


    json = requests.get(f'https://api.mcsrvstat.us/2/{args[0]}').json()

    hostname = json.get("hostname", "Not found")
    software = json.get("software", "Vanilla")
    ip = json["ip"]
    version = json["version"]
    p = json["players"]["online"]
    p1 = json["players"]["max"]
    query = json["debug"]["query"]
    online = json["online"]

    if len(json["motd"]["clean"]) == 1:
        motd0 = json["motd"]["clean"]
        motd = "".join(motd0)
    else:
        motd0 = json["motd"]["clean"][0]
        motd1 = json["motd"]["clean"][1]
        motd = motd0 + "\n" + motd1


    if "players" not in json:
        players = "Not found"
    else:
        if "list" not in "players":
            players = "Not found"
        else:
            players = json["players"]["list"]

    if "info" not in json:
        info = "Not found"
    else:
        info = json["info"]["clean"]

    await message.answer(f' <b> [Hostname]</b>: {hostname} [{p}/{p1}]\n' +
                         f'<b> [IP]</b>: {ip}\n' +
                         f'<b> [Version]</b>: {version}\n' +
                         f'<b> [Core]</b>: {software}\n' +
                         f'<b> [Query]</b>: {query}\n' +
                         f'<b> [Online]</b>: {online}\n' +
                         f'<b> [MOTD]</b>:\n{motd}\n' +
                         f'<b> [Info]</b>:\n {info}\n' +
                         f'<b> [Players]</b>: \n - {players}\n', parse_mode="HTML")


@dp.message_handler(commands=['q'])
async def query(message: types.Message):
    try:
        args = message.get_args().split()
        if args[1] == "stat":
            try:
                now = datetime.now()
                timelol = now.strftime("%H:%M:%S")
                timelol = str(timelol)
                print(f'[{timelol}] [@{message.from_user.username}] {message.from_user.first_name} /q {args}')
                srv = JavaServer.lookup(args[0])
                query = srv.query()
                host = srv.address.host
                status = srv.status()
                port = str(srv.address.port)
                latency = str(round(srv.ping(), 2))
                names = "\n- ".join(query.players.names)

                n = "\n"
                await message.answer(f'<b> [Hostname]: {host}:{port}</b> [{status.players.online}/{status.players.max}]' + n +
                                     f'<b> [Ping</b>: {latency}ms' + n +
                                     f'<b> [Ip</b>: {query.raw["hostip"]}' + n +
                                     f'<b> [Version</b>: {query.software.version}' + n +
                                     f'<b> [Brand</b>: {query.software.brand}' + n +
                                     f'<b> [Map</b>: {query.raw["map"]}' + n +
                                     f'<b> [Players online</b>:\n- {names}', parse_mode="HTML")
            except socket.timeout:
                await message.answer_photo("https://github.com/h4rmy/filehosting/blob/main/3.png?raw=true")
        elif args[1] == "plugins":
            try:
                now = datetime.now()
                timelol = now.strftime("%H:%M:%S")
                timelol = str(timelol)
                print(f'[{timelol}] [@{message.from_user.username}] {message.from_user.first_name} /q {args}')
                srv = JavaServer.lookup(args[0])
                query = srv.query()
                rawplugins = query.software.plugins
                plcount = len(rawplugins)
                plugins = [i.split()[0] for i in rawplugins]
                try:
                    plugins.sort()
                    return plugins
                finally:
                    plugins = "\n".join(plugins)
                    await message.answer(plugins + "\n\n<b>Plugins</b>: " + str(plcount), parse_mode="HTML")
            except socket.timeout:
                await message.answer_photo("https://github.com/h4rmy/filehosting/blob/main/3.png?raw=true")
    except IndexError:
        now = datetime.now()
        timelol = now.strftime("%H:%M:%S")
        timelol = str(timelol)
        print(f'[{timelol}] [@{message.from_user.username}] {message.from_user.first_name} {args}')
        await message.answer_photo("https://github.com/h4rmy/filehosting/blob/main/1.png?raw=true")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
