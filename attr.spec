%define major 1
%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name}
# https://bugs.gentoo.org/644048
%global ldflags %(echo %{ldflags} -fuse-ld=bfd |sed -e 's,-flto,,g')
%global optflags %(echo %{optflags} -fuse-ld=bfd |sed -e 's,-flto,,g')

Summary:	Utility for managing filesystem extended attributes
Name:		attr
Version:	2.4.48
Release:	3
License:	GPLv2
Group:		System/Kernel and hardware
Url:		http://savannah.nongnu.org/projects/attr
Source0:	http://download.savannah.nongnu.org/releases/%{name}/%{name}-%{version}.tar.gz
Source1:	%{name}.rpmlintrc
Source2:	attr.check
Patch0:		attr-2.4.48-test-perl-5.26.patch
BuildRequires:	gettext-devel

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

%package -n	%{devname}
Summary:	Extended attribute static libraries and headers
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
%rename		%{_lib}attr1-devel

%description -n	%{devname}
This package contains the libraries and header files needed to
develop programs which make use of extended attributes.
For Linux programs, the documented system call API is the
recommended interface, but an SGI IRIX compatibility interface
is also provided.

%prep
%autosetup -p1
chmod +rw -R .

%build
%configure \
	--libdir=/%{_lib}

%make

%install
%make_install DESTDIR=%{buildroot}

# fix conflict with man-pages-1.56
rm -rf %{buildroot}{%{_mandir}/man2,%{_datadir}/doc}

# Remove unpackaged symlinks
# TODO: finish up spec-helper script to automatically deal with
rm -f %{buildroot}/%{_lib}/libattr.{a,la,so}
mkdir -p %{buildroot}%{_libdir}
cd %{buildroot}%{_libdir}
ln -sf ../../%{_lib}/libattr.so.%{major}.* libattr.so
cd -
mv %{buildroot}/%{_lib}/pkgconfig %{buildroot}%{_libdir}
chmod +x %{buildroot}/%{_lib}/libattr.so.%{major}.*

%find_lang %{name}

%check
bash %{SOURCE2} %{buildroot}/%{_lib}/libattr.so.%{major}
make check

%files -f %{name}.lang
%config %{_sysconfdir}/xattr.conf
%{_bindir}/*
%{_mandir}/man1/*

%files -n %{libname}
/%{_lib}/libattr.so.%{major}*

%files -n %{devname}
%doc README
%{_libdir}/libattr.so
%{_mandir}/man3/*
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/pkgconfig/*.pc
