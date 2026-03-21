import resource

def memory_limit():
    resource.setrlimit(resource.RLIMIT_AS, (256 * 1024 * 1024, -1))