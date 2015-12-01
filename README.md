# git-vdiff

A utility program I wrote to help me see git diffs visually.  Prints to stdout vimdiff invocations.  Sometimes I want more than unified diff output in the terminal.  Each invocation compares a file in a commit with its previous version.

If GIT_VDIFF_USER is set in the environment, the program uses it as a search string to identify the author whose commits should be examined.  If GIT_VDIFF_USER is not set, the value of USER in the environment is used.

If ALWAYS_INCLUDE is set in the environment, it is taken to be a list of sha's of commits to be processed irregardless of the commit author.

If GIT_VDIFF_DEBUG is set in the environment, then list all parsed data rather than execute the functionality described above.

My `.my-vimdiffrc` file includes `color pablo`.

## my usage

Examples:

```
$ ( unset GIT_VDIFF_DEBUG ; export GIT_VDIFF_USER=bizcor ; ~/projects/bizcor/git-vdiff/bin/git-vdiff.py ~/projects/bizcor/junkjunkjunk/ )
USER => 'bizcor'
ALWAYS_INCLUDE => None

[...snip...]
vimdiff -u /Users/blarf/.my-vimdiffrc <( echo add9617... 632cdcf:a/README.md [M] Tue Dec 1 12:38:14 2015 -0800 "#74" ; git show 632cdcf ) <( echo add9617... c8189db:b/README.md [M] Tue Dec 1 12:38:14 2015 -0800 "#74" ; git show c8189db )
vimdiff -u /Users/blarf/.my-vimdiffrc <( echo b99e730... c8189db:a/README.md [M] Tue Dec 1 12:40:52 2015 -0800 "#75" ; git show c8189db ) <( echo b99e730... 3806eda:b/README.md [M] Tue Dec 1 12:40:52 2015 -0800 "#75" ; git show 3806eda )
vimdiff -u /Users/blarf/.my-vimdiffrc <( echo dca64f5... 3806eda:a/README.md [M] Tue Dec 1 12:41:45 2015 -0800 "#76" ; git show 3806eda ) <( echo dca64f5... 71b27bf:b/README.md [M] Tue Dec 1 12:41:45 2015 -0800 "#76" ; git show 71b27bf )
vimdiff -u /Users/blarf/.my-vimdiffrc <( echo 2ac343f... 71b27bf:a/README.md [M] Tue Dec 1 12:42:23 2015 -0800 "#77" ; git show 71b27bf ) <( echo 2ac343f... 5e6f3f5:b/README.md [M] Tue Dec 1 12:42:23 2015 -0800 "#77" ; git show 5e6f3f5 )
vimdiff -u /Users/blarf/.my-vimdiffrc <( echo c987960... 5e6f3f5:a/README.md [M] Tue Dec 1 12:44:06 2015 -0800 "#78" ; git show 5e6f3f5 ) <( echo c987960... fb29619:b/README.md [M] Tue Dec 1 12:44:06 2015 -0800 "#78" ; git show fb29619 )
vimdiff -u /Users/blarf/.my-vimdiffrc <( echo 0d96528... fb29619:a/README.md [M] Tue Dec 1 12:44:19 2015 -0800 "#79" ; git show fb29619 ) <( echo 0d96528... 94e1971:b/README.md [M] Tue Dec 1 12:44:19 2015 -0800 "#79" ; git show 94e1971 )
vimdiff -u /Users/blarf/.my-vimdiffrc <( echo e9ed435... 94e1971:a/README.md [M] Tue Dec 1 12:52:30 2015 -0800 "#80" ; git show 94e1971 ) <( echo e9ed435... 4376700:b/README.md [M] Tue Dec 1 12:52:30 2015 -0800 "#80" ; git show 4376700 )
vimdiff -u /Users/blarf/.my-vimdiffrc <( echo 264fdfe... 4376700:a/README.md [M] Tue Dec 1 12:54:42 2015 -0800 "#81" ; git show 4376700 ) <( echo 264fdfe... 7612d8c:b/README.md [M] Tue Dec 1 12:54:42 2015 -0800 "#81" ; git show 7612d8c )
vimdiff -u /Users/blarf/.my-vimdiffrc <( echo 1ebb3d3... 7612d8c:a/README.md [M] Tue Dec 1 12:55:35 2015 -0800 "#82" ; git show 7612d8c ) <( echo 1ebb3d3... 4aa161e:b/README.md [M] Tue Dec 1 12:55:35 2015 -0800 "#82" ; git show 4aa161e )
vimdiff -u /Users/blarf/.my-vimdiffrc <( echo 9c43637... 4aa161e:a/README.md [M] Tue Dec 1 12:57:42 2015 -0800 "#83" ; git show 4aa161e ) <( echo 9c43637... a461a5f:b/README.md [M] Tue Dec 1 12:57:42 2015 -0800 "#83" ; git show a461a5f )
```

