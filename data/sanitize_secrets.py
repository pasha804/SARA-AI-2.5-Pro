import os

# 1. Sanitize server.cjs
server_path = 'SARA/resources/app/dist/server.cjs'
if os.path.exists(server_path):
    with open(server_path, 'r', encoding='utf-8') as f:
        code = f.read()
    raw_key = 'sk-apx8a660d087a150ce79fbe12593375ea9401369fdac8ed70e'
    if raw_key in code:
        code = code.replace(f'"{raw_key}"', '""')
        with open(server_path, 'w', encoding='utf-8') as f:
            f.write(code)
        print('Sanitized server.cjs')

# 2. Sanitize data/test_all_apinex_models.py
p1 = 'data/test_all_apinex_models.py'
if os.path.exists(p1):
    with open(p1, 'r', encoding='utf-8') as f:
        t = f.read()
    raw_key = 'sk-apx8a660d087a150ce79fbe12593375ea9401369fdac8ed70e'
    t = t.replace(f'"{raw_key}"', 'os.environ.get("APINEX_API_KEY", "")')
    with open(p1, 'w', encoding='utf-8') as f:
        f.write(t)
    print('Sanitized data/test_all_apinex_models.py')

# 3. Sanitize data/test_candidate_models.py
p2 = 'data/test_candidate_models.py'
if os.path.exists(p2):
    with open(p2, 'r', encoding='utf-8') as f:
        t2 = f.read()
    raw_key = 'sk-apx8a660d087a150ce79fbe12593375ea9401369fdac8ed70e'
    t2 = t2.replace(f'"{raw_key}"', 'os.environ.get("APINEX_API_KEY", "")')
    with open(p2, 'w', encoding='utf-8') as f:
        f.write(t2)
    print('Sanitized data/test_candidate_models.py')

# 4. Sanitize docs/SARA_PROVIDER_TESTS.md
p3 = 'docs/SARA_PROVIDER_TESTS.md'
if os.path.exists(p3):
    with open(p3, 'r', encoding='utf-8') as f:
        t3 = f.read()
    raw_key = 'sk-apx8a660d087a150ce79fbe12593375ea9401369fdac8ed70e'
    t3 = t3.replace(raw_key, 'sk-apx********************************')
    with open(p3, 'w', encoding='utf-8') as f:
        f.write(t3)
    print('Sanitized docs/SARA_PROVIDER_TESTS.md')

