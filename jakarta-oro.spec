# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define _gcj_support 1

%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

%define base_name oro

%define section free

Name:           jakarta-oro
Version:        2.0.8
Release:        6.6%{?dist}
Epoch:          0
Summary:        Full regular expressions API
License:        ASL 1.1
Group:          Development/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1:        MANIFEST.MF
Patch1:         %{name}-build-xml.patch
URL:            http://jakarta.apache.org/oro
BuildRequires:  jpackage-utils > 1.6
BuildRequires:  ant
%if ! %{gcj_support}
Buildarch:      noarch
%endif
Buildroot:      %{_tmppath}/%{name}-%{version}-buildroot
Provides:       oro = %{epoch}:%{version}-%{release}
Obsoletes:      oro <= 0:2.0.8


%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
%endif

%description
The Jakarta-ORO Java classes are a set of text-processing Java classes
that provide Perl5 compatible regular expressions, AWK-like regular
expressions, glob expressions, and utility classes for performing
substitutions, splits, filtering filenames, etc. This library is the
successor to the OROMatcher, AwkTools, PerlTools, and TextTools
libraries from ORO, Inc. (www.oroinc.com). They have been donated to the
Jakarta Project by Daniel Savarese (www.savarese.org), the copyright
holder of the ORO libraries. Daniel will continue to participate in
their development under the Jakarta Project.

%package javadoc
Group:          Development/Libraries
Summary:        Javadoc for %{name}
Provides:       oro-javadoc = %{epoch}:%{version}-%{release}
Obsoletes:      oro-javadoc <= 0:2.0.8
#BuildRequires:  java-javadoc
# for /bin/rm and /bin/ln
Requires(post):  coreutils
Requires(postun): coreutils

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}-%{version}
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
# remove all CVS files
for dir in `find . -type d -name CVS`; do rm -rf $dir; done
for file in `find . -type f -name .cvsignore`; do rm -rf $file; done

%patch1
cp %{SOURCE1} .

%build
ant -Dfinal.name=%{base_name} jar javadocs

%install
rm -rf $RPM_BUILD_ROOT
#jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 %{base_name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && ln -sf %{name}-%{version}.jar %{base_name}-%{version}.jar)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
#javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink
rm -rf docs/api

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif


%files
%defattr(-,root,root)
%doc COMPILE ISSUES README TODO CHANGES CONTRIBUTORS LICENSE STYLE
%{_javadir}/*.jar

%if %{gcj_support}
%dir %attr(-,root,root) %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/jakarta-oro-2.0.8.jar.*
%endif

%files javadoc
%defattr(-,root,root)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%changelog
* Tue Feb 02 2010 Jeff Johnston <jjohnstn@redhat.com> - 0:2.0.8-6.6
- Resolves: #561148
- Remove post and postun steps for javadoc subpackage

* Fri Jan 08 2010 Jeff Johnston <jjohnstn@redhat.com> - 0:2.0.8-6.5
- Resolves: #553813
- Fix rpmlint warnings.

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0:2.0.8-6.4
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.0.8-6.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 23 2009 Jeff Johnston <jjohnstn@redhat.com> - 0:2.0.8-5.3
- Add OSGi metadata to Manifest.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.0.8-5.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:2.0.8-4.2
- drop repotag
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:2.0.8-4jpp.1
- Autorebuild for GCC 4.3

* Mon Aug 21 2006 Fernando Nasser <fnasser.redhat.com> 2.0.8-3jpp.1
- Merge with upstream

* Mon Aug 21 2006 Fernando Nasser <fnasser.redhat.com> 2.0.8-3jpp
- Add AOT bits
- Fix javadoc unversioned link handling
- Add requires for post/postun javadoc sections added above

* Tue Aug 24 2004 Fernando Nasser <fnasser.redhat.com> 2.0.8-2jpp
- Rebuild with Ant 1.6.2
- Changed name to jakarta-oro
- Add backward compatibility to 'oro' bits

* Fri Jan 02 2004 Henri Gomez <hgomez@users.sourceforge.net> 2.0.8-1jpp
- oro 2.0.8

* Tue Mar 25 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org> 2.0.7-1jpp
- oro 2.0.7
- for jpackage-utils 1.5

* Wed Jul 10 2002 Henri Gomez <hgomez@users.sourceforge.net> 2.0.6-1jpp
- oro 2.0.6

* Tue Jul 02 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.0.4-7jpp
- section macro
- use sed instead of bash 2.x extension in link area to make spec compatible with distro using bash 1.1x

* Fri Jan 18 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.0.4-6jpp 
- versioned dir for javadoc
- no dependencies javadoc package

* Sat Dec 1 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.0.4-5jpp
- javadoc in javadoc package
- official summary

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 2.0.4-4jpp
- removed packager tag
- new jpp extension

* Sun Sep 30 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.0.4-3jpp
- more macros

* Wed Sep 26 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.0.4-2jpp
- first unified release
- s/jPackage/JPackage

* Sun Aug 26 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.0.4-1mdk
- 2.0.4
- vendor tag
- packager tag
- s/Copyright/License/
- truncated description to 72 columns in spec
- spec cleanup
- used versioned jar
- used new source packaging policy

* Sat Feb 17 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 2.0.1-3mdk
- spec cleanup
- changelog correction

* Sun Feb 04 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 2.0.1-2mdk
- merged with Henri Gomez <hgomez@users.sourceforge.net> specs:
- changed name to oro
-  changed javadir to /usr/share/java
-  dropped jdk & jre requirement
-  added Jikes support
- changed jar name to oro.jar
- corrected doc
- more macros

* Sun Jan 14 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 2.0.1-1mdk
- first Mandrake release
