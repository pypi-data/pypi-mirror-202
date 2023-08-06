from __future__ import annotations

import json
from collections import defaultdict
from typing import Any

import boto3

from awsslack.utils.yaml import get_config, set_config, touch_config


class CodeBuildConfig:
    def __init__(self, projects: tuple[str] | None = None) -> None:
        self.projects: tuple = projects or tuple()

    def fetch_projects(self) -> None:
        print("fetching codebuild projects...")
        codebuild_client = boto3.client("codebuild")
        self.projects = tuple(
            codebuild_client.list_projects().get("projects", tuple()),
        )


class CodeDeployConfigApp:
    def __init__(self, app: str, group: str, repo: str):
        self.app = app
        self.group = group
        self.repo = repo

    def __repr__(self) -> str:
        return f"{self.app} {self.group} {self.repo}"

    def to_dict(self) -> dict[str, str]:
        return {
            "app_name": self.app,
            "deployment_group": self.group,
            "github_repository": self.repo,
        }


class CodeDeployConfig:
    def __init__(self, projects: tuple[dict[str, str]] | None = None) -> None:
        self.projects: tuple = projects or tuple()

    def fetch_projects(self) -> None:
        print("fetching codedeploy projects...")
        codedeploy_client = boto3.client("codedeploy")
        for codedeploy_application in codedeploy_client.list_applications().get(
            "applications",
        ):
            app_deployment_groups_response = codedeploy_client.list_deployment_groups(
                applicationName=codedeploy_application,
            )
            if not app_deployment_groups_response["deploymentGroups"]:
                continue

            for deployment_group in app_deployment_groups_response["deploymentGroups"]:
                app_deployments_response = codedeploy_client.list_deployments(
                    applicationName=codedeploy_application,
                    deploymentGroupName=deployment_group,
                )
                if not app_deployments_response.get("deployments"):
                    continue

                deployment_response = codedeploy_client.get_deployment(
                    deploymentId=app_deployments_response.get("deployments")[0],
                )
                deployment_revision = deployment_response.get("deploymentInfo", {}).get(
                    "revision",
                    {},
                )
                if deployment_revision.get("revisionType") != "GitHub":
                    continue

                github_repository = deployment_revision.get("gitHubLocation", {}).get(
                    "repository",
                )
                if not github_repository:
                    continue

                self.projects += (
                    CodeDeployConfigApp(
                        app=codedeploy_application,
                        group=deployment_group,
                        repo=github_repository,
                    ).to_dict(),
                )


class SlackConfig:
    def __init__(
        self,
        token: str | None = None,
        channel_name: str | None = None,
        iam_slack_users: dict[str, str] | None = None,
    ):
        self.token = token
        self.channel_name = channel_name
        self.iam_slack_users = iam_slack_users or {}

    def prompt_options(self):
        print("Slack Credentials")
        self.token = input("Slack access token:")
        self.channel_name = input("Slack channel name:")
        self.iam_slack_users = json.loads(input("IAM - Slack users mapping:"))

    def to_dict(self) -> dict[str, Any]:
        assert self.token
        assert self.channel_name
        assert self.iam_slack_users
        return {
            "token": self.token,
            "channel_name": self.channel_name,
            "iam_slack_users": self.iam_slack_users,
        }

    def from_dict(self, data) -> SlackConfig:
        self.token = data["token"]
        self.channel_name = data["channel_name"]
        self.iam_slack_users = data["iam_slack_users"]
        return self


