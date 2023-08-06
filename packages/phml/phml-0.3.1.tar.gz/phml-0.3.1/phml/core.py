from __future__ import annotations

import os
import sys
from contextlib import contextmanager
from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING, Any, NoReturn, overload

if TYPE_CHECKING:
    from collections.abc import Iterator

from .compiler import HypertextMarkupCompiler
from .components import ComponentManager, ComponentType

# TODO: Optimize and extract manipulation of import dicts
from .embedded import __FROM_IMPORTS__, __IMPORTS__, Module
from .helpers import PHMLTryCatch
from .nodes import AST, Node, Parent
from .parser import HypertextMarkupParser


class HypertextManager:
    parser: HypertextMarkupParser
    """PHML parser."""
    compiler: HypertextMarkupCompiler
    """PHML compiler to HTML."""
    components: ComponentManager
    """PHML component parser and manager."""
    context: dict[str, Any]
    """PHML global variables to expose to each phml file compiled with this instance.
    This is the highest scope and is overridden by more specific scoped variables.
    """

    def __init__(self) -> None:
        self.parser = HypertextMarkupParser()
        self.compiler = HypertextMarkupCompiler()
        self.components = ComponentManager()
        self.context = {"Module": Module}
        self._ast: AST | None = None
        self._from_path = None
        self._from_file = None
        self._to_file = None

    @staticmethod
    @contextmanager
    def open(
        _from: str | Path,
        _to: str | Path | None = None,
    ) -> Iterator[HypertextManager]:
        with PHMLTryCatch():
            core = HypertextManager()
            core._from_path = Path(_from)
            core._from_path.parent.mkdir(parents=True, exist_ok=True)
            core._from_file = Path(_from).open("r", encoding="utf-8")
            if _to is not None:
                output = Path(_to)
                output.parent.mkdir(parents=True, exist_ok=True)
                core._to_file = output.open("+w", encoding="utf-8")

            core.parse()

            yield core

            core._from_path = None
            core._from_file.close()
            if core._to_file is not None:
                core._to_file.close()

    @property
    def imports(self) -> dict:
        return dict(__IMPORTS__)

    @property
    def from_imports(self) -> dict:
        return dict(__FROM_IMPORTS__)

    def add_module(
        self,
        module: str,
        *,
        name: str | None = None,
        imports: list[str] | None = None,
    ) -> NoReturn:
        """Pass and imported a python file as a module. The modules are imported and added
        to phml's cached imports. These modules are **ONLY** exposed to the python elements.
        To use them in the python elements or the other scopes in the files you must use the python
        import syntax `import <module>` or `from <module> import <...objects>`. PHML will parse
        the imports first and remove them from the python elements. It then checks it's cache of
        python modules that have been imported and adds those imported modules to the local context
        for each embedded python execution.

        Note:
            - All imports will have a `.` prefixed to the module name. For example `current/file.py` gets the module
            name `.current.file`. This helps seperate and indicate what imports are injected with this method.
            Module import syntax will retain it's value, For example suppose the module `..module.name.here`
            is added. It is in directory `module/` which is in a sibling directory to `current/`. The path
            would look like `parent/ -> module/ -> name/ -> here.py` and the module would keep the name of
            `..module.name.here`.

            - All paths are resolved with the cwd in mind.

        Args:
            module (str): Absolute or relative path to a module, or module syntax reference to a module.
            name (str): Optional name for the module after it is imported.
            imports (list[str]): Optional list of objects to import from the module. Turns the import to
                `from <module> import <...objects>` from `import <module>`.

        Returns:
            str: Name of the imported module. The key to use for indexing imported modules
        """

        if module.startswith("~"):
            module = module.replace("~", str(Path.home()))

        mod = None
        file = Path(module).with_suffix(".py")
        cwd = os.getcwd()

        if file.is_file():
            current = Path(cwd).as_posix()
            path = file.resolve().as_posix()

            cwd_p = current.split("/")
            path_p = path.split("/")
            index = 0
            for cp, pp in zip(cwd_p, path_p):
                if cp != pp:
                    break
                index += 1

            name = "/".join(path_p[index:]).rsplit(".", 1)[0].replace("/", ".")
            path = "/".join(path_p[:index])

            # Make the path that is imported form the only path in sys.path
            # this will prevent module conflicts and garuntees the correct module is imported
            sys_path = list(sys.path)
            sys.path = [path]
            mod = import_module(name)
            sys.path = sys_path

            name = f".{name}"
        else:
            if module.startswith(".."):
                current = Path(os.getcwd()).as_posix()
                cwd_p = current.split("/")

                path = "/".join(cwd_p[:-1])

                sys_path = list(sys.path)
                sys.path = [path]
                mod = import_module(module.lstrip(".."))
                sys.path = sys_path
            else:
                mod = import_module(module)
            name = f".{module.lstrip('..')}"

        # Add imported module or module objects to appropriate collection
        if imports is not None and len(imports) > 0:
            for _import in imports:
                if name not in __FROM_IMPORTS__:
                    __FROM_IMPORTS__[name] = {}
                __FROM_IMPORTS__[name].update({_import: getattr(mod, _import)})
        else:
            __IMPORTS__[name] = mod

        return name

    def remove_module(self, module: str, imports: list[str] | None = None):
        if not module.startswith("."):
            module = f".{module}"
        if module in __IMPORTS__ and len(imports or []) == 0:
            __IMPORTS__.pop(module, None)
        if module in __FROM_IMPORTS__:
            if imports is not None and len(imports) > 0:
                for _import in imports:
                    __FROM_IMPORTS__[module].pop(_import, None)
                if len(__FROM_IMPORTS__[module]) == 0:
                    __FROM_IMPORTS__.pop(module, None)
            else:
                __FROM_IMPORTS__.pop(module, None)

        return self

    @property
    def ast(self) -> AST:
        """The current ast that has been parsed. Defaults to None."""
        return self._ast or AST()

    def load(self, path: str | Path):
        """Loads the contents of a file and sets the core objects ast
        to the results after parsing.
        """
        with PHMLTryCatch(), Path(path).open("r", encoding="utf-8") as file:
            self._from_path = path
            self._ast = self.parser.parse(file.read())
        return self

    def parse(self, data: str | dict | None = None):
        """Parse a given phml string or dict into a phml ast.

        Returns:
            Instance of the core object for method chaining.
        """

        if data is None and self._from_file is None:
            raise ValueError(
                "Must either provide a phml str/dict to parse or use parse in the open context manager",
            )

        with PHMLTryCatch(self._from_path, "phml:__parse__"):
            if isinstance(data, dict):
                ast = Node.from_dict(data)
                if not isinstance(ast, AST) and ast is not None:
                    ast = AST([ast])
                self._ast = ast
            elif data is not None:
                self._ast = self.parser.parse(data)
            elif self._from_file is not None:
                self._ast = self.parser.parse(self._from_file.read())
                self._from_file.seek(0)

        return self

    def format(
        self,
        *,
        code: str = "",
        file: str | Path | None = None,
        compress: bool = False,
    ) -> str | None:
        """Format a phml str or file.

        Args:
            code (str, optional): The phml str to format.

        Kwargs:
            file (str, optional): Path to a phml file. Can be used instead of
                `code` to parse and format a phml file.
            compress (bool, optional): Flag to compress the file and remove new lines. Defaults to False.

        Note:
            If both `code` and `file` are passed in then both will be formatted with the formatted `code`
            bing returned as a string and the formatted `file` being written to the files original location.

        Returns:
            str: When a phml str is passed in
            None: When a file path is passed in. Instead the resulting formatted string is written back to the file.
        """

        result = None
        if code != "":
            self.parse(code)
            result = self.compiler.render(
                self._ast,
                compress,
            )

        if file is not None:
            self.load(file)
            with Path(file).open("+w", encoding="utf-8") as phml_file:
                phml_file.write(
                    self.compiler.render(
                        self._ast,
                        compress,
                    ),
                )

        return result

    def compile(self, **context: Any) -> AST:
        """Compile the python blocks, python attributes, and phml components and return the resulting ast.
        The resulting ast replaces the core objects ast.
        """
        context = {**self.context, **context, "_phml_path_": self._from_path}
        if self._ast is not None:
            with PHMLTryCatch(self._from_path, "phml:__compile__"):
                ast = self.compiler.compile(self._ast, self.components, **context)
            return ast
        raise ValueError("Must first parse a phml file before compiling to an AST")

    def render(
        self, _compress: bool = False, _ast: AST | None = None, **context: Any
    ) -> str:
        """Renders the phml ast into an html string. If currently in a context manager
        the resulting string will also be output to an associated file.
        """
        context = {**self.context, **context, "_phml_path_": self._from_path}
        if self._ast is not None:
            with PHMLTryCatch(self._from_path, "phml:__render"):
                result = self.compiler.render(
                    _ast or self.compile(**context),
                    _compress,
                )

                if self._to_file is not None:
                    self._to_file.write(result)
                elif self._from_file is not None and self._from_path is not None:
                    self._to_file = (
                        Path(self._from_path)
                        .with_suffix(".html")
                        .open("+w", encoding="utf-8")
                    )
                    self._to_file.write(result)
            return result
        raise ValueError("Must first parse a phml file before rendering a phml AST")

    def write(
        self,
        _path: str | Path,
        _compress: bool = False,
        _ast: AST | None = None,
        **context: Any,
    ):
        """Render and write the current ast to a file.

        Args:
            path (str): The output path for the rendered html.
            compress (bool): Whether to compress the output. Defaults to False.
        """
        path = Path(_path).with_suffix(".html")
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("+w", encoding="utf-8") as file:
            file.write(self.compiler.render(_ast or self.compile(**context), _compress))
        return self

    @overload
    def add(self, file: str | Path, *, name: str|None=None, ignore: str = ""):
        """Add a component to the component manager with a file path. Also, componetes can be added to
        the component manager with a name and str or an already parsed component dict.

        Args:
            file (str): The file path to the component.
            ignore (str): The path prefix to remove before creating the comopnent name.
            name (str): The name of the component. This is the index/key in the component manager.
                This is also the name of the element in phml. Ex: `Some.Component` == `<Some.Component />`
            data (str | ComponentType): This is the data that is assigned in the manager. It can be a string
                representation of the component, or an already parsed component type dict.
        """
        ...

    @overload
    def add(self, *, name: str, data: str | ComponentType):
        """Add a component to the component manager with a file path. Also, componetes can be added to
        the component manager with a name and str or an already parsed component dict.

        Args:
            file (str): The file path to the component.
            ignore (str): The path prefix to remove before creating the comopnent name.
            name (str): The name of the component. This is the index/key in the component manager.
                This is also the name of the element in phml. Ex: `Some.Component` == `<Some.Component />`
            data (str | ComponentType): This is the data that is assigned in the manager. It can be a string
                representation of the component, or an already parsed component type dict.
        """
        ...

    def add(
        self,
        file: str | Path | None = None,
        *,
        name: str | None = None,
        data: ComponentType | str | None = None,
        ignore: str = "",
    ):
        """Add a component to the component manager. The components are used by the compiler
        when generating html files from phml.
        """
        with PHMLTryCatch(file or name or "_cmpt_"):
            self.components.add(file, name=name, data=data, ignore=ignore)

    def remove(self, key: str):
        """Remove a component from the component manager based on the components name/tag."""
        self.components.remove(key)

    def expose(self, _context: dict[str, Any] | None = None, **context: Any):
        """Expose global variables to each phml file compiled with this instance.
        This data is the highest scope and will be overridden by more specific
        scoped variables with equivelant names.
        """

        if _context:
            self.context.update(_context or {})
        self.context.update(context)

    def redact(self, *keys: str):
        """Remove global variable from this instance."""
        for key in keys:
            self.context.pop(key, None)
