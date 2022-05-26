# attr is used by libcap, libcap is used by systemd,
# libsystemd is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

%define major 1
%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name}
%define lib32name lib%{name}%{major}
%define dev32name lib%{name}-devel

Summary:	Utility for managing filesystem extended attributes
Name:		attr
Version:	2.5.1
Release:	3
License:	GPLv2
Group:		System/Kernel and hardware
Url:		http://savannah.nongnu.org/projects/attr
Source0:	http://download.savannah.nongnu.org/releases/%{name}/%{name}-%{version}.tar.xz
Source1:	%{name}.rpmlintrc
Source2:	attr.check
# (tpg) https://bugs.gentoo.org/644048#c38
Patch0:		attr-2.4.48-use-asm-symver.patch
BuildRequires:	gettext-devel

%description
A set of tools for manipulating extended attributes on filesystem
objects, in particular getfattr(1) and setfattr(1).
An attr(1) command is also provided which is largely compatible
with the SGI IRIX tool of the same name.

%package -n %{libname}
Summary:	Main library for libattr
Group:		System/Libraries

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with libattr.

%package -n %{devname}
Summary:	Extended attribute static libraries and headers
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
%rename		%{_lib}attr1-devel

%description -n %{devname}
This package contains the libraries and header files needed to
develop programs which make use of extended attributes.
For Linux programs, the documented system call API is the
recommended interface, but an SGI IRIX compatibility interface
is also provided.

%if %{with compat32}
%package -n %{lib32name}
Summary:	Main library for libattr (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
This package contains the library needed to run programs dynamically
linked with libattr.

%package -n %{dev32name}
Summary:	Extended attribute static libraries and headers (32-bit)
Group:		Development/C
Requires:	%{lib32name} = %{EVRD}
Requires:	%{devname} = %{EVRD}

%description -n %{dev32name}
This package contains the libraries and header files needed to
develop programs which make use of extended attributes.
For Linux programs, the documented system call API is the
recommended interface, but an SGI IRIX compatibility interface
is also provided.
%endif

%prep
%autosetup -p1
chmod +rw -R .

autoreconf -fiv

export CONFIGURE_TOP="$(pwd)"
%if %{with compat32}
mkdir build32
cd build32
%configure32
cd ..
%endif

mkdir build
cd build
%configure
cd ..

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

%install
%if %{with compat32}
%make_install -C build32 DESTDIR=%{buildroot}
%endif
%make_install -C build DESTDIR=%{buildroot}

# fix conflict with man-pages-1.56
rm -rf %{buildroot}{%{_mandir}/man2,%{_datadir}/doc}

# Remove unpackaged symlinks
# TODO: finish up spec-helper script to automatically deal with
rm -f %{buildroot}/%{_libdir}/libattr.{a,la}
chmod +x %{buildroot}/%{_libdir}/libattr.so.%{major}.*

%find_lang %{name}

%check
/bin/sh %{SOURCE2} %{buildroot}/%{_libdir}/libattr.so.%{major}

if ./setfattr -n user.name -v value .; then
    make check || exit $?
else
    printf '%s\n' '*** xattrs are probably not supported by the file system, the test-suite will NOT run ***'
fi

%files -f %{name}.lang
%config %{_sysconfdir}/xattr.conf
%{_bindir}/*
%doc %{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/libattr.so.%{major}*

%files -n %{devname}
%doc README
%{_libdir}/libattr.so
%doc %{_mandir}/man3/*
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/pkgconfig/*.pc

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libattr.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/libattr.so
%{_prefix}/lib/pkgconfig/*.pc
%endif
