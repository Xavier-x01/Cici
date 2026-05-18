# Predictive History Museum

This directory contains the repository of exhibit materials for *Predictive History: Civilization* and *Predictive History: Apocalypse*.

## Structure

```
Predictive History Museum/
  civilization/         ← exhibits for Book 1: Civilization
  apocalypse/           ← exhibits for Book 2: Apocalypse
  _templates/           ← blank templates for new chapter exhibits
  MUSEUM-README.md      ← this file
  COMPLETION-PLAN.md    ← roadmap for completing all exhibits
```

## Chapter Folder Naming

`{book-prefix}-{chapter-number-padded}-{slug}/`

- Civilization prefix: `civ-`
- Apocalypse prefix: `gt-`
- Example: `civ-053-dostoevsky-and-the-soul-of-russia/`
- Chapter number is always zero-padded to three digits.

## Artifact Folder Naming

`{NNN}-{artifact-slug}/`

- NNN is zero-padded to three digits.
- Example: `001-russian-orthodox-chant/`

## Artifact ID Convention

`{chapter-id}-{NNN}` — e.g. `civ-053-001`

`chapter_id` always uses padded form: `civ-053`, not `civ-53`.

---

## Controlled Vocabularies

### Museum Rooms

| Room ID | Purpose |
|---|---|
| `entrance_artifact` | The single object that orients the visitor before any text |
| `context_room` | Background — place, time, person |
| `primary_artifacts_and_texts` | Core primary sources for the chapter argument |
| `comparison_artifacts` | Contrasting or parallel cases |
| `pressure_systems` | Systemic and structural forces at work |
| `caution_room` | Epistemological limits; what this exhibit cannot prove |

### Artifact Types

`artwork`, `artifact`, `object`, `text`, `manuscript`, `map`, `place`, `portrait`, `chart`, `diagram`, `music`, `speech`, `document`, `performance`, `architecture`, `institution`, `pressure_system`, `symbolic_artifact`

### Rights Status Values

| Value | Meaning |
|---|---|
| `public_domain` | No copyright restrictions; file may be stored locally |
| `open_license` | Creative Commons or equivalent; file may be stored locally with attribution |
| `external_link_only` | Cannot host locally; source URL is the permanent reference |
| `needs_review` | Rights uncertain — requires legal check before download |
| `unavailable` | Cannot be obtained in any form |

### Storage Status Values

| Value | Meaning |
|---|---|
| `local_and_cloud` | File exists in `original/` and is synced to cloud vault |
| `url_only_pending_local` | Source URL known; file not yet downloaded |
| `pending_acquisition` | No URL yet, or curator-authored file not yet created |

---

## Per-Exhibit File Requirements

Each chapter folder must contain:

```
{chapter-id}-{slug}/
  index.md          ← reader-facing exhibit description, room layout, curatorial note
  exhibit.yaml      ← structured manifest (artifact IDs, rooms, status, curator sign-off)
  artifacts/
    {NNN}-{slug}/
      metadata.yaml       ← complete artifact metadata (all fields required)
      notes/
        curator-note.md   ← wall label: what to notice, limits, selection rationale
      original/
        {filename}        ← downloaded/acquired file (or .gitkeep if pending)
      derivatives/
        {filename}        ← thumbnail, display image, audio preview (or .gitkeep if pending)
```

### Minimum artifacts per exhibit: 5. Maximum: 15.

Every exhibit must include at least one artifact in `caution_room`.

---

## Adding a New Chapter Exhibit

1. Copy `_templates/chapter-template/` to the correct book folder (`civilization/` or `apocalypse/`)
2. Rename using the naming convention above
3. Edit `index.md`: fill in chapter title, summary, artifact inventory table, room layout, curatorial note
4. Edit `exhibit.yaml`: fill in chapter_id, title, and artifact list
5. For each artifact, copy `_templates/chapter-template/artifacts/000-artifact-name/` into `artifacts/`
6. Rename the artifact folder and fill in `metadata.yaml` and `notes/curator-note.md`
7. When rights are confirmed and file is ready: download into `original/`, replace `.gitkeep`
8. Run `sha256sum {file}` and paste the hash into `checksum_sha256` in `metadata.yaml`
9. Sync `original/` to cloud vault, update `cloud_original_path` and `storage_status: local_and_cloud`
10. Mark exhibit complete in `exhibit.yaml` and add curator sign-off

---

## Curatorial Standard

The museum is not a media dump. Every artifact must earn its place.

Each artifact requires:
- A specific reason it was chosen over alternatives
- A `what_to_notice` field pointing to concrete, observable details
- A `what_this_cannot_prove` field — honest about limits
- A `lecture_connection` field tying it to the chapter argument
- A `curator_note` explaining selection rationale

Human curators are responsible for: selection proportion, cultural judgment, emotional calibration, representative balance, and final sign-off. The `curator_sign_off` field in `exhibit.yaml` must be set before an exhibit is considered complete.
