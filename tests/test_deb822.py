#! /usr/bin/python
## vim: fileencoding=utf-8

# Copyright (C) 2006 Adeodato Simó <dato@net.com.org.es>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 2
# dated June, 1991.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import re
import sys
import unittest
from StringIO import StringIO

sys.path.insert(0, '../debian_bundle/')

import deb822

# Keep the test suite compatible with python2.3 for now
try:
    sorted
except NameError:
    def sorted(iterable, cmp=None):
        tmp = iterable[:]
        tmp.sort(cmp)
        return tmp


UNPARSED_PACKAGE = '''\
Package: mutt
Priority: standard
Section: mail
Installed-Size: 4471
Maintainer: Adeodato Simó <dato@net.com.org.es>
Architecture: i386
Version: 1.5.12-1
Replaces: mutt-utf8
Provides: mail-reader, imap-client
Depends: libc6 (>= 2.3.6-6), libdb4.4, libgnutls13 (>= 1.4.0-0), libidn11 (>= 0.5.18), libncursesw5 (>= 5.4-5), libsasl2 (>= 2.1.19.dfsg1), exim4 | mail-transport-agent
Recommends: locales, mime-support
Suggests: urlview, aspell | ispell, gnupg, mixmaster, openssl, ca-certificates
Conflicts: mutt-utf8
Filename: pool/main/m/mutt/mutt_1.5.12-1_i386.deb
Size: 1799444
MD5sum: d4a9e124beea99d8124c8e8543d22e9a
SHA1: 5e3c295a921c287cf7cb3944f3efdcf18dd6701a
SHA256: 02853602efe21d77cd88056a4e2a4350f298bcab3d895f5f9ae02aacad81442b
Description: text-based mailreader supporting MIME, GPG, PGP and threading
 Mutt is a sophisticated text-based Mail User Agent. Some highlights:
 .
  * MIME support (including RFC1522 encoding/decoding of 8-bit message
    headers and UTF-8 support).
  * PGP/MIME support (RFC 2015).
  * Advanced IMAP client supporting SSL encryption and SASL authentication.
  * POP3 support.
  * Mailbox threading (both strict and non-strict).
  * Default keybindings are much like ELM.
  * Keybindings are configurable; Mush and PINE-like ones are provided as
    examples.
  * Handles MMDF, MH and Maildir in addition to regular mbox format.
  * Messages may be (indefinitely) postponed.
  * Colour support.
  * Highly configurable through easy but powerful rc file.
Tag: interface::text-mode, made-of::lang:c, mail::imap, mail::pop, mail::user-agent, protocol::imap, protocol::ipv6, protocol::pop, protocol::ssl, role::sw:client, uitoolkit::ncurses, use::editing, works-with::mail
Task: mail-server
'''
        

PARSED_PACKAGE = deb822.Deb822Dict([
    ('Package', 'mutt'),
    ('Priority', 'standard'),
    ('Section', 'mail'),
    ('Installed-Size', '4471'),
    ('Maintainer', 'Adeodato Simó <dato@net.com.org.es>'),
    ('Architecture', 'i386'),
    ('Version', '1.5.12-1'),
    ('Replaces', 'mutt-utf8'),
    ('Provides', 'mail-reader, imap-client'),
    ('Depends', 'libc6 (>= 2.3.6-6), libdb4.4, libgnutls13 (>= 1.4.0-0), libidn11 (>= 0.5.18), libncursesw5 (>= 5.4-5), libsasl2 (>= 2.1.19.dfsg1), exim4 | mail-transport-agent'),
    ('Recommends', 'locales, mime-support'),
    ('Suggests', 'urlview, aspell | ispell, gnupg, mixmaster, openssl, ca-certificates'),
    ('Conflicts', 'mutt-utf8'),
    ('Filename', 'pool/main/m/mutt/mutt_1.5.12-1_i386.deb'),
    ('Size', '1799444'),
    ('MD5sum', 'd4a9e124beea99d8124c8e8543d22e9a'),
    ('SHA1', '5e3c295a921c287cf7cb3944f3efdcf18dd6701a'),
    ('SHA256', '02853602efe21d77cd88056a4e2a4350f298bcab3d895f5f9ae02aacad81442b'),
    ('Description', '''text-based mailreader supporting MIME, GPG, PGP and threading
 Mutt is a sophisticated text-based Mail User Agent. Some highlights:
 .
  * MIME support (including RFC1522 encoding/decoding of 8-bit message
    headers and UTF-8 support).
  * PGP/MIME support (RFC 2015).
  * Advanced IMAP client supporting SSL encryption and SASL authentication.
  * POP3 support.
  * Mailbox threading (both strict and non-strict).
  * Default keybindings are much like ELM.
  * Keybindings are configurable; Mush and PINE-like ones are provided as
    examples.
  * Handles MMDF, MH and Maildir in addition to regular mbox format.
  * Messages may be (indefinitely) postponed.
  * Colour support.
  * Highly configurable through easy but powerful rc file.'''),
    ('Tag', 'interface::text-mode, made-of::lang:c, mail::imap, mail::pop, mail::user-agent, protocol::imap, protocol::ipv6, protocol::pop, protocol::ssl, role::sw:client, uitoolkit::ncurses, use::editing, works-with::mail'),
    ('Task', 'mail-server'), ])


