#!/usr/bin/env python3
import os

from setuptools import setup

BASEDIR = os.path.abspath(os.path.dirname(__file__))

with open(f"{BASEDIR}/README.md", "r") as fh:
    long_desc = fh.read()


def get_version():
    """ Find the version of the package"""
    version = None
    version_file = os.path.join(BASEDIR, 'ovos_face_embeddings', 'version.py')
    major, minor, build, alpha = (None, None, None, None)
    with open(version_file) as f:
        for line in f:
            if 'VERSION_MAJOR' in line:
                major = line.split('=')[1].strip()
            elif 'VERSION_MINOR' in line:
                minor = line.split('=')[1].strip()
            elif 'VERSION_BUILD' in line:
                build = line.split('=')[1].strip()
            elif 'VERSION_ALPHA' in line:
                alpha = line.split('=')[1].strip()

            if ((major and minor and build and alpha) or
                    '# END_VERSION_BLOCK' in line):
                break
    version = f"{major}.{minor}.{build}"
    if alpha:
        version += f"a{alpha}"
    return version


def required(requirements_file):
    """ Read requirements file and remove comments and empty lines. """
    with open(os.path.join(BASEDIR, requirements_file), 'r') as f:
        requirements = f.read().splitlines()
        if 'MYCROFT_LOOSE_REQUIREMENTS' in os.environ:
            print('USING LOOSE REQUIREMENTS!')
            requirements = [r.replace('==', '>=').replace('~=', '>=') for r in requirements]
        return [pkg for pkg in requirements
                if pkg.strip() and not pkg.startswith("#")]


PLUGIN_ENTRY_POINT = 'ovos-face-embeddings-plugin=ovos_face_embeddings:FaceEmbeddingsRecognitionPlugin'

setup(
    name='ovos-face-embeddings-plugin',
    version=get_version(),
    description='A face recognition plugin for OVOS',
    url='https://github.com/TigreGotico/ovos-face-embeddings-plugin',
    author='jarbasai',
    author_email='jarbasai@mailfence.com',
    license='MIT',
    packages=['ovos_face_embeddings'],
    zip_safe=True,
    keywords='OVOS openvoiceos plugin face recognition',
    entry_points={'opm.embeddings.face': PLUGIN_ENTRY_POINT},
    install_requires=required("requirements.txt"),
    long_description=long_desc,
    long_description_content_type='text/markdown'
)
