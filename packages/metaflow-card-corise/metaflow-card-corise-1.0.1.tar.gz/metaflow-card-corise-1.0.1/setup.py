from setuptools import find_namespace_packages, setup

setup(
    name="metaflow-card-corise",
    version="1.0.1",
    description="Metaflow card template for the full-stack ML with Metaflow Corise course",
    author="Ville Tuulos",
    author_email="ville@outerbounds.co",
    license="Apache Software License 2.0",
    package_data={"": ["main.js", "base.html", "bundle.css"]},
    packages=find_namespace_packages(include=['metaflow_extensions.*']),
    include_package_data=True,
    zip_safe=False,
)
