# If you are thinking of upgrading opensync to 0.3x, please be
# prepared to justify yourself to those who actually use it. i.e.,
# you are going to need to prove that it's a) better, b) works, and
# c) won't eat anyone's data, or else be prepared to lose some major
# appendages. - AdamW 2008/03

%define major		0
%define libname		%mklibname opensync %major
%define develname	%mklibname opensync -d

%define with_python 1
%{?_without_python: %{expand: %%global _with_python 0}}

Name:		libopensync
Version:	0.22
Epoch:		1
Release:	%mkrel 17
Summary:	Multi-platform PIM synchronization framework
Source0:	http://www.opensync.org/download/releases/%{version}/%{name}-%{version}.tar.bz2
#Source1:	opensync.py
Patch0:		libopensync-python-lib-check-lib64.patch
Patch1:		libopensync-linkage_fix.diff
Patch2:		libopensync-python-fix.patch
Patch3:		libopensync-swig-fix.patch
URL:		http://www.opensync.org/
License:	GPLv2+
Group:		System/Libraries
BuildRequires:	bison
BuildRequires:	libxml2-devel
BuildRequires:	chrpath
BuildRequires:	glib2-devel
BuildRequires:	sqlite3-devel
BuildRequires:	pkgconfig
BuildRequires:	swig
BuildRequires:	autoconf
Obsoletes:	opensync0 < 0.22-7
Obsoletes:	libopensync-ipc < 0.22-8
Conflicts:	libopensync-ipc < 0.22-8
Conflicts:	%{mklibname opensync 0} < 0.22-7
Obsoletes:	%{mklibname opensync 1} <= 0.36-1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
OpenSync is a synchronization framework that is platform and distribution
independent. It consists of several plugins that can be used to connect to
devices, a powerful sync-engine and the framework itself.  The synchronization
framework is kept very flexible and is capable of synchronizing any type of
data, including contacts, calendar, tasks, notes and files.

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/opensync
%{_libdir}/osplugin

#--------------------------------------------------------

%package -n %{libname}
Summary:	Dynamic libraries from %{name}
Epoch:		0
Group:		System/Libraries
Conflicts:	opensync0 < 0.22-7

%description -n %{libname}
Dynamic libraries from %{name}.

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

#-------------------------------------------------------------

%package -n %{develname}
Summary:	Header files and static libraries from %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}
Obsoletes:	%{mklibname -d opensync 0} < 0.22-7

%description -n %{develname}
Libraries and includes files for developing programs based on %{name}.

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc

#-------------------------------------------------------------

%if %{with_python}

%package python
Summary:	Python bindings for %{name}
Group:		Development/Python
Obsoletes:	opensync0-python < 0.22-7
%py_requires -d

%description python
Python bindings for %{name}.

%files python
%defattr(-,root,root)
%{py_platsitedir}/*

%endif

#-------------------------------------------------------------

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p0
%patch3 -p1

%build
autoreconf -fis

%configure2_5x \
%if %{with_python}
    --enable-python \
%endif
    --disable-debug \
    --enable-engine \
    --enable-tools

%make pythondir=%{py_platsitedir}
										
%install
rm -rf %{buildroot}
%makeinstall_std pythondir=%{py_platsitedir}

#provide fixed opensync.py, patch doesn't exist on source (#54931)
#rm -f %{buildroot}%{py_platsitedir}/opensync.py
#install %{SOURCE1} %{buildroot}%{py_platsitedir}/opensync.py

%clean
rm -rf %{buildroot}
