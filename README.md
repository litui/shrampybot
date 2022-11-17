## ShrampyBot - The Golden Shrimp Guild Mastodon Bot

This is a bot being used and developed actively by the [Golden Shrimp Guild](https://gsg.live) for announcing when streamers on the gsg.live Mastodon instance go live.

This is a "serverless function" running in Python on DigitalOcean Functions. It leverages the Mastodon API for announcements and the Twitch API EventSub Webhooks to receive event notifications. It uses the Twitch REST API endpoint for getting more detailed information.

Some early work is present to enable automatic editing of past toots (eg: when a stream ends or raids out) but that functionality is not yet available in the Mastodon API.

A `project-example.yml` script is present with example options. Rename to `project.yml` and use the `doctl` utility to deploy to your DigitalOcean function namespace.

TODO: Additional documentation on deployment and configuration.