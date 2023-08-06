import re


def extract_requirements():
    with open('pyproject.toml', 'r') as f:
        toml = f.readlines()

    optional_section = False
    start = False
    deps = []
    for line in toml:
        line = line.strip()
        if line == 'dependencies = [':
            start = True
        elif line == '[project.optional-dependencies]':
            optional_section = True
        elif line.startswith('['):
            optional_section = False
        elif optional_section and re.search(r'^\w+ \= \[$', line):
            start = True
        elif line.startswith(']'):
            start = False
        elif start:
            deps.append(re.search(r'"([-_a-zA-Z0-9]+).*",?', line).group(1))

    return ' '.join(deps)


if __name__ == '__main__':
    print(extract_requirements())
