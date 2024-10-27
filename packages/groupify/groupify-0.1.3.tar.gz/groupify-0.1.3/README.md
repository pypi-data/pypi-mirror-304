# `groupify`
`groupify` is a Python package for automatically creating random groups in the classroom from a classlist. 

> NOTE: there is currently no way to ensure that Newton and Leibniz are not in the same group. They must cooperate if necessary.

## Basic examples

### Example 1

```python
import groupify

classlist = "sample_class.txt"

groupify.create(
    classlist=classlist,
    group_size=4,
)

groupify.savefig(dirname="../figures/", fname="example_1.svg")

groupify.show()

```

This will generate the following groups (randomly):

![example 1](https://raw.githubusercontent.com/reneaas/groupify/refs/heads/main/examples/figures/example_1.svg)


### Example 2

```python
import groupify

classlist = "sample_class.txt"

groupify.create(
    classlist=classlist,
    group_size=3,
)

groupify.savefig(dirname="../figures/", fname="example_2.svg")

groupify.show()
```

This will generate the following groups (randomly):

![example 2](https://raw.githubusercontent.com/reneaas/groupify/refs/heads/main/examples/figures/example_2.svg)



### Example 3

```python
import groupify

classlist = "sample_class.txt"

groupify.create(
    classlist=classlist,
    group_size=2,
)

groupify.savefig(dirname="../figures/", fname="example_3.svg")

groupify.show()

```

This will generate the following groups (randomly):

![example 3](https://raw.githubusercontent.com/reneaas/groupify/refs/heads/main/examples/figures/example_3.svg)