GPG_SIGNED = [ '''\
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA1

%s

-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1.4.3 (GNU/Linux)
Comment: Signed by Adeodato Simó <dato@net.com.org.es>

iEYEARECAAYFAkRqYxkACgkQgyNlRdHEGIKccQCgnnUgfwYjQ7xd3zGGS2y5cXKt
CcYAoOLYDF5G1h3oR1iDNyeCI6hRW03S
=Um8T
-----END PGP SIGNATURE-----
''', '''\
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA1

%s

-----BEGIN PGP SIGNATURE-----

iEYEARECAAYFAkRqYxkACgkQgyNlRdHEGIKccQCgnnUgfwYjQ7xd3zGGS2y5cXKt
CcYAoOLYDF5G1h3oR1iDNyeCI6hRW03S
=Um8T
-----END PGP SIGNATURE-----
''',
    ]


CHANGES_FILE = '''\
Format: 1.7
Date: Fri, 28 Dec 2007 17:08:48 +0100
Source: bzr-gtk
Binary: bzr-gtk
Architecture: source all
Version: 0.93.0-2
Distribution: unstable
Urgency: low
Maintainer: Debian Bazaar Maintainers <pkg-bazaar-maint@lists.alioth.debian.org>
Changed-By: Chris Lamb <chris@chris-lamb.co.uk>
Description:
 bzr-gtk    - provides graphical interfaces to Bazaar (bzr) version control
Closes: 440354 456438
Changes:
 bzr-gtk (0.93.0-2) unstable; urgency=low
 .
   [ Chris Lamb ]
   * Add patch for unclosed progress window. (Closes: #440354)
     Patch by Jean-François Fortin Tam <jeff@ecchi.ca>
   * Fix broken icons in .desktop files (Closes: #456438).
Files:
 0fd797f4138a9d4fdeb8c30597d46bc9 1003 python optional bzr-gtk_0.93.0-2.dsc
 d9523676ae75c4ced299689456f252f4 3860 python optional bzr-gtk_0.93.0-2.diff.gz
 8960459940314b21019dedd5519b47a5 168544 python optional bzr-gtk_0.93.0-2_all.deb
'''

CHECKSUM_CHANGES_FILE = '''\
Format: 1.8
Date: Wed, 30 Apr 2008 23:58:24 -0600
Source: python-debian
Binary: python-debian
Architecture: source all
Version: 0.1.10
Distribution: unstable
Urgency: low
Maintainer: Debian python-debian Maintainers <pkg-python-debian-maint@lists.alioth.debian.org>
Changed-By: John Wright <jsw@debian.org>
Description:
 python-debian - Python modules to work with Debian-related data formats
Closes: 473254 473259
Changes:
 python-debian (0.1.10) unstable; urgency=low
 .
   * debian_bundle/deb822.py, tests/test_deb822.py:
     - Do not cache _CaseInsensitiveString objects, since it causes case
       preservation issues under certain circumstances (Closes: #473254)
     - Add a test case
   * debian_bundle/deb822.py:
     - Add support for fixed-length subfields in multivalued fields.  I updated
       the Release and PdiffIndex classes to use this.  The default behavior for
       Release is that of apt-ftparchive, just because it's simpler.  Changing
       the behavior to resemble dak requires simply setting the
       size_field_behavior attribute to 'dak'.  (Ideally, deb822 would detect
       which behavior to use if given an actual Release file as input, but this
       is not implemented yet.)  (Closes: #473259)
     - Add support for Checksums-{Sha1,Sha256} multivalued fields in Dsc and
       Changes classes
   * debian/control:
     - "python" --> "Python" in the Description field
     - Change the section to "python"
Checksums-Sha1:
 d12d7c95563397ec37c0d877486367b409d849f5 1117 python-debian_0.1.10.dsc
 19efe23f688fb7f2b20f33d563146330064ab1fa 109573 python-debian_0.1.10.tar.gz
 22ff71048921a788ad9d90f9579c6667e6b3de3a 44260 python-debian_0.1.10_all.deb
Checksums-Sha256:
 aae63dfb18190558af8e71118813dd6a11157c6fd92fdc9b5c3ac370daefe5e1 1117 python-debian_0.1.10.dsc
 d297c07395ffa0c4a35932b58e9c2be541e8a91a83ce762d82a8474c4fc96139 109573 python-debian_0.1.10.tar.gz
 4c73727b6438d9ba60aeb5e314e2d8523f021da508405dc54317ad2b392834ee 44260 python-debian_0.1.10_all.deb
Files:
 469202dfd24d55a932af717c6377ee59 1117 python optional python-debian_0.1.10.dsc
 4857552b0156fdd4fa99d21ec131d3d2 109573 python optional python-debian_0.1.10.tar.gz
 81864d535c326c082de3763969c18be6 44260 python optional python-debian_0.1.10_all.deb
'''

