import vk

params = {
    "client_id": "111111",
    "scope": ("friends", "audio")    
}

auth = vk.VK_AUTH(params)
auth.authorization('your_mail@gmail.com', 'password')
access_token = auth.get_access_token()
user_id = auth.get_user_id()
print access_token, user_id