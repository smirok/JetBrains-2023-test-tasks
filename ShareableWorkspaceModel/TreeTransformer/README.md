# Description 

## Execute base task:

* `$ ./gradlew run --args="base <file1> <file2>"` - transform tree from <file1> state to <file2> state

Solution contract: transformation isn't possible for trees with different roots.

## Execute bonus task (via [Clikt](https://github.com/ajalt/clikt)):

* `$ ./gradlew run --args="bonus"` - init tree with hardcoded root (1 by default)
* `$ ./gradlew run --args="bonus --tree-path <path>"` - load tree from `<path>`

### CLI provides following inputs:
* `ADD(<parent>, <child>)` - add `<child>` node to `<parent>` 
* `REMOVE(<node>)` - remove `<node>` from tree
* `SAVE <path>` - save current tree into `<path>` file
* `EXIT` - exit from CLI
