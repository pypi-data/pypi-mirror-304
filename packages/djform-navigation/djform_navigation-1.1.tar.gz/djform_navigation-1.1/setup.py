import sys
from setuptools import find_namespace_packages, setup

def main(vv):

    install_requires = [
        "Django>=3",
    ]

    deploy_requires = [
        "bump2version",
        "readme_renderer[md]",
        "git-changelog",
    ]

    extras_require = {
        "development": [
            install_requires,
            deploy_requires,
        ],
        "deploy": deploy_requires,
    }

    with open("README.md", "r") as fh:
        long_description = fh.read()


    setup(
        name='djform_navigation',
        version=str(vv),
        description='Primary key based form navigation to explore next/prev records.',
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Sami Akram",
        author_email="samiakram@live.com",
        url="https://github.com/humblesami/djform_navigation.git",

        python_requires=">=3.6",
        install_requires=install_requires,
        tests_require=["coverage"],
        extras_require=extras_require,
        include_package_data=True,
        setup_requires=['setuptools_scm'],
        data_files=[
            ('1', ['form_navigation/templates/admin/change_form.html']),
            ('2', ['form_navigation/static/form_navigation/module.js'])
        ],
        packages=find_namespace_packages(include=["form_navigation"],),
    )


if __name__ == '__main__':
    version = ''
    if sys.argv:
        last_arg = sys.argv[-1:][0]
        if last_arg.startswith('-v='):
            sys.argv = sys.argv[:-1]
            version = last_arg[3:]
    try:
        main(version)
        print("Success")
    except Exception as ex:
        message = str(ex)
        print("Error in set up ", message)
    print("Complete")