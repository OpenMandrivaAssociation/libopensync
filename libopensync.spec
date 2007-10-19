%define with_python 1
%{?_without_python: %{expand: %%global _with_python 0}}

Name: libopensync
Version: 0.33
Release: %mkrel 1
Summary: Multi-platform PIM synchronization framework
Source: http://www.opensync.org/download/releases/%version/%name-%version.tar.bz2
Patch: libopensync-python-lib-check-lib64.patch
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
BuildRequires: autoconf

%description
OpenSync is a synchronization framework that is platform and distribution
independent.  It consists of several plugins that can be used to connect to
devices, a powerful sync-engine and the framework itself.  The synchronization
framework is kept very flexible and is capable of synchronizing any type of
data, including contacts, calendar, tasks, notes and files.

#-------------------------------------------------------------

%define libname %mklibname opensync 0

%package -n %{libname}
Summary: Dynamic libraries from %name
Group: System/Libraries
Obsoletes: %{_lib}opensync

%description -n %{libname}
Dynamic libraries from %name.

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/opensync
%{_libdir}/osplugin
%{_libdir}/*.so.*

#-------------------------------------------------------------

%define develname %mklibname -d opensync

%package -n %{develname}
Summary: Header files and static libraries from %name
Group: Development/C
Requires: %{libname} = %{version}
Provides: opensync-devel
Obsoletes: %mklibname -d %name 0
Provides: libopensync-devel = %version

%description -n %{develname}
Libraries and includes files for developing programs based on %name.

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc

#-------------------------------------------------------------

%if %{with_python}

%package -n	%name-python
Summary: Python bindings for %name
Group: Development/Python
Provides: opensync-python
%py_requires -d

%description -n %name-python
Python bindings for %name

%files -n %name-python
%defattr(-,root,root)
%{python_sitearch}/*

%endif

#-------------------------------------------------------------

%prep
%setup -q
#%patch -p1


%build
autoreconf -if

%configure2_5x \
%if %{with_python}
    --enable-python \
%endif
    --disable-debug \
    --enable-engine \
    --enable-tools

%make pythondir=%{python_sitearch}
										
%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std pythondir=%{python_sitearch}

%clean
rm -rf $RPM_BUILD_ROOT

