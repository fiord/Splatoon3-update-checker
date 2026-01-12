# Splatoon3 update checker

### usage

1. configure settings

```bash
gcloud auth application-default login
cd terraform
terraform init
```

You can edit `terraform/variables.tf` to set default values for `project_id` and `discord_token`.

2. check plan

You can check what changes will be applied.

```bash
terraform plan \
    -var="project_id=YOUR_PROJECT_ID" \
    -var="discord_token=YOUR_DISCORD_TOKEN"
```

3. deploy
```bash
terraform apply \
    -var="project_id=YOUR_PROJECT_ID" \
    -var="discord_token=YOUR_DISCORD_TOKEN"
```

### troubleshooting

`journalctl` is useful to check logs.

```
sudo journalctl -u discord-bot.service
```