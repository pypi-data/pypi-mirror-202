import tempfile
import subprocess

def test_pip_install() -> None:
    print('testing pip install\ncreating tempdir')
    with tempfile.TemporaryDirectory() as tmpdir:
        print('creating venv')
        subprocess.run(
            "python -m venv venv", check=True, cwd=tmpdir,
        )
        print('pip installing np-zro')
        subprocess.run(
            f"{tmpdir}\\venv\\scripts\\python.exe -m pip install --extra-index-url https://pypi.org/simple np-zro", check=True, cwd=tmpdir,
        )
        response = subprocess.run(
            f"{tmpdir}\\venv\\scripts\\python.exe -c \"import np_zro\"", check=False, cwd=tmpdir,
        )
    assert response.returncode == 0, 'pip install failed'
    print('pip install succeeded\ntempdir deleted')
    
if __name__ == '__main__':
    test_pip_install()