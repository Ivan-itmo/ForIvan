#!/usr/bin/env bash
set -u

GRADLE_COMMAND="${GRADLE_COMMAND:-gradle}"
GIT_COMMAND="${GIT_COMMAND:-git}"
HISTORY_OUTPUT_DIR="${HISTORY_OUTPUT_DIR:-history-output}"
HISTORY_DIFF_FILE="${HISTORY_DIFF_FILE:-history-output/last-working-revision.diff}"
HISTORY_WORKTREE_DIR="${HISTORY_WORKTREE_DIR:-../history-worktree}"

mkdir -p "$HISTORY_OUTPUT_DIR"
rm -f "$HISTORY_DIFF_FILE"
rm -rf "$HISTORY_WORKTREE_DIR"

last_working_revision=""
previous_bad_revision=""

for revision in $($GIT_COMMAND rev-list HEAD); do
    echo "Проверяется ревизия $revision"

    rm -rf "$HISTORY_WORKTREE_DIR"
    "$GIT_COMMAND" worktree prune >/dev/null 2>&1

    if ! "$GIT_COMMAND" worktree add --detach "$HISTORY_WORKTREE_DIR" "$revision" >/dev/null 2>&1; then
        echo "Не удалось создать worktree для ревизии $revision"
        continue
    fi

    if (
        cd "$HISTORY_WORKTREE_DIR/Lab3" &&
        "$GRADLE_COMMAND" --no-daemon clean compile >/dev/null 2>&1
    ); then
        last_working_revision="$revision"
        "$GIT_COMMAND" worktree remove --force "$HISTORY_WORKTREE_DIR" >/dev/null 2>&1
        break
    fi

    previous_bad_revision="$revision"

    "$GIT_COMMAND" worktree remove --force "$HISTORY_WORKTREE_DIR" >/dev/null 2>&1
done

rm -rf "$HISTORY_WORKTREE_DIR"
"$GIT_COMMAND" worktree prune >/dev/null 2>&1

if [ -z "$last_working_revision" ]; then
    echo "Компилируемая ревизия не найдена"
    exit 1
fi

if [ -z "$previous_bad_revision" ]; then
    echo "Текущая ревизия уже компилируется, rollback не требуется."
    echo "Текущая ревизия уже компилируется, rollback не требуется." > "$HISTORY_DIFF_FILE"
    exit 0
fi

echo "Найдена последняя рабочая ревизия: $last_working_revision"
echo "Первая нерабочая ревизия после неё: $previous_bad_revision"
echo "Формируется diff: $HISTORY_DIFF_FILE"

"$GIT_COMMAND" diff "$last_working_revision" "$previous_bad_revision" > "$HISTORY_DIFF_FILE"

echo "Diff сохранён в $HISTORY_DIFF_FILE"