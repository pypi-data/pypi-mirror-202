from setuptools import setup

setup(
    name='local_pipeline_lib',
    version='0.1.0',
    packages=['local_pipeline_lib'],
    install_requires=[
        # your package dependencies here
    ],
    setup_requires=['wheel'],
    include_package_data=True,
    zip_safe=False,
)
