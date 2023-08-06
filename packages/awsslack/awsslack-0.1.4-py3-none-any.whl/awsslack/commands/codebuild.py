import argparse

from awsslack.commands.config import AWSSlackConfig
from awsslack.utils.code_build import execute_cb, update_sources_i


def trigger_cb(config: AWSSlackConfig, args: argparse.Namespace) -> int:
    # parse args
    cb_name = args.project
    cb_env = args.environment
    update_sources_interactively = args.update_sources_interactively

    # validate args
    assert cb_name in config.projects_config.projects
    assert cb_env in config.projects_config.projects[cb_name]
    cb_conf = config.projects_config.projects[cb_name][cb_env]["codebuild"]

    if update_sources_interactively:
        update_sources_i(cb_conf=cb_conf)

    return execute_cb(
        cb_conf=cb_conf,
        slack_conf=config.slack_config,
        aws_conf=config.aws_config,
    )
