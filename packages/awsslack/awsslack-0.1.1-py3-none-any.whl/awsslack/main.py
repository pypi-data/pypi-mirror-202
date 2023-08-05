import argparse

from awsslack.commands.config import auto_generate


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

    args = parser.parse_args()

    if args.command == "config":
        if args.auto_generate:
            auto_generate()
        else:
            raise NotImplementedError
    elif args.command == "codebuild":
        pass
    elif args.command == "codedeploy":
        pass
    else:
        raise NotImplementedError

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
