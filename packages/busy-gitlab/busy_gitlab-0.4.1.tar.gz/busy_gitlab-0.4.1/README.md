# Busy integration plugin for GitLab issue checkboxes

GitLab Issue ID's are represented in Busy task descriptions with `%i`:

```
Fix the bug in Busy #wilib #busy %i3
```

## get

Returns the issue number

```
busy get gitlab
3
```


A very basic demonstration of [Busy integrations](https://busy.wizlib.ca/integrations.html) that generates a simple output that can be copy/pasted into an issue description for all the tasks of a tag.

Might work to install it:

```
$HOME/.local/pipx/venvs/busy/bin/python -m pip install --upgrade busy-gitlab
```
