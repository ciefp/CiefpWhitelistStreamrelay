
# CiefpWhitelistStreamrelay

![Bouquet](https://github.com/ciefp/CiefpWhitelistStreamrelay/blob/main/whiteliststreamrelay.jpg)

## CiefpWhitelistStreamrelay is a plugin for Enigma2 receivers, designed for automated generation of
## `whitelist_streamrelay` file using data from predefined userbouquet files.

# Main functionalities:
- **1. Generation of whitelist_streamrelay file:**
- **The plugin processes data from selected bouquet files (userbouquet) and extracts valid lines containing**
- **information about streams.**
- **Creates or updates `whitelist_streamrelay` file in `/etc/enigma2` directory.**
- **Packages supported SKYDE 19.0E - SKYUK 28.2E.**

# 2. Display information to user:
- **Displays the number of lines added to `whitelist_streamrelay` file, providing the user with an overview of the processing results.**

# 3. Restart Enigma2:
- **After the file generation is complete, the user has the option to confirm restart Enigma2 to load the new settings.**
- **Restart is performed only after the user presses OK on the remote control.**

Why use this plugin?
- **It is suitable for users who frequently update their streamrelay lists and want an automated process without manually editing files.**
- **A simple and intuitive interface allows viewing of generated lines and control over system restart.**
- **This plugin is a practical tool for advanced Enigma2 system users who want better management and organization of streamrelay configurations.**
# This plugin was specifically created for my settings, it will not work with other settings.**

# ..::ciefpsettings::..