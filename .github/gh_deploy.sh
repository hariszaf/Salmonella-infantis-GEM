#!/usr/bin/env bash

# Do NOT set -v or -x or your GitHub API token will be leaked!
set -ue # exit with nonzero exit code if anything fails

echo "Parse memote.ini for values."
deployment=$(awk -F '=' '{if (! ($0 ~ /^;/) && $0 ~ /deployment/) print $2}' memote.ini | tr -d ' ')
location=$(awk -F '=' '{if (! ($0 ~ /^;/) && $0 ~ /location/) print $2}' memote.ini | tr -d ' ')


GITHUB_TOKEN="$1"
TRAVIS_BRANCH="$2"
TRAVIS_REPO_SLUG="$3"
TRAVIS_PULL_REQUEST="$4"

echo $GITHUB_TOKEN 
echo $TRAVIS_BRANCH
echo $TRAVIS_REPO_SLUG
echo $TRAVIS_PULL_REQUEST

if [[ "${TRAVIS_PULL_REQUEST}" != "false" || "${TRAVIS_REPO_SLUG}" != "hariszaf/Salmonella-infantis-GEM" ]]; then
    echo "Untracked build."
    memote run --ignore-git
    echo "Skip deploy."
    exit 0
else
    # Always need the deployment branch available locally for storing results.
    git checkout "${deployment}"
    git checkout "${TRAVIS_BRANCH}"
    echo "Tracked build."
    memote run 1>log 2>log
    echo "Start deploy to ${deployment}..."
fi

# Generate the history report on the deployment branch.
output="index.html"
git checkout "${deployment}"
echo "Generating updated history report '${output}'."
memote report history --filename="${output}"

# Add, commit and push the files.
git add "${output}"
git commit -m "GitHub action report # ${{github.run_number}}"
git push --quiet "https://${GITHUB_TOKEN}@github.com/${TRAVIS_REPO_SLUG}.git" "${deployment}" > /dev/null

echo "Your new report will be visible at https://hariszaf.github.io/Salmonella-infantis-GEM in a moment."
