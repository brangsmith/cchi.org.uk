# Cambridge Centre for Healthcare Innovation: website

A static site. Everything people edit is a plain text file. Every change to `main` is built and
uploaded to the web server over SFTP by GitHub Actions.

## Layout

| Path | What it is |
| --- | --- |
| `content/` | All the words: people, news, events, SIGs, testimonials, site settings. Edit these. See `content/README.md`. |
| `img/` | Shared images, logos, people photos and the home page video. |
| `sites/cambridge/` | The Cambridge blue design: `template.html`, `site.json`, `icons/`. |
| `sites/classic/` | The original colourful design, same structure. |
| `build.py` | Builds one design into `dist/<name>/`. |
| `.github/workflows/deploy.yml` | The automatic build and upload to the server. |

Both designs read the same `content/` and `img/`, so a content change shows up in either one.

## One-time setup

1. **Add the login** (repo > Settings > Secrets and variables > Actions > *Secrets* > New repository secret).
   The names start `FTP_` for historical reasons; the values are your SFTP details:
   - `FTP_SERVER`: `pallas.mythic-beasts.com` (host name only)
   - `FTP_USERNAME`: `ihsg`
   - `FTP_PASSWORD`: the SFTP password
2. **Add the variables** (same page, *Variables* tab):
   - `FTP_DIR`: `www/www.cchi.org.uk/` (relative to the login folder, `/home/ihsg`; keep the trailing `/`)
   - `SFTP_KNOWN_HOSTS`: the output of this command run in Terminal on your Mac. It makes the upload refuse to
     talk to anything that isn't your server:
     ```
     ssh-keyscan pallas.mythic-beasts.com
     ```
   - Optional: `SITE` (`cambridge` or `classic`, default `cambridge`), `SFTP_PORT` (default `22`),
     `DELETE_REMOVED` (`true` to also delete server files that are no longer in the repo; default `false`)
3. **Try it safely.** Actions tab > *Build and deploy website* > Run workflow. It defaults to a *dry run*, which
   lists what would be uploaded and changes nothing on the server.
4. **Go live.** Run it again with the dry run box unticked, then check the site. From then on every commit to
   `main` deploys by itself.

## Day to day

- **Edit text:** open a file in `content/` on GitHub, click the pencil, edit, *Commit changes*.
  The site updates after a minute or two (Actions tab shows progress and any error).
- **Add news, a SIG or an event:** add the next numbered file (for example `content/news/004.md`) using an
  existing one as a template. `content/README.md` lists every field.
- **Add or replace an image:** upload it to `img/` (or next to the content file that uses it) with
  *Add file > Upload files*, then reference it in the markdown.
- **Switch design:** change the `SITE` variable and run the workflow.
- **Undo a change:** open the commit on GitHub and click *Revert*. That makes a new commit, which deploys.
- **Review before publishing:** make the change on a branch and open a pull request. Pull requests only
  build (a check that nothing is broken); they never upload.

## Changing the design

Edit `sites/<name>/template.html`. To see it locally:

```
python3 build.py cambridge
python3 -m http.server -d dist/cambridge 8000   # then open http://localhost:8000
```

(Opening `index.html` straight from disk won't load the content files; use the small server above.)

## Good to know

- Every deploy sends the whole site (about 4 MB), so what is online always matches the repo.
- By default nothing is ever deleted on the server. Files you upload by hand are left alone, and so are pages you remove from the repo. Turn on `DELETE_REMOVED` only when this folder holds nothing but the website.
- Never put a password in a file in this repo. It lives only in GitHub secrets.
- `dist/` is created by the build and is not stored in git.
