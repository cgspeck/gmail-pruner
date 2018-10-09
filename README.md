# Gmail Pruner

Quick and dirty way to keep your mail box in check. 

Inspired by [this](http://radtek.ca/blog/delete-old-email-messages-programatically-using-python-imaplib/) and [this](https://stackoverflow.com/questions/46642764/python-3-move-email-to-trash-by-uid-imaplib) post.

***USE AT YOUR OWN RISK!***

**This is explicitly designed to facilitate the total and irrecoverable deletion of your email. It is licensed to you under the MIT License underwhich you agree that this software is provided "as is"; without warranty of any kind; and to not hold the authors liable for any claim, damages or other liability. You may read the [full text of the license here.](./LICENSE.md)**

## Requirements

Enable IMAP access on your gmail account. Create an application password (if using two-factor) or find the option to "Enable Less Secure Apps".

## Running

```
$ python prune.py 
usage: prune.py [-h] folder age
prune.py: error: the following arguments are required: folder, age

$ GMAIL_PASS={password} GMAIL_USER='{username}@gmail.com' python prune.py '[Gmail]/Sent Mail' 365
```

## Installation with systemd

1. Copy `prune.py` to a location.

2. Make copies of `prune-sent-mail.service.example` and `prune-sent-mail.timer.example`
    a) change the name of the service/timer, file names, set age and folder
    b) remove `.example` from file names

3. Run `sudo systemctl daemon-reload`.

4. Run `sudo systemctl edit {name}` and set `GMAIL_USER` and `GMAIL_PASS`.

5. Start and Enable the timer with `systemctl start {name}.timer` and `sudo systemctl enable {name}.timer`.
