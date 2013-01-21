import urllib 
import urllib2 
import cookielib
import re

from HTMLParser import HTMLParser

class Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.params = {}

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()        
        if tag == "form":
            for n, v in attrs:
                if n == "action":
                    self.action_url = v
        elif tag == "input":
            attrs = dict((name, val) for name, val in attrs)
            if attrs["type"] in ["hidden", "text", "password"]:
                if "value" in attrs: 
                    self.params[attrs["name"]] = attrs["value"]
                else:
                    self.params[attrs["name"]] = ""   


class VK_AUTH():
    def __init__(self, params):
        self.auth_params = params
        self.auth_params["response_type"] = "token"
        self.auth_params["display"] = "popup"
        self.user_id = None
        self.access_token = None
        self.authorization_url = "http://oauth.vk.com/oauth/authorize"

    def __get_opener(self):
        return urllib2.build_opener(
            urllib2.HTTPCookieProcessor(cookielib.CookieJar()),
            urllib2.HTTPRedirectHandler()
        )

    def __obtaining_data(self, url):
        access_token_pattern = '(access_token)=(\w+)'
        user_id_pattern = '(user_id)=(\w+)'
        try:
            access_token = re.findall(access_token_pattern, url)[0][1]
            user_id = re.findall(user_id_pattern, url)[0][1]
            return access_token, user_id
        except:            
            return None

    def authorization(self, email, password):
        opener = self.__get_opener()
        params = urllib.urlencode(self.auth_params)
        try:
            request = opener.open(self.authorization_url, params)
            response = request.read()            
        except IOError:
            print "Can't open %s" % self.authorization_url
        else:
            parser = Parser()
            parser.feed(response)
            parser.close()        
            parser.params["email"] = email
            parser.params["pass"] = password
            return self.allow_access(parser.action_url, parser.params)            
            
    def allow_access(self, url, params):
        opener = self.__get_opener()
        params = urllib.urlencode(params)
        try:            
            request = opener.open(url, params)
            resp_url = request.geturl()
            self.access_token, self.user_id = self.__obtaining_data(resp_url)
        except IOError:
            print "Can't open %s" % url

    def get_access_token(self):
        return self.access_token

    def get_user_id(self):
        return self.user_id

            
class VK_API():
    def __init__(self, access_token, user_id):
        self.access_token = access_token
        self.user_id = user_id
        self.api_url = "https://api.vk.com/method/"

    def __get_url(self, method, fields):
        params = self.__get_params(fields)
        return urllib2.Request(self.api_url + method, params)

    def __get_params(self, fields):
        params = {
            "uids": self.user_id,
            "access_token": self.access_token
        }
        if fields:            
            params["fields"] = fields
        return urllib.urlencode(params)    

    def request(self, method, fields=None):
        url = self.__get_url(method, fields)
        try:
            request = urllib2.urlopen(url)
        except IOError:
            print "Can't open %s" % url
        response = request.read()
        return json.loads(response)