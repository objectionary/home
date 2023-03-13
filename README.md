<img src="https://www.objectionary.com/cactus.svg" height="100px" />

[![make](https://github.com/yegor256/objectionary/actions/workflows/make.yml/badge.svg?branch=master)](https://github.com/yegor256/objectionary/actions/workflows/make.yml)
[![Hits-of-Code](https://hitsofcode.com/github/objectionary/home)](https://hitsofcode.com/view/github/objectionary/home)
![Lines of code](https://img.shields.io/tokei/lines/github/objectionary/home)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/objectionary/home/blob/master/LICENSE.txt)

The term **Objectionary** was coined by [David West](https://www.youtube.com/watch?v=s-hdZZzMCac)
in his great book
[Object Thinking](http://amzn.to/266oJr4). The original idea was to
have a place where objects are hosted. Not libraries or software packages,
but individual objects. This is exactly what this repository is about:
it hosts [EO](https://www.eolang.org) objects. More details
in [this blog post](https://www.yegor256.com/2021/10/21/objectionary.html).

When you are ready to publish a new object to this repository
and make it visible for users of EO, you just create a new
`.eo` file and place it to the right location, in one of the sub-directories
inside the `objects` directory.
Then, you add tests also written in EO, and place them next
to your file in a subdirectory named after your object.

For example:

```
objects/
  org/
    eolang/
      bool.eo
tests/
  org/
    eolang/
      bool-tests.eo
```

Then, you add a meta to your object code, mentioning the location
of the runtime package, where all necessary atoms are available. For example,
you create a new random numbers generator:

```
+package org.example
+rt jvm org.example:example-runtime:1.0

[] > random
  [max] > next-int
    as-int.
      mul.
        max
        ^
  [] > @ /float
```

The meta `+rt` clearly points us to the place where a JAR with
the class for `random.@` atom can be found.

When ready, submit us a pull request. Our scripts will try to
build and test all objects, together with your new one, to make
sure you didn't break anything and your objects work together
with your atoms. Then, we'll merge it and the repository
will be updated. All users will be able to use your objects.

## How to Publish a Library

Once the library is ready for publishing (i.e. all required changes are released)
it can be published. Publishing includes several steps.

Create new Git branch from this repo to get the latest changes. 

There is a Bash script `pull.sh`, which may help you publish the entire
library. We use it to publish [`eo-files`](https://github.com/objectionary/eo-files),
[`eo-hamcrest`](https://github.com/objectionary/eo-hamcrest), and others. In order
to use it, you should first configure your library so that it publishes its full list of EO
objects on each release into its `gh-pages` branch. See, how Rultor does it in
eo-files: [`.rultor.yml`](https://github.com/objectionary/eo-files/blob/master/.rultor.yml).
This is the file required by the script:
[`objectionary.lst`](https://github.com/objectionary/eo-files/blob/gh-pages/objectionary.lst).

Then, when ready, run the script this way inside your local clone of this repo:

```bash
$ ./pull.sh objectionary/eo-files
```

Here, `objectionary/eo-files` is the name of GitHub repository you are trying to publish
to Objectionary. The script will
pull all necessary `.eo` sources from the repo and put them into the right
places.

If several libraries need to be published as well then repeat this step for them as well.

Library objects within Objectionary must not contain any puzzles so it needs 
to be removed from pulled objects.

Next, the build needs to be verified. To do this, run the following:

```bash
$ make clean; make
```
If the build fails the issues need to be resolved.

If the build is clean, commit the changes and push the branch. Then, submit a pull request. 
Once your pull request is merged, all EO programmers will be able to use your library.

