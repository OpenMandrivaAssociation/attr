%define	major	1
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname -d %{name}

%bcond_without	uclibc

Summary:	Utility for managing filesystem extended attributes
Name:		attr
Version:	2.4.46
Release:	5
URL:		http://savannah.nongnu.org/projects/attr
Source0:	http://mirrors.aixtools.net/sv/%{name}/%{name}-%{version}.src.tar.gz
Source1:	http://mirrors.aixtools.net/sv/%{name}/%{name}-%{version}.src.tar.gz.sig
License:	GPLv2
Group:		System/Kernel and hardware
BuildRequires:	gettext-devel
%if %{with uclibc}
BuildRequires:	uClibc-devel >= 0.9.33.2-16
%endif

%description
A set of tools for manipulating extended attributes on filesystem
objects, in particular getfattr(1) and setfattr(1).
An attr(1) command is also provided which is largely compatible
with the SGI IRIX tool of the same name.

%package -n	%{libname}
Summary:	Main library for libattr
Group:		System/Libraries

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with libattr.

%package -n	uclibc-%{libname}
Summary:	Main library for libattr (uClibc linked)
Group:		System/Libraries

%description -n	uclibc-%{libname}
This package contains the library needed to run programs dynamically
linked with libattr.

%package -n	%{devname}
Summary:	Extended attribute static libraries and headers
Group:		Development/C
Requires:	%{libname} = %{EVRD}
%if %{with uclibc}
Requires:	uclibc-%{libname} = %{EVRD}
%endif
Provides:	attr-devel = %{EVRD}
%rename		%{_lib}attr1-devel

%description -n	%{devname}
This package contains the libraries and header files needed to
develop programs which make use of extended attributes.
For Linux programs, the documented system call API is the
recommended interface, but an SGI IRIX compatibility interface
is also provided.

Currently only ext2, ext3, JFS and XFS support extended attributes.
The SGI IRIX compatibility API built above the Linux system calls is
used by programs such as xfsdump(8), xfsrestore(8) and xfs_fsr(8).

You should install libattr-devel if you want to develop programs
which make use of extended attributes.  If you install libattr-devel
then you'll also want to install attr.

%prep
%setup -q
chmod +rw -R .

