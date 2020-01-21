
def _lambda_python_pkg_impl(ctx):
    inputs = ctx.attr.src.default_runfiles.files.to_list()
    extras = []
    # This is clunky: some modules have inits at the root, some have a file
    # named the same as the module.  In the latter case we need to import the
    # more specific
    for i in inputs:
        if i.extension == 'py':
            sans_ext =i.basename.split('.')[0]
            if i.dirname.endswith(sans_ext):
                extras.append('/'.join([i.dirname, sans_ext]))
            else:
                extras.append(i.dirname)
    dirs = ','.join(extras)
    args = ctx.actions.args()
    args.add("-o", ctx.outputs.out.path)
    f = ctx.attr.main.files.to_list()[0]
    args.add("-e", f)
    strip_prefix = f.dirname
    args.add("-D", dirs)
    args.add("-s", strip_prefix)
    args.add_all(inputs)
    ctx.actions.run(
        inputs = inputs,
        progress_message = "Building lambda executable %s" % ctx.label,
        arguments = [args],
        executable = ctx.executable.zipper,
        outputs = [ctx.outputs.out],
        mnemonic = "LambdaPackagePython",
    )
    return []


lambda_python_pkg = rule(
    implementation = _lambda_python_pkg_impl,
    attrs = {
        "deps": attr.label_list(),
        "src": attr.label(mandatory = True),
        "out": attr.output(),
        "main": attr.label(mandatory = True, allow_files = True),
        "zipper": attr.label(
            default = Label("//:zipper"),
            cfg = "host",
            executable = True,
            allow_files = True,
        ),
    },
)


def _lambda_deploy_impl(ctx):
    print(ctx)

lambda_deploy = rule(
    implementation = _lambda_deploy_impl,
    attrs = {
        "pkg": attr.label(mandatory = True),
    },
)