class TestDeb822Dict(unittest.TestCase):
    def make_dict(self):
        d = deb822.Deb822Dict()
        d['TestKey'] = 1
        d['another_key'] = 2

        return d

    def test_case_insensitive_lookup(self):
        d = self.make_dict()

        self.assertEqual(1, d['testkey'])
        self.assertEqual(2, d['Another_keY'])

    def test_case_insensitive_assignment(self):
        d = self.make_dict()
        d['testkey'] = 3

        self.assertEqual(3, d['TestKey'])
        self.assertEqual(3, d['testkey'])

        d.setdefault('foo', 4)
        self.assertEqual(4, d['Foo'])

    def test_case_preserved(self):
        d = self.make_dict()

        self.assertEqual(sorted(['another_key', 'TestKey']), sorted(d.keys()))

    def test_order_preserved(self):
        d = self.make_dict()
        d['Third_key'] = 3
        d['another_Key'] = 2.5

        keys = ['TestKey', 'another_key', 'Third_key']

        self.assertEqual(keys, d.keys())
        self.assertEqual(keys, list(d.iterkeys()))
        self.assertEqual(zip(keys, d.values()), d.items())

        keys2 = []
        for key in d:
            keys2.append(key)

        self.assertEqual(keys, keys2)

    def test_derived_dict_equality(self):
        d1 = self.make_dict()
        d2 = dict(d1)

        self.assertEqual(d1, d2)