class ProjectsConfig:
    def __init__(
        self,
        projects: dict | None = None,
        cb: CodeBuildConfig | None = None,
        cd: CodeDeployConfig | None = None,
    ):
        # self.projects type: 'project {}' -> 'env {}' -> 'cb/cd {}'
        self.projects: dict = projects or defaultdict(dict)
        self.code_build = cb
        self.code_deploy = cd

    def prompt_projects(self):
        q = "Would you like to define your projects interactively? (yes/no) "
        a = input(q)
        if a not in ("yes", "y"):
            return

        _0 = f"\n0. (skips)"
        _A = f"\nChoice: "

        cbs = self.code_build.projects
        cb_str = _0
        for i, p in enumerate(cbs, 1):
            cb_str += f"\n{i}. {p}"
        cb_str += _A

        cds = self.code_deploy.projects
        cd_str = _0
        for i, p in enumerate(cds, 1):
            cd_str += f"\n{i}. {p['app_name']} -- {p['deployment_group']}"
        cd_str += _A

        envs = ("qa", "dev", "prod")
        env_str = _0
        for i, e in enumerate(envs, 1):
            env_str += f"\n{i}. {e}"
        env_str += _A

        while True:
            project_name = input("Project Name: ")

            env_i = int(input(f"Choose env: {env_str}")) - 1
            env = envs[env_i]

            cb_i = int(input(f"Choose CodeBuild for {env} env: {cb_str}")) - 1
            codebuild = {"name": cbs[cb_i]}

            cd_i = int(input(f"Choose CodeDeploy for {env} env: {cd_str}")) - 1
            _cd = cds[cd_i]
            codedeploy = {
                "name": _cd["app_name"],
                "group": _cd["deployment_group"],
            }

            self.projects[project_name][env] = {
                "codebuild": codebuild,
                "codedeploy": codedeploy,
            }

            more = input("Would you like to add more Projects? (yes/no) ")
            if more not in ("yes", "y"):
                break

        self.projects = dict(self.projects)


class AWSConfig:
    def __init__(self, region: str | None = None) -> None:
        self.region = region

    def fetch_config(self) -> None:
        self.region = boto3.session.Session().region_name

    def to_dict(self) -> dict[str, str]:
        assert self.region
        return {"region": self.region}

    def from_dict(self, data: dict[str, str]) -> AWSConfig:
        self.region = data["region"]
        return self


class AWSSlackConfig:
    def __init__(
        self,
        cb: CodeBuildConfig,
        cd: CodeDeployConfig,
        aws: AWSConfig,
        slk: SlackConfig,
        proj: ProjectsConfig,
    ):
        self.code_build_config = cb
        self.code_deploy_config = cd
        self.aws_config = aws
        self.slack_config = slk
        self.projects_config = proj


def auto_generate() -> int:
    """
    Attempt to auto-generate .awsslack-config.yaml
    - input slack data from USER
    - fetch codebuild data from AWS
    - fetch codedeploy data from AWS
    - set codebuild/codedeploy data to config file
    """
    touch_config()

    code_build_config = CodeBuildConfig()
    code_build_config.fetch_projects()

    code_deploy_config = CodeDeployConfig()
    code_deploy_config.fetch_projects()

    aws_config = AWSConfig()
    aws_config.fetch_config()

    projects_config = ProjectsConfig(cb=code_build_config, cd=code_deploy_config)
    projects_config.prompt_projects()

    slack_config = SlackConfig()
    slack_config.prompt_options()

    data = get_config() or {}
    data["codebuild"] = code_build_config.projects
    data["codedeploy"] = code_deploy_config.projects
    data["aws"] = aws_config.to_dict()
    data["projects"] = projects_config.projects
    data["slack"] = slack_config.to_dict()
    set_config(data=data)

    return 0


def get_config_object():
    data = get_config()
    code_build_data = data["codebuild"]
    code_deploy_data = data["codedeploy"]
    aws_data = data["aws"]
    projects_data = data["projects"]
    slack_data = data["slack"]

    code_build_config = CodeBuildConfig(projects=tuple(code_build_data))
    code_deploy_config = CodeDeployConfig(
        projects=tuple(
            CodeDeployConfigApp(
                app=p["app_name"],
                group=p["deployment_group"],
                repo=p["github_repository"],
            )
            for p in code_deploy_data
        ),
    )
    aws_config = AWSConfig().from_dict(data=aws_data)
    project_config = ProjectsConfig(projects=projects_data)
    slack_config = SlackConfig().from_dict(data=slack_data)

    return AWSSlackConfig(
        cb=code_build_config,
        cd=code_deploy_config,
        aws=aws_config,
        proj=project_config,
        slk=slack_config,
    )
