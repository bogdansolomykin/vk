import vk

params = {
    "client_id": "111111",         #your application id
    "scope": ("friends", "audio")  #access rights requested by your app
}                                  #see https://vk.com/developers.php?oid=-17680044&p=Application_Access_Rights

#auth
auth = vk.VK_AUTH(params)
auth.authorization('user_mail@gmail.com', 'password')
access_token = auth.get_access_token()
user_id = auth.get_user_id()

#api requests
api = VK_API(access_token, user_id)
user_info = api.request('users.get')
user_audios = api.request('audio.get', uid=user_id})
user_friends = api.request('friends.get', uid=user_id, fields="first_name, last_name, sex", order="name")

# more api methods: 
# https://vk.com/developers.php?oid=-17680044&p=API_Method_Description
# or 
# https://vk.com/developers.php?oid=-17680044&p=Advanced_API_Methods