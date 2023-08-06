LAST_COMMIT=$(git log -1 --pretty=%B)
if [[ "$LAST_COMMIT" =~ ^(feat|fix|refactor|perf) ]]; then
	return
else
	echo "[SKIP] release"
	exit 0
fi
