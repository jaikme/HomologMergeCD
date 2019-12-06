import re
import semver

p = re.compile(r'(?<=release\/v)(.+)')
m = p.search("release/v1.0.9")

if m:
    version = m.group()

    print(f'str {version}')

    ver = semver.parse(version)

    print(version)
