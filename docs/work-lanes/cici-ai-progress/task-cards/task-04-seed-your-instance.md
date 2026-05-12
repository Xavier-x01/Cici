# Task 4 — Seed Your Instance

**Phase:** 1 — Personal OB1  
**Prerequisite:** Task 3 complete (10+ thoughts captured)  
**Estimated time:** 20–30 minutes

---

## Goal

Give your OB1 fork a proper identity in the governed-state layer. You will copy the instance template, fill in your details, validate it, and commit it to your GitHub fork. This makes your instance official and your progress permanently visible on GitHub.

---

## Steps

### Step 1 — Open your fork in a terminal or Cursor

```bash
git clone https://github.com/<your-github-handle>/Cici.git
cd Cici
git checkout -b seed/my-instance
```

(If you already have it cloned locally, just `cd` into it and create the branch.)

### Step 2 — Copy the template

```bash
cp -r users/_template users/<your-instance-id>
```

Choose an instance ID that's lowercase, hyphen-separated, and identifies you. Examples:
- `pango-ph`
- `ell-ph`
- `kyle-ob1`

### Step 3 — Fill in your seed intent

Open `users/<your-instance-id>/seed_intent.json`. Replace the placeholder values:

```json
{
  "instance_id": "your-instance-id",
  "instance_display_name": "Your Name's OB1",
  "owner": "your-github-handle",
  "created_at": "2026-05-XX",
  "purpose": "Personal AI memory for [your name] — capturing skills, goals, and learning context.",
  "capabilities": ["capture", "search", "recent_thoughts", "stats"],
  "operational_bridges": {
    "supabase_project_ref": "your-project-ref"
  }
}
```

Fill in real values. `supabase_project_ref` is the short code from your Supabase project URL (e.g., `abcdefghijklmnop`).

### Step 4 — Create your governed-state instance record

```bash
mkdir -p users/<your-instance-id>/governed-state/identity
cp users/<your-instance-id>/seed_intent.json users/<your-instance-id>/governed-state/identity/instance.json
```

Remove the `instructions` field from `instance.json` if it was in the template — that field is for the template only.

### Step 5 — Validate

From the repo root:

```bash
python3 scripts/validate-governed-state.py
```

The validator must pass with no errors. If it fails, read the error message — it will tell you exactly which field is missing or malformed. Fix it and run again.

### Step 6 — Commit and push

```bash
git add users/<your-instance-id>/
git commit -m "seed: initialize <your-instance-id> instance"
git push origin seed/my-instance
```

Your fork on GitHub will now show your instance directory. That's your proof.

---

## Proof

Link to your GitHub fork showing the `users/<your-instance-id>/` directory with your committed files.

**Option A — Telegram:** Paste the GitHub URL to your `users/` directory in the group with your name + "Task 4 done."

**Option B — GitHub:** Create `proof/task-04/README.md` in your fork:
```
Instance <your-instance-id> seeded on YYYY-MM-DD. Validate passed.
GitHub: https://github.com/<handle>/Cici/tree/seed/my-instance/users/<your-instance-id>
```

---

## Reference

Full walkthrough: [`docs/seed-phase.md`](../../../../docs/seed-phase.md)  
Template location: [`users/_template/`](../../../../users/_template/)  
Validation script: [`scripts/validate-governed-state.py`](../../../../scripts/validate-governed-state.py)

---

## Stuck?

- If `validate-governed-state.py` errors on "missing surface-map," add a `surface-map.json` — look at `users/cici/governed-state/surface-map.json` as a reference and copy the structure.
- If you're unsure what `supabase_project_ref` looks like, open your Supabase dashboard → your project → Project Settings → General → the Reference ID.
- Ask in the group — don't guess.
