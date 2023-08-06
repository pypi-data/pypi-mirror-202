from __future__ import annotations

import argparse

from awsslack.commands.codebuild import trigger_cb
from awsslack.commands.codedeploy import trigger_cd
from awsslack.commands.config import auto_generate, get_config_object


def main() -> int:
    parser = argparse.ArgumentParser(prog="awsslack")

    # subparsers
    subparsers = parser.add_subparsers(dest="command")
    config_parser = subparsers.add_parser(
        "config",
        help=".awsslack-config.yaml options",
    )
    code_build_parser = subparsers.add_parser(
        "codebuild",
        help="AWS CodeBuild trigger & push updates to Slack",
    )
    code_deploy_parser = subparsers.add_parser(
        "codedeploy",
        help="AWS CodeDeploy trigger & push updates to Slack",
    )

    # config subparser commands
    config_parser.add_argument(
        "--auto-generate",
        action="store_true",
        default=False,
        help="Attempt to auto generate .awsslack-config.yaml by fetching metadata from aws",
    )

    # codebuild subparser commands
    code_build_parser.add_argument(
        "--project",
        "-P",
        required=True,
        help="Project name setup in ~/.aws/.awsslack-config.yaml",
    )
    code_build_parser.add_argument(
        "--environment",
        "-E",
        choices=["qa", "dev", "prod"],
        const="dev",
        default="dev",
        nargs="?",
        help="Project env setup in ~/.aws/.awsslack-config.yaml",
    )
    code_build_parser.add_argument(
        "--update-sources-interactively",
        action="store_true",
        default=False,
        help="CodeBuild Source(s) will be updated prior to execution",
    )

    # codedeploy subparser commands
    code_deploy_parser.add_argument(
        "--project",
        "-P",
        required=True,
        help="Project name setup in ~/.aws/.awsslack-config.yaml",
    )
    code_deploy_parser.add_argument(
        "--environment",
        "-E",
        choices=["qa", "dev", "prod"],
        const="dev",
        default="dev",
        nargs="?",
        help="Project env setup in ~/.aws/.awsslack-config.yaml",
    )
    code_deploy_parser.add_argument(
        "--commit",
        "-C",
        help="Repository's commit-hash that'll be deployed",
    )
    code_deploy_parser.add_argument(
        "--branch",
        "-B",
        help="Repository's branch-name; required when '--commit' not provided",
    )

    args = parser.parse_args()

    if args.command == "config" and args.auto_generate:
        return auto_generate()

    config = get_config_object()

    if args.command == "codebuild":
        return trigger_cb(config=config, args=args)

    if args.command == "codedeploy":
        return trigger_cd(config=config, args=args)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
