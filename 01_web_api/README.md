# 🌐 Web & API Examples

This folder contains 10 complete web and API-related Python programs.

## Programs

### 01. REST API Server
**File**: `01_rest_api_server.py`

Flask-based REST API server with full CRUD operations for task management.

**Features**:
- GET, POST, PUT, DELETE endpoints
- In-memory database
- JSON responses
- Error handling

**Run**:
```bash
python 01_rest_api_server.py
# Access at http://localhost:5000
```

---

### 02. Web Scraper
**File**: `02_web_scraper.py`

BeautifulSoup-based web scraping tool.

**Features**:
- Extract links, images, and text
- Save results to JSON
- Error handling
- Customizable selectors

**Run**:
```bash
python 02_web_scraper.py
```

---

### 03. Data Visualization
**File**: `03_data_visualization.py`

Matplotlib-based data visualization toolkit.

**Features**:
- Line charts
- Bar charts
- Pie charts
- Scatter plots
- Histograms

**Run**:
```bash
python 03_data_visualization.py
```

---

### 04. JWT Authentication
**File**: `04_jwt_authentication.py`

JWT token-based authentication system.

**Features**:
- User login/authentication
- Token generation and verification
- Role-based access control
- Protected routes

**Run**:
```bash
python 04_jwt_authentication.py
# Test: admin/admin123 or user/user123
```

---

### 05. Email Sender
**File**: `05_email_sender.py`

SMTP-based email sending system.

**Features**:
- Simple text emails
- HTML emails
- Attachments
- Bulk sending

**Run**:
```bash
python 05_email_sender.py
# Configure SMTP settings first
```

---

### 06. File Encryption
**File**: `06_file_encryption.py`

Cryptography-based file encryption/decryption.

**Features**:
- File encryption
- File decryption
- Password-based keys
- Text encryption

**Run**:
```bash
python 06_file_encryption.py
```

---

### 07. Image Processor
**File**: `07_image_processor.py`

PIL/Pillow-based image processing.

**Features**:
- Resize, rotate, flip
- Filters (blur, sharpen)
- Brightness/contrast adjustment
- Watermarks
- Thumbnails

**Run**:
```bash
python 07_image_processor.py
```

---

### 08. Chatbot
**File**: `08_chatbot.py`

Rule-based conversational chatbot.

**Features**:
- Pattern matching
- Conversation history
- Multiple response patterns
- File saving

**Run**:
```bash
python 08_chatbot.py
```

---

### 09. URL Shortener
**File**: `09_url_shortener.py`

Flask-based URL shortening service.

**Features**:
- Shorten URLs
- Custom short codes
- Click tracking
- SQLite database

**Run**:
```bash
python 09_url_shortener.py
# Access at http://localhost:5002
```

---

### 10. Password Manager
**File**: `10_password_manager.py`

Encrypted password management system.

**Features**:
- Master password protection
- Password generation
- Encrypted storage
- Password strength checker

**Run**:
```bash
python 10_password_manager.py
```

---

## Dependencies

```bash
pip install flask requests beautifulsoup4 matplotlib pillow cryptography pyjwt
```

## Quick Start

```bash
cd 01_web_api
python 01_rest_api_server.py
```

---

**Total Programs**: 10 | **Category**: Web & API
