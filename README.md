# Bazel AWS Lambda Rules

Borne of a desire to create python packages compatible with _AWS Lambda_, this ruleset is
designed to work with the existing language binary rules, and provide a
mechanism for deploying them to AWS lambda.  It's inspired by a mix of subpar
and rules_pkg, the former being a bit heavy for our use and not really lambda
compatible, while the latter isn't specialized enough.

This is very, very much a work in progress

### Setup

Add the following to your **`WORKSPACE`**:

```
rules_aws_lambda_version = "2ccfd4bbaf1e21dafcd68e0976dabbd2069f3142"  # latest @ 4th April 2020

http_archive(
    name = "rules_aws_lambda",
    url = "https://github.com/surlyengineer/rules_aws_lambda/archive/{version}.tar.gz".format(version = rules_aws_lambda_version),
    sha256 = "",
    strip_prefix = "rules_aws_lambda-{version}".format(version = rules_aws_lambda_version),
)
```

Here's the minimal setup for a building a Python handler into a working `.zip`: 

**`handler.py`**

```python
def handle(event, context):
    return {
        "message": "Hello World!",
    }
```

**`BUILD`**

```
load("@rules_aws_lambda//:defs.bzl", "lambda_python_pkg")

py_binary(
    name = "handler",
    srcs = ["handler.py"],
    deps = [],
)

lambda_python_pkg(
    name = "handler_func",
    out = "handler_func.zip",
    main = "handler.py",
    src = ":handler",
)
```

Running `bazel build //foo/bar:handler_func` would then produce `handler_func.zip` at `bazel-bin/foo/bar/handle_func.zip`.

