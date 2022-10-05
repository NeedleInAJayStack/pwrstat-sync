# pwrstat sync

This repo contains a script that runs the
[CyberPower PowerPanel](https://www.cyberpowersystems.com/product/software/power-panel-personal/powerpanel-for-linux/)
, parses the output, and inserts a few fields of interest into a web API

## Run

1. Install Python 3
2. Update/clone from the git repository. Enter directory.
3. Install relevant modules: pip install -r requirements.txt
4. Run the main.py process on the desired recording interval, typically using cron.
  1. This is because the pwrstat process requires sudoers permissions and access to the UPS USB stream so we can't containerize it easily.

### Environment

To run, you must provide the following environment variables:

- `API_USER`
- `API_PASSWORD`

Often this is most easily done using a `.env` file at the root directory.