class TestDeb822(unittest.TestCase):
    def assertWellParsed(self, deb822_, dict_):
        """Check that the given Deb822 object has the very same keys and
           values as the given dict.
        """

        self.assertEqual(deb822_.keys(), dict_.keys())

        for k, v in dict_.items():
            self.assertEqual(v, deb822_[k])
        self.assertEqual(0, deb822_.__cmp__(dict_))

    def gen_random_string(length=20):
        from random import choice
        import string
        chars = string.letters + string.digits
        return ''.join([choice(chars) for i in range(length)])
    gen_random_string = staticmethod(gen_random_string)

    def deb822_from_format_string(self, string, dict_=PARSED_PACKAGE, cls=deb822.Deb822):
        """Construct a Deb822 object by formatting string with % dict.
        
        Returns the formatted string, and a dict object containing only the
        keys that were used for the formatting."""

        dict_subset = DictSubset(dict_)
        string = string % dict_subset
        parsed = cls(string.splitlines())
        return parsed, dict_subset

    def test_parser(self):
        deb822_ = deb822.Deb822(UNPARSED_PACKAGE.splitlines())
        self.assertWellParsed(deb822_, PARSED_PACKAGE)

    def test_parser_with_newlines(self):
        deb822_ = deb822.Deb822([ l+'\n' for l in UNPARSED_PACKAGE.splitlines()])
        self.assertWellParsed(deb822_, PARSED_PACKAGE)

    def test_strip_initial_blanklines(self):
        deb822_ = deb822.Deb822(['\n'] * 3 + UNPARSED_PACKAGE.splitlines())
        self.assertWellParsed(deb822_, PARSED_PACKAGE)

    def test_gpg_stripping(self):
        for string in GPG_SIGNED:
            unparsed_with_gpg = string % UNPARSED_PACKAGE
            deb822_ = deb822.Deb822(unparsed_with_gpg.splitlines())
            self.assertWellParsed(deb822_, PARSED_PACKAGE)

    def test_iter_paragraphs_array(self):
        text = (UNPARSED_PACKAGE + '\n\n\n' + UNPARSED_PACKAGE).splitlines()

        for d in deb822.Deb822.iter_paragraphs(text):
            self.assertWellParsed(d, PARSED_PACKAGE)

    def test_iter_paragraphs_file(self):
        text = StringIO(UNPARSED_PACKAGE + '\n\n\n' + UNPARSED_PACKAGE)

        for d in deb822.Deb822.iter_paragraphs(text):
            self.assertWellParsed(d, PARSED_PACKAGE)

    def test_iter_paragraphs_with_gpg(self):
        for string in GPG_SIGNED:
            string = string % UNPARSED_PACKAGE
            text = (string + '\n\n\n' + string).splitlines()

            for d in deb822.Deb822.iter_paragraphs(text):
                self.assertWellParsed(d, PARSED_PACKAGE)

    def test_parser_empty_input(self):
        self.assertEqual({}, deb822.Deb822([]))

    def test_iter_paragraphs_empty_input(self):
        generator = deb822.Deb822.iter_paragraphs([])
        self.assertRaises(StopIteration, generator.next)

    def test_parser_limit_fields(self):
        wanted_fields = [ 'Package', 'MD5sum', 'Filename', 'Description' ]
        deb822_ = deb822.Deb822(UNPARSED_PACKAGE.splitlines(), wanted_fields)

        self.assertEquals(sorted(wanted_fields), sorted(deb822_.keys()))

        for key in wanted_fields:
            self.assertEquals(PARSED_PACKAGE[key], deb822_[key])

    def test_iter_paragraphs_limit_fields(self):
        wanted_fields = [ 'Package', 'MD5sum', 'Filename', 'Tag' ]

        for deb822_ in deb822.Deb822.iter_paragraphs(
                UNPARSED_PACKAGE.splitlines(), wanted_fields):

            self.assertEquals(sorted(wanted_fields), sorted(deb822_.keys()))

            for key in wanted_fields:
                self.assertEquals(PARSED_PACKAGE[key], deb822_[key])

    def test_dont_assume_trailing_newline(self):
        deb822a = deb822.Deb822(['Package: foo'])
        deb822b = deb822.Deb822(['Package: foo\n'])

        self.assertEqual(deb822a['Package'], deb822b['Package'])

        deb822a = deb822.Deb822(['Description: foo\n', 'bar'])
        deb822b = deb822.Deb822(['Description: foo', 'bar\n'])

        self.assertEqual(deb822a['Description'], deb822b['Description'])

    def test__delitem__(self):
        parsed = deb822.Deb822(UNPARSED_PACKAGE.splitlines())
        dict_ = PARSED_PACKAGE.copy()

        for key in ('Package', 'MD5sum', 'Description'):
            del parsed[key]
            del dict_[key]

            parsed.keys() # ensure this does not raise error
            self.assertWellParsed(parsed, dict_)

    def test_policy_compliant_whitespace(self):
        string = (
            'Package: %(Package)s\n'
            'Version :%(Version)s \n'
            'Priority:%(Priority)s\t \n'
            'Section \t :%(Section)s \n'
            'Empty-Field:        \t\t\t\n'
            'Multiline-Field : a \n b\n c\n'
        ) % PARSED_PACKAGE

        deb822_ = deb822.Deb822(string.splitlines())
        dict_   = PARSED_PACKAGE.copy()

        dict_['Empty-Field'] = ''
        dict_['Multiline-Field'] = 'a\n b\n c' # XXX should be 'a\nb\nc'?

        for k, v in deb822_.items():
            self.assertEquals(dict_[k], v)
    
    def test_case_insensitive(self):
        # PARSED_PACKAGE is a deb822.Deb822Dict object, so we can test
        # it directly
        self.assertEqual(PARSED_PACKAGE['Architecture'],
                         PARSED_PACKAGE['architecture'])

        c_i_dict = deb822.Deb822Dict()

        test_string = self.gen_random_string()
        c_i_dict['Test-Key'] = test_string
        self.assertEqual(test_string, c_i_dict['test-key'])

        test_string_2 = self.gen_random_string()
        c_i_dict['TeSt-KeY'] = test_string_2
        self.assertEqual(test_string_2, c_i_dict['Test-Key'])

        deb822_ = deb822.Deb822(StringIO(UNPARSED_PACKAGE))
        # deb822_.keys() will return non-normalized keys
        for k in deb822_.keys():
            self.assertEqual(deb822_[k], deb822_[k.lower()])

    def test_multiline_trailing_whitespace_after_colon(self):
        """Trailing whitespace after the field name on multiline fields

        If the field's value starts with a newline (e.g. on MD5Sum fields in
        Release files, or Files field in .dsc's, the dumped string should not
        have a trailing space after the colon.  If the value does not start
        with a newline (e.g. the control file Description field), then there
        should be a space after the colon, as with non-multiline fields.
        """
        
        # bad_re: match a line that starts with a "Field:", and ends in
        # whitespace
        bad_re = re.compile(r"^\S+:\s+$")
        for cls in deb822.Deb822, deb822.Changes:
            parsed = cls(CHANGES_FILE.splitlines())
            for line in parsed.dump().splitlines():
                self.assert_(bad_re.match(line) is None,
                            "There should not be trailing whitespace after the "
                            "colon in a multiline field starting with a newline")

        
        control_paragraph = """Package: python-debian
Architecture: all
Depends: ${python:Depends}
Suggests: python-apt
Provides: python-deb822
Conflicts: python-deb822
Replaces: python-deb822
Description: python modules to work with Debian-related data formats
 This package provides python modules that abstract many formats of Debian
 related files. Currently handled are:
  * Debtags information (debian_bundle.debtags module)
  * debian/changelog (debian_bundle.changelog module)
  * Packages files, pdiffs (debian_bundle.debian_support module)
  * Control files of single or multple RFC822-style paragraphs, e.g
    debian/control, .changes, .dsc, Packages, Sources, Release, etc.
    (debian_bundle.deb822 module)
"""
        parsed_control = deb822.Deb822(control_paragraph.splitlines())
        field_re = re.compile(r"^\S+:")
        field_with_space_re = re.compile(r"^\S+: ")
        for line in parsed_control.dump().splitlines():
            if field_re.match(line):
                self.assert_(field_with_space_re.match(line),
                             "Multiline fields that do not start with newline "
                             "should have a space between the colon and the "
                             "beginning of the value")

    def test_blank_value(self):
        """Fields with blank values are parsable--so they should be dumpable"""

        d = deb822.Deb822()
        d['Foo'] = 'bar'
        d['Baz'] = ''
        d['Another-Key'] = 'another value'
        
        # Previous versions would raise an exception here -- this makes the
        # test fail and gives useful information, so I won't try to wrap around
        # it.
        dumped = d.dump()
        
        # May as well make sure the resulting string is what we want
        expected = "Foo: bar\nBaz:\nAnother-Key: another value\n"
        self.assertEqual(dumped, expected)

    def test_copy(self):
        """The copy method of Deb822 should return another Deb822 object"""
        d = deb822.Deb822()
        d['Foo'] = 'bar'
        d['Bar'] = 'baz'
        d_copy = d.copy()

        self.assert_(isinstance(d_copy, deb822.Deb822))
        expected_dump = "Foo: bar\nBar: baz\n"
        self.assertEqual(d_copy.dump(), expected_dump)

    def test_bug457929_multivalued_dump_works(self):
        """dump() was not working in multivalued classes, see #457929."""
        changesobj = deb822.Changes(CHANGES_FILE.splitlines())
        self.assertEqual(CHANGES_FILE, changesobj.dump())

    def test_bug487902_multivalued_checksums(self):
        """New multivalued field Checksums was not handled correctly, see #487902."""
        changesobj = deb822.Changes(CHECKSUM_CHANGES_FILE.splitlines())
        self.assertEqual(CHECKSUM_CHANGES_FILE, changesobj.dump())

    def test_case_preserved_in_input(self):
        """The field case in the output from dump() should be the same as the
        input, even if multiple Deb822 objects have been created using
        different case conventions.

        This is related to bug 473254 - the fix for this issue is probably the
        same as the fix for that bug.
        """
        input1 = "Foo: bar\nBaz: bang\n"
        input2 = "foo: baz\nQux: thud\n"
        d1 = deb822.Deb822(input1.splitlines())
        d2 = deb822.Deb822(input2.splitlines())
        self.assertEqual(input1, d1.dump())
        self.assertEqual(input2, d2.dump())

        d3 = deb822.Deb822()
        if not d3.has_key('some-test-key'):
            d3['Some-Test-Key'] = 'some value'
        self.assertEqual(d3.dump(), "Some-Test-Key: some value\n")

if __name__ == '__main__':
    unittest.main()
