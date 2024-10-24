from setuptools import setup, find_packages

setup(
    name="django-assets-tags",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    description="Reusable Django template tags for public and private asset URLs.",
    author="Akib Kamani",
    author_email="your-email@example.com",  # Replace with your email
    url="https://github.com/akibkamani/django-assets-tags",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "Django>=3.0",
    ],
)
