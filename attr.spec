%define	major	1
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname -d %{name}

%bcond_without	uclibc

Summary:	Utility for managing filesystem extended attributes
Name:		attr
Version:	2.4.46
Release:	6
License:	GPLv2
Group:		System/Kernel and hardware
Url:		http://savannah.nongnu.org/projects/attr
Source0:	http://mirrors.aixtools.net/sv/%{name}/%{name}-%{version}.src.tar.gz
Source1:	http://mirrors.aixtools.net/sv/%{name}/%{name}-%{version}.src.tar.gz.sig
Patch0:		attr-aarch64.patch
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
Provides:	%{name}-devel = %{EVRD}
%rename		%{_lib}attr1-devel

%description -n	%{devname}
This package contains the libraries and header files needed to
develop programs which make use of extended attributes.
For Linux programs, the documented system call API is the
recommended interface, but an SGI IRIX compatibility interface
is also provided.

%prep
%setup -q
%patch0 -p1
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
%configure2_5x \
	OPTIMIZER="%{optflags} -Os" \
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
/%{_lib}/libattr.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%{uclibc_root}/%{_lib}/libattr.so.%{major}*
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