Then I edit some-output-file.  In vim, I have the following command defined:

```
:command
    Name        Args Range Complete  Definition
[...]
    Exec        0                    :.w !bash
[...]
```

Then I place the cursor on each line in turn and do:

```
:Exec<return>
```

Here is the debug output:

```
$ ( export GIT_VDIFF_DEBUG=1 ; export GIT_VDIFF_USER=bizcor ; ~/projects/bizcor/git-vdiff/bin/git-vdiff.py ~/projects/bizcor/junkjunkjunk/ )
0 bash  1 delve  2 bash  3 bash  4* bash
USER => 'bizcor'
ALWAYS_INCLUDE => None

commit add9617fea82dc9df8310241edf761f4d8dbb00a
Author: <bizcor@gmail.com>
Date:   Tue Dec 1 12:38:14 2015 -0800
:100644 100644 632cdcf... c8189db... M  README.md

commit b99e7303554a8048388acdf6d1aab77a73cfff8c
Author: <bizcor@gmail.com>
Date:   Tue Dec 1 12:40:52 2015 -0800
:100644 100644 c8189db... 3806eda... M  README.md

commit dca64f55ed5eceece8eba491431c19599fbd57ba
Author: <bizcor@gmail.com>
Date:   Tue Dec 1 12:41:45 2015 -0800
:100644 100644 3806eda... 71b27bf... M  README.md

commit 2ac343f53fa55b017aa43b9df5517c5adf0155cc
Author: <bizcor@gmail.com>
Date:   Tue Dec 1 12:42:23 2015 -0800
:100644 100644 71b27bf... 5e6f3f5... M  README.md

commit c987960e266d92c0498063a385ba167afa394b2c
Author: <bizcor@gmail.com>
Date:   Tue Dec 1 12:44:06 2015 -0800
:100644 100644 5e6f3f5... fb29619... M  README.md

commit 0d965287a31dff642fc11ea761dde268dfffa237
Author: <bizcor@gmail.com>
Date:   Tue Dec 1 12:44:19 2015 -0800
:100644 100644 fb29619... 94e1971... M  README.md

commit e9ed4359553d0f6df3155b3e0c96e76a98665809
Author: <bizcor@gmail.com>
Date:   Tue Dec 1 12:52:30 2015 -0800
:100644 100644 94e1971... 4376700... M  README.md

commit 264fdfee3cc3a39a0c47b336fe32ed22bea803d3
Author: <bizcor@gmail.com>
Date:   Tue Dec 1 12:54:42 2015 -0800
:100644 100644 4376700... 7612d8c... M  README.md

commit 1ebb3d35e549700bf82752aaf6807befef942126
Author: <bizcor@gmail.com>
Date:   Tue Dec 1 12:55:35 2015 -0800
:100644 100644 7612d8c... 4aa161e... M  README.md

commit 9c43637e7542c9a955aede2d7ec7f555577113ec
Author: <bizcor@gmail.com>
Date:   Tue Dec 1 12:57:42 2015 -0800
:100644 100644 4aa161e... a461a5f... M  README.md
```
