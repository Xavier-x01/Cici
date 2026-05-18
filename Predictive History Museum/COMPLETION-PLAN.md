# Museum Completion Plan

**Date:** 2026-05-18
**Current status:** 2 sample exhibits scaffolded (civ-053, gt-021). All remaining chapters pending Airtable export and artifact acquisition.

---

## Current Exhibit Status

| Exhibit | Status | Artifacts | Storage |
|---|---|---|---|
| civ-053-dostoevsky-and-the-soul-of-russia | scaffold_complete | 7 | url_only_pending_local |
| gt-021-live-crisis-pressure | scaffold_complete | 6 | url_only_pending_local |

---

## Process for Completing Each Exhibit

### Step 1: Export from Airtable

Export the flat artifact inventory as CSV. Required columns:

| Airtable column | metadata.yaml field |
|---|---|
| Artifact ID | `artifact_id` |
| Chapter | `chapter_id` |
| Title | `title` |
| Type | `item_type` |
| Room | `room` |
| Source URL | `source_url` |
| Source Name | `source_name` |
| Rights | `rights_status` |
| What to notice | `what_to_notice` |
| Limits | `what_this_cannot_prove` |
| Lecture connection | `lecture_connection` |
| Curator note | `curator_note` |

### Step 2: Create chapter folder

For each chapter:
1. Copy `_templates/chapter-template/` to the correct book folder
2. Rename using naming convention (e.g. `civ-053-dostoevsky-and-the-soul-of-russia/`)
3. Fill in `index.md` and `exhibit.yaml`

### Step 3: Populate artifacts

For each artifact row in the Airtable export:
1. Copy `_templates/chapter-template/artifacts/000-artifact-name/` into the chapter's `artifacts/` folder
2. Rename the artifact folder (e.g. `001-russian-orthodox-chant/`)
3. Fill in `metadata.yaml` from the Airtable row
4. Write `notes/curator-note.md` (wall label)

### Step 4: Acquire files

For each artifact with `rights_status: public_domain` or `open_license`:
1. Download the file from `source_url`
2. Place in `original/` folder (replace `.gitkeep`)
3. Run `sha256sum {file}` and paste into `checksum_sha256`
4. Create derivatives as needed: `thumb.webp`, `display.webp` (images); `preview.mp3`, `waveform.webp` (audio)

For `external_link_only` artifacts: leave `original/.gitkeep`, record reason in `curator-note.md`.

### Step 5: Sync to cloud

1. Mirror the `Predictive History Museum/` folder to your cloud vault (Google Drive, Dropbox, or iCloud)
2. Update `cloud_original_path` in `metadata.yaml` to match the cloud path
3. Update `storage_status: local_and_cloud`

### Step 6: Curator sign-off

When all artifacts for a chapter are complete:
1. Review `index.md` for accuracy
2. Set `exhibit_status: complete` in `exhibit.yaml`
3. Set `curator_sign_off: "approved — [initials] [date]"` in `exhibit.yaml`

---

## Storage Checklist

### Local Vault
- [ ] All `public_domain` and `open_license` files downloaded to `original/`
- [ ] Checksums computed for all local files
- [ ] Derivatives created for display artifacts

### Cloud Sync
- [ ] Local vault folder synced to cloud storage
- [ ] All `cloud_original_path` fields updated in `metadata.yaml`
- [ ] All `storage_status` fields updated to `local_and_cloud`

---

## Completion Tracking

Once the full chapter list is provided, a row per chapter will be added to the status table above. A chapter counts as complete only when:
- All 5–15 artifacts have complete `metadata.yaml`
- All `public_domain` and `open_license` files are in `original/` with checksums
- All curator notes are written
- `exhibit.yaml` carries a curator sign-off
- Chapter is synced to cloud vault

---

## Submission Requirements Checklist (per Robert's email)

- [ ] 1. Durable export, not just an Airtable link
- [ ] 2. Folder-based sample of at least two finished chapter exhibits
- [x] 3. Local storage structure for sample exhibits (scaffolded)
- [ ] 4. Shared cloud folder structure (requires cloud sync step above)
- [ ] 5. Stored artifact files, not URL-only references
- [x] 6. Metadata for every artifact (scaffolded; needs population from Airtable)
- [ ] 7. Rights status for every artifact
- [x] 8. Mapping from each artifact to a chapter, room, and exhibit
- [ ] 9. Statement of which chapters are actually complete
- [ ] 10. Plan for completing one exhibit per chapter across Civilization and Apocalypse (this document)
