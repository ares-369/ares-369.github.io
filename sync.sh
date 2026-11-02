#!/usr/bin/env bash
# =============================================================================
# PRABHU MANIKANDAN VISWANATHAN — PORTFOLIO CONTINUOUS SYNC ENGINE
# Syncs local changes -> Forgejo CT 122 -> CT 120 Production -> GitHub Pages
# =============================================================================

set -e

REPO_DIR="/root/projects/portfolio"
CT_ID="120"
DEST_DIR="/opt/portfolio"
COMMIT_MSG="${1:-Update portfolio: $(date '+%Y-%m-%d %H:%M:%S')}"

cd "$REPO_DIR"

echo "====================================================================="
echo " [1/4] STAGING & COMMITTING LOCAL GIT CHANGES"
echo "====================================================================="
git add -A
if git diff-index --quiet HEAD -- 2>/dev/null; then
    echo "No uncommitted changes found. Proceeding with sync..."
else
    git commit -m "$COMMIT_MSG"
    echo "✓ Committed changes: $COMMIT_MSG"
fi

echo ""
echo "====================================================================="
echo " [2/4] DEPLOYING TO HOMELAB PRODUCTION (CT $CT_ID :8089)"
echo "====================================================================="
pct exec "$CT_ID" -- mkdir -p "$DEST_DIR"
for file in index.html styles.css app.js logo.png Prabhu_Manikandan_Viswanathan_CV.pdf README.md; do
    if [ -f "$file" ]; then
        pct push "$CT_ID" "$file" "$DEST_DIR/$file"
    fi
done

# Restart systemd service
pct exec "$CT_ID" -- systemctl restart proxc-portfolio.service
echo "✓ Homelab production updated and proxc-portfolio.service restarted."
echo "  Live URLs: https://portfolio.fieldofruin.com and https://prabhu.fieldofruin.com"

echo ""
echo "====================================================================="
echo " [3/4] PUSHING TO FORGEJO INTERNAL GIT SERVER (CT 122)"
echo "====================================================================="
if git remote | grep -q "^origin$"; then
    git push -u origin main 2>/dev/null || git push -u origin master 2>/dev/null || echo "Notice: Push to origin skipped or already up to date."
else
    echo "Notice: Remote 'origin' not configured yet."
fi

echo ""
echo "====================================================================="
echo " [4/4] PUSHING TO GITHUB (ares-369)"
echo "====================================================================="
if git remote | grep -q "^github$"; then
    echo "Pushing to GitHub remote..."
    if git push -u github main 2>&1 || git push -u github master 2>&1; then
        echo "✓ Successfully pushed to GitHub!"
        echo "  Live GitHub Pages: https://ares-369.github.io"
    else
        echo "⚠ Notice: Push to GitHub requires the repository to exist and deploy key added."
        echo "  See instructions below to link your GitHub repository."
    fi
else
    echo "Notice: Remote 'github' not set up yet."
fi

echo ""
echo "====================================================================="
echo "✓ CONTINUOUS SYNC COMPLETE"
echo "====================================================================="
