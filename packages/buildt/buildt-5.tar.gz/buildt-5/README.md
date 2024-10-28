This is a **b**uild **t**ool like Make with Python **b**uild **s**cripts.<br>
Python 3.12 is required.<br>
Setting bt up in a project is easy; see the [setup section](#setup).

[**API documentation**](//nnym.github.io/bt)

```py
bt.debug = True

options = ["-std=c2x", "-Ofast", parameter("options")]
main = "main"
mainc = main + ".c"

@task(export = False, output = mainc)
def generateSource():
	write(mainc, outdent("""
		#include <stdio.h>
		int main() {puts("foo bar");}
	"""))

@task(generateSource, default = True, input = options, output = main)
def compile():
	sh(Arguments("gcc -o", main, options, generateSource.outputFiles))

@task(compile)
def run():
	sh("./" + main)
```
```sh
$ bt run
> generateSource
> compile
> run
foo bar

$ bt run
> run
foo bar

$ bt run options="-Oz -flto"
> compile
> run
foo bar

$ bt run options="-Oz -flto"
> run
foo bar
```

### Overview
The execution of bt is always accompanied by a build script.
bt lets the build script run and define [tasks](#tasks) and do any other setup.
When the build script exits, bt takes over.
It looks at the command line arguments that were passed and sets [parameters](//nnym.github.io/bt#parameter) and determines which tasks to run.
Before running a task, bt runs all of its [dependencies](#dependencies) which may include tasks and callables.
Since tasks can take long, bt provides facilities for [caching](#cache) them so that they don't have to run every time.

### Setup
bt can be installed [globally](#global) or [locally](#local) per project (as a Git submodule for example).

#### Global
1. Install bt: `python -m pip install --user buildt`. On macOS and some Linux distributions, `--break-system-packages` might be necessary.
2. If pip shows something like `WARNING: The script bt is installed in '/home/x/.local/bin' which is not on PATH.`,
then add the directory in the message to `PATH`.
3. [Run](#executable) it in a directory with a build script.

Alternatively, bt can be cloned anywhere; [`__main__.py`](__main__.py) is the executable.

#### Local
1. Enter a new or existing project directory.
2. a. In a Git repository, add bt as a submodule: `git submodule add https://github.com/nnym/bt`<br>
   b. otherwise, clone it: `git clone https://github.com/nnym/bt`.
3. Use it by [importing](#library) it in the build script.

### Running
bt can run as an [executable](#executable) or as a [library](#library) imported by the build script.

bt can be run as an executable if the build script is named `bs` or `bs.py` and bt is installed
- globally (`bt foo` if bt is in `PATH` or `python -m bt foo`)
- or locally (`python bt foo`).

In both cases, bt can be run by being [imported](#library) by the build script (`./bs foo` or `python bs foo`).

On Windows, `py` can be used instead of `python`. It can be useful if the build script's name does not have the extension `.py`.

#### Executable
bt searches for a build script named `bs` or `bs.py` in the current directory and runs it.

1. Make a build script in a new or existing project directory.
```py
from bt import * # This is optional but recommended for language server support.

@task
def alfa(): print("bar")
```
2. Run it: `bt alfa # bar`.

#### Library
The build script—which may be named anything—is the main module and imports bt as a package.
bt starts automatically when the build script's thread stops.

1. Make a build script (here `bs`):
```py
#!/usr/bin/env python
from bt import *

@task
def quebec(): print("bar")
```
2. (Outside Windows) make it executable: `chmod +x bs`.
3. Run it: `./bs quebec # bar` (`py bs quebec` on Windows).

### Usage
bt takes as arguments names of tasks to run and `name=value` pairs which set [parameters](//nnym.github.io/bt#parameter) for the build.

### Tasks
Tasks are functions that can be run on demand from the command line or as [dependencies](#dependencies) of other tasks.<br>
A function can be declared a task by using the decorator `@task`. The task's name is the function's name.

[`bt.debug = True`](#debug) is implicit in all of the examples below.

```py
@task
def bravo():
	print("bar")
```
This declares a task `bravo` that prints `"bar"`.
```sh
$ bt bravo
> bravo
bar
```

### Options
Options can be set for a task as keyword arguments to its decorator's `task` call.
The following example sets the options [`default`](#defaults) and [`source`](#source).
```py
@task(default = True, source = "main.c")
def sierra(): pass
```

Alternatively, they can be set as non-positional-only parameters' default values
or annotations (in Python 3.14 or 3.13 with `__future__.annotations`).
The latter are lazily evaluated when they are needed.

If the task has a [vararg parameter](#task-arguments), then only keyword-only parameters are interpreted as options.

```py
@task
def tango(default: True, source: "main.c"): pass
```

#### Task arguments
The command line arguments after the first instance of `--` are passed
to the last task in the command line or the last declared [default](#defaults) task.
A task can accept or require them as non-[option](#options) parameters. The arguments must match the task's arity.

This task accepts any number of arguments.
```py
@task
def oscar(*args):
	print(args)
```
```sh
$ bt oscar -- foo -- bar
> oscar
('foo', '--', 'bar')
```

This task requires exactly 2 arguments.
```py
@task
def papa(a, b, /):
	print(a, "|", b)
```
```sh
$ bt papa
Task papa: received 0 arguments instead of 2.
$ bt papa --
Task papa: received 0 arguments instead of 2.
$ bt papa -- foo
Task papa: received 1 argument instead of 2.
$ bt papa -- foo bar baz
Task papa: received 3 arguments instead of 2.

$ bt papa -- foo bar
> papa
foo | bar
```

#### Dependencies
Any non-keyword argument to `task` is considered as a dependency which may be another task or its name or a callable.
Before a task runs, its dependencies run first.

```py
@task
def charlie(): pass

@task(charlie)
def delta(): pass
```
Here `charlie` will always run before `delta`.
```sh
$ bt delta
> charlie
> delta

$ bt delta charlie
> charlie
> delta
```

#### Defaults
`task`'s parameter `default` controls whether the task runs when the command line has not specified any tasks.
```py
@task(default = True)
def echo():
	print("baz")
```
bt automatically runs `echo` when the user has not selected any tasks.
```sh
$ bt
> echo
baz
```

#### Exports
Any task can be run from the command line by default. This can be changed by the option `export`.
```py
@task(default = True, export = False)
def foxtrot():
	print("foo")
```
This will make `foxtrot` run by default but not runnable explicitly.
```sh
$ bt foxtrot
No task matched 'foxtrot'.
```

#### Cache
Setting any of `source`, `input` and `output` for a task enables caching which allows unnecessary tasks to be skipped.
`source` contains glob patterns that specify files;
`input` may be any object;
and `output` contains filenames.
The absence of a source file specified by an exact filename just before the task runs is an error.

A task will be skipped only if
- it has caching enabled
- no im[pure](#pure-tasks) task dependencies run
- `input` and the source files' mtimes are the same values from the task's previous run
- and all output files exist.

The cache file containing tasks' inputs from their previous runs is `.bt`.

#### `source`
```py
@task(source = "foo")
def hotel(): pass
```
When this task is called, it runs if this time is the first or `foo`'s mtime changed.
```sh
$ touch foo
$ bt hotel
> hotel
$ bt hotel
$ touch foo
$ bt hotel
> hotel
```

#### `input`
```py
@task(input = "baz")
def golf(): pass
```
This task will run only once ever: Since `input` has not been cached before the first run, `golf` is run once.
Thereafter whenever the task is about to run, since `input` does not change, it matches the cached version and `golf` is skipped.
Therefore `golf` runs only once.
```sh
$ bt golf
> golf
$ bt golf
```

#### `output`
bt ensures that the parent directories of all outputs exist.

```py
@task(output = "foo/bar/baz")
def india():
	sh("touch foo/bar/baz")
```
This task will be skipped if `foo/bar/baz` exists.
```sh
$ ls foo
ls: cannot access 'foo': No such file or directory
$ bt india
> india
$ ls foo/bar
baz
$ bt india
```

#### Ignoring the cache
A task can be forced to run by passing as an argument its name suffixed by `!`.
```py
@task(default = True, input = 0)
def juliett(): pass

@task(juliett, input = 0)
def kilo(): pass

@task(kilo, input = 0)
def lima(): pass
```
```sh
$ bt lima
> juliett
> kilo
> lima

$ bt kilo
$ bt kilo!
> kilo
```

Passing `!` forces all initial tasks to run.
```sh
$ bt !
> juliett

$ bt kilo !
> kilo
```

Passing `!` twice forces all required tasks to run.
```sh
$ bt ! !
> juliett

$ bt kilo ! !
> juliett
> kilo
```

#### Pure tasks
Pure tasks act like they don't have side effects: their execution does not prevent tasks that depend on them from being skipped.

```py
@task(pure = True)
def mike(): pass

@task(mike, input = 0)
def november(): pass
```
When `november` is called after the first run, it will be skipped but `mike` will run.
```sh
$ bt november
> mike
> november

$ bt november
> mike
```

#### Name
A task can be given a name different from that of its function by using the option `name`.
```py
for n in range(100):
	@task(name = str(n))
	def romeo():
		n = int(bt.current.name)
		print(f"{n} * {n} = {n * n}")
```
This will generate 100 tasks with the numbers 0-99 as their names.
```sh
$ bt 37
> 37
37 * 37 = 1369
```
