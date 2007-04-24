%define name	libopensync
%define version	0.22
%define release %mkrel 1

%define major	0
%define libname %mklibname opensync %major

Name: 	 	%{name}
Summary: 	Multi-platform PIM synchronization framework
Version: 	%{version}
Release: 	%{release}

Source:		%{name}-%{version}.tar.bz2
Patch:		libopensyc-python-lib-check-lib64.patch
URL:		http://www.opensync.org/
License:	GPL
Group:		System/Libraries
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	bison libxml2-devel python-devel
BuildRequires:	chrpath
BuildRequires:	glib2-devel
BuildRequires:	sqlite3-devel
BuildRequires:	swig

%description
OpenSync is a synchronization framework that is platform and distribution
independent.  It consists of several plugins that can be used to connect to
devices, a powerful sync-engine and the framework itself.  The synchronization
framework is kept very flexible and is capable of synchronizing any type of
data, including contacts, calendar, tasks, notes and files.

%package -n 	%{libname}
Summary:        Dynamic libraries from %name
Group:          System/Libraries
#Provides:	%name
#Obsoletes:	%name = %version-%release

%description -n %{libname}
Dynamic libraries from %name.

%package -n 	%{libname}-devel
Summary: 	Header files and static libraries from %name
Group: 		Development/C
Requires: 	%{libname} >= %{version}
Provides: 	opensync-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release} 
Obsoletes: 	%name-devel

%description -n %{libname}-devel
Libraries and includes files for developing programs based on %name.

%package -n	%name-python
Summary:	Python binding for %name
Group:		Development/Python
Provides:	opensync-python

%description -n %name-python
Python bindings for %name

%prep
%setup -q
%patch -p1
autoconf

%build
%configure2_5x --enable-python
%make pythondir=%{python_sitearch}
										
%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std pythondir=%{python_sitearch}
chrpath -d %buildroot/%{_bindir}/*
chrpath -d %buildroot/%{_libdir}/*.so.%major.?.?
chrpath -d %buildroot/%{python_sitearch}/_opensync.so

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/opensync
%{_libdir}/osplugin

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
#%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc

%files -n %name-python
%defattr(-,root,root)
%{python_sitearch}/*


