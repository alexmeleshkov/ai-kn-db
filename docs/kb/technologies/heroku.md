# Heroku

**Category**: Platform as a Service (PaaS) / Deployment
**Website**: https://www.heroku.com/
**Documentation**: https://devcenter.heroku.com/

---

## Overview

Heroku is a cloud platform (PaaS) that enables developers to build, run, and operate applications entirely in the cloud. It abstracts away infrastructure management and provides add-ons for databases, caching, monitoring, etc.

---

## Key Features

**Dynos**: Lightweight Linux containers that run your application
**Buildpacks**: Scripts that install dependencies and configure environment
**Add-ons**: Third-party services (PostgreSQL, Redis, monitoring, etc.)
**Git-based deployment**: Deploy by pushing to Heroku Git remote

---

## Common Use Cases

- **Web applications**: Node.js, Python, Ruby, Java, Go, PHP apps
- **API backends**: RESTful APIs and microservices
- **Staging environments**: Test deploys before production
- **Rapid prototyping**: Quick MVP deployment

---

## Pricing Tiers

**Free Tier** (Deprecated as of Nov 2022):
- No longer available

**Hobby Tier**: ~$7/month per dyno
- Good for personal projects
- SSL, custom domains
- Sleeps after 30 minutes of inactivity

**Production Tier**: ~$25-$500/month
- Always on
- Horizontal scaling
- Advanced metrics

---

## Key Considerations

**Timeouts**:
- 30-second request timeout (HTTP)
- 55-second timeout for long-polling connections
- Use heartbeat polling to prevent timeouts on long operations

**Ephemeral Filesystem**:
- Files written to disk are lost on dyno restart
- Use S3 or similar for persistent file storage

**PostgreSQL**:
- Heroku Postgres add-on available
- Automatically sets DATABASE_URL environment variable

---

## Related

**Used in projects**: [[db-chat-nl-master]]
**Code snippets**: See `snippets/*/heroku/`
**Technologies often used with**: [[postgresql]], [[redis]]
**Alternatives**: [[aws-ecs]], [[vercel]], [[railway]]
**People**: [[dima-efremov]]
