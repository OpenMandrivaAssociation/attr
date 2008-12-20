%define	name	attr
%define	version	2.4.43
%define minor_version 1
%define	release	%mkrel 2

%define	lib_name_orig	lib%{name}
%define	lib_major	1
%define	lib_name 	%mklibname %{name} %{lib_major}

Summary:	Utility for managing filesystem extended attributes
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	ftp://oss.sgi.com/projects/xfs/download/cmd_tars/%{name}_%{version}-%{minor_version}.tar.gz
License:	GPLv2
Group:		System/Kernel and hardware
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	libtool
URL:		http://oss.sgi.com/projects/xfs/

%description
A set of tools for manipulating extended attributes on filesystem
objects, in particular getfattr(1) and setfattr(1).
An attr(1) command is also provided which is largely compatible
with the SGI IRIX tool of the same name.

%package -n	%{lib_name}
Summary:	Main library for %{lib_name_orig}
Group:		System/Libraries
Provides:	%{lib_name_orig} = %{version}-%{release}

%description -n	%{lib_name}
This package contains the library needed to run programs dynamically
linked with %{lib_name_orig}.

%package -n	%{lib_name}-devel
Summary:	Extended attribute static libraries and headers
Group:		Development/C
Requires:	%{lib_name} = %{version}
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Provides:	attr-devel = %{version}-%{release}
Obsoletes:	attr-devel

%description -n	%{lib_name}-devel
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
aclocal && autoconf
%configure2_5x --libdir=/%{_lib}
%make

%install
rm -rf $RPM_BUILD_ROOT
make install DIST_ROOT=%{buildroot}/
make install-dev DIST_ROOT=%{buildroot}/
make install-lib DIST_ROOT=%{buildroot}/
# fix conflict with man-pages-1.56
rm -fr $RPM_BUILD_ROOT{%_mandir/man2,%_datadir/doc}

# Remove unpackaged symlinks
rm -fr $RPM_BUILD_ROOT/%{_lib}/libattr.{a,la} \
 $RPM_BUILD_ROOT/%{_libdir}/libattr.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc doc/CHANGES.gz README 
%{_bindir}/*
%{_mandir}/man1/*

%files -n %{lib_name}
%defattr(-,root,root)
%doc doc/COPYING
/%{_lib}/*.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root)
%doc doc/CHANGES.gz doc/COPYING README
/%{_lib}/*.so
%{_libdir}/*.so
%{_libdir}/*a
%{_mandir}/man3/*
%{_mandir}/man5/*
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*


