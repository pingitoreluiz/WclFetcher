# WclFetcher 🔥

A Python desktop app to fetch the **top talent loadouts** for any WoW raid encounter directly from the [Warcraft Logs](https://www.warcraftlogs.com) API.

## Features

- 🔍 Browse all current raid zones and encounters
- ⚔️ Filter by Class, Specialization, and Difficulty (Normal / Heroic / Mythic)
- 🏆 Fetch the **Rank #1** player's talent string for any encounter
- 🌐 Direct link to the full Warcraft Logs report
- 🇧🇷 / 🇺🇸 English & Portuguese UI support

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure your API credentials

Create a `.env` file in the project root (or fill in the credentials directly in the app UI):

```
WCL_CLIENT_ID=your_client_id_here
WCL_CLIENT_SECRET=your_client_secret_here
```

> Get your credentials at: https://www.warcraftlogs.com/api/clients/

### 3. Run the app

```bash
python wcl_talents_app.py
```

## Tech Stack

- Python 3.x
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — modern UI
- Warcraft Logs GraphQL API v2

## Screenshot

_Coming soon_
