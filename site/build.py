#!/usr/bin/env python3
"""Generate the GitHub Pages download site, split into two channels by the
GitHub Release `prerelease` flag:

  _site/index.html                        -> redirect wrapper to releases/
  _site/releases/{index.html,data.json}   -> official firmware (prerelease == false)
  _site/snapshots/{index.html,data.json}  -> test firmware     (prerelease == true)

The SAME site/index.html template is copied into both channel dirs; it detects
its own channel from its URL path at runtime and fetches the sibling data.json.
"""
import json, os, re, shutil, urllib.request

repo = os.environ["GITHUB_REPOSITORY"]
headers = {"Authorization": f"Bearer {os.environ['GH_TOKEN']}",
           "Accept": "application/vnd.github+json", "User-Agent": "pages-gen"}

items, url = [], f"https://api.github.com/repos/{repo}/releases?per_page=100"
while url:
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers)) as r:
        items.extend(json.load(r))
        m = re.search(r'<([^>]+)>;\s*rel="next"', r.headers.get("Link", ""))
        url = m.group(1) if m else None

releases, snapshots = [], []
for rel in items:
    board = rel["tag_name"].split("-")[-1]            # board is the last tag segment
    bucket = snapshots if rel["prerelease"] else releases   # prerelease flag == channel
    for a in rel["assets"]:
        if a["name"].endswith((".img", ".img.xz")):
            bucket.append({"board": board, "tag": rel["tag_name"], "date": rel["published_at"],
                           "asset": a["name"], "size": a["size"],
                           "url": a["browser_download_url"], "release_url": rel["html_url"]})
for b in (releases, snapshots):
    b.sort(key=lambda x: x["date"], reverse=True)

os.makedirs("_site/releases", exist_ok=True)
os.makedirs("_site/snapshots", exist_ok=True)
json.dump(releases,  open("_site/releases/data.json", "w"),  indent=2, ensure_ascii=False)
json.dump(snapshots, open("_site/snapshots/data.json", "w"), indent=2, ensure_ascii=False)
shutil.copy("site/index.html", "_site/releases/index.html")
shutil.copy("site/index.html", "_site/snapshots/index.html")

# root wrapper: redirect the bare base URL to releases/ (carry any deep-link hash)
with open("_site/index.html", "w") as f:
    f.write(
        '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">'
        '<title>Focalcrest Rockchip Linux Images</title>'
        '<meta http-equiv="refresh" content="0; url=releases/">'
        '<link rel="canonical" href="releases/">'
        "<script>location.replace('releases/' + location.hash);</script>"
        '</head><body><p>Redirecting to <a href="releases/">releases/</a>…</p></body></html>\n')

print(f"releases={len(releases)} snapshots={len(snapshots)}")
