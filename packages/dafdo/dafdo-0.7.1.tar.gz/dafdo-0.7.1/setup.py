from setuptools import setup, find_packages

setup(
    name='dafdo',
    version='0.7.1',  # Contoh versi
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dafdo=dafdo.__init__:main',  # Pastikan ini sesuai dengan fungsi main
        ],
    },
    install_requires=[],  # Daftar ketergantungan jika ada
    description='Dafdo adalah bahasa pemrograman asal indonesia versi bahasa jawa',  # Deskripsi singkat
    author='Daffa Danur Windho',  # Nama penulis
    author_email='danuwindha@gmail.com',  # Email penulis
    url='https://pypi.org/project/dafdo/',  # URL proyek
)
