# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2022)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from pathlib import Path

from setuptools import setup


AUTHOR = "Eric Debreuve"
E_MAIL = "eric.debreuve@univ-cotedazur.fr"

PYPI_NAME = "babelplot"
DESCRIPTION = "A Meta Plotting Library That Speaks Several Backends"
KEYWORDS = "plot, library"
TOPIC = "Scientific/Engineering"
SUBTOPIC = "Visualization"
AUDIENCE = "Science/Research"
LICENSE = "CeCILL-2.1"
VERSION = (2022, 10)  # /!\ str(2021.10) -> "2021.1"
STATUS = "3 - Alpha"
PY_VERSION = "3.10"

REPOSITORY_NAME = "babelplot"
REPOSITORY_USER = "eric.debreuve"
REPOSITORY_SITE = "src.koda.cnrs.fr"
DOCUMENTATION_SITE = "-/wikis/HOME"

IMPORT_NAME = "babelplot"
PACKAGES = [
    IMPORT_NAME,
    f"{IMPORT_NAME}.backend",
    f"{IMPORT_NAME}.backend.brick",
    f"{IMPORT_NAME}.backend.helper",
    f"{IMPORT_NAME}.backend.specification",
    f"{IMPORT_NAME}.brick",
    f"{IMPORT_NAME}.type",
]
EXCLUDED_FOLDERS = ("documentation", "test")

HERE = Path(__file__).parent.resolve()


long_description = (HERE / "README.rst").read_text(encoding="utf-8")
repository_url = f"https://{REPOSITORY_SITE}/{REPOSITORY_USER}/{REPOSITORY_NAME}"
documentation_url = f"{repository_url}/{DOCUMENTATION_SITE}"
version = f"{VERSION[0]}.{VERSION[1]}"

folders = [IMPORT_NAME]
for node in (HERE / IMPORT_NAME).rglob("*"):
    if node.is_dir() and not str(node).startswith("."):
        node = node.relative_to(HERE)
        node = ".".join(node.parts)
        if not (
            (node in EXCLUDED_FOLDERS)
            or any(node.startswith(_fld + ".") for _fld in EXCLUDED_FOLDERS)
        ):
            folders.append(node)
folders = sorted(folders)
if PACKAGES != folders:
    raise ValueError(
        f"Missing packages in setup:\n"
        f"    - Declared={PACKAGES}\n"
        f"    - Actual={folders}"
    )


if __name__ == "__main__":
    #
    setup(
        author=AUTHOR,
        author_email=E_MAIL,
        #
        name=PYPI_NAME,
        description=DESCRIPTION,
        long_description=long_description,
        long_description_content_type="text/x-rst",
        version=version,
        license=LICENSE,
        #
        classifiers=[
            f"Topic :: {TOPIC} :: {SUBTOPIC}",
            f"Intended Audience :: {AUDIENCE}",
            f"License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 ({LICENSE})",
            f"Programming Language :: Python :: {PY_VERSION}",
            f"Development Status :: {STATUS}",
        ],
        keywords=KEYWORDS,
        #
        url=repository_url,
        project_urls={
            "Documentation": documentation_url,
            "Source": repository_url,
        },
        #
        packages=PACKAGES,
        python_requires=f">={PY_VERSION}",
        install_requires=[
            "numpy",
            "PySide6",
            "scikit-image",
        ],
    )
