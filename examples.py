import vk

params = {
    "client_id": "111111",
    "scope": ("friends", "audio")    
}

#auth
auth = vk.VK_AUTH(params)
auth.authorization('your_mail@gmail.com', 'password')
access_token = auth.get_access_token()
user_id = auth.get_user_id()

#api request
api = VK_API(access_token, user_id)
api.request('users.get', fields=("last_name", "first_name"))