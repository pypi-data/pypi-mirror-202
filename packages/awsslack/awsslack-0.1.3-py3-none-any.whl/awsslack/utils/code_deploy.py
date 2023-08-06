from __future__ import annotations

import subprocess
import time
from collections import OrderedDict
from typing import Any

import boto3

from awsslack.commands.config import AWSConfig, CodeDeployConfigApp, SlackConfig
from progress_bar import SlackProgress


def execute_cd(
    cd_conf: CodeDeployConfigApp,
    slack_conf: SlackConfig,
    aws_conf: AWSConfig,
    commit: str,
) -> int:
    project_name = cd_conf.app
    deployment_group = cd_conf.group
    github_repository = cd_conf.repo

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

    # create Deployment
    print(f"Creating deployment for commit: {commit}")
    codedeploy_client = boto3.client("codedeploy")
    deploy_response_data: dict = codedeploy_client.create_deployment(
        applicationName=project_name,
        deploymentGroupName=deployment_group,
        deploymentConfigName="CodeDeployDefault.AllAtOnce",
        description=f"Initiated using `awsslack` package - by {iam_username}",
        revision={
            "revisionType": "GitHub",
            "gitHubLocation": {
                "repository": github_repository,
                "commitId": commit,
            },
        },
        fileExistsBehavior="OVERWRITE",
    )
    deployment_id = deploy_response_data["deploymentId"]

    # get Deployment
    deploy_response_data = codedeploy_client.get_deployment(deploymentId=deployment_id)
    deployment_info = deploy_response_data["deploymentInfo"]
    deployment_status = deployment_info["status"]

    # list Deployment Instances
    is_deployment_ready = False
    while not is_deployment_ready:
        try:
            response = codedeploy_client.list_deployment_instances(
                deploymentId=deployment_id,
            )
            instances_list = response["instancesList"]
            is_deployment_ready = True
        except Exception:
            # sleeping for 5 sec
            time.sleep(5)

    deploy_phases_updated_in_slack_mapping: dict[str, Any] = {}
    for instance in instances_list:
        deploy_phases_updated_in_slack_mapping[instance] = OrderedDict()

    # Batch Get Deployment Targets
    response = codedeploy_client.batch_get_deployment_instances(
        deploymentId=deployment_id,
        instanceIds=instances_list,
    )
    for deployment_instance in response["instancesSummary"]:
        deployment_instance_id = deployment_instance["instanceId"]
        _instance_id = deployment_instance_id.rpartition("/")[-1]
        deployment_instance_lifecycle_events = deployment_instance["lifecycleEvents"]
        deploy_phases_updated_in_slack_mapping[_instance_id] = {}

        for deployment_instance_lifecycle_event in deployment_instance_lifecycle_events:
            lifecycle_event_name = deployment_instance_lifecycle_event[
                "lifecycleEventName"
            ]
            deploy_phases_updated_in_slack_mapping[_instance_id][
                lifecycle_event_name
            ] = False

    # generate AWS CodeDeploy Console URL
    code_deploy_console_link = f"https://{aws_conf.region}.console.aws.amazon.com/codesuite/codedeploy/deployments/{deployment_id}?region={aws_conf.region}"

    # Initialize Slack here
    prefix = f"<{code_deploy_console_link}|*CodeDeploy: {project_name} - {deployment_group}*>"
    sp = SlackProgress(
        token=slack_conf.token,
        channel=slack_conf.channel_name,
        prefix=prefix,
    )
    current_percentage_int = 0.0

    # Initialize Slack ProgressBar here
    pbar = sp.new()
    log_message = f"Build: *{project_name}*, DeploymentStatus=`{deployment_status}`, Initiated by: {iam_username_log_message}"
    pbar.pos = current_percentage_int
    pbar.log(log_message)

    is_deployment_in_progress = (
        True if deployment_status not in ["Succeeded", "Failed", "Stopped"] else False
    )
    while is_deployment_in_progress:
        # Sleeping for 5 sec
        time.sleep(5)

        ## Update new phases
        # Get Deployment
        deploy_response_data = codedeploy_client.get_deployment(
            deploymentId=deployment_id,
        )
        deployment_info = deploy_response_data["deploymentInfo"]
        deployment_status = deployment_info["status"]
        is_deployment_in_progress = (
            True
            if deployment_status not in ["Succeeded", "Failed", "Stopped"]
            else False
        )
        if not is_deployment_in_progress:
            # break here and update slack finally.
            log_message = (
                f"Deploy: *{project_name}*, DeployentStatus=`{deployment_status}`"
            )
            if deployment_status == "Succeeded":
                log_message_emoji = ":large_blue_circle:"
            else:
                log_message_emoji = ":red_circle:"
            log_message += log_message_emoji
            pbar.pos = 100
            pbar.log(log_message)
            break

        # List Deployment Instances
        response = codedeploy_client.list_deployment_instances(
            deploymentId=deployment_id,
        )
        instances_list = response["instancesList"]

        # Batch Get Deployment Targets
        response = codedeploy_client.batch_get_deployment_instances(
            deploymentId=deployment_id,
            instanceIds=instances_list,
        )
        for deployment_instance in response["instancesSummary"]:
            deployment_instance_id = deployment_instance["instanceId"]
            _instance_id = deployment_instance_id.rpartition("/")[-1]
            deployment_instance_lifecycle_events = deployment_instance[
                "lifecycleEvents"
            ]
            if not deploy_phases_updated_in_slack_mapping.get(_instance_id):
                deploy_phases_updated_in_slack_mapping[_instance_id] = {}

            for (
                deployment_instance_lifecycle_event
            ) in deployment_instance_lifecycle_events:
                lifecycle_event_name = deployment_instance_lifecycle_event[
                    "lifecycleEventName"
                ]
                # lifecycle_event_status = deployment_instance_lifecycle_event["status"]
                if (
                    lifecycle_event_name
                    not in deploy_phases_updated_in_slack_mapping[_instance_id]
                ):
                    deploy_phases_updated_in_slack_mapping[_instance_id][
                        lifecycle_event_name
                    ] = False

        #
        for (
            instance_id,
            instance_phases,
        ) in deploy_phases_updated_in_slack_mapping.items():
            deploy_phase_found = False
            for (
                _deploy_phase,
                _is_deploy_phase_updated_in_slack,
            ) in instance_phases.items():
                if _is_deploy_phase_updated_in_slack:
                    continue

                print(f"updating slack, Deploy Phase: {_deploy_phase}")
                phases_found = []
                break_main = False
                for deployment_instance in response["instancesSummary"]:
                    if break_main:
                        break

                    deployment_instance_id = deployment_instance["instanceId"]
                    _instance_id = deployment_instance_id.rpartition("/")[-1]
                    if instance_id != _instance_id:
                        continue

                    deployment_instance_lifecycle_events = deployment_instance[
                        "lifecycleEvents"
                    ]
                    for (
                        deployment_instance_lifecycle_event
                    ) in deployment_instance_lifecycle_events:
                        lifecycle_event_name = deployment_instance_lifecycle_event[
                            "lifecycleEventName"
                        ]
                        # lifecycle_event_status = deployment_instance_lifecycle_event["status"]
                        phases_found.append(lifecycle_event_name)
                        if _deploy_phase != lifecycle_event_name:
                            continue

                        break_main = True
                        phase_type, phase_status, instance_label = (
                            lifecycle_event_name,
                            deployment_instance_lifecycle_event.get("status"),
                            deployment_instance.get("instanceType"),
                        )

                        if not phase_status:
                            # Deploy Phase has no status yet
                            break

                        if phase_status in ["Pending", "InProgress"]:
                            # skipping, phase is either Pending or InProgress
                            continue

                        log_message = f"Deploy: *{project_name}*, DeployentStatus=`{deployment_status}`"

                        if instance_label == "Blue":
                            log_message_emoji = ":blue_book:"
                        else:
                            log_message_emoji = ":green_book:"

                        instance_link = f"https://{aws_conf.region}.console.aws.amazon.com/ec2/v2/home?region={aws_conf.region}#Instances:instanceId={_instance_id}"
                        log_message = f"Deployment's Phase: {phase_type}, [{log_message_emoji} <{instance_link}|*{_instance_id}*>] PhaseStatus=*{phase_status}*"
                        current_percentage_int += 100 / 13
                        current_percentage_int = round(current_percentage_int, 1)
                        pbar.pos = current_percentage_int
                        pbar.log(log_message)
                        deploy_phases_updated_in_slack_mapping[_instance_id][
                            _deploy_phase
                        ] = True
                        break

    log_message = f"{prefix} *{deployment_status}!* {iam_username_log_message}"
    pbar.log_thread(log_message)

    return 0


def get_commit_remote(repo: str, branch: str) -> str:
    ssh_git_repo_url = f"git@github.com:{repo}.git"

    cmd = f'echo "$(git ls-remote {ssh_git_repo_url} | grep refs/heads/{branch} | cut -f 1)"'
    p_stdout = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
    assert p_stdout, "can't fetch commit, please consider providing'--commit'"

    return p_stdout.read().decode("utf-8").strip("\n")
