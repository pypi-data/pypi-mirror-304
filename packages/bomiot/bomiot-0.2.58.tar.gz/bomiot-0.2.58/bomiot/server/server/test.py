import pkg_resources

installed_packages = [pkg.key for pkg in pkg_resources.working_set]
print(installed_packages)