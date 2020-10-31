## Msys Notes

`msys` is a fully capable POSIX environment meant to mimic and emulate the linux terminal env.

`mingw_w64` is the mode of `msys` that allows for linux GUI apps to run in windows.  Git Bash uses `msys`.

## Fish shell inside msys

The awesome `fish` shell is available inside `msys`.  It has a built in tool called `abbr` that abbreviates commands into smaller commands.

I just used it to abbreviate cd'ing to my `awsomesawce.github.io` directory on my d drive to a simple `cdawsdir`

The path in Cygwin and Msys is different.  You don't use the backslashes like Windows does.  In linux, you use forward slashes.
Also, every `http` URL I've come across also uses forward slashes.  **Windows** seems to be the only operating system that uses these stupid backslashes.

Anyway, to navigate to this directory, I used `cd /d/carl/documents/github/awsomesawce.github.io`.

Unlike WSL, MSYS and Cygwin aren't a separate operating system.  They're part of windows.  So there's no need to network map the drive or anything weird like what WSL does.
