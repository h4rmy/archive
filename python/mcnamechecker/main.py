import requests, time, json, simplejson
#wordlist = requests.get("https://random-word-api.herokuapp.com/all").json()
wordlist = open("input.txt").read().splitlines()
print(wordlist)
i = 0
ratelimit = {'error': 'TooManyRequestsException', 'errorMessage': 'The client has sent too many requests within a certain amount of time'}

for word in wordlist:
    try:
        #request if word is available
        mcapi = requests.get("https://api.mojang.com/users/profiles/minecraft/" + word).json()
        print(mcapi)
        if mcapi == ratelimit:
            while mcapi == ratelimit:
                mcapi = requests.get("https://api.mojang.com/users/profiles/minecraft/" + word).json()
                i = i + 1
                print("rate limited x" + str(i))
                time.sleep(603)
        with open('usernames.txt', 'a') as f:
            if mcapi == ratelimit:
                continue
            else:
                f.write(str(mcapi) + "\n")
    except simplejson.errors.JSONDecodeError:
        with open('usernames.txt', 'a') as f:
            if mcapi == ratelimit:
                continue
            else:
                f.write(str(word) + "\n")
        print(word)
    time.sleep(1)
