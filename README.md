# QuickPass

QuickPass is a native component written in Python 3 that can
be used with [browserpass][bp] to provide list of passwords
and credentials for a given page.

[bp]: https://github.com/dannyvankooten/browserpass

## Installation

### Windows

Open `quickpass.json` and add full path to `quickpass.bat` in `path` key.

Use this command to register extension for Firefox:

    REG ADD "HKEY_CURRENT_USER\SOFTWARE\Mozilla\NativeMessagingHosts\com.dannyvankooten.browserpass" /ve /d "C:\quickpass\quickpass.json" /f
