%define	major	1
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname -d %{name}

%bcond_without	uclibc

Summary:	Utility for managing filesystem extended attributes
Name:		attr
Version:	2.4.46
Release:	3
URL:		http://savannah.nongnu.org/projects/attr
Source0:	http://mirrors.aixtools.net/sv/%{name}/%{name}-%{version}.src.tar.gz
Source1:	http://mirrors.aixtools.net/sv/%{name}/%{name}-%{version}.src.tar.gz.sig
License:	GPLv2
Group:		System/Kernel and hardware
%if %{with uclibc}
BuildRequires:	uClibc-devel >= 0.9.33.2-9
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
%configure2_5x	CC=%{uclibc_cc} \
		OPTIMIZER="%{uclibc_cflags}" \
		--libdir=%{uclibc_root}/%{_lib} \
		--enable-gettext
# gettext isn't provided by uClibc, se we need to explicitly link against
# libintl
%make LTLIBS=-lintl
popd
%endif

pushd .system
%configure2_5x	OPTIMIZER="%{optflags} -Os" \
		--libdir=/%{_lib}
%make
popd

%install
%if %{with uclibc}
make -C .uclibc install-lib DIST_ROOT=%{buildroot}
%endif

make -C .system install DIST_ROOT=%{buildroot}/
make -C .system install-dev DIST_ROOT=%{buildroot}/
make -C .system install-lib DIST_ROOT=%{buildroot}/

# fix conflict with man-pages-1.56
rm -rf %{buildroot}{%{_mandir}/man2,%{_datadir}/doc}

# Remove unpackaged symlinks
# TOdO: finish up spec-helper script ot automatically deal with
rm -rf %{buildroot}/%{_lib}/libattr.{a,la,so}
ln -srf %{buildroot}/%{_lib}/libattr.so.%{major}.* %{buildroot}%{_libdir}/libattr.so
%if %{with uclibc}
install -d %{buildroot}%{uclibc_root}%{_libdir}
ln -srf %{buildroot}/%{uclibc_root}%{_lib}/libattr.so.%{major}.* %{buildroot}%{uclibc_root}%{_libdir}/libattr.so
%endif

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
%{_libdir}/libattr.a
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libattr.so
%endif
%{_mandir}/man3/*
%{_mandir}/man5/*
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
