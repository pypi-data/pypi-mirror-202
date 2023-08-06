import sys
import os
import random
import json
import time
from urllib.parse import urlparse
import urllib.parse
import http.client

def SetKey(key):
    if key == "":
        print("Please set a key")
    else:
        print("Key set")

def sdapi(query2, width, height, samples, name):
    query = urllib.parse.quote(query2)
    img = name
    conn = http.client.HTTPSConnection("stablediffusionapi.com")
    payload = ''

    if width < 512:
        width = urllib.parse.quote(512)
    else:
        width = urllib.parse.quote(width)

    if width > 1024:
        width = urllib.parse.quote(1024)
    else:
        width = urllib.parse.quote(width)

    if height < 512:
        height = urllib.parse.quote(512)
    else:
        height = urllib.parse.quote(height)

    if height > 1024:
        wiheightdth = urllib.parse.quote(1024)
    else:
        height = urllib.parse.quote(height)

    headers = {
    'key': key
    }
    uriPrompt = str("/api/v3/text2img?prompt=" + query + "&width=" + width + "&height="+ height +"&samples=1")
    conn.request("POST", uriPrompt, payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data)

    jrespone = json.loads(data)

    if jrespone["output"]:
        print(jrespone["output"])
        url = jrespone["output"]
        urlHost = url[0]
        uri = urlHost
        print (urlHost)

        parsed = urlparse(uri)

        print(parsed)

        base = parsed.netloc
        print(base)

        path = parsed.path
        print(path)

        with_path = base + '/'.join(path.split('/')[:-1])
        print(with_path)

        print(path.split('/')) 

        conn.close()

        conn = http.client.HTTPSConnection(base)
        payload = ''
        headers = {}
        conn.request("GET", path, headers)
        res = conn.getresponse()
        data = res.read()

        if res.status == 200:
            with open(img, "wb") as f:
                f.write(data)
                print("Image downloaded successfully!")
        else:
            print(f"Error downloading image: {response.status} {response.reason}")
        conn.close()
    else:
        print("No results")
        print(jrespone["fetch_result"])
        timetotry = jrespone["eta"]
        print("Trying in: ", timetotry)
        time.sleep(timetotry)
        conn.close()
        conn.request("POST", jrespone["fetch_result"], payload, headers)
        fetchResponse = conn.getresponse()
        fetchData = fetchResponse.read()

        jFetchData = json.loads(fetchData)

        jFetch = jFetchData["output"]

        print(jFetch)

        parsed = urlparse(jFetch[0])

        print(parsed)

        base = parsed.netloc
        print(base)

        path = parsed.path
        print(path)

        with_path = base + '/'.join(path.split('/')[:-1])
        print(with_path)

        print(path.split('/')) 

        conn.close()

        conn = http.client.HTTPSConnection(base)
        payload = ''
        headers = {}
        conn.request("GET", path, payload, headers)
        res = conn.getresponse()
        data = res.read()


        if res.status == 200:
            with open(img, "wb") as f:
                f.write(data)
                print("Image downloaded successfully!")
        else:
            print(f"Error downloading image: {response.status} {response.reason}")
        conn.close()
    conn.close()
