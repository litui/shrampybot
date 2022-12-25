## ShrampyBot Mk. III - The Golden Shrimp Guild API

This is a bot/backend being used and developed actively by the [Golden Shrimp Guild](https://gsg.live) for announcing when streamers on the gsg.live Mastodon instance go live and other fun things.

ShrampyBot Mk. III has been rewritten (yes, again...) in Django!

This version broke all the functionality in 2.0 so please don't expect anything to work as it used to.

The current version uses Docker.

### Installation - Development

Please make sure you have docker-ce installed on Linux or Docker Desktop installed on Mac OS. If you will be deploying between different platforms (eg: M1 Mac to x86_64 vps) you will need to setup your docker compose to support cross-compilation with `buildx bake` which is out of scope of this guide.

#### Obtaining the Files

For the latest main development version:

`git clone https://github.com/litui/shrampybot`

Or download a zip of this repository and extract it to your dev environment.

#### Config File Setup

Copy `.env.example` to `.env` in the root of the repository. `SB_ENV` within this file should be set to `development` and the values you'd like to initialize the postgresql database with should be populated here as well. `BASE_URL` should be set to the protocol, hostname, and port (if different from the default) of your site. You'll also need to set the same values for NGINX. By default the external webserver image uses HTTPS so you'll need to provide the names of a certificate and key pair located in `nginx/ssl`. It's best to use filenames based on environment so these can differ in each .env file.

In the `etc` directory, copy `sb-backend_example.env` to `sb-backend_development.env`. This file will be automatically selected by the django backend based on the `SB_ENV` variable value you set previously. Generate your random keys (there are web tools for this) and populate your `psql://` database URL based on the values you set for initial population of your postgresql database.

You do not have to use AWS/S3 storage but you will need to change the `DEFAULT_FILE_STORAGE` and `STATICFILES_STORAGE` entries to appropriate values as per the Django documentation if you wish to use something else. For my part I use DigitalOcean Spaces with this configuration.

