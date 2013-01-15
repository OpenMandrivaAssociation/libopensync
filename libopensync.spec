# If you are thinking of upgrading opensync to 0.3x, please be
# prepared to justify yourself to those who actually use it. i.e.,
# you are going to need to prove that it's a) better, b) works, and
# c) won't eat anyone's data, or else be prepared to lose some major
# appendages. - AdamW 2008/03

%define major	0
%define libname	%mklibname opensync %{major}
%define devname	%mklibname opensync -d

%define with_python 1
%{?_without_python: %{expand: %%global _with_python 0}}

Summary:	Multi-platform PIM synchronization framework
Name:		libopensync
Epoch:		1
Version:	0.22
Release:	21
License:	GPLv2+
Group:		System/Libraries
URL:		http://www.opensync.org/
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
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(sqlite3)

%description
OpenSync is a synchronization framework that is platform and distribution
independent. It consists of several plugins that can be used to connect to
devices, a powerful sync-engine and the framework itself.  The synchronization
framework is kept very flexible and is capable of synchronizing any type of
data, including contacts, calendar, tasks, notes and files.

%files
%{_bindir}/*
%{_libdir}/opensync
%{_libdir}/osplugin

#--------------------------------------------------------

%package -n %{libname}
Summary:	Dynamic libraries from %{name}
Epoch:		0
Group:		System/Libraries

%description -n %{libname}
Dynamic libraries from %{name}.

%files -n %{libname}
%{_libdir}/*.so.%{major}*

#-------------------------------------------------------------

%package -n %{devname}
Summary:	Header files and static libraries from %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}

%description -n %{devname}
Libraries and includes files for developing programs based on %{name}.

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

#-------------------------------------------------------------

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

#-------------------------------------------------------------

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p0
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1 -b .am113~

%build
autoreconf -fi
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

#provide fixed opensync.py, patch doesn't exist on source (#54931)
#rm -f %{buildroot}%{py_platsitedir}/opensync.py
#install %{SOURCE1} %{buildroot}%{py_platsitedir}/opensync.py


%changelog
* Fri Jun 08 2012 Matthew Dawkins <mattydaw@mandriva.org> 1:0.22-19
+ Revision: 803584
- rebuild to remove .la files
- cleaned up spec

* Thu May 26 2011 Alex Burmashev <burmashev@mandriva.org> 1:0.22-18
+ Revision: 679177
- swig fix

* Fri Apr 29 2011 Funda Wang <fwang@mandriva.org> 1:0.22-17
+ Revision: 660632
- add fedora patch to build with gcc 4.6

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Mon Nov 01 2010 Funda Wang <fwang@mandriva.org> 1:0.22-16mdv2011.0
+ Revision: 591297
- rebuild for py2.7

  + Emmanuel Andry <eandry@mandriva.org>
    - add p3 to cleanly fix compat issue with latest swig (#54931)

* Mon Jan 25 2010 Emmanuel Andry <eandry@mandriva.org> 1:0.22-14mdv2010.1
+ Revision: 496281
- (ugly) fix for bug #54931

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 1:0.22-12mdv2010.0
+ Revision: 425673
- rebuild

* Fri Dec 26 2008 Funda Wang <fwang@mandriva.org> 1:0.22-11mdv2009.1
+ Revision: 319218
- rebuild for new python

* Sat Jul 12 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.22-10mdv2009.0
+ Revision: 234066
- fix linkage

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Fri Mar 28 2008 Adam Williamson <awilliamson@mandriva.org> 1:0.22-9mdv2008.1
+ Revision: 190932
- obsolete libopensync1 (fix upgrade from RC1, thanks tv)

* Sat Mar 15 2008 Adam Williamson <awilliamson@mandriva.org> 1:0.22-8mdv2008.1
+ Revision: 188056
- drop separate ipc package as the file it contained is actually vital for opensync to be able to do anything at all

* Thu Mar 13 2008 Adam Williamson <awilliamson@mandriva.org> 1:0.22-7mdv2008.1
+ Revision: 187306
- add note explaining why anyone who upgrades to 0.3x again must be willing to part with several limbs
- move non-library files from lib to main package
- use epochs, obsoletes, conflicts and various other ugly stuff to handle 'upgrading' from 0.36
- clean spec up (tabs, update python macros, fix some description issues)
- revert to 0.22, based on last 0.22 spec from SVN

* Mon Jan 28 2008 Funda Wang <fwang@mandriva.org> 0.36-1mdv2008.1
+ Revision: 158951
- fix osplugin location
- update to new version 0.36

* Thu Jan 03 2008 Funda Wang <fwang@mandriva.org> 0.35-2mdv2008.1
+ Revision: 141160
- don't obsolete old package

* Sun Dec 23 2007 Funda Wang <fwang@mandriva.org> 0.35-1mdv2008.1
+ Revision: 137337
- split out ipc plugin
- osplugin should be arch independent
- use %%py_platsitedir
- New version 0.35
- rediff python-wrapper patch

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 04 2007 Funda Wang <fwang@mandriva.org> 0.34-2mdv2008.1
+ Revision: 105820
- Obsoletes old lib
- fix obsoletes name

* Sun Nov 04 2007 Funda Wang <fwang@mandriva.org> 0.34-1mdv2008.1
+ Revision: 105771
- fix python wrapper building
- New major ( 1.0.0 -> 1 )
- New version 0.34

* Mon Oct 22 2007 Thierry Vignaud <tv@mandriva.org> 0.33-5mdv2008.1
+ Revision: 101182
- fix upgrading

* Sat Oct 20 2007 Funda Wang <fwang@mandriva.org> 0.33-4mdv2008.1
+ Revision: 100598
- build python wrapper

* Fri Oct 19 2007 Funda Wang <fwang@mandriva.org> 0.33-3mdv2008.1
+ Revision: 100397
- use our own optflags
- add conflicts to ease upgrade
- remove useless optflag

* Fri Oct 19 2007 Funda Wang <fwang@mandriva.org> 0.33-2mdv2008.1
+ Revision: 100174
- Remove wrong obsoletes

* Fri Oct 19 2007 Funda Wang <fwang@mandriva.org> 0.33-1mdv2008.1
+ Revision: 100144
- fix building in x86_64
- fix building
- Provides with version
- New version 0.33

* Fri Aug 10 2007 Helio Chissini de Castro <helio@mandriva.com> 0.22-4mdv2008.0
+ Revision: 61017
- Missing correct provides

* Fri Aug 10 2007 Helio Chissini de Castro <helio@mandriva.com> 0.22-3mdv2008.0
+ Revision: 60963
- Remove package libopensync. Binaries are moved to libopensync0
- Enable build for engine and removed wrong chrpath
- Added proper provides in devel and remove wrong obsoletes and requires
- Added missing buildrequires and fixed pyhoen requires with proper macro

* Thu Aug 09 2007 Funda Wang <fwang@mandriva.org> 0.22-2mdv2008.0
+ Revision: 60878
- highlight libmajor
- Revert to 0.22 due to unsatisfied plugins version
- New version 0.31

* Tue Apr 24 2007 Guillaume Rousse <guillomovitch@mandriva.org> 0.22-1mdv2008.0
+ Revision: 17967
- new version


* Sun Nov 12 2006 Buchan Milne <bgmilne@mandriva.org> 0.20-1mdv2007.0
+ Revision: 83444
-update to 0.20
-fix python library search in configure on x86_64
-buildrequire swig, required for python binding
- Import libopensync

* Wed Sep 06 2006 Buchan Milne <bgmilne@mandriva.org> 0.18-6mdv2007.0
- fix python location on x86_64

* Tue Aug 29 2006 Buchan Milne <bgmilne@mandriva.org> 0.18-5mdv2007.0
- buildrequires

* Tue Aug 29 2006 Buchan Milne <bgmilne@mandriva.org> 0.18-4mdv2007.0
- rebuild

* Sat Dec 03 2005 Austin Acton <austin@mandriva.org> 0.18-3mdk
- lib64 fix

* Tue Nov 29 2005 Austin Acton <austin@mandriva.org> 0.18-2mdk
- fix provides

* Fri Nov 25 2005 Austin Acton <austin@mandriva.org> 0.18-1mdk
- initial package

