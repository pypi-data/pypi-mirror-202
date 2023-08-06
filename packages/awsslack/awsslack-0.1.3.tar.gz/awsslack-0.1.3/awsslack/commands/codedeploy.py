import argparse

from awsslack.commands.config import AWSSlackConfig
from awsslack.utils.code_deploy import execute_cd, get_commit_remote


def trigger_cd(config: AWSSlackConfig, args: argparse.Namespace) -> int:
    # parse args
    cd_name = args.project
    cd_env = args.environment

    # validate args
    assert cd_name in config.projects_config.projects
    assert cd_env in config.projects_config.projects[cd_name]
    cd_proj = config.projects_config.projects[cd_name][cd_env]["codedeploy"]

    for cd_conf in config.code_deploy_config.projects:
        if (
            cd_conf["app_name"] == cd_proj["name"]
            and cd_conf["deployment_group"] == cd_proj["group"]
        ):
            break
    else:
        err = "can't find CodeDeploy configuration, please consider 'awsslack --auto-generate' again?"
        raise ValueError(err)

    commit = args.commit
    if not commit:
        assert args.branch, "'--branch' not provided, unable to fetch commit"
        commit = get_commit_remote(repo=cd_conf.repo, branch=args.branch)

    return execute_cd(
        cd_conf=cd_conf,
        slack_conf=config.slack_config,
        aws_conf=config.aws_config,
        commit=commit,
    )
