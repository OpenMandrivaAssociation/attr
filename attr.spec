%define major 1
%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name}

Summary:	Utility for managing filesystem extended attributes
Name:		attr
Version:	2.4.47
Release:	8
License:	GPLv2
Group:		System/Kernel and hardware
Url:		http://savannah.nongnu.org/projects/attr
Source0:	http://mirrors.aixtools.net/sv/%{name}/%{name}-%{version}.src.tar.gz
Source1:	%{name}.rpmlintrc
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
%setup -q
chmod +rw -R .

%build
%configure \
	OPTIMIZER="%{optflags}" \
	--disable-static \
	--libdir=/%{_lib}

%make

%install
make install DIST_ROOT=%{buildroot}
make install-dev DIST_ROOT=%{buildroot}
make install-lib DIST_ROOT=%{buildroot}

# fix conflict with man-pages-1.56
rm -rf %{buildroot}{%{_mandir}/man2,%{_datadir}/doc}

# Remove unpackaged symlinks
# TODO: finish up spec-helper script ot automatically deal with
rm -f %{buildroot}/%{_lib}/libattr.{a,la,so}
mkdir -p %{buildroot}%{_libdir}
ln -sf /%{_lib}/libattr.so.%{major}.* %{buildroot}%{_libdir}/libattr.so
chmod +x %{buildroot}/%{_lib}/libattr.so.%{major}.*

%find_lang %{name}

%files -f %{name}.lang
%{_bindir}/*
%{_mandir}/man1/*

%files -n %{libname}
/%{_lib}/libattr.so.%{major}*

%files -n %{devname}
%doc .system/doc/CHANGES.gz README
%{_libdir}/libattr.so
%{_mandir}/man3/*
%{_mandir}/man5/*
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
