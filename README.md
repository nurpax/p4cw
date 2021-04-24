# P4CW (Perforce Client spec Wrapper)

A helper tool for making it slightly easier to edit Perforce client specs on the command line.

## What it does

`p4cw` creates the illusion that you can edit client specs without cumbersome redundancy.  More specifically, instead of this syntax:

```
View:
    //depot/path/to/project/... //client_spec_name/path/to/project/...
```

you can use the below syntax instead:

```
View:
    //depot/path/to/project/...
```

## Usage

### Installation:

1. `git clone https://github.com/nurpax/p4cw`
2. `cd p4cw && pip install .`

### Using with the `p4` command line client

Set `P4EDITOR` environment variable to `p4cw`.

As `p4cw` itself needs to spawn an editor, you should ensure you have `EDITOR` environment variable pointing to your desired client spec editor.

Or you can prefix your `p4` invocations like so: `P4EDITOR=p4cw p4 client`
