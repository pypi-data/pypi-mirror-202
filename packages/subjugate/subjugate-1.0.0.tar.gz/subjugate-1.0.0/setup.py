from setuptools import find_packages, setup

with open("README.md") as readme:
    setup(
        name="subjugate",
        # version=__import__("subjugate.__version__").__version__,
        version="1.0.0",
        url="https://github.com/estheruary/subjugate",
        license="LGPLv3",
        description="Write templates in Django with Dominate",
        long_description=readme.read(),
        long_description_content_type="text/markdown",
        author="Estelle Poulin",
        author_email="dev@inspiredby.es",
        packages=find_packages(exclude=["tests"]),
        include_package_data=True,
        install_requires=["Django>=2.2"],
        python_requires=">=3.6",
        zip_safe=False,
        project_urls={
            "Source": "https://github.com/estheruary/subjugate",
            "Changelog": "https://github.com/estheruary/subjugate/blob/main/CHANGELOG.md",
        },
    )
