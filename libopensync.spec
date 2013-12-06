# If you are thinking of upgrading opensync to 0.3x, please be
# prepared to justify yourself to those who actually use it. i.e.,
# you are going to need to prove that it's a) better, b) works, and
# c) won't eat anyone's data, or else be prepared to lose some major
# appendages. - AdamW 2008/03

%define major	0
%define libname	%mklibname opensync %{major}
%define libxml %mklibname opensync-xml %{major}
%define libosengine %mklibname osengine %{major}
%define devname	%mklibname opensync -d

%define with_python 1
%{?_without_python: %{expand: %%global _with_python 0}}

Summary:	Multi-platform PIM synchronization framework
Name:		libopensync
Epoch:		1
Version:	0.22
Release:	23
License:	GPLv2+
Group:		System/Libraries
Url:		http://www.opensync.org/
Source0:	http://www.opensync.org/download/releases/%{version}/%{name}-%{version}.tar.bz2
#Source1:	opensync.py
Patch0:		libopensync-python-lib-check-lib64.patch
Patch1:		libopensync-linkage_fix.diff
Patch2:		libopensync-python-fix.patch
Patch3:		libopensync-swig-fix.patch
Patch4:		libopensync-0.22-unusedvar.patch
Patch5:		libopensync-swig-fix2.patch
Patch6:		libopensync-automake-1.13.patch

BuildRequires:	bison
BuildRequires:	chrpath
BuildRequires:	swig
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(sqlite3)

%description
OpenSync is a synchronization framework that is platform and distribution
independent. It consists of several plugins that can be used to connect to
devices, a powerful sync-engine and the framework itself.  The synchronization
framework is kept very flexible and is capable of synchronizing any type of
data, including contacts, calendar, tasks, notes and files.

%package -n %{libname}
Summary:	Dynamic libraries from %{name}
Group:		System/Libraries

%description -n %{libname}
Dynamic libraries from %{name}.

%package -n %{libxml}
Summary:	Dynamic libraries from %{name}
Group:		System/Libraries
Conflicts:	%{_lib}opensync0 < 1:0.22-22

%description -n %{libxml}
Dynamic libraries from %{name}.

%package -n %{libosengine}
Summary:	Dynamic libraries from %{name}
Group:		System/Libraries
Conflicts:	%{_lib}opensync0 < 1:0.22-22

%description -n %{libosengine}
Dynamic libraries from %{name}.

%package -n %{devname}
Summary:	Header files and static libraries from %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{libxml} = %{EVRD}
Requires:	%{libosengine} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
Libraries and includes files for developing programs based on %{name}.

%if %{with_python}
%package python
Summary:	Python bindings for %{name}
Group:		Development/Python
%py_requires -d

%description python
Python bindings for %{name}.

%files python
%{py_platsitedir}/*
%endif

%prep
%setup -q
%apply_patches
autoreconf -fi

%build
export CFLAGS="%{optflags} -Wno-error"
%configure2_5x \
	--disable-static \
%if %{with_python}
	--enable-python \
%endif
	--disable-debug \
	--enable-engine \
	--enable-tools

%make pythondir=%{py_platsitedir}
										
%install
%makeinstall_std pythondir=%{py_platsitedir}

%files
%{_bindir}/*
%{_libdir}/opensync
%{_libdir}/osplugin

%files -n %{libname}
%{_libdir}/libopensync.so.%{major}*

%files -n %{libxml}
%{_libdir}/libopensync-xml.so.%{major}*

%files -n %{libosengine}
%{_libdir}/libosengine.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

