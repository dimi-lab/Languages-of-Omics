# Publish this repository to GitHub

The intended repository name is **`Languages-of-Omics`**.

## 1. Create the empty GitHub repository

While signed in to GitHub, open <https://github.com/new> and create:

- **Repository name:** `Languages-of-Omics`
- **Visibility:** Public
- **Initialize this repository:** leave README, `.gitignore`, and license unchecked

## 2. Connect and push the prepared local repository

In PowerShell, run:

```powershell
Set-Location "C:\Users\m092469\Documents\Codex\2026-08-25\i\outputs\Languages-of-Omics"
git remote add origin https://github.com/apeterswu/Languages-of-Omics.git
git push -u origin main
```

If the GitHub owner is not `apeterswu`, replace that part of the URL with the correct username or organization.

If `origin` was added previously, replace the `git remote add` line with:

```powershell
git remote set-url origin https://github.com/apeterswu/Languages-of-Omics.git
```

## 3. Verify

```powershell
git remote -v
git status
```

The expected final status is `Your branch is up to date with 'origin/main'` and `nothing to commit, working tree clean`.
