from setuptools import setup, find_packages

setup(
    name='simple_mobile_packager',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Buraya gerekli bağımlılıkları ekleyin
    ],
    include_package_data=True,
    long_description='Bu kütüphane, Python ile yazılmış uygulamaları mobil APK dosyalarına dönüştürmek için tasarlanmıştır.',
    long_description_content_type='text/markdown',
)
