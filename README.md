The term **Objectionary** was coined by [David West](https://www.youtube.com/watch?v=s-hdZZzMCac)
in his great book
[Object Thinking](http://amzn.to/266oJr4). The original idea was to
have a place where objects are hosted. Not libraries or software packages,
but individual objects. This is exactly what this repository is about:
it hosts [EOLANG](https://www.eolang.org) objects.

When you are ready to publish a new object to this repository
and make it visible for users of EOLANG, you just create a new
`.eo` file and place it to the right location, in one of the sub-directories
inside the `objects` directory.
Then, you add tests also written in EOLANG, and place them next
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
      bool/
        simple-tests.eo
```

Then, you add a meta to your object code, mentioning the location
of the runtime package, where all necessary atoms are available. For example,
you create a new random numbers generator:

```
+package org.example
+java org.example:example-runtime:1.0

[] > random
  [max] > nextInt /int
  [] > nextFloat /float
```

The meta `+java` clearly points us to the place where a JAR with
classes for `nextInt` and `nextFloat` atoms can be found.

When ready, submit us a pull request. Our scripts will try to
build and test all objects, together with your new one, to make
sure you didn't break anything and your objects work together
with your atoms. Then, we'll merge it and the website objectionary.com
will be update. All users will be able to use your objects.


