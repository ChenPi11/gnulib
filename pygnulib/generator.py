#!/usr/bin/python
# encoding: UTF-8



import os

from .config import Config
from .module import Module



class Generator:
    """gnulib file content generator"""
    _TEMPLATE_ = (
        "## DO NOT EDIT! GENERATED AUTOMATICALLY!",
        "#",
        "# This file is free software; you can redistribute it and/or modify",
        "# it under the terms of the GNU General Public License as published by",
        "# the Free Software Foundation; either version 3 of the License, or",
        "# (at your option) any later version.",
        "#",
        "# This file is distributed in the hope that it will be useful,",
        "# but WITHOUT ANY WARRANTY; without even the implied warranty of",
        "# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the",
        "# GNU General Public License for more details.",
        "#",
        "# You should have received a copy of the GNU General Public License",
        "# along with this file.  If not, see <http://www.gnu.org/licenses/>.",
        "#",
        "# As a special exception to the GNU General Public License,",
        "# this file may be distributed as part of a program that",
        "# contains a configuration script generated by Autoconf, under",
        "# the same distribution terms as the rest of that program.",
        "#",
        "# Generated by gnulib-tool.",
    )

    def __repr__(self):
        return "pygnulib.generator.Generator"

    def __str__(self):
        return "\n".join([_ for _ in self])

    def __iter__(self):
        for line in Generator._TEMPLATE_:
            yield line



class POMakefile(Generator):
    """PO Makefile parameterization"""
    _TEMPLATE_ = (
        "# These options get passed to xgettext.",
        "XGETTEXT_OPTIONS = \\",
        "  --keyword=_ --flag=_:1:pass-c-format \\",
        "  --keyword=N_ --flag=N_:1:pass-c-format \\",
        "  --keyword='proper_name:1,\"This is a proper name." # comma omitted
        " See the gettext manual, section Names.\"' \\",
        "  --keyword='proper_name_utf8:1,\"This is a proper name." # comma omitted
        " See the gettext manual, section Names.\"' \\",
        "  --flag=error:3:c-format --flag=error_at_line:5:c-format",
        "",
        "# This is the copyright holder that gets inserted into the header of the",
        "# $(DOMAIN).pot file.  gnulib is copyrighted by the FSF.",
        "COPYRIGHT_HOLDER = Free Software Foundation, Inc.",
        "",
        "# This is the email address or URL to which the translators shall report",
        "# bugs in the untranslated strings:",
        "# - Strings which are not entire sentences, see the maintainer guidelines",
        "#   in the GNU gettext documentation, section 'Preparing Strings'.",
        "# - Strings which use unclear terms or require additional context to be",
        "#   understood.",
        "# - Strings which make invalid assumptions about notation of date, time or",
        "#   money.",
        "# - Pluralisation problems.",
        "# - Incorrect English spelling.",
        "# - Incorrect formatting.",
        "# It can be your email address, or a mailing list address where translators",
        "# can write to without being subscribed, or the URL of a web page through",
        "# which the translators can contact you.",
        "MSGID_BUGS_ADDRESS = bug-gnulib@gnu.org",
        "",
        "# This is the list of locale categories, beyond LC_MESSAGES, for which the",
        "# message catalogs shall be used.  It is usually empty.",
        "EXTRA_LOCALE_CATEGORIES =",
        "",
        "# This tells whether the $(DOMAIN).pot file contains messages with an 'msgctxt'",
        "# context.  Possible values are \"yes\" and \"no\".  Set this to yes if the",
        "# package uses functions taking also a message context, like pgettext(), or",
        "# if in $(XGETTEXT_OPTIONS) you define keywords with a context argument.",
        "USE_MSGCTXT = no"
    )
    def __init__(self, config):
        if not isinstance(config, Config):
            raise TypeError("config must be of pygnulib.Config type")
        self._config_ = config
        super().__init__()


    @property
    def po_base(self):
        """directory relative to ROOT where *.po files are placed; defaults to 'po'"""
        return self._config_.po_base


    @property
    def po_domain(self):
        """the prefix of the i18n domain"""
        return self._config_.po_domain


    def __repr__(self):
        fmt = "pygnulib.generator.POMakefile(po_base=%r, po_domain=%r)"
        return fmt % (self.po_base, self.po_domain)


    def __iter__(self):
        for line in super().__iter__():
            yield line
        yield "# Usually the message domain is the same as the package name."
        yield "# But here it has a '-gnulib' suffix."
        yield "DOMAIN = %s-gnulib" % self.po_domain
        yield ""
        yield "# These two variables depend on the location of this directory."
        yield "subdir = %s" % self.po_domain
        yield "top_subdir = %s" % "/".join([".." for _ in self.po_base.split(os.path.sep)])
        for line in POMakefile._TEMPLATE_:
            yield line



