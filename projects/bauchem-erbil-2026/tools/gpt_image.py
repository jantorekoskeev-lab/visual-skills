import os, json, base64, urllib.request, time

def gen(model, prompt, size="1536x1024", out="/tmp/t.png", quality=None):
    body = {"model": model, "prompt": prompt, "size": size, "n": 1}
    if quality: body["quality"] = quality
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"],
                 "Content-Type": "application/json"})
    t = time.time()
    try:
        r = json.load(urllib.request.urlopen(req, timeout=300))
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}: {e.read().decode()[:300]}"
    d = r["data"][0]
    raw = base64.b64decode(d["b64_json"]) if "b64_json" in d else urllib.request.urlopen(d["url"]).read()
    open(out, "wb").write(raw)
    return f"OK {model} {size} -> {out} {len(raw)//1024} KB, {time.time()-t:.0f}s"

if __name__ == "__main__":
    import sys
    print(gen(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
