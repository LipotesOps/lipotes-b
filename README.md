# octo-fibula
DevOps aha


# Installing memcached on Mac with Homebrew and Lunchy

This is a quick guide for installing memcached on a Mac with Homebrew, and starting and stopping it with Lunchy. I hope this tutorial will get your memcached up and running in no time.

## Step 1 — Install Homebrew

Installing Homebrew is super easy. Just paste this in your terminal —

```sh
$ ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"
```

You should also make sure your Homebrew is up-to-date. Use update and doctor commands to update and fix any issues it may have.

```sh
$ brew update
$ brew doctor
```

## Step 2 — Install memcached

Installing anything with Homebrew is a breeze. All you need is

```sh
$ brew install memcached
```

When you installed memcached, it put a file named homebrew.mxcl.memcached.plist in /usr/local/Cellar/memcached/$version/; you copy that file into ```~/Library/LaunchAgents``` and then tell launchd to start it with ```launchctl load -w ~/Library/LaunchAgents/homebrew.mxcl.memcached.plist```.

If you were watching the console carefully during the brew install command, it should have said something about doing these exact steps. If you run brew info it’ll re-print this information, e.g. brew info memcached.

## Step 3 — Install Lunchy

But why remember this long location to start memcached every time? Lunchy is a gem that simplifies the command line interface to launchctl. To install Lunchy, do

```sh
$ gem install lunchy
```

## Step 4 — Start/Stop memcached

Now we configure lunchy to start/stop memcached using simple lunchy commands.

```sh
$ mkdir ~/Library/LaunchAgents
$ cp /usr/local/Cellar/memcached/$version/homebrew.mxcl.memcached.plist ~/Library/LaunchAgents/
$ lunchy start memcached
$ lunchy stop memcached
```

Lines 1 and 2 copy the plist file to LaunchAgents. The lines 3 and 4 start and stop memcached. Since lunchy takes care of the long commands we talked about in Step 2, we don’t have to use the launchctl command to launch anymore.

## Verify the Installation

Verify that you have successfully installed Memcached.

```sh
$ memcached -V
```

Using the Memcached Telnet Interface
You can connect to the Memcached server with Telnet.

```sh
telnet localhost 11211
```

To test if everything is working correctly, set a cache item.

```sh
set foo 0 900 5
hello
```

To retrieve the cache item.

```sh
get foo
```

To exit the Telnet session.

```sh
quit
```

For more information on using Memcached Telnet commands.

## Invalidate All Cache Items

To flush the contents of your Memcached server. Useful in a development environment.

```sh
echo 'flush_all' | nc localhost 11211
```

That's it.