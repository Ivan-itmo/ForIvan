#!/bin/sh
set -u

repo_dir="${1:-.}"
git_cmd="${2:-git}"
ant_cmd="${3:-ant}"
worktree_dir="${4:-../history-worktree-ant}"
diff_file="${5:-history-output/last-working-revision.diff}"

mkdir -p "$(dirname "$diff_file")"
rm -f "$diff_file"
rm -rf "$worktree_dir"

last_working_revision=""
previous_bad_revision=""

for revision in $("$git_cmd" -C "$repo_dir" rev-list HEAD); do
    echo "Проверяется ревизия $revision"

    rm -rf "$worktree_dir"
    "$git_cmd" -C "$repo_dir" worktree prune >/dev/null 2>&1

    if ! "$git_cmd" -C "$repo_dir" worktree add --detach "$worktree_dir" "$revision" >/dev/null 2>&1; then
        echo "Не удалось создать worktree для ревизии $revision"
        continue
    fi

    if (
        cd "$worktree_dir/Lab3" &&
        "$ant_cmd" -q compile >/dev/null 2>&1
    ); then
        last_working_revision="$revision"
        "$git_cmd" -C "$repo_dir" worktree remove --force "$worktree_dir" >/dev/null 2>&1
        break
    fi

    previous_bad_revision="$revision"

    "$git_cmd" -C "$repo_dir" worktree remove --force "$worktree_dir" >/dev/null 2>&1
done

rm -rf "$worktree_dir"
"$git_cmd" -C "$repo_dir" worktree prune >/dev/null 2>&1

if [ -z "$last_working_revision" ]; then
    echo "Компилируемая ревизия не найдена"
    echo "Компилируемая ревизия не найдена" > "$diff_file"
    exit 1
fi

if [ -z "$previous_bad_revision" ]; then
    echo "Текущая ревизия уже компилируется, rollback не требуется."
    echo "Текущая ревизия уже компилируется, rollback не требуется." > "$diff_file"
    exit 0
fi

echo "Найдена последняя рабочая ревизия: $last_working_revision"
echo "Первая нерабочая ревизия после неё: $previous_bad_revision"
echo "Формируется diff: $diff_file"

"$git_cmd" -C "$repo_dir" diff "$last_working_revision" "$previous_bad_revision" > "$diff_file"

echo "Diff сохранён в $diff_file"