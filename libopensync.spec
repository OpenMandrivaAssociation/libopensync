Name: libopensync
Version: 0.35
Release: %mkrel 1
Summary: Multi-platform PIM synchronization framework
Source: http://www.opensync.org/download/releases/%version/%name-%version.tar.bz2
Patch1: libopensync-0.35-fix-python-wrapper-build.patch
URL: http://www.opensync.org/
License: LGPLv2.1+
Group: System/Libraries
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: bison 
BuildRequires: libxml2-devel 
BuildRequires: chrpath
BuildRequires: glib2-devel
BuildRequires: sqlite3-devel
BuildRequires: pkgconfig
BuildRequires: swig
BuildRequires: cmake
Obsoletes: %mklibname opensync 0

%description
OpenSync is a synchronization framework that is platform and distribution
independent.  It consists of several plugins that can be used to connect to
devices, a powerful sync-engine and the framework itself.  The synchronization
framework is kept very flexible and is capable of synchronizing any type of
data, including contacts, calendar, tasks, notes and files.

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/opensync-1.0
%dir %{_prefix}/lib/opensync-1.0
%{_prefix}/lib/opensync-1.0/osplugin

#-------------------------------------------------------------

%define major 1
%define libname %mklibname opensync %major

%package -n %{libname}
Summary: Dynamic libraries from %name
Group: System/Libraries
Obsoletes: %mklibname opensync 1.0.0
Requires: %name = %version-%release

%description -n %{libname}
Dynamic libraries from %name.

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%dir %{_libdir}/opensync-1.0
%{_libdir}/opensync-1.0/formats
%{_libdir}/libopensync.so.%{major}*

#-------------------------------------------------------------

%define develname %mklibname -d opensync

%package -n %{develname}
Summary: Header files and static libraries from %name
Group: Development/C
Requires: %{libname} = %{version}-%{release}
Provides: opensync-devel = %{version}-%{release}
Obsoletes: %mklibname -d opensync 0
Provides: libopensync-devel = %version-%{release}

%description -n %{develname}
Libraries and includes files for developing programs based on %name.

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/opensync-1.0
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

#-------------------------------------------------------------

%package python 
Summary: Python bindings for %name 
Group: Development/Python 
Provides: opensync-python = %version-%release
%py_requires -d
 
%description python 
Python bindings for %name 
 
%files python 
%defattr(-,root,root) 
%{py_platsitedir}/*

#-------------------------------------------------------------

%prep
%setup -q
%patch1 -p0 -b .orig

%build
%cmake
%make

%install
rm -rf $RPM_BUILD_ROOT
cd build
%makeinstall_std

%clean
rm -rf $RPM_BUILD_ROOT
