
import os
import subprocess
from pathlib import Path

GITHUB_USER = "xmbh"
REPO_NAME = "contribution-graph"

DATES = [
    "2026-10-04",
    "2026-10-06",
    "2026-10-08",
    "2026-10-24",
    "2026-10-28",
    "2026-10-29",
    "2026-10-30",
    "2026-10-31",
    "2026-11-02",
    "2026-11-04",
]

def run(*args, env=None, capture=False):
    return subprocess.run(
        list(args),
        check=True,
        env=env,
        text=True,
        capture_output=capture
    )

def main():
    print(f"GitHub Contribution Graph - {GITHUB_USER}")

    # Check GitHub authentication
    run("gh", "auth", "status")
    account = run(
        "gh", "api", "user", "--jq", ".login",
        capture=True
    ).stdout.strip()

    if account.lower() != GITHUB_USER.lower():
        raise RuntimeError("Wrong GitHub account!")

    # Use existing repository, or clone it
    repo = Path.cwd() / REPO_NAME

    if repo.exists():
        os.chdir(repo)
        run("git", "rev-parse", "--show-toplevel")
    else:
        run(
            "gh", "repo", "clone",
            f"{GITHUB_USER}/{REPO_NAME}",
            str(repo)
        )
        os.chdir(repo)

    # Ensure main branch
    run("git", "checkout", "main")
    run("git", "pull", "--ff-only", "origin", "main")

    # Make commits for each date
    for date in DATES:
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = f"{date}T12:00:00 +0200"
        env["GIT_COMMITTER_DATE"] = f"{date}T12:00:00 +0200"

        filename = Path("contribution-history.md")

        with filename.open("a", encoding="utf-8") as f:
            f.write(f"- Historical entry: {date}\n")

        run("git", "add", str(filename))
        run(
            "git", "commit",
            "-m", f"Historical entry {date}",
            env=env
        )

        print(f"Commit created: {date}")

    # Push all commits
    run("git", "push", "origin", "main")

    print("\nAll 10 commits pushed!")
    print(f"https://github.com/{GITHUB_USER}/{REPO_NAME}")

if __name__ == "__main__":
    main()
