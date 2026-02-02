# Instagram Non-Followers Checker

This project helps you identify **accounts you follow on Instagram that do not follow you back**, using Instagram's official data export and a simple Python script.

No third-party apps, no API access, no login automation — just your own data.

---

## Prerequisites

* Python **3.9+**
* An Instagram account
* A computer (Windows, macOS, or Linux)

---

## Step 1: Request Your Instagram Data

1. Go to **Instagram** → **Settings & privacy**
2. Navigate to:

   **Accounts Center → Your information and permissions → Download your information**
3. Select **Download or transfer information**
4. Choose **Some of your information**
5. Under **Connections**, select:

   * ✅ **Followers and following**
6. Click **Next**
7. Choose:

   * **Download to device**
   * Format: **JSON**
   * Date range: **All time**
   * Media quality: **Low** (media not needed)
8. Submit the request

Instagram will email you when the download is ready (usually within minutes, sometimes hours).

---

## Step 2: Download and Extract the Data

1. Download the ZIP file from Instagram
2. Extract it
3. Navigate to:

```
connections/
  followers_and_following/
```

You should see files similar to:

```
followers.json
following.json
```

> ⚠️ Filenames may vary slightly depending on export version. Rename them if needed.

---

## Step 3: Project Setup

Create a new folder:

```
ig_unfollow/
```

Place these files inside:

```
ig_unfollow/
  unfollow_check.py
  followers.json
  following.json
```

---

## Step 4: Python Script

Save file as **`unfollow_check.py`**:

---

## Step 5: Run the Script

From the project directory:

```bash
python unfollow_check.py
```

Output:

* Printed list of accounts that **don’t follow you back**
* File created:

```
not_following_back.csv
```

---

## Notes & Guarantees

* ✅ Uses **official Instagram export only**
* ✅ No API usage
* ✅ No risk to your account
* ✅ Works offline
* ❌ Does **not** automatically unfollow anyone

---

## Troubleshooting

### Script shows zero results

* Verify the files are correct:

  * `followers.json`
  * `following.json`
* Open them and confirm usernames appear under `string_list_data`

### Filenames differ

Rename them to:

```
followers.json
following.json
```

---

## Legal / Ethical Note

This script **only reads data you own**. You are responsible for how you use the output. Instagram's ToS prohibits automated actions — this script does **not** perform any.

---

## Optional Next Steps

* Compare mutuals only
* Build a UI
* Add whitelist / ignore list

