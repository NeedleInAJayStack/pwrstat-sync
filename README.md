
## Run

1. Install node
2. Update/clone from the git repository. Enter directory.
3. Install relevant modules: npm install
4. Run the main.js process on the desired recording interval, typically using cron.
  1. This is because the pwrstat process requires sudoers permissions and access to the UPS USB stream so we can't containerize it easily.
