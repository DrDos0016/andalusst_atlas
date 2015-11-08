# Placeholder external login to run on Python 2.7.10
import sys, urllib2, time, json

def main():
    ip = sys.argv[1]
    url = sys.argv[2]
    fn = str(ip + ".json")
    output = open("/var/projects/pmdu.org/assets/data/logins/" + fn, "w")
    response = urllib2.urlopen(url)
    data = json.load(response)
    token = data["access_token"]
    response = urllib2.urlopen("https://www.deviantart.com/api/draft15/user/whoami?access_token="+token)
    output.write(response.read())
    output.close()
    return True

if __name__ == "__main__":main()