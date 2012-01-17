Name:           libwacom
Version:        0.2
Release:        1%{?dist}
Summary:        Tablet Information Client Library

Group:          System Environment/Libraries
License:        MIT
URL:            http://linuxwacom.sourceforge.net

Source0:        http://prdownloads.sourceforge.net/linuxwacom/%{name}/%{name}-%{version}.tar.xz

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

%description data
Tablet information client library library data files.

%prep
%setup -q -n %{name}-%{version}

%build
autoreconf -v --install || exit 1
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"

# We intentionally don't ship *.la files
rm -f %{buildroot}%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README 
%{_libdir}/libwacom.so.*

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
* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 0.2-1
- Update to 0.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.1-1
- Initial import (#768800)
