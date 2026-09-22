# Setting Up a Private, Folder-Restricted Google Drive Remote with rclone (A Casual Developer's Survival Guide)

I spent an afternoon doing something that *should* have been simple: creating my own private Google Drive remote for rclone using custom OAuth credentials. It turned into a small adventure through Google Cloud Console's labyrinth, rclone's interactive config wizard, and a handful of cryptic errors that felt like boss fights.

If you're a developer who wants a clean, future-proof rclone setup — especially one restricted to a single folder — this guide is for you. I'll walk through what I did, what went wrong, and what finally worked.

## Why I Did This

rclone ships with a shared Google OAuth client, but Google has been tightening API policies. Using your own OAuth credentials:

- avoids shared-client rate limits
- avoids future deprecations
- gives you full control
- lets you restrict rclone to a single folder
- lets you reuse the same credentials for Python/JS Drive API experiments

It's the "grown-up" way to use rclone.

## 1. Creating the Google Cloud Project (The Easy Part)

1. Go to Google Cloud Console
2. Create a new project
3. Enable the **Google Drive API**
4. Go to **APIs & Services → OAuth consent screen**
5. Set it to **External**
6. Add *your own Gmail* under **Test users**
7. Save

This "Test users" step is critical. If you skip it, Google will block your OAuth flow with:

```text
Access blocked: rclone has not completed the Google verification process
Error 403: access_denied
```

This error doesn't mean your app is broken — it means you forgot to add yourself as a tester.

## 2. Creating OAuth Credentials (The Important Part)

Go to:

**APIs & Services → Credentials → Create Credentials → OAuth client ID**

Choose:

- **Application type:** Desktop app
- **Name:** anything you want

Google gives you:

- `client_id`
- `client_secret`

These are the keys rclone will use.

## 3. Running `rclone config` (The Interactive Dance)

Start:

```bash
rclone config
```

Create a new remote, choose **Google Drive**, and enter your `client_id` and `client_secret`.

Then rclone asks for **scope**. Choose:

```text
1) Full access (drive)
```

Even though it says "full access," you'll restrict rclone to one folder later using `root_folder_id`.

Next prompts:

- **service_account_file** → leave blank
- **Edit advanced config?** → no
- Browser window opens → authorize your OAuth client
- **Replace token?** → no (keep the fresh token rclone just saved)

## 4. The Folder ID Trap (Where I Lost Time)

To restrict rclone to a single folder, you need the folder's ID.

**How to get it:**

1. Open the folder in Google Drive
2. Look at the URL:

```text
https://drive.google.com/drive/folders/1AbCDefGhIjKlMnOpQrStUvWxYz
```

3. Copy the long ID after `/folders/` — and only that ID.

Here's the part that actually tripped me up: Google sometimes appends extra junk to the URL after the folder ID, like:

```text
?usp=sharing
?resourcekey=0-abc123xyz
```

If you paste the whole tail into `root_folder_id`, rclone will throw:

```text
Error 404: File not found: ., notFound
```

because it treats the entire string — query params and all — as the folder ID. The fix is simple once you know it: strip everything from the `?` onward and keep just the ID itself.

**Other common mistakes:**

- Copying the entire URL instead of just the ID
- Copying a shortcut's ID
- Copying a file ID
- Using a folder inside a Shared Drive
- Using a folder you don't own
- Using a folder not accessible to your Google account

Any of these will also get you the same `404: File not found: ., notFound` error — it's a catch-all for "this ID doesn't resolve to a folder your account can actually see."

## 5. Adding the Folder Restriction

After OAuth finishes, rclone asks:

```text
Edit config? (yes/no)
```

Choose **yes**, then:

```text
e) Edit existing remote
```

Find:

```text
root_folder_id =
```

Paste your (clean, no query string) folder ID:

```text
root_folder_id = 1AbCDefGhIjKlMnOpQrStUvWxYz
```

Save and exit.

This tells rclone: "Pretend this folder is the root of Google Drive." Meaning:

- rclone cannot see anything outside that folder
- rclone cannot read other folders
- rclone cannot write outside that folder
- sync operations are confined to that folder

This is the cleanest, safest setup.

## 6. Testing the Remote

Try listing:

```bash
rclone ls GDrive:
```

Try syncing:

```bash
rclone sync localfolder/ GDrive:
```

If it works, you're done.

If you temporarily set the folder to "Anyone with the link can view" to debug — yes, you can turn that off afterward. rclone doesn't use public sharing; it uses your OAuth token.

## 7. Reusing These Credentials in Python or JavaScript

Your OAuth client isn't rclone-specific. You can use it in:

- Python (`google-api-python-client`)
- Node.js (`googleapis`)
- Deno
- Any OAuth library

Example (Python):

```python
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

flow = InstalledAppFlow.from_client_config(
    {
        "installed": {
            "client_id": "YOUR_CLIENT_ID",
            "client_secret": "YOUR_CLIENT_SECRET",
            "redirect_uris": ["http://localhost"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    },
    scopes=["https://www.googleapis.com/auth/drive"]
)

creds = flow.run_local_server(port=0)
service = build("drive", "v3", credentials=creds)

print(service.files().list(pageSize=10).execute())
```

Same credentials. Same OAuth flow. Same Drive API.

## 8. Lessons Learned (So You Don't Suffer Like I Did)

- Add yourself as a **Test user** or Google will block you
- Use **Desktop app** OAuth credentials
- Choose **scope 1 (drive)**
- Skip service accounts
- Skip advanced config
- Don't replace the token
- Strip query params (`?usp=sharing`, `?resourcekey=...`) off the folder ID before pasting it anywhere
- Don't use shortcuts as folder roots
- Don't use Shared Drives unless you mean to
- Don't make the folder public — rclone doesn't need it
- Always test with `rclone ls` before syncing
- `root_folder_id` is the magic ingredient

## Final Thoughts

This setup is absolutely worth doing. You end up with a private, secure Google Drive remote, full control over OAuth credentials, a restricted folder boundary, a future-proof configuration, and reusable credentials for Drive API development.

It's a little frustrating the first time, but once you understand the moving parts, it's rock-solid.
