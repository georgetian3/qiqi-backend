def location_inner(text: str) -> str:
    lines = text.split('\n')
    for i in range(14, 26):
        lines[i] = '//' + lines[i]
    return '\n'.join(lines)

files = {
    'model/validation_error_loc_inner.dart': location_inner,
}

dir = '/Users/george/repos/qiqi-app/lib/api/lib/'


for file in files:
    try:
        path = dir + file
        with open(path) as f:
            text = f.read()
        text = files[file](text)
        with open(path, 'w') as f:
            f.write(text)
    except Exception as e:
        print(f'Exception for file {file}: {e}')