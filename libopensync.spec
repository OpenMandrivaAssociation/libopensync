Name: libopensync
Version: 0.33
Release: %mkrel 1
Summary: Multi-platform PIM synchronization framework
Source: http://www.opensync.org/download/releases/%version/%name-%version.tar.bz2
URL: http://www.opensync.org/
License: GPL
Group: System/Libraries
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: bison 
BuildRequires: libxml2-devel 
BuildRequires: chrpath
BuildRequires: glib2-devel
BuildRequires: sqlite3-devel
BuildRequires: pkgconfig
BuildRequires: swig
BuildRequires: scons

%description
OpenSync is a synchronization framework that is platform and distribution
independent.  It consists of several plugins that can be used to connect to
devices, a powerful sync-engine and the framework itself.  The synchronization
framework is kept very flexible and is capable of synchronizing any type of
data, including contacts, calendar, tasks, notes and files.

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/opensync

#-------------------------------------------------------------

%define major 1.0.0
%define libname %mklibname opensync %major

%package -n %{libname}
Summary: Dynamic libraries from %name
Group: System/Libraries
Obsoletes: %{_lib}opensync
Requires: %name = %version-%release

%description -n %{libname}
Dynamic libraries from %name.

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/opensync
%{_libdir}/libopensync.so.%{major}*

#-------------------------------------------------------------

%define develname %mklibname -d opensync

%package -n %{develname}
Summary: Header files and static libraries from %name
Group: Development/C
Requires: %{libname} = %{version}-%{release}
Provides: opensync-devel = %{version}-%{release}
Obsoletes: %mklibname -d %name 0
Provides: libopensync-devel = %version-%{release}

%description -n %{develname}
Libraries and includes files for developing programs based on %name.

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/opensync-1.0
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%prep
%setup -q

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export FFLAGS="%{optflags}"
export APPEND_CCFLAGS="%{optflags}"
scons prefix=%{_prefix} libsuffix=%{_lib}
										
%install
rm -rf $RPM_BUILD_ROOT
scons install DESTDIR=%{buildroot}

%clean
rm -rf $RPM_BUILD_ROOT
