#!/usr/bin/env bash
set -eu

GRADLE_COMMAND="${GRADLE_COMMAND:-gradle}"
GIT_COMMAND="${GIT_COMMAND:-git}"
HISTORY_OUTPUT_DIR="${HISTORY_OUTPUT_DIR:-history-output}"
HISTORY_DIFF_FILE="${HISTORY_DIFF_FILE:-history-output/last-working-revision.diff}"
HISTORY_WORKTREE_DIR="${HISTORY_WORKTREE_DIR:-history-output/worktree}"

mkdir -p "$HISTORY_OUTPUT_DIR"
rm -f "$HISTORY_DIFF_FILE"

current_revision="$($GIT_COMMAND rev-parse HEAD)"
previous_bad_revision="$current_revision"
last_working_revision=""

mapfile -t revisions < <($GIT_COMMAND rev-list HEAD)

for revision in "${revisions[@]}"; do
    rm -rf "$HISTORY_WORKTREE_DIR"

    if ! "$GIT_COMMAND" worktree add --detach "$HISTORY_WORKTREE_DIR" "$revision" >/dev/null 2>&1; then
        echo "Не удалось создать worktree для ревизии $revision"
        continue
    fi

    echo "Проверяется ревизия $revision"

    (
        cd "$HISTORY_WORKTREE_DIR" || exit 1
        "$GRADLE_COMMAND" --no-daemon clean compile
    )

    status=$?

    "$GIT_COMMAND" worktree remove --force "$HISTORY_WORKTREE_DIR" >/dev/null 2>&1

    if [ "$status" -eq 0 ]; then
        last_working_revision="$revision"
        break
    fi

    previous_bad_revision="$revision"
done

if [ -z "$last_working_revision" ]; then
    echo "Компилируемая ревизия не найдена"
    exit 1
fi

echo "Найдена последняя рабочая ревизия: $last_working_revision"
echo "Формируется diff: $HISTORY_DIFF_FILE"

"$GIT_COMMAND" diff "$last_working_revision" "$previous_bad_revision" > "$HISTORY_DIFF_FILE"

echo "Diff сохранён в $HISTORY_DIFF_FILE"
