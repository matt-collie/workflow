#!/usr/bin/env python3
"""
Create a GitHub pull request via API.

This script is used by agents to automatically create pull requests
when features are ready for review.
"""

import os
import sys
import json
import argparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError


def create_pull_request(
    repo: str,
    title: str,
    body: str,
    head: str,
    base: str = "main",
    token: str = None
) -> dict:
    """
    Create a pull request using GitHub API.

    Args:
        repo: Repository in format "owner/repo"
        title: PR title
        body: PR description
        head: Branch to merge from
        base: Branch to merge into (default: main)
        token: GitHub personal access token

    Returns:
        dict: PR data from GitHub API

    Raises:
        HTTPError: If API request fails
    """
    # Get token from environment if not provided
    if not token:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            raise ValueError(
                "GitHub token required. Set GITHUB_TOKEN environment variable "
                "or pass --token argument"
            )

    # GitHub API endpoint
    url = f"https://api.github.com/repos/{repo}/pulls"

    # PR data
    data = {
        "title": title,
        "body": body,
        "head": head,
        "base": base
    }

    # Create request
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }

    request = Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    # Make request
    try:
        with urlopen(request) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result
    except HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"Error creating PR: {e.code} {e.reason}", file=sys.stderr)
        print(f"Response: {error_body}", file=sys.stderr)
        raise


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Create a GitHub pull request"
    )
    parser.add_argument(
        "repo",
        help="Repository in format 'owner/repo'"
    )
    parser.add_argument(
        "--title",
        required=True,
        help="PR title"
    )
    parser.add_argument(
        "--body",
        help="PR description (markdown supported)"
    )
    parser.add_argument(
        "--head",
        required=True,
        help="Branch to merge from"
    )
    parser.add_argument(
        "--base",
        default="main",
        help="Branch to merge into (default: main)"
    )
    parser.add_argument(
        "--token",
        help="GitHub personal access token (or set GITHUB_TOKEN env var)"
    )
    parser.add_argument(
        "--body-file",
        help="Read PR body from file"
    )

    args = parser.parse_args()

    # Read body from file if specified
    body = args.body
    if args.body_file:
        with open(args.body_file, "r") as f:
            body = f.read()

    if not body:
        body = ""

    # Create PR
    try:
        result = create_pull_request(
            repo=args.repo,
            title=args.title,
            body=body,
            head=args.head,
            base=args.base,
            token=args.token
        )

        # Output results
        print(f"✓ Pull request created successfully!")
        print(f"  Number: #{result['number']}")
        print(f"  URL: {result['html_url']}")
        print(f"  State: {result['state']}")

        # Return success
        return 0

    except Exception as e:
        print(f"✗ Failed to create pull request: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
