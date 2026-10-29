# Cambridge Centre for Healthcare Innovation: website

A static site. Everything people edit is a plain text file. Every change to `main` is built and
uploaded to the web server over FTP by GitHub Actions.

## Layout

| Path | What it is |
| --- | --- |
| `content/` | All the words: people, news, events, SIGs, testimonials, site settings. Edit these. See `content/README.md`. |
| `img/` | Shared images, logos, people photos and the home page video. |
| `sites/cambridge/` | The Cambridge blue design: `template.html`, `site.json`, `icons/`. |
| `sites/classic/` | The original colourful design, same structure. |
| `build.py` | Builds one design into `dist/<name>/`. |
| `.github/workflows/deploy.yml` | The automatic build and FTP upload. |

Both designs read the same `content/` and `img/`, so a content change shows up in either one.

## One-time setup

1. **Push this folder to the repo** (`brangsmith/cchi.org.uk`, branch `main`).
2. **Add the FTP details** as secrets: repo > Settings > Secrets and variables > Actions > *Secrets* > New repository secret.
   - `FTP_SERVER`: the host name only, for example `ftp.example.ac.uk` (no `ftp://`)
   - `FTP_USERNAME`
   - `FTP_PASSWORD`
3. **Optional settings** as variables (same page, *Variables* tab). Leave them out to use the defaults.

   | Variable | Default | Use |
   | --- | --- | --- |
   | `SITE` | `cambridge` | Which design goes live: `cambridge` or `classic`. |
   | `FTP_DIR` | `./` | Folder on the server. Must end in `/`, for example `public_html/` or `chi-test/`. |
   | `FTP_PROTOCOL` | `ftps` | `ftps` (explicit TLS), `ftps-legacy` (implicit TLS) or `ftp` (no encryption, last resort). |
   | `FTP_PORT` | `21` | Change only if your host says so. |

4. **Try it safely first.** Actions tab > *Build and deploy website* > Run workflow. It defaults to a
   *dry run*, which lists what would be uploaded and changes nothing on the server.
5. **First real upload to a test folder.** Set `FTP_DIR` to something like `chi-test/`, run the workflow
   again with the dry run box unticked, and check the site there. When it looks right, set `FTP_DIR`
   to the real folder (or delete the variable) and push any change, or run it once more.

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

- The upload only sends files that changed since last time. It records what it sent in
  `.ftp-deploy-sync-state.json` on the server, and only ever deletes files it put there itself.
  Anything you upload to the server by hand is left alone. Don't delete that file.
- Never put the FTP password in a file in this repo. It lives only in GitHub secrets.
- `dist/` is created by the build and is not stored in git.
- If the host only allows SFTP/SSH rather than FTP, the upload step needs swapping for an rsync/SFTP one.