%if %{with uclibc}
mkdir .uclibc
pushd .uclibc
cp -a ../* .
popd
%endif

mkdir .system
pushd .system
cp -a ../* .
popd

%build
%if %{with uclibc}
pushd .uclibc
%uclibc_configure \
		OPTIMIZER="%{uclibc_cflags}" \
		--prefix=%{uclibc_root} \
		--exec-prefix=%{uclibc_root} \
		--libdir=%{uclibc_root}/%{_lib} \
		--enable-static \
		--enable-shared \
		--enable-gettext \
		--with-sysroot=%{uclibc_root}
sed -i -e 's,^LOADERFLAGS =,LOADERFLAGS = -lintl,' include/builddefs
%make
popd
%endif

pushd .system
%configure2_5x	OPTIMIZER="%{optflags} -Os" \
		--disable-static \
		--libdir=/%{_lib}
%make
popd

%install
%if %{with uclibc}
make -C .uclibc install-lib DIST_ROOT=%{buildroot}
make -C .uclibc install-dev DIST_ROOT=%{buildroot}
install -d %{buildroot}%{uclibc_root}%{_libdir}
rm %{buildroot}%{uclibc_root}/%{_lib}/libattr.{a,la,so}
rm -r %{buildroot}%{uclibc_root}%{_bindir}
ln -sr %{buildroot}%{uclibc_root}/%{_lib}/libattr.so.%{major}.* %{buildroot}%{uclibc_root}%{_libdir}/libattr.so
chmod +x %{buildroot}%{uclibc_root}/%{_lib}/libattr.so.%{major}.*
mv %{buildroot}%{_libdir}/libattr.a %{buildroot}%{uclibc_root}%{_libdir}/libattr.a
%endif

make -C .system install DIST_ROOT=%{buildroot}
make -C .system install-dev DIST_ROOT=%{buildroot}
make -C .system install-lib DIST_ROOT=%{buildroot}

# fix conflict with man-pages-1.56
rm -rf %{buildroot}{%{_mandir}/man2,%{_datadir}/doc}

# Remove unpackaged symlinks
# TOdO: finish up spec-helper script ot automatically deal with
rm %{buildroot}/%{_lib}/libattr.{a,la,so} %{buildroot}%{_libdir}/libattr.so
ln -srf %{buildroot}/%{_lib}/libattr.so.%{major}.* %{buildroot}%{_libdir}/libattr.so
chmod +x %{buildroot}/%{_lib}/libattr.so.%{major}.*

%find_lang %{name}

%files -f %{name}.lang
%doc README 
%{_bindir}/*
%{_mandir}/man1/*

%files -n %{libname}
%attr(755,root,root) /%{_lib}/libattr.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%attr(755,root,root) %{uclibc_root}/%{_lib}/libattr.so.%{major}*
%endif

%files -n %{devname}
%doc .system/doc/CHANGES.gz README
%{_libdir}/libattr.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libattr.a
%{uclibc_root}%{_libdir}/libattr.so
%endif
%{_mandir}/man3/*
%{_mandir}/man5/*
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*

%changelog
* Wed Dec 12 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.4.46-4
- rebuild on ABF

* Sun Oct 28 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.4.46-3
+ Revision: 820179
- use %%uclibc_configure macro
- hm, build broke, dunno why, let's just try revert %%uclibc_configure usage first
- make libraries executable
- use %%uclibc_configure from latest uclibc
- just workaround library mess for now..
- %rename %%{_lib}attr1-devel
- fix broken library symlinks
- compile system library with -Os as well
- do uClibc build of library

* Wed Mar 07 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.4.46-2
+ Revision: 782688
- only package one libattr.so symlink (/usr/lib64/libattr.so)
- fix shared-lib-not-executable
- fix non-readable
- ship 'CHANGES.gz' in -devel package only
- don't ship 'COPYING'
- use %%{EVRD} macro
- drop ancient obsoletes
- drop excessive provides
- cleanups

* Thu May 12 2011 Oden Eriksson <oeriksson@mandriva.com> 2.4.46-1mdv2011.0
+ Revision: 673745
- 2.4.46

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 2.4.44-3
+ Revision: 662887
- mass rebuild

* Tue Nov 30 2010 Oden Eriksson <oeriksson@mandriva.com> 2.4.44-2mdv2011.0
+ Revision: 603477
- rebuild

* Sun Dec 27 2009 Frederik Himpe <fhimpe@mandriva.org> 2.4.44-1mdv2010.1
+ Revision: 482852
- Update to new version 2.4.44
- New URL
- Don't run autoconf and friends, drop libtool BuildRequires

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 2.4.43-3mdv2010.0
+ Revision: 413121
- rebuild

* Sat Dec 20 2008 Oden Eriksson <oeriksson@mandriva.com> 2.4.43-2mdv2009.1
+ Revision: 316460
- rebuild

* Tue Aug 05 2008 Frederik Himpe <fhimpe@mandriva.org> 2.4.43-1mdv2009.0
+ Revision: 264074
- New version 2.4.43

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 2.4.41-2mdv2009.0
+ Revision: 220467
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon Feb 11 2008 Frederik Himpe <fhimpe@mandriva.org> 2.4.41-1mdv2008.1
+ Revision: 165416
- New upstream release

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Nov 19 2007 JÃ©rÃ´me Soyer <saispo@mandriva.org> 2.4.39-1mdv2008.1
+ Revision: 110198
- New release 2.4.39

* Tue Sep 18 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.4.38-4mdv2008.0
+ Revision: 89578
- rebuild

* Thu Jun 07 2007 Anssi Hannula <anssi@mandriva.org> 2.4.38-3mdv2008.0
+ Revision: 36139
- rebuild with correct optflags

  + Christiaan Welvaart <spturtle@mandriva.org>
    - 2.4.38


* Sat Mar 03 2007 Giuseppe GhibÃ² <ghibo@mandriva.com> 2.4.32-2mdv2007.0
+ Revision: 131826
- Rebuilt.

* Tue Oct 31 2006 Oden Eriksson <oeriksson@mandriva.com> 2.4.32-1mdv2007.1
+ Revision: 74654
- Import attr

* Sun Jul 09 2006 Giuseppe Ghibò <ghibo@mandriva.com> 2.4.32-1mdv2007.0
- 2.4.32.

* Fri May 05 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.4.28-1mdk
- 2.4.28

* Wed Jan 11 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 2.4.23-2mdk
- add BuildRequires: libtool

* Wed Aug 03 2005 Giuseppe Ghibò <ghibo@mandriva.com> 2.4.23-1mdk
- 2.4.23.

* Mon May 09 2005 Frederic Crozat <fcrozat@mandriva.com> 2.4.16-2mdk 
- Don't package .la file, libtool doesn't handle well .a and .so.* in
  separates directories

* Mon May 24 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.4.16-1mdk
- 2.4.16.

* Fri Apr 30 2004 Juan Quintela <quintela@mandrakesoft.com> 2.4.15-1mdk
- 2.4.15.

