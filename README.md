# pkgbot

An IRC bot which provides information about packages in various distros'
repos.

# Using it

The bot is written in Python and requires the following modules:
* twisted
* requests
* beautifulsoup

On Fedora and RHEL, this can be obtained with:
`yum install python-twisted python-requests python-BeautifulSoup`

(On RHEL/CentOS this requires EPEL.)

There's a set of scripts that determine how to obtain search results
for a given distro.

This is all still a work in progress, but I'd like to have at least two
ways to obtain package information:

- Call a web service API (e.g. the one on apps.fedoraproject.org/packages)
- Periodically obtain (and use) a package database to search.
  - This is for distros that don't offer a web interface to their pkgdb.

In an irc channel, you can query the bot using:

* .pkg fedora 17 kernel
* .pkg archlinux firefox
* .pkg ubuntu bash
* .pkg debian emacs
* ... etc.

# How it works

How it works internally varies greatly based on which distro is being queried.

<table>
  <tr>
    <th>Distro/Repo</th>
    <th>Key (to query bot with)</th>
    <th>Summary</th>
  </tr>
  <tr>
    <td><a href="https://www.archlinux.org/">Arch Linux*</a></td>
    <td>archlinux</td>
    <td>
      Queries the JSON API at
      https://www.archlinux.org/packages/search/json/?name=[...]<br />
      * Does not currently support "AUR" packages.
    </td>
  </tr>
</table>

# What distros are supported?

Everything listed in the above table is currently supported. However, I would
like to support the following soon, as well:

* Fedora
* EPEL
* Debian
* Ubuntu
* FreeBSD
* NetBSD
* Homebrew (OS X)
* [your favorite distro here]

I'd also eventually like to support a `.provides` command that takes a distro
argument and a file path argument, and determines which package owns the file.
Example:

```
< relrod> .provides fedora-17 /usr/bin/firefox
< pkgbot> relrod: firefox
```

# License & Hacking

Licensed under GPLv2+.

When hacking please ensure all tests pass (when they exist).

Also please ensure that your code passes PEP8 tests.

A good .git/hooks/pre-commit hook is: `find -name '*.py' | xargs pep8`
(and ensure the hook is `chmod +x`).
