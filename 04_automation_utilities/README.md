# 🤖 Automation & Utilities

This folder contains 10 automation and utility programs.

## Programs

### 31. Web Automation
**File**: `31_web_automation.py`

Selenium-based web automation framework.

**Features**:
- Browser automation
- Element interaction
- Form filling
- Screenshots
- JavaScript execution

**Run**:
```bash
python 31_web_automation.py
# Requires: pip install selenium
```

---

### 32. PDF Generator
**File**: `32_pdf_generator.py`

ReportLab-based PDF creation.

**Features**:
- Text and paragraphs
- Tables and charts
- Images
- Headers and footers
- Custom styling

**Run**:
```bash
python 32_pdf_generator.py
# Requires: pip install reportlab
```

---

### 33. CLI Tool
**File**: `33_cli_tool.py`

Command-line interface framework.

**Features**:
- Argument parsing
- Subcommands
- Progress bars
- Table output
- Color support

**Run**:
```bash
python 33_cli_tool.py hello --name Alice
python 33_cli_tool.py list --format table
```

---

### 34. Config Manager
**File**: `34_config_manager.py`

Multi-format configuration manager.

**Formats**:
- JSON
- INI
- Environment variables
- Nested keys
- Default values

**Run**:
```bash
python 34_config_manager.py
```

---

### 35. QR Code Generator
**File**: `35_qr_code_generator.py`

QR code creation and scanning.

**Features**:
- Basic QR codes
- Colored QR codes
- QR with logos
- WiFi QR codes
- vCard QR codes

**Run**:
```bash
python 35_qr_code_generator.py
# Requires: pip install qrcode[pil]
```

---

### 36. Text to Speech
**File**: `36_text_to_speech.py`

TTS engine with multiple voices.

**Features**:
- Offline TTS (pyttsx3)
- Online TTS (Google)
- Multiple languages
- Voice selection
- File saving

**Run**:
```bash
python 36_text_to_speech.py
# Requires: pip install pyttsx3 gtts
```

---

### 37. Backup Tool
**File**: `37_backup_tool.py`

File backup and restore system.

**Features**:
- ZIP backups
- TAR backups
- Incremental backups
- Restore functionality
- Backup rotation

**Run**:
```bash
python 37_backup_tool.py
```

---

### 38. System Monitor
**File**: `38_system_monitor.py`

Real-time system resource monitoring.

**Monitors**:
- CPU usage
- Memory usage
- Disk usage
- Network I/O
- Process list
- Battery status

**Run**:
```bash
python 38_system_monitor.py
# Requires: pip install psutil
```

---

### 39. Notification System
**File**: `39_notification_system.py`

Multi-channel notification system.

**Channels**:
- Desktop notifications
- Email
- Slack
- Condition-based alerts
- Notification log

**Run**:
```bash
python 39_notification_system.py
# Requires: pip install win10toast (Windows)
```

---

### 40. API Client
**File**: `40_api_client.py`

REST API client library.

**Features**:
- GET, POST, PUT, DELETE
- Authentication
- Caching
- Rate limiting
- Retry logic
- Example: GitHub API

**Run**:
```bash
python 40_api_client.py
# Requires: pip install requests
```

---

## Use Cases

- **Automation**: Web scraping, task scheduling
- **Monitoring**: System resources, logs
- **Notifications**: Alerts, status updates
- **Document Generation**: PDFs, reports
- **Configuration**: Multi-environment setup

## Dependencies

```bash
pip install selenium reportlab qrcode pyttsx3 gtts psutil requests win10toast
```

## Quick Start

```bash
cd 04_automation_utilities
python 38_system_monitor.py
```

---

**Total Programs**: 10 | **Category**: Automation & Utilities
