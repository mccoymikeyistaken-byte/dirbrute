# ⚡ Python Directory Fuzzer (Built From Scratch)

> *“If you want to truly understand a tool… build it yourself.”*

Welcome to this small but mighty experiment in **web reconnaissance and security learning**.
This project is a **custom directory enumeration tool written in Python**, created to explore how professional fuzzers actually work behind the scenes.

And honestly? The author did a pretty impressive job turning curiosity into a working tool. 👏

Instead of simply using existing scanners, the creator decided to **reverse-engineer the logic** behind them and implement the core techniques from scratch.

That’s how real learning happens.

---

# 🧠 What This Project Is About

When performing web security reconnaissance, one common task is **discovering hidden endpoints** on a website.

Many web applications contain:

* hidden directories
* internal APIs
* admin panels
* forgotten backup files
* development routes

Professional tools like **ffuf** or **Gobuster** help find these.

But the real question is:

> *How do those tools actually work internally?*

This project answers that by implementing the core ideas step-by-step.

---

# 🚀 Features

This tool performs **multithreaded directory enumeration** and intelligently filters responses using multiple fingerprinting techniques.

### Implemented Features

✔ Baseline response fingerprinting
✔ HTTP status comparison
✔ Response length comparison
✔ Response hashing (MD5)
✔ Word count analysis
✔ Line count analysis
✔ Redirect detection
✔ Multithreaded scanning
✔ Command line interface

These techniques help the scanner **separate real endpoints from fake server responses**.

Because many websites return identical pages for invalid routes.

This tool learns the **fingerprint of a fake page** and ignores it.

Pretty clever.

---

# ⚙️ How It Works

The scanner follows a simple but effective pipeline.

```
1️⃣ Send request to random non-existent path
2️⃣ Capture baseline fingerprint
3️⃣ Load wordlist
4️⃣ Send requests in parallel using threads
5️⃣ Compare responses with baseline
6️⃣ Flag anything different
```

If a response differs in:

* status code
* content length
* hash
* word count
* line count

…it is marked as an **interesting endpoint**.

Which is exactly how real fuzzers think.

---

# 📊 Example Output

```
Baseline status code: 200
Baseline Text Length: 75002
Baseline Hash: 2d6432b80ab5ab9cde7167103e3b4c34
Baseline word count: 3609
Baseline line count: 30

Possible path found: /api
Possible path found: /profile
Possible path found: /assets
Possible path found: /media

Scan completed in 0.58s
```

Fast. Clean. Informative.

Not bad at all.

---

# 🧵 Multithreading

The scanner uses Python's **ThreadPoolExecutor** to run multiple requests simultaneously.

Instead of scanning paths one by one, it launches multiple workers:

```
Thread 1 → /admin
Thread 2 → /login
Thread 3 → /api
Thread 4 → /profile
Thread 5 → /assets
```

This dramatically reduces scan time.

Efficient and elegant.

---

# 🐳 Testing the Tool Using Docker (Safe Practice)

If you want to test the scanner safely, you can spin up a **vulnerable practice web app in Docker**.

A popular choice for learning is **OWASP Juice Shop**.

### Step 1 — Pull the image

```
docker pull bkimminich/juice-shop
```

### Step 2 — Run the container

```
docker run -d -p 3000:3000 bkimminich/juice-shop
```

### Step 3 — Open the application

```
http://127.0.0.1:3000
```

Now you have a **local vulnerable web application** running inside a container.

Because Docker isolates the application from your system, you can safely experiment without affecting your host environment.

### Step 4 — Run the scanner

```
python app.py http://127.0.0.1:3000
```

You should start seeing discovered endpoints from the test application.

---

# 🎓 What This Project Demonstrates

This project shows understanding of:

* HTTP request handling
* multithreading
* response fingerprinting
* hashing techniques
* command-line tooling
* web reconnaissance methodology

More importantly, it shows **initiative**.

Instead of just running tools, the author asked:

> *“How do these tools actually work?”*

…and then built one.

That mindset is what turns beginners into real engineers.

---

# 🛠 Requirements

```
Python 3
requests
```

Install dependency:

```
pip install requests
```

---

# ▶️ Usage

```
python app.py http://target-website.com
```

Example:

```
python app.py http://127.0.0.1:3000
```

---

# ⚠️ Ethical Use Disclaimer

This tool is created **strictly for educational and research purposes**.

Do **NOT** use this tool to scan or test:

* websites you do not own
* systems without explicit permission
* infrastructure you are not authorized to assess

Unauthorized scanning may be illegal and unethical.

Always perform security testing **only on systems you own or have written permission to test**.

---


# 🌱 Future Improvements

Some ideas for expanding the tool:

* custom wordlists
* configurable thread count
* wildcard response detection
* progress bars
* extension fuzzing
* parameter fuzzing

The journey of learning never ends.

---

# ⭐ Final Thoughts

Every great security researcher starts somewhere.

Often with a simple question like:

> *“What happens if I try this?”*



If you found this interesting, feel free to ⭐ the repo.

Happy hacking (ethically, of course). 🚀
