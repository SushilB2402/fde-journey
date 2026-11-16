# Git workflow notes

My own reference for working with Git and GitHub on the fde-journey repo. I use Git Bash on Windows and the `gh` command-line tool.

## 1. The normal loop

Every change, however small, follows these steps.

```bash
git switch main                      # start from main
git pull                             # get the latest main
git switch -c week3/my-change        # new branch for this change
# ...edit files...
git status -sb                       # what changed, and which branch am I on?
git add path/to/file.py              # add files by name, never "git add ."
git diff --cached --stat             # check the staged list is exactly what I expect
git commit -m 'Short message'        # save the snapshot
git push -u origin week3/my-change   # publish the branch (-u links it to GitHub)
gh pr create --fill                  # open the pull request
gh pr diff                           # read the diff (or: gh pr view --web)
gh pr merge --merge --delete-branch  # merge, and delete the branch on GitHub
git switch main                      # go back
git pull                             # bring the merged work into local main
git fetch --prune                    # forget remote branches that no longer exist
git branch -d week3/my-change        # delete the local branch if it is still there
```

Before every commit and every push, I run `git branch --show-current` and `git status -sb`. It takes a second and prevents most of my mistakes.

I add files by name because `git add .` can stage things I never meant to share, like generated data or a virtual environment.

## 2. Conflicts

A conflict happens when two branches change the same lines of the same file and Git cannot decide which version to keep. Git stops the merge and writes both versions into the file between three marker lines:

```
<<<<<<< HEAD
my version (the branch I am on)
=======
their version (the branch I am merging in)
>>>>>>> other-branch-name
```

- `<<<<<<< HEAD` marks the start of my current branch's version.
- `=======` is the divider between the two versions.
- `>>>>>>> other-branch-name` marks the end of the incoming version.

How I resolve one:

1. `git status` shows which files are conflicted ("both modified").
2. Open each conflicted file and find the markers.
3. Decide what the final text should be: mine, theirs, or a mix.
4. Delete all three marker lines, keeping only the final text. The markers are not valid code and must not be committed.
5. Check the file reads correctly and runs.
6. `git add the-file` to tell Git the conflict is resolved.
7. `git commit` (or `git merge --continue`) to finish the merge.
8. `git log --oneline -5` to confirm the merge commit is there.

If I get lost, `git merge --abort` puts everything back to before the merge.

## 3. Mistakes I made and the fix

| What went wrong | How I noticed | The fix |
|---|---|---|
| A branch with that name already existed, so `git switch -c` never created the new branch and I kept working on the old one | `git switch -c` said "already exists" and I carried on anyway | Run `git branch -a` to see all branches. Pick a new name, or switch to the old one on purpose. Delete an old branch only after `git log main..branch-name --oneline` shows no unique commits; `git branch -d` also refuses if the work is not merged |
| I committed on `main` by accident | The commit appeared on main instead of a branch | Run `git branch --show-current` before every commit. If the commit is not pushed: make a branch from it (`git branch my-branch`), then move main back (`git reset --hard origin/main`, only when nothing else is uncommitted). If it is pushed, leave it or revert it, and be more careful next time |
| Adding a file to `.gitignore` did not stop Git tracking it | The file still showed up in `git status` | `.gitignore` only affects untracked files. Run `git rm --cached path/to/file` (add `-r` for a folder), then commit |
| I wanted to change a commit message after pushing | Git refused or the history diverged | `git commit --amend` is only safe on commits I have not pushed, because it rewrites history |
| Branches I deleted on GitHub still showed in my local list | `git branch -a` listed `remotes/origin/...` branches that no longer exist | `git fetch --prune` removes the stale remote-tracking names |
| `gh pr create` failed with "head branch main is the same as base branch main" | I was on `main` | A pull request needs a different branch from main. Create a branch, commit there, push it, then open the PR |
| A script with a relative path created a nested folder (`week3/pandas/week3/pandas/data`) outside my `.gitignore` rule | Generated files appeared as untracked | Build paths from the script's own location: `DATA = Path(__file__).parent / "data"` |
| Code pasted from a list had leading spaces and caused an `IndentationError` | Python refused to run the file | Python uses indentation as syntax. Paste into the editor and check the left edge, or use "Paste without formatting". Every top-level line must start in column 1 |

## 4. My cheat sheet

| Command | What it means |
|---|---|
| `git status -sb` | Short status plus my branch and whether I am ahead or behind |
| `git branch --show-current` | Which branch am I on right now? |
| `git switch -c name` | Create a new branch and move to it |
| `git pull` | Download and merge the latest changes from GitHub |
| `git add file` | Stage one named file for the next commit |
| `git diff --cached --stat` | Summary of what is staged and about to be committed |
| `git commit -m 'msg'` | Save the staged changes as a commit |
| `git push -u origin name` | Publish the branch to GitHub and link it |
| `gh pr create --fill` | Open a pull request using the commit messages |
| `git fetch --prune` | Update my view of GitHub and forget deleted branches |
