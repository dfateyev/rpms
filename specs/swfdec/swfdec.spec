# $Id$
# Authority: dag

%{?dist: %{expand: %%define %dist 1}}
%{?fedora: %{expand: %%define fc%{fedora} 1}}

%{!?dist: %define _without_gstreamer 1}
%{?fc5:   %define _without_gstreamer 1}
%{!?dist: %define _with_modxorg 1}
%{?fc5:   %define _with_modxorg 1}
%{!?dist: %define gimp_plugin 1}
%{?fc5:   %define gimp_plugin 1}
%{?el4:   %define gimp_plugin 1}
%{?fc4:   %define gimp_plugin 1}
%{?fc3:   %define gimp_plugin 1}
%{?fc2:   %define gimp_plugin 1}
%{?yd4:   %define gimp_plugin 1}
%{!?dist: %define _without_mozilla 1}
%{?fc5:   %define _without_mozilla 1}
%{?fc1:   %define _without_mozilla 1}
%{?el3:   %define _without_mozilla 1}
%{?el3:   %define _without_gstreamer 1}
%{?rh9:   %define _without_mozilla 1}
%{?rh9:   %define _without_gstreamer 1}
%{?rh7:   %define _without_mozilla 1}
%{?rh7:   %define _without_gstreamer 1}
%{?el2:   %define _without_mozilla 1}
%{?el2:   %define _without_gstreamer 1}

Summary: Flash animations rendering library
Name: swfdec
Version: 0.3.6
Release: 1
License: LGPL
Group: System Environment/Libraries
URL: http://swfdec.sourceforge.net/
Source: http://www.schleef.org/swfdec/download/swfdec-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: libart_lgpl-devel, gtk2-devel >= 2.1.2
BuildRequires: libmad-devel, SDL-devel, gdk-pixbuf-devel, gcc-c++
BuildRequires: liboil-devel, GConf2-devel, js-devel
%{?gimp_plugin:BuildRequires: gimp-devel >= 2.0}
%{!?_without_mozilla:BuildRequires: mozilla-devel}
%{!?_without_gstreamer:BuildRequires: gstreamer-plugins-devel}
%{?_with_modxorg:BuildRequires: libXt-devel}

%description
Libswfdec is a library for rendering Flash animations. Currently it
handles mostFlash 3 animations and some Flash 4. No interactivity is
supported yet.


%package devel
Summary: Header files, libraries and development documentation for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}, glib2-devel, liboil-devel

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.


%package -n mozilla-swfdec
Summary: Mozilla plugin for Flash rendering
Group: Applications/Internet
Requires: %{name} = %{version}

%description -n mozilla-swfdec
Mozilla plugin for rendering of Flash animations based on the swfdec library.


%prep
%setup


%build
%configure \
%{?_without_mozilla:--disable-mozilla-plugin}
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}


%clean
%{__rm} -rf %{buildroot}


%post
/sbin/ldconfig 2>/dev/null
/usr/bin/update-gdk-pixbuf-loaders . || :

### Backward compatibility for gtk < 2.4.13-9
[ -x %{_bindir}/gdk-pixbuf-query-loaders ] && \
    %{_bindir}/gdk-pixbuf-query-loaders > \
        %{_sysconfdir}/gtk-2.0/gdk-pixbuf.loaders || :

%postun
/sbin/ldconfig 2>/dev/null
/usr/bin/update-gdk-pixbuf-loaders . || :

### Backward compatibility for gtk < 2.4.13-9
[ -x %{_bindir}/gdk-pixbuf-query-loaders ] && \
    %{_bindir}/gdk-pixbuf-query-loaders > \
        %{_sysconfdir}/gtk-2.0/gdk-pixbuf.loaders || :


%files 
%defattr(-, root, root, 0755)
%doc AUTHORS COPYING README TODO
%{_libdir}/libswfdec*.so.*
%{?gimp_plugin:%{_libdir}/gimp/2.0/plug-ins/swf}
%{_libdir}/gtk-2.0/*/loaders/swf_loader.so

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/swfdec*/
%exclude %{_libdir}/gtk-2.0/*/loaders/swf_loader.a
%exclude %{_libdir}/gtk-2.0/*/loaders/swf_loader.la
%{_libdir}/libswfdec*.a
%exclude %{_libdir}/libswfdec*.la
%{_libdir}/libswfdec*.so
%{_libdir}/pkgconfig/swfdec*.pc

%if %{!?_without_mozilla:1}0
%files -n mozilla-swfdec
%defattr(-, root, root, 0755)
%{_bindir}/swfdec-mozilla-player
%exclude %{_libdir}/mozilla/plugins/libswfdecmozilla.a
%exclude %{_libdir}/mozilla/plugins/libswfdecmozilla.la
%{_libdir}/mozilla/plugins/libswfdecmozilla.so
%endif


%changelog
* Thu Jan 19 2006 Matthias Saou <http://freshrpms.net/> 0.3.6-1
- Update to 0.3.6.
- Add js-devel buil requirement, configure should check this.
- Remove no longer included swf_play.

* Thu Jan 12 2006 Matthias Saou <http://freshrpms.net/> 0.3.5-2
- Disable gstreamer support on FC5 (as it's for 0.8).
- Disable mozilla plugin on FC5 (no more mozilla-config script).
- Add modular xorg build conditional.

* Wed May 25 2005 Matthias Saou <http://freshrpms.net/> 0.3.5-1
- Update to 0.3.5.

* Thu May  5 2005 Matthias Saou <http://freshrpms.net/> 0.3.4-2
- Add missing glib2-devel and liboil-devel reqs in the devel package.

* Sat Apr  2 2005 Matthias Saou <http://freshrpms.net/> 0.3.4-1
- Update to 0.3.4.
- Change %%makeinstall for DESTDIR method because of the gimp plugin.

* Fri Nov 26 2004 Dag Wieers <dag@wieers.com> - 0.3.2-2
- Added update-gdk-pixbuf-loaders to scriptlets.

* Thu Nov 25 2004 Matthias Saou <http://freshrpms.net/> 0.3.2-2
- Make scriplets never return a failure.

* Wed Nov 24 2004 Matthias Saou <http://freshrpms.net/> 0.3.2-1
- Update to 0.3.2.

* Tue Nov  9 2004 Matthias Saou <http://freshrpms.net/> 0.3.1-1
- Make gimp plugin conditional and build only for FC2, FC3 and YD4 (gimp2).

* Fri Nov 05 2004 Dag Wieers <dag@wieers.com> - 0.3.1-1
- Updated to release 0.3.1.

* Wed Oct 20 2004 Matthias Saou <http://freshrpms.net/> 0.3.0-1
- Update to 0.3.0.
- Added new liboil-devel and gimp2-devel dependencies.
- Added gimp plugin... strange, it goes into 1.3 :-/

* Tue Jan 20 2004 Dag Wieers <dag@wieers.com> - 0.2.2-1
- Added missing swfdec requirement. (Alexandre Oliva)

* Thu Aug 28 2003 Dag Wieers <dag@wieers.com> - 0.2.2-0
- Initial package. (using DAR)

