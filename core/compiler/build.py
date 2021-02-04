def function(gen_llvm, token):
    body = gen_llvm(token.body)

    return """declare i32 @{name} {
    {body}
    }""".format(name=token.name, body=body)