class POTFILES(Generator):
    """File list to be passed to xgettext"""
    def __init__(self, config, files):
        if not isinstance(config, Config):
            raise TypeError("config must be of pygnulib.Config type")
        super().__init__()
        self._config_ = config
        self._files_ = tuple(files)


    @property
    def source_base(self):
        """directory relative to ROOT where source code is placed; defaults to 'lib'"""
        return self._config_.source_base


    @property
    def files(self):
        """list of files"""
        return tuple(self.files)


    def __repr__(self):
        fmt = "pygnulib.generator.POTFILES(source_base=%r, files=%r)"
        return fmt % (self.source_base, self.files)


    def __iter__(self):
        for line in super().__iter__():
            yield line
        yield "# List of files which contain translatable strings."
        for file in [_ for _ in self.files if _.startswith("lib/")]:
            yield os.path.join(self.source_base, file[4:])



class AutoconfSnippet(Generator):
    """autoconf snippet generator for standalone module"""
    def __init__(self, config, module, toplevel, no_libtool, no_gettext):
        """
        config: gnulib configuration
        module: gnulib module instance
        toplevel: make a subordinate use of gnulib if False
        no_libtool: disable libtool (regardless of configuration)
        no_gettext: disable AM_GNU_GETTEXT invocations if True
        """
        if not isinstance(config, Config):
            raise TypeError("config must be of pygnulib.config.Config type")
        if not isinstance(module, Module):
            raise TypeError("module must be of pygnulib.module.Module type")
        if not isinstance(toplevel, bool):
            raise TypeError("toplevel must be of bool type")
        if not isinstance(no_libtool, bool):
            raise TypeError("no_libtool must be of bool type")
        if not isinstance(no_gettext, bool):
            raise TypeError("no_gettext must be of bool type")
        super().__init__()
        self._config_ = config
        self._module_ = module
        self._toplevel_ = toplevel
        self._no_libtool_ = no_libtool
        self._no_gettext_ = no_gettext


    @property
    def toplevel(self):
        """top level indicator; subordinate use of pygnulib"""
        return self._toplevel_


    @property
    def libtool(self):
        """libtool switch, disabling libtool configuration parameter"""
        return self._config_.libtool and not self._no_libtool_


    @property
    def gettext(self):
        """gettext switch, disabling AM_GNU_GETTEXT invocations"""
        return not self._no_gettext_


    def __repr__(self):
        flags = []
        if self.toplevel:
            flags += ["toplevel"]
        if self.libtool:
            flags += ["libtool"]
        if self.gettext:
            flags += ["gettext"]
        fmt = "pygnulib.generator.AutoconfSnippet(include_guard_prefix=%r, flags=%s)"
        include_guard_prefix = self._config_.include_guard_prefix
        return fmt % (include_guard_prefix, "|".join(flags))


    def __iter__(self):
        module = self._module_
        if module.name not in ("gnumakefile", "maintainer-makefile") or self.toplevel:
            snippet = module.configure_ac_snippet
            include_guard_prefix = self._config_.include_guard_prefix
            snippet.replace(r"${gl_include_guard_prefix}", include_guard_prefix)
            if not self.libtool:
                table = (
                    (r"$gl_cond_libtool", "false"),
                    ("gl_libdeps", "gltests_libdeps"),
                    ("gl_ltlibdeps", "gltests_ltlibdeps"),
                )
                for (src, dst) in table:
                    snippet = snippet.replace(src, dst)
            if not self.gettext:
                src = "AM_GNU_GETTEXT([external])"
                dst = "dnl you must add AM_GNU_GETTEXT([external]) or similar to configure.ac.'"
                snippet = snippet.replace(src, dst)
            lines = (_ for _ in snippet.split("\n") if _)
            for line in lines:
                yield line
            if module.name == "alloca" and self.libtool:
                yield "changequote(,)dnl"
                yield "LTALLOCA=`echo \"$ALLOCA\" | sed -e 's/\\.[^.]* /.lo /g;s/\\.[^.]*$/.lo/'`"
                yield "changequote([, ])dnl"
                yield "AC_SUBST([LTALLOCA])"