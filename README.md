# Demo Slack Bot app

## When the app is installed and finished you should be able to see something like this.
![screen demo](./media/command_demo.gif)


## Required software
* gnu make
* nodejs 
* npm
* terraform
* tfswitch
* docker
* docker-compose ~> 1.29
* python ~> 3.9
* python-poetry
* aws cli


# Pre Setup (making this your own)
## Terraform
edit [./tf/main.tf](./tf/main.tf) and adjust the region in the aws provider
block .

## Edit config.sjon
edit [./config.json](./config.json) and adjust the values as needed


## Initialize Environment

### Set your AWS REGION and UID (for docker layer generation)
```
export AWS_REGION="us-east-x"
export UID="$(id -u)"
```

### Poetry
`poetry update`

## Run terraform
```
cd ./tf
tfswitch
terraform init
terraform plan -out plan.out
terraform apply plan.out
```

## Initialize a blank ssm secret
```
./bin/crypt.sh save
```
Running this script the first time will create an empty `.secrets.json` file in your project, and then populate it with a secrets template. These secrets are put in the parameter store in AWS SSM. 
These values will be filled in and updated in AWS SSM later.

## Install npm packages
```
npm install
```

## Build backend layer
```
make backend_layer
```

## Generate slack manifest
```
make gen_slack_manifest
```
This will generate a slack manifest template for you to create your Slack App and generate the secrets stored in the AWS SSM Parameter store.

## Setup Slack App
* Create two channels in your workspace, one as a primary channel for your app,
    and another for exceptions the application may throw (for monitoring)
    * ![Create Two Channels for app in your workspace](./media/create_slack_channels_for_app.png)

* Navigate to the slack apps [page](https://api.slack.com/apps/)
* Select "Create New App"
    * ![Create New App](./media/create_new_app.png)
* Select "Create App from Manifest"
    ![Create app from manifest](./media/create_new_from_manifest.png)

* Select your desired workspace
    * ![](./media/create_new_select_workspace.png)

* Copy the text in `./slack/manifest.yaml` generated from the previous command,
    and past into the window
    * ![Copy paste generated manifest data](./media/create_new_paste_manifest.png)

* Change all the `url` keys to `http://localhost` - this will be updated later.

* Finalize your app creation
    * ![Finalize](./media/create_new_finalize.png)

* Click "Install to Workspace"
    * ![install to workspace](./media/install_app_start.png)

* Authorize App, and select your primary channel you created in a previous step
    * ![select primary channel](./media/install_app_authorize.png)

* Go to "Incoming Webhooks" and click "Add New Webhook to workspace"
    * ![add new webhook](./media/wh_add_new_webhook.png)

* Select the exception webhook you created earlier
    * ![select exception webhook](./media/wh_create_exception_webhook.png)

* Edit your .secrets.json file, and populate with values from the various parts
of the application. You secrets json file should look like the first image.
    * ![secrets edit](./media/creds_secrets_json_edit.png)
    * ![webhooks](./media/creds_webhook_copy_paste.png)
    * ![application creds](./media/creds_app.png)
    * ![bot token](./media/creds_bot_token.png)

* Once all these are updated save the file and issue the command
    *
```
./bin/crypt.sh save
```

After your secrets are saved, deploy the backend;
```
make deploy_all
```

Now that the backend is in place, you can generate an updated manifest with the URL for your App's deployment;
```
make gen_slack_manifest
```

Copy your new `slack/manifest.yml` file into your App's configuration.

* Once the backend is built and your manifest is updated, go your "App Manifest" section, and click the verify
location
    * ![verify](./media/verify_endpoint.png)

* At this point you should be done, save your source control, and follow the
steps below to maintain / update the application.



## Maintenance

# Deploy instructions

## Serverless

### updating / adding packages
```
## Upgrade existing packages
poetry upgrade

## add new direct packages (will be in layer)
poetry add xyz

## Add development package
poetry add -D foo
```

### Deploying layer changes
```
make deploy_all
```

### Deploying only code changes
```
make deploy_only_serverless
```

## Tailing logs
```
# Tail lambda web
make logs
```

## Updating Terraform

```
cd ./tf
terraform plan -out plan.out
terraform apply plan.out
```
