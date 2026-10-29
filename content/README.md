# Editing site content

All of the changing content is Markdown. There is nothing to build or run: edit a file, save, upload.

```
content/
  people.md          everyone, one section each
  testimonials.md    the quotes, one section each
  site.md            footer details: social links, what3words address
  events.md          upcoming events, one section each
  news/001.md ...    one numbered file per news item or blog post
  sigs/001.md ...    one numbered file per special interest group
  seo.md             the short description of each page for search results and sharing
```

## The format

Every item looks the same, whether it sits in a list file or has a file to itself:

```
## Dr Tom Bashford

- subtitle: Unit 1 Lead
- groups: International Health Systems Group
- titles:
  - Assistant Professor in Healthcare Systems
  - Consultant Neuroanaesthetist, Cambridge University Hospitals
- image: img/people/bashford.webp

Any text goes here, after a blank line.
```

- A heading with the name or title. In `people.md` and `testimonials.md` each item is a `##` heading. In a numbered file the heading is `#` on the first line.
- A bullet for each detail, written `- name: value`. Values can contain colons and quotes freely.
- A detail with several values is either a comma-separated line (`- groups: A, B`) or the values as indented bullets underneath, as `titles` does above. Use the indented bullets when a value itself contains a comma.
- A blank line ends the bullets. Anything after it is the text.
- Every file lists every detail it can have. You only change the values. Leave a value blank when you have nothing for it, and don't delete the line. Switches are `true` or `false`. Pictures and links in the details start from the top of the site, for example `img/people/ward.webp`.
- In the text of an article or group page, use `##` for headings and write pictures relative to the file, for example `![Describe the image](007/photo.jpg)`. Always write the description. Links, lists, quotes and tables work. Scripts, embeds and custom styles are stripped out.

## Starting a new item

Copy one of these, paste it in, and fill in the values.

A new person, at the end of `people.md`:

```
## Name

- subtitle:
- category:
- groups:
- sigs:
- leads:
- titles:
  - First post
  - Second post
- image:
- profile_url:
- order:
```

A new quote, at the end of `testimonials.md`:

```
## Name

- role:
- group: student
- order:

The quote.
```

A new event, at the end of `events.md`:

```
## Event name

- date: 2027-01-20
- end_date:
- start_time:
- end_time:
- location:
- summary:
- image:
- image_alt:
- link:
- hidden: false
```

A new news item, as the next number in `news/` (for example `004.md`):

```
# Headline

- date:
- tag:
- summary:
- featured: false
- image:
- image_alt:
- link:
- when:
- hidden: false

The article text.
```

A new special interest group, as the next number in `sigs/`:

```
# Full name of the group

- short:
- summary:
- status: current
- from:
- until:
- project:
- url:
- logo:
- logo_dark:
- logo_alt:

The text of the group's page.
```

## people.md

Add a `##` section per person.

| detail | what goes in it |
|---|---|
| subtitle | Their role in the Centre, shown under the name |
| category | `leadership`, `unit-lead`, `researcher`, `staff`. Drives the Role filter |
| groups | Research groups by name, for example `International Health Systems Group`. Shown as badges, and drives the Research group filter |
| sigs | Special interest groups by name or short name, for example `SCAN`. Shown as dashed badges, drives the SIG filter, and puts the person on that group's page |
| leads | Research groups this person leads, by name, separated by commas or semicolons. Shown as "Group lead" on the Research page |
| titles | Their posts, one per line on the card. No full stops at the end |
| image | Path to the photo, for example `img/people/ward.webp`. Square, at least 240 px wide. Leave out to show initials |
| profile_url | Link to their profile page |
| order | Number for sort order. Without one, people sort last, then A to Z |

## testimonials.md

A `##` section per quote. The heading is who said it (write `Anonymous` for no name) and the text is the quote, without quotation marks. Leave a blank line between paragraphs.

| detail | what goes in it |
|---|---|
| role | Job title and organisation |
| group | `student` or `industry`. Sets which list it appears in |
| order | Number for sort order within its group |

## site.md

Details for the footer.

| detail | what goes in it |
|---|---|
| linkedin | Full address of the LinkedIn page. Leave blank to hide the icon |
| x | Full address of the X account, for example `https://x.com/CamHealthInnov`. Leave blank to hide the icon |
| what3words | Three words separated by dots, for example `agent.first.engage`, without the `///`. Used in the footer and on the Contact page |

## events.md

A `##` section per event. Every event links to an outside page, normally on Luma, so there is no page for it on this site. The Events section on the home page lists upcoming events, soonest first, as cards. **When no event is upcoming the whole section disappears.** An event drops off by itself after its last day, so there is no need to delete it straight away, though clearing out old ones keeps the file tidy.

