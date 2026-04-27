#!/bin/sh
set -eu

repo_dir=$1
git_cmd=$2
gradle_cmd=$3
worktree_dir=$4
diff_file=$5

rm -rf "$worktree_dir"
mkdir -p "$(dirname "$diff_file")"

last_good=""
next_commit=""

for commit in $("$git_cmd" -C "$repo_dir" rev-list HEAD); do
    rm -rf "$worktree_dir"
    "$git_cmd" -C "$repo_dir" worktree add --force --detach "$worktree_dir" "$commit" >/dev/null 2>&1

    if (
        cd "$worktree_dir"
        "$gradle_cmd" classes >/dev/null 2>&1
    ); then
        last_good=$commit
        next_commit=$("$git_cmd" -C "$repo_dir" rev-list --ancestry-path --reverse "${commit}..HEAD" | head -n 1 || true)
        "$git_cmd" -C "$repo_dir" worktree remove --force "$worktree_dir" >/dev/null 2>&1 || true
        break
    fi

    "$git_cmd" -C "$repo_dir" worktree remove --force "$worktree_dir" >/dev/null 2>&1 || true
done

rm -rf "$worktree_dir"

if [ -z "$last_good" ]; then
    printf 'No compilable revision found.\n' >"$diff_file"
    exit 0
fi

if [ -z "$next_commit" ]; then
    {
        printf 'Working revision: %s\n' "$last_good"
        printf 'HEAD is already compilable; no later revision to compare.\n'
    } >"$diff_file"
    exit 0
fi

changed_files=$("$git_cmd" -C "$repo_dir" diff --name-only "$last_good" "$next_commit")

if [ -z "$changed_files" ]; then
    {
        printf 'Working revision: %s\n' "$last_good"
        printf 'Next revision: %s\n' "$next_commit"
        printf 'No changed files detected.\n'
    } >"$diff_file"
    exit 0
fi

"$git_cmd" -C "$repo_dir" diff "$last_good" "$next_commit" -- $changed_files >"$diff_file"
