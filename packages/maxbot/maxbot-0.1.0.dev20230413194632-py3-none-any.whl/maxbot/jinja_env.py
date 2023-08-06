"""Jinja environment for NLG templates."""
import logging

import jinja2
from jinja2 import nodes
from jinja2.compiler import CodeGenerator
from jinja2.ext import Extension
from jinja2.runtime import Macro

from .markdown import Markup, escape

logger = logging.getLogger(__name__)


class _AutoEscapeCodeGenerator(CodeGenerator):
    def visit_Template(self, *args, **kwargs):  # noqa: N802
        super().visit_Template(*args, **kwargs)
        self.writeline("")
        self.writeline("escape = environment.escape_fn")
        self.writeline("Markup = environment.markup_class")
        self.writeline("Macro = environment.macro_class")


class _AutoEscapeMacro(Macro):
    async def _async_invoke(self, arguments, autoescape):
        return Markup(await self._func(*arguments))

    def _invoke(self, arguments, autoescape):
        assert autoescape
        assert self._environment.is_async
        return self._async_invoke(arguments, autoescape)


class AutoEscapeEnvironment(jinja2.Environment):
    """Jinja environment with autoescaping HTML and Markdown sequences."""

    code_generator_class = _AutoEscapeCodeGenerator

    def __init__(self, **kwargs):
        """Create new class instance."""
        super().__init__(**{**kwargs, **{"autoescape": True}})
        for name in self.filters:
            self._filter_return_markup(name)
        self.filters.update(e=escape, escape=escape)
        self.escape_fn = escape
        self.markup_class = Markup
        self.macro_class = _AutoEscapeMacro

    def _filter_return_markup(self, name):
        original_fn = self.filters[name]

        def wrapper(*arga, **argw):
            rv = original_fn(*arga, **argw)
            if hasattr(rv, "__html__") and not hasattr(rv, "__markdown__"):
                rv = Markup(rv.__html__())
            return rv

        self.filters[name] = wrapper
        if hasattr(original_fn, "jinja_pass_arg"):
            # @pass_* decorators
            self.filters[name].jinja_pass_arg = original_fn.jinja_pass_arg


def create_jinja_env(options=None):
    """Create Jinja environment with the passes options.

    The `autoescape` option defaults to `True`.

    The :class:`~VariablesExtension` is added to the environment.

    The function and filter `mandatory` is added to the environment.

    Using :class:`EnclosedUndefined` avoids throwing an :class:`~jinja2.UndefinedError`
    to expresions like `{% if entities.menu.standard %}` in cases where `entities.menu` is
    not recognized and returns `undefined`.
    This undefined type cannot be formatted into a string or put into a user variable/slot using
    the Jinja-tag `user` or `slot` (an exception will be thrown).

    :param dict|None options: An options for the Jinja environment.
    :return jinja2.Environment:
    """
    options = dict(options) if options else {}
    # nosec note: autoescape is not actual when rendering yaml
    options.setdefault("extensions", []).extend(
        [
            VariablesExtension,
            LoggingExtension,
        ]
    )
    options.setdefault("undefined", EnclosedUndefined)
    options.setdefault("trim_blocks", True)
    options.setdefault("lstrip_blocks", True)
    env_class = AutoEscapeEnvironment if options.get("autoescape", True) else jinja2.Environment
    env = env_class(enable_async=True, **options)  # nosec: B701
    env.filters.update(mandatory=mandatory)
    env.filters.update(nl2br=nl2br)
    env.globals.update(mandatory=mandatory)
    return env


class VariablesExtension(Extension):
    """Jinja extension for custom tags `slot` and `user` used to set state variables.

    Example of assigning to a user variable:

        {% user name = 'Bob' %}

    Example of assigning to a slot variable:

        {% slot guests = entities.number %}
    """

    tags = {"slot", "user"}

    def parse(self, parser):
        """Transform our custom statements into dict updates.

        Works something like this

            {% user name = 'Bob' %}
            -> {% set _ = user.update({'name': mandatory('Bob')}) %}
            {% slot guests = entities.number %}
            -> {% set _ = slots.update({'guests': mandatory(entities.number)}) %}

        This method is called by Jinja environment.

        :param jinja.parser.Parser parser: Jinja parser.
        :return jinja.nodes.Node: Jinja node.
        """
        var = parser.stream.current.value
        lineno = next(parser.stream).lineno

        name = parser.stream.expect("name").value
        parser.stream.expect("assign")
        value = parser.parse_expression()

        if var == "slot":
            var = "slots"
        method = nodes.Getattr(nodes.Name(var, "load"), "update", nodes.ContextReference())
        mandatory_call = nodes.Call(
            nodes.Name("mandatory", "load"),
            [
                value,
            ],
            [],
            None,
            None,
        )
        call = nodes.Call(method, [], [nodes.Keyword(name, mandatory_call)], None, None)
        dummy = nodes.Name("_", "store")
        return nodes.Assign(dummy, call).set_lineno(lineno)


class LoggingExtension(Extension):
    """Jinja extension for custom tags `debug` and `warning` used to logging."""

    tags = {"debug", "warning"}

    def parse(self, parser):
        """Transform our custom statements into logging hooks calls.

        This method is called by Jinja environment.

        :param jinja.parser.Parser parser: Jinja parser.
        :return jinja.nodes.Node: Jinja node.
        """
        level = parser.stream.current.value
        lineno = next(parser.stream).lineno
        objects = parser.parse_tuple()
        node = nodes.ExprStmt(lineno=lineno)
        node.node = self.call_method(
            "_call_logger",
            [nodes.ContextReference(), nodes.Const(level.upper()), objects],
            lineno=lineno,
        )
        return node

    def _call_logger(self, context, level, objects):
        turn_context = context.get("_turn_context")
        if turn_context:
            turn_context.log(level, objects)
        else:
            logger.log(getattr(logging, level, "DEBUG"), repr(objects))
        return objects


_fail_with_undefined_error = jinja2.Undefined._fail_with_undefined_error  # pylint: disable=W0212


class EnclosedUndefined(jinja2.Undefined):
    """Child class from :class:`~jinja2.Undefined`.

    Example of cast to bool:
        >>> jinja2.Environment(undefined=EnclosedUndefined).from_string("{% if xxx %}defined{% else %}undefined{% endif %}").render()
        'undefined'

    Example of cast to string:
        >>> jinja2.Environment(undefined=EnclosedUndefined).from_string("{{ xxx }}").render()
          File "<template>", line 1, in top-level template code
        jinja2.exceptions.UndefinedError: 'xxx' is undefined
    """

    def __getattr__(self, _):
        """Get any attribute as undefined."""
        return self

    __getitem__ = __getattr__

    __str__ = _fail_with_undefined_error


def mandatory(o):
    """Throws an :class:`~UndefinedError` exception if the argument is undefined otherwise returns it.

    :raise UndefinedError: The argument is undefined.
    :param any o: Any object.
    :return any: Input argument.
    """
    if isinstance(o, jinja2.Undefined):
        _fail_with_undefined_error(o)
    return o


def nl2br(text):
    """Convert newlines to <br /> element."""
    return Markup("<br />".join(text.splitlines()))
