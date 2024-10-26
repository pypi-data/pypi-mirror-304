# python-sage-imap


![Black](https://img.shields.io/badge/code%20style-black-000000.svg)
![Pylint](https://img.shields.io/badge/pylint-9-brightgreen)
[![codecov](https://codecov.io/gh/sageteamorg/python-sage-imap/graph/badge.svg?token=I10LGK910X)](https://codecov.io/gh/sageteamorg/python-sage-imap)

![PyPI release](https://img.shields.io/pypi/v/python-sage-imap "python-sage-imap")
![Supported Python versions](https://img.shields.io/pypi/pyversions/python-sage-imap "python-sage-imap")
![Documentation](https://img.shields.io/readthedocs/python-sage-imap "python-sage-imap")
![License](https://img.shields.io/badge/license-MIT-red)
![GitHub last commit](https://img.shields.io/github/last-commit/sageteamorg/python-sage-imap)


## Table of Contents
- [python-sage-imap](#python-sage-imap)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Examples](#examples)
    - [Example 1: Creating an IMAP Client](#example-1-creating-an-imap-client)
      - [Explanation](#explanation)
    - [Example 2: Working with Folder Service](#example-2-working-with-folder-service)
    - [Example 3: Working with Mailbox Methods](#example-3-working-with-mailbox-methods)
    - [IMAPMailboxService Example](#imapmailboxservice-example)
      - [Example Usage with Nested Context Managers:](#example-usage-with-nested-context-managers)
  - [License](#license)

## Introduction
`python-sage-imap` is a robust Python package designed for managing IMAP connections and performing various email operations. It provides easy-to-use interfaces for managing email folders, flags, searching emails, and sending emails using SMTP. This package is ideal for developers looking to integrate email functionalities into their applications seamlessly.

## Features
- Context manager for managing IMAP connections
- Handling IMAP flags (add/remove)
- Managing IMAP folders (create/rename/delete/list)
- Searching emails with various criteria
- Sending emails using SMTP with support for attachments and templates
- Parsing and handling email messages

## Installation
To install `python-sage-imap`, use pip:
```bash
pip install python-sage-imap
```

## Configuration
Before using the package, you need to set up logging for better debugging and monitoring:
```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

## Examples

### Example 1: Creating an IMAP Client

This example demonstrates how to create an IMAP client using the `IMAPClient` class.

The `IMAPClient` class can also be used without a context manager; simply call `connect()` to establish the connection and `disconnect()` to close it

```python
from sage_imap.services import IMAPClient

with IMAPClient('imap.example.com', 'username', 'password') as client:
    # Use the client for IMAP operations
    capabilities = client.capability()
    print(f"Server capabilities: {capabilities}")

    status, messages = client.select("INBOX")
    print(f"Selected INBOX with status: {status}")
```

#### Explanation

This example illustrates a low-level approach to working with IMAP. If you want to use `imaplib` directly but need the added convenience of managing the connection lifecycle, the `IMAPClient` class is a perfect choice. It allows you to create a connection with the IMAP server and then use all the capabilities of `imaplib` to customize your workflow.

1. **IMAPClient Context Manager**:
   - The `IMAPClient` class is used within a context manager (`with` statement). This ensures that the connection to the IMAP server is properly opened and closed.
   - When the `with` block is entered, the connection to the IMAP server is established, and the user is authenticated.
   - When the `with` block is exited, the connection is automatically closed, ensuring that resources are cleaned up properly.

2. **Why Use IMAPClient**:
   - The `IMAPClient` exists to simplify the management of IMAP connections. By using it as a context manager, you don't have to worry about manually opening and closing the connection. This reduces the risk of resource leaks and makes your code cleaner and more maintainable.
   - Within the context manager, you have access to the `imaplib` capabilities directly through the `client` object. This allows you to perform various IMAP operations seamlessly.

3. **Capabilities and Select Methods**:
   - The `.capability()` method is called to retrieve the server's capabilities, providing information about what commands and features the server supports.
   - The `.select("INBOX")` method is used to select the "INBOX" mailbox for further operations. It returns the status of the selection and the number of messages in the mailbox.

By using the `IMAPClient` class in this way, you can take advantage of the full power of `imaplib` while benefiting from the convenience and safety of automatic connection management.


### Example 2: Working with Folder Service
This example demonstrates how to work with folders using the `IMAPFolderService`.

```python
from sage_imap.services.client import IMAPClient
from sage_imap.services.folder import IMAPFolderService

with IMAPClient('imap.example.com', 'username', 'password') as client:
    folder_service = IMAPFolderService(client)

    # Create a new folder
    folder_service.create_folder('NewFolder')

    # Rename the folder
    folder_service.rename_folder('NewFolder', 'RenamedFolder')

    # List all folders
    folders = folder_service.list_folders()
    print(f"Folders: {folders}")

    # Delete the folder
    folder_service.delete_folder('RenamedFolder')
```

### Example 3: Working with Mailbox Methods

Below are usage examples of the `IMAPClient` and `IMAPMailboxService` classes, demonstrating their context manager capabilities and various methods:

### IMAPMailboxService Example

The `IMAPMailboxService` class provides methods for managing mailbox operations such as selecting, closing, checking, deleting, moving, and getting status of mailboxes.

**Purpose:** This class allows for performing various mailbox-related operations within the context of an IMAP connection, ensuring proper error handling and cleanup.

#### Example Usage with Nested Context Managers:

```python
from sage_imap.services.client import IMAPClient
from sage_imap.services.mailbox import IMAPMailboxService
from sage_imap.helpers.mailbox import DefaultMailboxes
from sage_imap.helpers.message import MessageSet

from helpers.exceptions import IMAPClientError, IMAPMailboxCheckError, IMAPMailboxClosureError

username = 'username'
password = 'password'

try:
    with IMAPClient('imap.example.com', username, password) as client:
        with IMAPMailboxService(client) as mailbox:
            # Select a mailbox
            mailbox.select(DefaultMailboxes.INBOX)

            # Delete messages temporarily (move to trash)
            msg_set = MessageSet('1,2,3')
            mailbox.trash(msg_set)

            # Restore messages from trash to original folder
            mailbox.restore(msg_set, DefaultMailboxes.INBOX)

            # Permanently delete messages
            mailbox.delete(msg_set)

except IMAPClientError as e:
    print(f"An error occurred with the IMAP client: {e}")
```

## License
This project is licensed under the MIT License.
