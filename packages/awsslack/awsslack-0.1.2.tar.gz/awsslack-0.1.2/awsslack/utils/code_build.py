from __future__ import annotations

import time
import urllib.parse
from collections import OrderedDict

import boto3

from awsslack.commands.config import AWSConfig, SlackConfig
from progress_bar import SlackProgress


def execute_cb(
    cb_conf: dict[str, str],
    slack_conf: SlackConfig,
    aws_conf: AWSConfig,
) -> int:
    project_name = cb_conf["name"]

    # Not Live Yet!
    # breakpoint()
    return 1

    # get IAM User
    print("fetching IAM User...")
    sts_client = boto3.client("sts")
    response = sts_client.get_caller_identity()
    iam_username = response["Arn"].partition("/")[-1]
    iam_account_id = response["Account"]

    # get Slack User
    print("fetching Slack User...")
    if slack_conf.iam_slack_users.get(iam_username):
        iam_username_log_message = f"<@{slack_conf.iam_slack_users[iam_username]}>"
    else:
        iam_username_log_message = f"'AWS User {iam_username}'"

    # start Build
    print("Starting CodeBuild...")
    codebuild_client = boto3.client("codebuild")
    build_response_data_init: dict = codebuild_client.start_build(
        projectName=project_name,
    )
    build_id = build_response_data_init["build"]["id"]
    build_status = build_response_data_init["build"]["buildStatus"]
    build_phases = build_response_data_init["build"]["phases"]
    build_phases_updated_in_slack_mapping = OrderedDict()
    for _start_build_phase in build_phases:
        build_phases_updated_in_slack_mapping[_start_build_phase["phaseType"]] = False

    # generate AWS CodeBuild Console URL
    build_id_url_encoded = urllib.parse.quote_plus(build_id)
    code_build_console_link = f"https://{aws_conf.region}.console.aws.amazon.com/codesuite/codebuild/{iam_account_id}/projects/{project_name}/build/{build_id_url_encoded}/phase?region={aws_conf.region}"

    # Initialize Slack here
    prefix = f"<{code_build_console_link}|*CodeBuild: {project_name}*>"
    sp = SlackProgress(
        token=slack_conf.token,
        channel=slack_conf.channel_name,
        prefix=prefix,
    )
    current_percentage = 0.0

    # Initialize Slack ProgressBar here
    pbar = sp.new()
    log_message = f"Build: *{project_name}*, BuildStatus=`{build_status}`, Initiated by: {iam_username_log_message}"
    pbar.pos = current_percentage
    pbar.log(log_message)

    # send updates to Slack
    is_build_running = True
    while is_build_running:
        # Sleeping for 5 sec
        time.sleep(5)

        build_response_data: dict = codebuild_client.batch_get_builds(ids=[build_id])

        build_status = build_response_data["builds"][0]["buildStatus"]
        if build_status != "IN_PROGRESS":
            # break here and update slack finally.
            is_build_running = False
            log_message = f"Build: *{project_name}*, BuildStatus=`{build_status}`"
            if build_status == "SUCCEEDED":
                log_message_emoji = ":large_blue_circle:"
            else:
                log_message_emoji = ":red_circle:"
            log_message += log_message_emoji
            pbar.pos = 100
            pbar.log(log_message)
            break

        current_build_phases = build_response_data["builds"][0]["phases"]
        for _cbp in current_build_phases:
            if _cbp["phaseType"] not in build_phases_updated_in_slack_mapping:
                build_phases_updated_in_slack_mapping[_cbp["phaseType"]] = False

        for _, (_build_phase, _is_build_phase_updated_in_slack) in enumerate(
            list(build_phases_updated_in_slack_mapping.items()),
            start=1,
        ):
            if _is_build_phase_updated_in_slack:
                continue

            print(f"updating slack, Build Phase: {_build_phase}")
            build_phase_found = False
            phases_found = []
            for current_build_phase in current_build_phases:
                phaseType = current_build_phase["phaseType"]
                phases_found.append(phaseType)

                if _build_phase != phaseType:
                    continue

                build_phase_found = True
                break

            if not build_phase_found:
                # Build Phase not found, try again
                break

            if not current_build_phase.get("phaseStatus"):
                # Build Phase has no status yet, try again
                break

            phase_type, phase_status = (
                current_build_phase["phaseType"],
                current_build_phase["phaseStatus"],
            )
            log_message = f"Build's Phase: {phase_type}, PhaseStatus=*{phase_status}*"
            current_percentage += 100 / 11
            current_percentage = round(current_percentage, 1)
            pbar.pos = current_percentage
            pbar.log(log_message)
            build_phases_updated_in_slack_mapping[_build_phase] = True

    # send final update to Slack - reply in the thread
    build_phases_contexts = ""
    for current_build_phase in current_build_phases:
        if not current_build_phase.get("contexts"):
            continue
        for context in current_build_phase.get("contexts"):
            if context.get("message"):
                build_phases_contexts += f"\n\nBuild's Phase: *{current_build_phase['phaseType']}* Context: `{context.get('message')}`."
    pbar.log_thread(
        f"{prefix} *{build_status}!* {iam_username_log_message} {build_phases_contexts}",
    )

    return 0


def update_sources_i(cb_conf: dict[str, str]) -> None:
    raise NotImplementedError
