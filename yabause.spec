%undefine _hardened_build

Name:           yabause
Version:        0.9.15
Release:        10%{?dist}
Summary:        A Sega Saturn emulator
License:        GPLv2+
URL:            http://yabause.org
Source0:        https://download.tuxfamily.org/%{name}/releases/%{version}/%{name}-%{version}.tar.gz
# https://github.com/Yabause/yabause/commit/06a816c032c6f7fd79ced6e594dd4b33571a0e73
Patch0:         Fix_qt_5.11.patch

BuildRequires:  cmake3
BuildRequires:  dos2unix
BuildRequires:  desktop-file-utils
BuildRequires:  freeglut-devel
BuildRequires:  glew-devel
BuildRequires:  libXmu-devel
BuildRequires:  openal-devel
%if 0%{?fedora} >= 25
BuildRequires:  libXi-devel
BuildRequires:  qt5-devel
%else
BuildRequires:  qt4-devel
%endif
BuildRequires:  SDL2-devel

%description
Yabause is a Sega Saturn emulator. A popular console of the early 1990s. It
includes an 'emulated' Saturn BIOS which is compatible with at least some games
but optionally a real Saturn BIOS can be used, however it is not included.


%prep
%setup
# Fix the dos crap to make patching easy
dos2unix src/qt/ui/*
%patch0 -p2

#fix end-of-line encoding
find \( -name \*.c\* -or -name \*.h\* -or -name AUTHORS \) -exec sed -i 's/\r$//' {} \;

#fix permissions
find \( -name \*.c\* -or -name \*.h\* \) -exec chmod -x {} \;

%build
CFLAGS="$RPM_OPT_FLAGS -Wl,-z,relro -Wl,-z,now"
CXXFLAGS="$RPM_OPT_FLAGS -Wl,-z,relro -Wl,-z,now"

export CFLAGS
export CXXFLAGS

#arm dynarec is broken
%ifarch %{ix86} x86_64
%cmake3 -DBUILD_SHARED_LIBS:BOOL=OFF -DYAB_PORTS=qt -DYAB_OPTIMIZATION=-O2 .
%else
%cmake3 -DBUILD_SHARED_LIBS:BOOL=OFF -DYAB_PORTS=qt -DYAB_OPTIMIZATION=-O2 \
    -DSH2_DYNAREC:BOOL=OFF .
%endif
%make_build


%install
%make_install

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%doc AUTHORS ChangeLog COPYING README


%changelog
* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9.15-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9.15-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Sep 30 2018 Sérgio Basto <sergio@serjux.com> - 0.9.15-8
- Rebuild for glew 2.1.0

* Sun Aug 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.9.15-7
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Sat Jul 28 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.9.15-6
- Fix qt 5.11 build

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.9.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.9.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.9.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 21 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.9.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Oct 29 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.15-1
- Updated to 0.9.15
- Use Qt5 on F25 and above
- Switched to SDL2
- Updated Source0 URL
- Fixed permissions and end-of-line encoding rpmlint warnings/errors
- Modernised the .spec file
- Disabled dynarec on arm

* Thu Jun 02 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.14-2
- Disabled hardened build for now, assembly is not ready

* Sat Jun 06 2015 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.14-1
- Updated to 0.9.14

* Mon Sep 01 2014 Sérgio Basto <sergio@serjux.com> - 0.9.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Apr 29 2014 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.13.1-1
- Updated to 0.9.13.1
- Ensured optimization level -O2 is used

* Tue May 14 2013 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.12-1
- Updated to 0.9.12
- Switched to the qt port
- Switched to the upstream .desktop file

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.9.11.1-2
- Mass rebuilt for Fedora 19 Features

* Tue Feb 21 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.11.1-1
- Updated to 0.9.11.1
- Dropped obsolete Group, Buildroot, %%clean and %%defattr
- Updated scriptlets to the latest spec
- Switched to cmake
- Dropped the selinux patch

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.9.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 05 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.9.10-2
- Rebuilt against openal-soft

* Tue Jun 02 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.9.10-1
- Updated to 0.9.10
- Added openal-devel to BuildRequires
- Dropped unnecessary configure switches, they don't change anything

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.9.9-2
- rebuild for new F11 features

* Tue Jan 13 2009 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.9.9-1
- Updated to 0.9.9
- Re-enabled parallel build

* Wed Dec 17 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.9.8-1
- Updated to 0.9.8
- Dropped obsolete docs

* Sun Oct 19 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.9.7-1
- Updated to 0.9.7
- Dropped addlimits patch
- Disabled paralled build

* Sun Sep 14 2008 Xavier Lamien <lxntow[at]gmail.com> - 0.9.3-2
- Update files and rebuild for rpmfusion for inclusion.

* Mon Jan 21 2008 Ian Chapman <packages[AT]amiga-hardware.com> 0.9.3-1
- Upgrade to 0.9.3

* Wed Jan 09 2008 Ian Chapman <packages[AT]amiga-hardware.com> 0.9.2-1
- Upgrade to 0.9.2

* Sun Nov 18 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.9.1-1
- Upgrade to 0.9.1
- Added patch for devel only to link against selinux possibly due to broken
  GL libs

* Fri Sep 28 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.9.0-1
- Upgrade to 0.9.0

* Tue Aug 28 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.8.6-1
- Upgrade to 0.8.6
- License field changed due to new guidelines
- Added patch needed for compilation with F8 (devel)

* Tue Jun 26 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.8.5-1
- Upgrade to 0.8.5
- Minor changes to SPEC for new Fedora guidelines

* Sun Mar 04 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.8.0-2
- Dropped dribble-menus requirement, due to be obsoleted
- Changed .desktop category to Game;Emulator;

* Thu Jan 04 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.8.0-1
- Upgrade to 0.8.0

* Wed Sep 20 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.7.2-1
- Upgrade to 0.7.2

* Wed Aug 30 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.7.1-1
- Upgrade to 0.7.1
- Removed big endian patch as it's now merged upstream

* Sat Aug 26 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.7.0-2
- Added libXt-devel buildrequire
- Added patch to fix compilation on big endian systems

* Wed Aug 23 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.7.0-1
- Initial Release
