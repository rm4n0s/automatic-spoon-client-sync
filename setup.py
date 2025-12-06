from setuptools import find_packages, setup

setup(
    name="automatic_spoon_client_sync",
    version="0.1",
    license="MIT",
    author="Manos Ragiadakos",
    author_email="",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/rm4n0s/automatic_spoon_client_sync",
    keywords="http client automatic-spoon",
    install_requires=["httpx", "pydantic", "httpx-ws", "pytsterrors"],
    include_package_data=True,
)
