"""Production adapters for the async War Room run.

These touch real systems in deployment but are seam-injected so tests run with
no network: pass mock probe/repo/deploy objects, or rely on env-gated defaults.
"""
import os
import subprocess
import urllib.request


class ShopApiProbe:
    """Reproduce the incident against the live shop-api."""

    def __init__(self, base_url=None):
        self.base_url = (base_url or os.environ.get("SHOP_API_URL", "")).rstrip("/")

    def overcharge(self, ticket):
        # returns (path, charged) for the probe call described by the ticket
        path = ticket["probe"]
        url = f"{self.base_url}{path}"
        with urllib.request.urlopen(url, timeout=10) as r:  # noqa: S310 (trusted base)
            import json

            data = json.loads(r.read().decode())
        return path, data.get(ticket["probe_field"])


class RepoOps:
    """Clone, patch, branch and open a PR against the app repo (ADO)."""

    def __init__(self, repo_dir, branch=None, runner=subprocess.run):
        self.repo_dir = repo_dir
        self.branch = branch or "warroom/fix"
        self.run = runner

    def patch(self, rel_path, content):
        with open(os.path.join(self.repo_dir, rel_path), "w") as fh:
            fh.write(content)

    def branch_and_pr(self, title):
        self.run(["git", "checkout", "-b", self.branch], cwd=self.repo_dir, check=True)
        self.run(["git", "commit", "-am", title], cwd=self.repo_dir, check=True)
        self.run(["git", "push", "-u", "origin", self.branch], cwd=self.repo_dir, check=True)
        self.run(["az", "repos", "pr", "create", "--title", title, "--source-branch", self.branch],
                 cwd=self.repo_dir, check=True)
        return self.branch


class Redeployer:
    """Trigger the ADO pipeline that ships shop-api."""

    def __init__(self, runner=subprocess.run):
        self.run = runner

    def trigger(self, branch):
        self.run(["az", "pipelines", "run", "--branch", branch], check=True)
        return "queued"
