# $Id$
# Authority: matthias

%define desktop_vendor freshrpms
%define prefix         %{_prefix}/games/armagetron

Summary: Multiplayer 'Tron' 3D racing game
Name: armagetron
Version: 0.2.5.2
Release: 3
License: GPL
Group: Amusements/Games
URL: http://armagetron.sourceforge.net/
Source: http://dl.sf.net/armagetron/armagetron-%{version}.tar.bz2
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: SDL_image >= 1.2.0, esound
BuildRequires: gcc-c++, libstdc++-devel, zlib-devel, libpng-devel, libjpeg-devel
BuildRequires: XFree86-devel, SDL_image-devel, SDL-devel, esound-devel
BuildRequires: /usr/bin/find, unzip, ImageMagick
#BuildRequires: XFree86-Mesa-libGLU
BuildRequires: xorg-x11-Mesa-libGLU
%{!?_without_freedesktop:BuildRequires: desktop-file-utils}

%description
There is not much to be said about the game: you ride a lightcycle,
a kind of motorbike that can't be stoppen and leaves a wall where
it goes. You can make turns of 90 degrees and can accelerate by 
driving close to walls. Make your enemies hit a wall while avoiding
the same fate.

Available rpmbuild rebuild options :
--without : freedesktop


%prep
%setup


%build
%configure
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot} installed-docs
%makeinstall

# Put the docs where we include them with %%doc
%{__mv} %{buildroot}%{prefix}/doc installed-docs

# Yeah, add an icon for the menu entry!
%{__mkdir_p} %{buildroot}%{_datadir}/pixmaps
convert tron.ico %{buildroot}%{_datadir}/pixmaps/armagetron.png

# The wrapper script (overwrite the default)
%{__cat} > %{buildroot}%{_bindir}/armagetron << 'EOF'
#!/bin/sh -e

INSTALL=%{prefix}
VARDIR=$HOME/.armagetron/var

if test ! -d $VARDIR ; then
    mkdir -p $VARDIR
        
    # Migrate old configuration
    files=$( find $HOME/.armagetron -type f -maxdepth 1 )
 
    test "$files" != "" && echo "Porting old configuration..." && mv $files $VARDIR
fi

$INSTALL/bin/armagetron --datadir $INSTALL --configdir %{_sysconfdir}/armagetron --userconfigdir $HOME/.armagetron --vardir $VARDIR "$@"

EOF

%{__cat} > %{name}.desktop << EOF
[Desktop Entry]
Name=Armagetron
Comment=Multiplayer 'Tron' 3D racing game
Exec=%{_bindir}/armagetron
Icon=armagetron.png
Terminal=false
Type=Application
Encoding=UTF-8
EOF

%if %{!?_without_freedesktop:1}%{?_without_freedesktop:0}
%{__mkdir_p} %{buildroot}%{_datadir}/applications
desktop-file-install --vendor %{desktop_vendor} \
  --dir %{buildroot}%{_datadir}/applications    \
  --add-category Application                    \
  --add-category Game                           \
  %{name}.desktop
%else
%{__install} -D -m 644 %{name}.desktop \
  %{buildroot}/etc/X11/applnk/Games/%{name}.desktop
%endif


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%doc installed-docs/*
%dir %{_sysconfdir}/armagetron
%config(noreplace) %{_sysconfdir}/armagetron/*
%exclude %{_sysconfdir}/armagetron/.orig
%{_bindir}/armagetron
%{_bindir}/armagetron-stat
%dir %{prefix}
%exclude %{prefix}/COPYING.txt
%{prefix}/arenas
%{prefix}/bin
%exclude %{prefix}/bin/uninstall
%{prefix}/language
%exclude %{prefix}/log
%{prefix}/models
%{prefix}/music
%{prefix}/sound
%{prefix}/textures
%{_datadir}/pixmaps/armagetron.png
%{!?_without_freedesktop:%{_datadir}/applications/%{desktop_vendor}-%{name}.desktop}
%{?_without_freedesktop:/etc/X11/applnk/Games/%{name}.desktop}


%changelog
* Fri May 21 2004 Matthias Saou <http://freshrpms.net/> 0.2.5.2-3
- Rebuild for Fedora Core 2.
- Split off the moviepack files into their own noarch package.

* Fri Dec 12 2003 Matthias Saou <http://freshrpms.net/> 0.2.5.2-2
- Added missing XFree86-Mesa-libGLU build dep :-(
- Rebuild for Fedora Core 1 at last.

* Wed Oct 15 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.2.5.2.
- Removed %%{prever} stuff.

* Sun Jul 20 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.2.5.

* Thu Jul 10 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.2.4.

* Sun Jul  6 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.2.3.

* Mon Jun 30 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.2.2.
- The build is now more standard, no more manual copying of files.
- PPC include workaround removed, not needed anymore.
- Major spec file updates.

* Sat Jun 14 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.2.pre3.

* Mon Jun  2 2003 Matthias Saou <http://freshrpms.net/>
- s/Games/Game for the desktop file, doh!

* Mon Mar 31 2003 Matthias Saou <http://freshrpms.net/>
- Rebuilt for Red Hat Linux 9.

* Sat Mar 15 2003 Matthias Saou <http://freshrpms.net/>
- Remove CVS directories from the docs.
- Added --without freedesktop option in order to rebuild for 7.x.
- Added YellowDog 2.3 include path workaround.

* Sat Feb 15 2003 Matthias Saou <http://freshrpms.net/>
- Applied Ben Liblit's changes at last!
- Install language files.
- Change wrapper to save settings to ~/.armagetron/

* Sun Sep 29 2002 Matthias Saou <http://freshrpms.net/>
- Rebuilt for Red Hat Linux 8.0.
- New menu entry.

* Tue Jul  2 2002 Matthias Saou <http://freshrpms.net/>
- Update to 0.2.0.pre_020624.

* Thu May  2 2002 Matthias Saou <http://freshrpms.net/>
- Rebuilt against Red Hat Linux 7.3.
- Added the %{?_smp_mflags} expansion.

* Fri Apr 19 2002 Matthias Saou <http://freshrpms.net/>
- Rebuilt without the NVIDIA libGLcore.so.1 dependency (doh!).

* Tue Nov 20 2001 Matthias Saou <http://freshrpms.net/>
- Added a simple shell script to have the menu entry work with KDE.
- Added a separate package for the "moviepack"... that thing is cool :-)
- Changed the binary to sgid "games" so that high scores are saved.
- Added an icon for the menu entry.

* Mon Nov 19 2001 Matthias Saou <http://freshrpms.net/>
- Update to 0.1.4.9.
- Spec file cleanup.

* Thu Jan  4 2001 Tim Powers <timp@redhat.com>
- defattr was in wrong place in files list, leaving files owned by the
  build system, fixed

* Tue Nov 28 2000 Karsten Hopp <karsten@redhat.de>
- initial RPM

