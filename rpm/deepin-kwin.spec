%global repo dde-kwin
%global __provides_exclude_from ^%{_qt5_plugindir}.*\.so$

Name:           deepin-kwin
Version:        5.2.0.13
Release:        1%{?dist}
Summary:        KWin configuration for Deepin Desktop Environment
License:        GPLv3+
URL:            https://github.com/linuxdeepin/%{repo}
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  extra-cmake-modules >= 5.54
BuildRequires:  kwin-devel
BuildRequires:  kwayland-server-devel
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  pkgconfig(Qt5Qml)
BuildRequires:  gsettings-qt-devel
BuildRequires:  libepoxy-devel
BuildRequires:  dtkgui-devel
BuildRequires:  kf5-kwayland-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  cmake(KDecoration2)
BuildRequires:  cmake(KF5I18n)
BuildRequires:  qt5-linguist
# for libQt5EdidSupport.a
BuildRequires:  qt5-qtbase-static
BuildRequires:  qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
Requires:       deepin-qt5integration%{?_isa}
Requires:       kwin-x11%{?_isa} >= 5.21
# since F31
Obsoletes:      deepin-wm <= 1.9.38
Obsoletes:      deepin-wm-switcher <= 1.1.9
Obsoletes:      deepin-metacity <= 3.22.24
Obsoletes:      deepin-metacity-devel <= 3.22.24
Obsoletes:      deepin-mutter <= 3.20.38
Obsoletes:      deepin-mutter-devel <= 3.20.38

%description
This package provides a kwin configuration that used as the new WM for Deepin
Desktop Environment.

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kwin-devel%{?_isa}
Requires:       qt5-qtx11extras-devel%{?_isa}
Requires:       gsettings-qt-devel%{?_isa}
Requires:       dtkcore-devel%{?_isa}
Requires:       kf5-kglobalaccel-devel%{?_isa}


%description devel
Header files and libraries for %{name}.

%prep
%autosetup -p1 -n %{repo}-%{version}

sed -i 's:/lib/:%{_libdir}/:' plugins/platforms/lib/CMakeLists.txt
sed -i 's:/lib/:/%{_lib}/:' plugins/platforms/plugin/main.cpp \
                            plugins/platforms/plugin/main_wayland.cpp
sed -i 's:/usr/lib:%{_libexecdir}:' deepin-wm-dbus/deepinwmfaker.cpp

%build
# help find (and prefer) qt5 utilities, e.g. qmake, lrelease
export PATH=%{_qt5_bindir}:$PATH
%cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
       -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DKWIN_VERSION=$(rpm -q --qf '%%{version}' kwin-devel)
%cmake_build

%install
%cmake_install
chmod 755 %{buildroot}%{_bindir}/kwin_no_scale

%files
%doc CHANGELOG.md
%license LICENSE
%{_sysconfdir}/xdg/*
%{_bindir}/deepin-wm-dbus
%{_bindir}/kwin_no_scale
%{_qt5_plugindir}/org.kde.kdecoration2/libdeepin-chameleon.so
%{_qt5_plugindir}/platforms/lib%{repo}-xcb.so
%{_qt5_plugindir}/platforms/lib%{repo}-wayland.so
%{_qt5_plugindir}/kwin/effects/plugins/
%{_datadir}/dde-kwin-xcb/
%{_datadir}/dbus-1/services/*.service
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/kwin/scripts/*
%{_datadir}/kwin/tabbox/*
%{_libdir}/libkwin-xcb.so.0
%{_libdir}/libkwin-xcb.so.0.*

%files devel
%{_libdir}/libkwin-xcb.so
%{_libdir}/pkgconfig/%{repo}.pc
%{_includedir}/%{repo}

%changelog
