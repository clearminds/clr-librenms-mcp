# clr-librenms-mcp

[![PyPI](https://img.shields.io/pypi/v/clr-librenms-mcp)](https://pypi.org/project/clr-librenms-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

MCP server for LibreNMS network monitoring — query devices, alerts, sensors, ports, and more through AI assistants like Claude.

## Features

- **Device monitoring** — list devices, health summary, availability, outages, down devices
- **Alert management** — list, filter, acknowledge alerts, alert rules
- **Sensor data** — health sensors by device and type (temperature, voltage, fan, etc.)
- **Port/interface info** — list ports, search by name, find by MAC address
- **ARP & FDB lookups** — resolve IPs to MACs, find MAC on switch ports
- **Hardware inventory** — chassis, modules, power supplies, serial numbers
- **IP address management** — list IPs assigned to devices
- **Token-based auth** — simple X-Auth-Token authentication

## Installation

```bash
pip install clr-librenms-mcp
# or
uvx clr-librenms-mcp
```

## Configuration

**Preferred:** Configuration file at `~/.config/librenms/credentials.json` (chmod 600):

```json
{
  "url": "https://librenms.example.com",
  "token": "your-api-token"
}
```

**Alternative:** Environment variables are also supported:

| Variable | Description | Example |
|----------|-------------|---------|
| `LIBRENMS_URL` | LibreNMS base URL | `https://librenms.example.com` |
| `LIBRENMS_TOKEN` | API token (generate in LibreNMS UI under API Settings) | `abc123...` |

Optional:

| Variable | Description | Default |
|----------|-------------|---------|
| `LIBRENMS_TRANSPORT` | Transport protocol (`stdio` or `http`) | `stdio` |
| `LIBRENMS_LOG_LEVEL` | Log level | `INFO` |

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "librenms": {
      "command": "uvx",
      "args": ["clr-librenms-mcp"]
    }
  }
}
```

### Claude Code

Add via CLI:

```bash
claude mcp add librenms -- uvx clr-librenms-mcp
```

Or add to your `.mcp.json`:

```json
{
  "librenms": {
    "command": "uvx",
    "args": ["clr-librenms-mcp"]
  }
}
```

### VS Code

Add to your VS Code settings or `.vscode/mcp.json`:

```json
{
  "mcp": {
    "servers": {
      "librenms": {
        "command": "uvx",
        "args": ["clr-librenms-mcp"]
      }
    }
  }
}
```

**Note:** Configuration is read from `~/.config/librenms/credentials.json` or environment variables. No need to specify credentials in MCP config files.

### HTTP Transport

To run as a standalone HTTP server:

```bash
clr-librenms-mcp --transport http --host 0.0.0.0 --port 8000
```

## Tools

### System

| Tool | Description |
|------|-------------|
| `librenms_system` | Get LibreNMS version and system information |

### Devices

| Tool | Description | Parameters |
|------|-------------|------------|
| `librenms_list_devices` | List all monitored devices | `device_type?`, `query?` |
| `librenms_get_device` | Get full detail for a single device | `device` |
| `librenms_down_devices` | List all devices currently down | — |
| `librenms_device_summary` | Aggregate status summary (up/down/disabled) | — |
| `librenms_device_availability` | Availability percentages (24h, 7d, 30d, 365d) | `device` |
| `librenms_device_outages` | Outage history for a device | `device` |
| `librenms_device_ips` | IP addresses assigned to a device | `device` |
| `librenms_inventory` | Hardware inventory (chassis, modules, PSUs) | `device`, `physical_class?` |

### Alerts

| Tool | Description | Parameters |
|------|-------------|------------|
| `librenms_list_alerts` | List alerts with optional filters | `state?`, `severity?` |
| `librenms_get_alert` | Get full detail for a single alert | `alert_id` |
| `librenms_alert_count` | Alert count by state and severity | — |
| `librenms_ack_alert` | Acknowledge an alert | `alert_id`, `note?` |
| `librenms_list_alert_rules` | List all alert rules | — |

**Alert filter values:**

| Parameter | Accepted values |
|-----------|----------------|
| `state` | `active`, `acknowledged`, `resolved` |
| `severity` | `ok`, `warning`, `critical` |

### Sensors & Health

| Tool | Description | Parameters |
|------|-------------|------------|
| `librenms_list_sensors` | List all sensors or filter by device | `device?` |
| `librenms_device_health` | Health sensors for a device by type | `device`, `health_type?` |

**Health types:** `temperature`, `voltage`, `fanspeed`, `power`, `humidity`, `state`, and more.

### Ports & Interfaces

| Tool | Description | Parameters |
|------|-------------|------------|
| `librenms_list_ports` | List ports/interfaces for a device | `device` |
| `librenms_search_ports` | Search ports by name, alias, or description | `search` |
| `librenms_port_by_mac` | Find port(s) by MAC address | `mac` |

### Network Lookups

| Tool | Description | Parameters |
|------|-------------|------------|
| `librenms_arp_lookup` | ARP lookup by IP, MAC, or CIDR | `query`, `device?` |
| `librenms_fdb` | MAC/FDB table for a device | `device` |

## Example Usage

Once connected, you can ask your AI assistant things like:

- "Are any devices down in LibreNMS?"
- "Show me all critical alerts"
- "What are the temperature sensors on router01?"
- "Find which switch port has MAC aa:bb:cc:dd:ee:ff"
- "What's the availability for switch01 over the last 30 days?"
- "Acknowledge alert 42"
- "Show me the ARP table for 10.0.0.0/24"
- "List the hardware inventory for core-switch"

## Safety

All tools are **read-only** except `librenms_ack_alert`, which is a non-destructive write operation — it marks an alert as acknowledged but does not modify device configuration or monitoring state.

## Technical Notes

- **Auth:** Token-based via X-Auth-Token header (generate tokens in LibreNMS under API Settings)
- **API version:** Uses LibreNMS REST API v0
- **Device parameter:** Most tools accept hostname, IP address, or device_id interchangeably
- **Sensors:** Use `librenms_device_health` with `health_type` for filtered sensor views, or `librenms_list_sensors` for all sensors across all devices

## Development

```bash
git clone https://github.com/clearminds/clr-librenms-mcp.git
cd clr-librenms-mcp
uv sync
uv run clr-librenms-mcp
```

## License

MIT — see [LICENSE](LICENSE) for details.
