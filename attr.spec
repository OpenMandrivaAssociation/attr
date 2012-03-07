%define	lib_name_orig	lib%{name}
%define	major	1
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname -d %{name}

Summary:	Utility for managing filesystem extended attributes
Name:		attr
Version:	2.4.46
Release:	2
URL:		http://savannah.nongnu.org/projects/attr
Source0:	http://mirrors.aixtools.net/sv/%{name}/%{name}-%{version}.src.tar.gz
Source1:	http://mirrors.aixtools.net/sv/%{name}/%{name}-%{version}.src.tar.gz.sig
License:	GPLv2
Group:		System/Kernel and hardware

%description
A set of tools for manipulating extended attributes on filesystem
objects, in particular getfattr(1) and setfattr(1).
An attr(1) command is also provided which is largely compatible
with the SGI IRIX tool of the same name.

%package -n	%{libname}
Summary:	Main library for %{lib_name_orig}
Group:		System/Libraries
Provides:	%{lib_name_orig} = %{version}-%{release}

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with %{lib_name_orig}.

%package -n	%{devname}
Summary:	Extended attribute static libraries and headers
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Provides:	attr-devel = %{version}-%{release}
Obsoletes:	attr-devel

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

%build
%configure2_5x --libdir=/%{_lib}
%make

%install
make install DIST_ROOT=%{buildroot}/
make install-dev DIST_ROOT=%{buildroot}/
make install-lib DIST_ROOT=%{buildroot}/
# fix conflict with man-pages-1.56
rm -rf %{buildroot}{%_mandir/man2,%_datadir/doc}

# Remove unpackaged symlinks
rm -rf %{buildroot}/%{_lib}/libattr.{a,la} %{buildroot}/%{_libdir}/libattr.la

%find_lang %{name}


%files -f %{name}.lang
%doc doc/CHANGES.gz README 
%{_bindir}/*
%{_mandir}/man1/*

%files -n %{libname}
%doc doc/COPYING
/%{_lib}/libattr.so.%{major}*

%files -n %{devname}
%doc doc/CHANGES.gz doc/COPYING README
/%{_lib}/*.so
%{_libdir}/*.so
%{_libdir}/*a
%{_mandir}/man3/*
%{_mandir}/man5/*
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*


