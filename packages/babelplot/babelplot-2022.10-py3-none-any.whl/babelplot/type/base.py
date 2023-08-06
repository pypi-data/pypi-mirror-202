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

import dataclasses as dtcl
from typing import Any, TypeVar

from babelplot.backend.runtime import BackendTranslations
from babelplot.backend.specification.plot import TranslatedArguments
from babelplot.brick.log import LOGGER


backend_figure_h = TypeVar("backend_figure_h")
backend_frame_h = TypeVar("backend_frame_h")
backend_plot_h = TypeVar("backend_plot_h")
backend_element_h = backend_figure_h | backend_frame_h | backend_plot_h


@dtcl.dataclass(repr=False, eq=False)
class babelplot_element_t:
    pbe: str = None  # Cannot be backend_e since external backends would not be accounted for then
    # In case the backend does not make it easy to retrieve some properties, they are stored here. E.g., how to retrieve
    # the marker of a scatter plot in Matplotlib?
    # /!\ Do not forget to initialize it with kwargs during element instanciation.
    property: dict[str, Any] = dtcl.field(default_factory=dict)
    backend: backend_element_h = dtcl.field(init=False, default=None)

    @staticmethod
    def BackendSetProperty(
        element: backend_element_h, name: str, value: Any, /
    ) -> None:
        """"""
        LOGGER.warn(
            f"{babelplot_element_t.BackendSetProperty.__name__}: Not provided by backend."
        )

    @staticmethod
    def BackendProperty(element: backend_element_h, name: str, /) -> Any:
        """"""
        LOGGER.warn(
            f"{babelplot_element_t.BackendProperty.__name__}: Not provided by backend."
        )

    def SetProperty(self, *args, **kwargs) -> None:
        """"""
        args, kwargs = TranslatedArguments(
            "SetProperty", args, kwargs, BackendTranslations(self.pbe)
        )

        if (n_properties := args.__len__()) > 0:
            if (n_properties % 2) > 0:
                LOGGER.error(
                    f"N. argument(s)={n_properties}: Properties not passed in matching key-value pairs. "
                    f"Expected=Even number."
                )

            for name, value in zip(args[:-1:2], args[1::2]):
                self._SetProperty(name, value)

        for name, value in kwargs.items():
            self._SetProperty(name, value)

    def _SetProperty(self, name: str, value: Any, /) -> None:
        """"""
        self.property[name] = value
        self.BackendSetProperty(self.backend, name, value)

    def Property(self, *args) -> Any | tuple[Any]:
        """"""
        output = []

        args, _ = TranslatedArguments(
            "Property", args, {}, BackendTranslations(self.pbe)
        )

        for name in args:
            if name in self.property:
                output.append(self.property[name])
            else:
                output.append(self.BackendProperty(self.backend, name))

        if output.__len__() > 1:
            return output

        return output[0]
