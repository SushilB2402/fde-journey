# Git workflow notes

My own reference for working with Git and GitHub on the fde-journey repo. I use Git Bash on Windows and the `gh` command-line tool.

## 1. The normal loop

Every change, however small, follows these steps.

```bash
git switch main                      # start from main, so my branch begins from the latest code
git pull                             # latest main, so I don't build on an old copy
git switch -c week3/my-change        # -c creates the branch and moves me onto it; main stays untouched
# ...edit files...
git status -sb                       # short status: my branch, ahead/behind GitHub, and any changed or untracked files
git branch --show-current            # am I really on my branch, not main?
git add path/to/file.py              # add by name, so lab folders and sandboxes never sneak in
git diff --cached --stat             # last look: exactly the files I expect, or I stop
git commit -m 'Short message'        # save a snapshot of what I staged
git push -u origin week3/my-change   # publish the branch; -u links it to GitHub
gh pr create --fill                  # open the pull request from my commit messages
gh pr diff                           # read my own diff before merging (or: gh pr view --web)
gh pr merge --merge --delete-branch  # merge into main and delete the branch on GitHub
git switch main                      # back to main
git pull                             # bring the merged work into my local main
git fetch --prune                    # forget remote branches that no longer exist
git branch -d week3/my-change        # delete the local branch (gh may already have done it)
```

Before every commit and every push, I run `git branch --show-current` and `git status -sb`. It takes a second and prevents most of my mistakes.

I add files by name because `git add .` can stage things I never meant to share, like generated data or a virtual environment.

## 2. Conflicts

A conflict happens when two branches changed the same lines of the same file. Git can't choose, so it stops the merge and writes both versions into the file:

```
<<<<<<< HEAD
the version on the branch I am standing on
=======
the version coming in from the other branch
>>>>>>> green
```

- `<<<<<<< HEAD` starts my side, the branch I am on.
- `=======` is the divider between my side and theirs.
- `>>>>>>> green` ends their side, and the name after it is the branch I merged in.

How I fix one:
1. `git status` shows the file as "both modified".
2. Open the file and read both versions.
3. Write the final text I want: mine, theirs, or a mix.
4. Delete all three marker lines. They are not code, and they must never be committed.
5. `grep -n '<<<<<<<\|=======\|>>>>>>>' file` prints nothing when I've got them all.
6. `git add file`, then `git commit`.
7. `git log --oneline -3` shows the merge commit.

If I get lost, `git merge --abort` puts everything back as it was before the merge.

## 3. Mistakes I made and the fix

| What I did | How I noticed | The fix |
|---|---|---|
| Reused a branch name that already existed, so the new branch never got created | `git switch -c` said "already exists" and I carried on | `git branch -a` first. Delete an old branch only when `git log main..name` is empty |
| Committed the join file on `main` | The commit showed on `main`, and I had pushed it | `git branch --show-current` before every commit |
| Added a file to `.gitignore` and Git kept tracking it | It still showed in `git status` | `git rm --cached file`, then commit |
| Wanted to `--amend` after pushing | The history no longer matched GitHub | Amend only commits I haven't pushed |
| Deleted branches still showed locally | `git branch -a` listed branches that no longer exist | `git fetch --prune` |
| Ran `gh pr create` while on `main` | "head branch main is the same as base branch main" | A PR needs a branch with its own commits |
| A script with a relative path made a nested folder | `week3/pandas/week3/pandas/data` appeared | `Path(__file__).parent / "data"` |
| Pasted code with leading spaces | `IndentationError` | Check column 1 after pasting |
| Ran the commit chain before editing the file | "nothing to commit" | Edit, save, then `git status -sb` must show `M` |
| Ran the conflict lab inside my real repo | The prompt said `(red\|MERGING)` | Do labs in a scratch folder outside the repo, and check `pwd` |
| Used a stale `python` after deleting a clone | "No such file" for every command | `deactivate`, then `hash -r` |
| Ran the clone test before merging | The clone had no scripts | Push and merge first, then clone |

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
