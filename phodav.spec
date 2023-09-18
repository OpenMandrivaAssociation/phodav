%define api 3.0
%define major 0

%define libphodav %mklibname phodav %api %major
%define libphodavdevel %mklibname phodav -d

%define url_ver	%(echo %{version}|cut -d. -f1,2)

Name:		phodav
Version:	3.0
Release:	4
Summary:	A WebDAV server using libsoup
Group:		System/Servers
License:	LGPLv2+
URL:		https://wiki.gnome.org/phodav
Source0:	https://download.gnome.org/sources/phodav/%{url_ver}/%{name}-%{version}.tar.xz
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(udev)
BuildRequires:	systemd-units
BuildRequires:	pkgconfig(libsoup-3.0)
BuildRequires:	pkgconfig(avahi-gobject)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:	meson
BuildRequires:	intltool
BuildRequires:	asciidoc
BuildRequires:	gtk-doc
BuildRequires:	xmlto

%description
phởdav is a WebDAV server implementation using libsoup (RFC 4918).

%package i18n
Group:		System/Internationalization
Summary:	Translation files for %{name}
BuildArch:	noarch

%description i18n
phởdav is a WebDAV server implementation using libsoup (RFC 4918).

%package -n     %{libphodav}
Group:		System/Libraries
Summary:        A library to serve files with WebDAV
Requires:	%{name}-i18n

%description -n %{libphodav}
phởdav is a WebDAV server implementation using libsoup (RFC 4918).
This package provides the library.

%package -n     %{libphodavdevel}
Group:		Development/C
Summary:        Development files for libphodav
Requires:       %{libphodav} = %{version}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{libphodavdevel}
The libphodav-devel package includes the header files for libphodav.

%package -n     chezdav
Group:		System/Servers
Summary:        A simple WebDAV server program

%description -n chezdav
The chezdav package contains a simple tool to share a directory
with WebDAV. The service is announced over mDNS for clients to discover.

%package -n     spice-webdavd
Summary:        Spice daemon for the DAV channel
Group:          System/Servers
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description -n spice-webdavd
The spice-webdavd package contains a daemon to proxy WebDAV request to
the Spice virtio channel.

%prep
%setup -q

%build
%meson -Davahi=enabled
%meson_build

%install
%meson_install

%find_lang phodav --with-gnome --all-name

%post -n spice-webdavd
%_post_service spice-webdavd

%preun -n spice-webdavd
%_preun_service spice-webdavd

%files i18n -f %{name}.lang

%files -n %{libphodav}
%doc NEWS COPYING
%{_libdir}/libphodav-%{api}.so.%{major}
%{_libdir}/libphodav-%{api}.so.%{major}.*

%files -n %{libphodavdevel}
%{_includedir}/libphodav-%{api}
%{_libdir}/libphodav-%{api}.so
%{_libdir}/pkgconfig/libphodav-%{api}.pc
%{_datadir}/gtk-doc/html/phodav-%{api}

%files -n chezdav
%{_bindir}/chezdav
%{_mandir}/man1/chezdav.1*

%files -n spice-webdavd
%doc NEWS COPYING
%{_sbindir}/spice-webdavd
%{_udevrulesdir}/70-spice-webdavd.rules
%{_unitdir}/spice-webdavd.service
