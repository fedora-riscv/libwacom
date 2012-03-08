Name:           libwacom
Version:        0.3
Release:        5%{?dist}
Summary:        Tablet Information Client Library
Requires:       %{name}-data

Group:          System Environment/Libraries
License:        MIT
URL:            http://linuxwacom.sourceforge.net

Source0:        http://prdownloads.sourceforge.net/linuxwacom/%{name}/%{name}-%{version}.tar.bz2
Source1:        libwacom.rules

Patch01:        libwacom-0.3-add-list-devices.patch
Patch02:        libwacom-0.3-add-udev-generator.patch
Patch03:        libwacom-0.3-add-bamboo-one.patch

BuildRequires:  autoconf automake libtool doxygen
BuildRequires:  glib2-devel libgudev1-devel

%description
%{name} is a library that provides information about Wacom tablets and
tools. This information can then be used by drivers or applications to tweak
the UI or general settings to match the physical tablet.

%package devel
Summary:        Tablet Information Client Library Library Development Package
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Tablet information client library library development package.

%package data
Summary:        Tablet Information Client Library Library Data Files
BuildArch:      noarch

%description data
Tablet information client library library data files.

%prep
%setup -q -n %{name}-%{version}

%patch01 -p1
%patch02 -p1
%patch03 -p1

%build
autoreconf --force -v --install || exit 1
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
install -d ${RPM_BUILD_ROOT}/lib/udev/rules.d
install -p -m 644 %SOURCE1 ${RPM_BUILD_ROOT}/lib/udev/rules.d/65-libwacom.rules

# We intentionally don't ship *.la files
rm -f %{buildroot}%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README 
%{_libdir}/libwacom.so.*
/lib/udev/rules.d/65-libwacom.rules

%files devel
%defattr(-,root,root,-)
%doc COPYING
%dir %{_includedir}/libwacom-1.0/
%dir %{_includedir}/libwacom-1.0/libwacom
%{_includedir}/libwacom-1.0/libwacom/libwacom.h
%{_libdir}/libwacom.so
%{_libdir}/pkgconfig/libwacom.pc

%files data
%defattr(-,root,root,-)
%doc COPYING
%dir %{_datadir}/libwacom
%{_datadir}/libwacom/*.tablet
%{_datadir}/libwacom/*.stylus

%changelog
* Thu Mar 08 2012 Olivier Fourdan <ofourdan@redhat.com> 0.3-5
- Mark data subpackage as noarch and make it a requirement for libwacom
- Use generated udev rule file to list only known devices from libwacom
  database

* Tue Mar 06 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.3-4
- libwacom-0.3-add-list-devices.patch: add API to list devices
- libwacom-0.3-add-udev-generator.patch: add a udev rules generater tool
- libwacom-0.3-add-bamboo-one.patch: add Bamboo One definition

* Tue Feb 21 2012 Olivier Fourdan <ofourdan@redhat.com> - 0.3-2
- Add udev rules to identify Wacom as tablets for libwacom

* Tue Feb 21 2012 Peter Hutterer <peter.hutterer@redhat.com>
- Source file is .bz2, not .xz

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 0.3-1
- Update to 0.3

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 0.2-1
- Update to 0.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.1-1
- Initial import (#768800)
