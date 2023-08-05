import json
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

import boto3

from awsslack.utils.yaml import get_config, set_config, touch_config


class CodeBuildConfig:
    def __init__(self, projects: Optional[Tuple[str]] = None) -> None:
        self.projects: Tuple = projects or tuple()

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

    def to_dict(self) -> Dict[str, str]:
        return {
            "app_name": self.app,
            "deployment_group": self.group,
            "github_repository": self.repo,
        }


class CodeDeployConfig:
    def __init__(self, projects: Optional[Tuple[Dict[str, str]]] = None) -> None:
        self.projects: Tuple = projects or tuple()

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


class Option:
    def __init__(self, name: str, prompt: str, value: str = ""):
        self.name = name
        self.prompt = prompt
        self.value = value

    def __repr__(self):
        return f"{self.name}: {self.value}"


class SlackConfig:
    def __init__(self):
        self.options = [
            Option("token", "Slack access token:"),
            Option("channel_name", "Slack channel name:"),
            Option("iam_slack_users", "IAM - Slack users mapping:"),
        ]

    def prompt_options(self):
        print("Slack Credentials")
        for option in self.options:
            option.value = input(option.prompt)

            if option.name == "iam_slack_users":
                option.value = json.loads(option.value)


class ProjectsConfig:
    def __init__(self, cb: CodeBuildConfig, cd: CodeDeployConfig):
        # self.projects type: 'project {}' -> 'env {}' -> 'cb/cd {}'
        self.projects: Dict = defaultdict(dict)
        self.code_build = cb
        self.code_deploy = cd

    def prompt_projects(self):
        q = "Would you like to define your projects interactively? (yes/no) "
        a = input(q)
        if a not in ("yes", "y"):
            self.projects = {}
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
            codebuild = cbs[cb_i]

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


def auto_generate() -> None:
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

    projects_config = ProjectsConfig(code_build_config, code_deploy_config)
    projects_config.prompt_projects()

    slack_config = SlackConfig()
    slack_config.prompt_options()

    data = get_config() or {}
    data["codebuild"] = code_build_config.projects
    data["codedeploy"] = code_deploy_config.projects
    data["projects"] = projects_config.projects
    data["slack"] = {o.name: o.value for o in slack_config.options}
    set_config(data=data)