| detail | what goes in it |
|---|---|
| date | `YYYY-MM-DD`, the first day. Required |
| end_date | `YYYY-MM-DD` for a multi-day event, otherwise leave blank. Dates are shown as a range, for example `11–15 January 2027` |
| start_time | For example `18:00`. Every event should have one |
| end_time | For example `20:00`. Shown with the start time as `18:00 – 20:00` |
| location | Optional, for example `Cambridge` or `Online`. Shown after the time, on the line under the date |
| summary | One sentence |
| image | Optional, for example `content/events/summer-school.webp`. Square, like the cover image on Luma, at least 800 px wide and under about 300 KB. Other shapes are cropped to a square from the middle |
| image_alt | Describes the image for screen readers. Needed whenever there is an image |
| link | The Luma address, starting `http`. Required: an event without one is not shown. Opens in a new tab |
| hidden | `true` to hide the event without deleting it |

Events are shown as cards in the style of the special interest groups, two to a row, with a coloured dashed border. Up to four are shown.

## news/

One file per item, named with a three-digit number: `001.md`, `002.md`, `003.md`. **Use the next number up for each new item and never leave a gap.** The site shows the highest numbers first. The home page loads the latest five, and the News page loads more as people ask for them.

To take an item down, do not delete the file. Set `- hidden: true` instead. (The site tolerates a gap of up to two missing numbers, but anything after a longer gap is not found.)

```
# What we learned from the first cohort

- date: 2026-11-02
- tag: Students
- summary: Six months in, the students on what worked and what didn't.
- image: content/news/007/group.jpg
- image_alt: The cohort outside the department

The article text starts here.
```

| detail | what goes in it |
|---|---|
| date | `YYYY-MM-DD`, shown on the card. A future date hides the item until that day. Order comes from the file number, not the date |
| tag | Topic, for example `MSt`, `Research`, `Students`. Drives the Topic filter, and a new topic appears as soon as someone uses it |
| summary | One sentence for cards. Optional |
| featured | `true` to make it the big card on the home page. Only the latest five items are looked at, and the newest featured one wins |
| image | Optional image for the card, for example `content/news/007/group.jpg`. Landscape (16:9) works best. Use at least 1600 px wide, as a JPG or WebP under about 300 KB: a small image will look soft when shown large. On the big home card it sits to the right of the text, on all other cards at the bottom |
| image_alt | Describes the image for screen readers. Needed whenever there is an image |
| link | Leave out for an article written in the text below. Put a web address starting `http` to link to another site, which opens in a new tab. Start with `/` (for example `/mst/` or `/people/`) for a page on this site. An item with a link needs no text |
| when | Optional text shown in place of the date, for example `11 to 15 Jan 2027` for an event |
| hidden | `true` to hide the item without deleting it |

A long post with many pictures can keep them in a folder named after it, for example `news/007/`, next to `007.md`. In the text, write `![Describe the image](007/photo1.jpg)`.

The article address is the number, so item 7 lives at `#news/7`.

## sigs/

One numbered file per special interest group, in the same way as news: `001.md`, `002.md`, no gaps. The heading is the group's name and the text below the bullets is the group's own page. It can hold an introduction, publications, pictures and anything else.

| detail | what goes in it |
|---|---|
| short | Optional short label, such as an acronym. Used on badges and filter chips so long names don't crowd the cards, and for the page address (`#sig/scan`) |
| summary | One or two sentences. Shown on the card and at the top of the page |
| status | `current` or `past`. Past groups move to a small list under the cards. Without one, the group is current |
| from | Optional start year. Shown as "Since 2025" |
| until | Optional end year. Shown as "Until 2027", or "2025–2027" with a start year. Nothing is shown if both are left out |
| project | Optional. The project the group is linked to |
| url | Optional. Link to an outside website for the group. Opens in a new tab |
| logo | Optional. The group's logo, shown in place of the title at the top of its page. Use a picture with a transparent background (PNG or WebP). Path from the top of the site, for example `content/sigs/003/scan-logo.webp` |
| logo_dark | Optional. A second version of the logo for dark mode, with light-coloured lettering. Without one, dark mode shows the logo on a pale tile |
| logo_alt | The words in the logo, for screen readers, for example `SCAN: Spatial Computing Assisted Neuronavigation`. Without one the group's name is used |

The team on a group's page, and the faces and count on its card, come from the `sigs` detail in `people.md`. A person is matched by the group's short name or full name, so `SCAN` and `Spatial Computing Assisted Neuronavigation` both work.

## Page addresses

Pages have their own addresses: `/research/`, `/people/`, `/mst/`, `/cebc/`, `/news/`, `/contact/`. A news item is `/news/3/` (the number of its file) and a special interest group is `/research/` plus its short name in lower case, for example `/research/scan/`. When a link in an item points at another page on this site, write the address, for example `/mst/`. Old-style links such as `#education` still work.

## seo.md

One section per page, each with a `description`: the short text search engines show under the page title and that appears when the page is shared. One or two sentences, under about 160 characters. News items and special interest groups use their own `summary`, and the page title comes from the item's heading.

## Putting it on a web server

Upload `index.html`, `img/` and `content/` together. The content files load with `fetch`, so the site must be served over http or https. Opening `index.html` straight from a folder will show "could not be loaded". For a local preview, run `python3 -m http.server` in the folder.

The site looks for numbered files that are not there, so a web server log will show a few "not found" lines for `news/004.md` and similar. That is normal.
