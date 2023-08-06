# `awsslack`

Basic view of how it would look in Slack (reality is much better with live progress-bar)

```
my-slack-bot APP  12:02 AM
    ████████████████████ 100.0%
    00:02:12 - [Build: <project-name> BuildStatus=IN_PROGRESS!]
    00:02:17 - [Build's Phase: SUBMITTED PhaseStatus=SUCCEEDED]
    00:02:18 - [Build's Phase: QUEUED PhaseStatus=SUCCEEDED]
    00:02:48 - [Build's Phase: PROVISIONING PhaseStatus=SUCCEEDED]
    00:02:53 - [Build's Phase: DOWNLOAD_SOURCE PhaseStatus=SUCCEEDED]
    00:03:14 - [Build's Phase: INSTALL PhaseStatus=SUCCEEDED]
    00:03:19 - [Build's Phase: PRE_BUILD PhaseStatus=SUCCEEDED]
    00:05:00 - [Build's Phase: BUILD PhaseStatus=SUCCEEDED]
    00:05:31 - [Build's Phase: POST_BUILD PhaseStatus=SUCCEEDED]
    00:05:36 - [Build: <project-name> BuildStatus=SUCCEEDED!] (edited)
```

## Installation

```console
$ pip install awsslack
```

# Usage

## Config

Config file path is: `~/.aws/.awsslack-config.yaml`

```console
$ awsslack config --auto-generate
```

See help: `awsslack config --help`

## CodeBuild

Trigger Codebuild project for `dev` environment:

```console
$ awsslack codebuild -P <project-name> -E dev
```

Similarly, for `prod` environment:

```console
$ awsslack codebuild -P <project-name> -E prod
```

See help: `awsslack codebuild --help`

## CodeDeploy

Trigger CodeDeploy project for `dev` environment:

```console
$ awsslack codedeploy -P <project-name> -E dev
```

Similarly, for `prod` environment:

```console
$ awsslack codedeploy -P <project-name> -E prod
```

Note: If `--commit` is not provided, will fetch latest Commit ID from  `--branch`.

See help: `awsslack codedeploy --help`
