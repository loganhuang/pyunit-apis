import re

if __name__ == '__main__':
    data = {"phoneNo": "18701082122", "smsCode": "111111", "appid": "${appid}+wijgjjoi${billNo}", "billNo": "${billNo}"}

    def double(matched):
        value = int(matched.group('value'))
        return str(value * 2)

    s = 'A23G4HFD567'
    print(re.sub('(?P<value>\d+)', double, s))

    def get_value(matched):
        cached = {"appid":"1256983258", "billNo":"78954228"}
        key = matched.group('value')
        key = key[2:-1]
        if key in cached.keys():
            return cached[key]
        return ""



    for key in data:
        data[key] = re.sub('(?P<value>\${.*?})', get_value, data[key])

    print(data)
