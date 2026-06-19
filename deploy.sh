set -e
set -x

./make_site.py
python ./build_pdf.py
cp leanprover-community-zh.pdf build/

if [ "$github_ref" = "refs/heads/lean4" ]; then
  git fetch origin gh-pages || true
  git worktree add -B gh-pages gh-pages-worktree origin/gh-pages || git worktree add -B gh-pages gh-pages-worktree
  find gh-pages-worktree -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
  cp -a build/. gh-pages-worktree/
  touch gh-pages-worktree/.nojekyll
  cd gh-pages-worktree/
  git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
  git config user.name "github-actions[bot]"
  git add -A .
  git diff-index --quiet HEAD || { git commit -m "Deploy Chinese documentation from $git_hash" && git push origin gh-pages; }
fi
