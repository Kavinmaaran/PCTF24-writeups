#!/bin/bash
echo "p_ctf{71M3_F0R_4_N3W_Kw35710N}" > ./webserver/files/blahblah.txt
echo "block" > ./webserver/files/block.txt
gunicorn --workers=3 -b 127.0.0.1:5001 --chdir /application/anotherserver/ c:app &
gunicorn --workers=3 -b 0.0.0.0:5000 --chdir /application/webserver/ app:app
# python webserver/app.py &
# python anotherserver/c.py