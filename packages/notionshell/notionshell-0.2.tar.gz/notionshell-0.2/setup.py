import setuptools

setuptools.setup(
    name="notionshell",
    version=0.2,
    author="TalWrii",
    long_description_content_type="text/markdown",
    author_email="talwrii@gmail.com",
    description=(
        "Partial notion commad line. Introduction to api, using official library."
    ),
    license="BSD",
    long_description=open("readme.md").read(),
    install_requires=["notion_client"],
    entry_points={"console_scripts": ["notionshell=notionshell:main"]},
    test_suite="nose.collector",
)
