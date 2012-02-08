Name:           yabause
Version:        0.9.10
Release:        3%{?dist}
Summary:        A Sega Saturn emulator
Group:          Applications/Emulators
License:        GPLv2+
URL:            http://yabause.org
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:        %{name}.desktop
Patch1:         yabause-0.9.1.addselinux.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  desktop-file-utils
BuildRequires:  freeglut-devel
BuildRequires:  gtk+-devel
BuildRequires:  gtkglext-devel
BuildRequires:  libGLU-devel
BuildRequires:  libICE-devel
BuildRequires:  libselinux-devel
BuildRequires:  libXt-devel
BuildRequires:  openal-devel
BuildRequires:  pkgconfig
BuildRequires:  SDL-devel
Requires:       hicolor-icon-theme

%description
Yabause is a Sega Saturn emulator. A popular console of the early 1990s. It
includes an 'emulated' Saturn BIOS which is compatible with at least some games
but optionally a real Saturn BIOS can be used, however it is not included.


%prep
%setup -q
%if 0%{?fedora} > 8
%patch1 -p1
%endif


%build
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps

# Some cleanups
rm -rf %{buildroot}%{_datadir}/%{name} %{buildroot}%{_datadir}/pixmaps
rm -f %{buildroot}%{_datadir}/applications/*.desktop %{buildroot}%{_bindir}/gen68k

install -pm0644 src/logo.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png

desktop-file-install --vendor dribble \
                     --dir %{buildroot}%{_datadir}/applications \
                     %{SOURCE1}


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz
%{_datadir}/applications/dribble-%{name}.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%doc AUTHORS ChangeLog COPYING GOALS README README.LIN TODO


%changelog
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
