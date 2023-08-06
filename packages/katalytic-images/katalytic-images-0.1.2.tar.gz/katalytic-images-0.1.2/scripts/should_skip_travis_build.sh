LAST_COMMIT=$(git log -1 --pretty=%B)
if [[ "$LAST_COMMIT" =~ ^(feat|fix|test|refactor|perf|style|chore) ]]; then
	# I include "style" and others to make sure the functionality is kept the same
	return
else
	echo "[SKIP] build"
	exit 0
fi
