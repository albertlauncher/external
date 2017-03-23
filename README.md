### This is the official repository for external extensions.

Currently these extensions are not distributed with the app. Just clone the
repository and pull from time to time. If you like to share your extensions, you
have to fork the repository before you clone, add the extension, commit, push
and send a pull request on GitHub.

To install the extensions in user space type the following in your terminal:
```bash
git clone git@github.com:albertlauncher/external.git "$HOME/.local/share/albert/"
```

If you want the extensions to be installed system wide, use the following:
```bash
git clone git@github.com:albertlauncher/external.git "/usr/local/share/albert/"
```

If you feel uncomfortable installing third party extensions that are executed on
your system (you should), note that the code is open source and reviewed
before it gets into the repository. If you are the detective kind of guy you are
free to join the team and review code that people send us.

We do not have the time to take care of packaging compiled external
extensions for all platforms out there. If you want to share your extension,
please use one of the dozens of script languages out there.
