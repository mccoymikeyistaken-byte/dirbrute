import requests
import argparse
import hashlib
import time
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser(description= "Directory Brute Forcing tool")

parser.add_argument("url", help="target website")

args = parser.parse_args()

class BaseLineDetails:
  def __init__(self,status,length,location,hash,wc,lc):
    self.status = status
    self.length = length
    self.location = location
    self.hash = hash
    self.wc = wc
    self.lc = lc


# BaseLine request for the server
def get_baseline_details(url):
  try:
    baseline_req = requests.get(f"{url}/randomjunk",timeout=3,allow_redirects=False)
    baseline_status_code = baseline_req.status_code
    baseline_textlength = len(baseline_req.text)
    baseline_location = baseline_req.headers.get("Location")
    baseline_hash = hashlib.md5(baseline_req.text.encode()).hexdigest()
    baseline_wc = len(baseline_req.text.split())
    baseline_lc = len(baseline_req.text.splitlines())
    print(f"Baseline status code: {baseline_status_code}")
    print(f"Baseline Text Length: {baseline_textlength}")
    print(f"Baseline location: {baseline_location}")
    print(f"Baseline Hash: {baseline_hash}")
    print(f"Baseline word count: {baseline_wc}")
    print(f"Baseline line count: {baseline_lc}\n")
  except Exception as e:
    print(f"Couldn't fetch due to {e}")

  baselinedetails = BaseLineDetails(baseline_status_code,baseline_textlength,baseline_location,baseline_hash,baseline_wc,baseline_lc)
  return baselinedetails

def start_bruteforce(url,base,path):
      try:
        response = requests.get(f"{url}{path}",timeout=3,allow_redirects=False)
        currStatusCode = response.status_code
        currtextlength = len(response.text)
        currLocation = response.headers.get("Location")
        currHash = hashlib.md5(response.text.encode()).hexdigest()
        currWC = len(response.text.split())
        currLC = len(response.text.splitlines())
        if response.status_code in [301,302,303,307,308]:
          print(f"Redirect detected-> {currLocation}")
      except Exception as e:
        print(f"Couldn't fetch {path} due to {e}")
      if (
        currStatusCode != base.status
        or currtextlength != base.length
        or currLocation != base.location
        or currHash != base.hash
        or currWC != base.wc
        or currLC != base.lc
        ):
       print(f"Possible path found: {path} [{currStatusCode} | {currtextlength} | {currLocation} | {currHash} | {currWC} words | {currLC} lines] ")
  

start_time = time.time()
base = get_baseline_details(args.url)
with ThreadPoolExecutor(max_workers=10) as executors:
    with open("wordLists.txt","r") as f:
      for currPath in f:
        currPath = currPath.strip()
        executors.submit(start_bruteforce(args.url,base,currPath))
      
print(f"Scan completed in {time.time() - start_time: .2f}s")