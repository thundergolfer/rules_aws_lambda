load("//:defs.bzl", "lambda_python_pkg")

py_binary(
    name = "hello",
    srcs = [
        "hello.py",
    ],
)

lambda_python_pkg(
    name = "hello_func",
    out = "hello_func.zip",
    main = "hello.py",
    src = ":hello",
)
