Name:           uwsm
Summary:        Universal Wayland Session Manager
Version:        0.26.1
Release:        1%{?dist}

License:        MIT
URL:            https://github.com/Vladimir-csp/%{name}
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  meson
BuildRequires:  python3
BuildRequires:  python3-dbus
BuildRequires:  python3-pyxdg
BuildRequires:  python3-rpm-macros
BuildRequires:  scdoc
BuildRequires:  systemd-rpm-macros

Requires:       python3-dbus
Requires:       python3-pyxdg
Requires:       util-linux

Recommends:     /usr/bin/notify-send
Recommends:     /usr/bin/whiptail
Recommends:     wofi

%description
Wayland session manager for standalone compositors
uwsm (Universal Wayland Session Manager) provides a lightweight, modular
session management framework for Wayland environments based on systemd user
units and various helpers.

It handles various session-related tasks for standalone Wayland compositors,
such as:

- startup from login shell or DM
- dynamic loading and cleanup of environment variables for graphical session
- binding lifetime of graphical session and login session together

It sets the stage for systemd to do launch and lifecycle management,
XDG autostart, clean shutdown.

dbus-broker is recommended for better systemd integration and environment
cleanup.

%package        plugin-hyprland
Summary:        uwsm plugin for Hyprland
Requires:       %{name} = %{version}-%{release}
Supplements:    (%{name} and hyprland)
BuildArch:      noarch

%description    plugin-hyprland
uwsm plugin for the Hyprland compositor.

%package        plugin-labwc
Summary:        uwsm plugin for labwc
Requires:       %{name} = %{version}-%{release}
Supplements:    (%{name} and labwc)
BuildArch:      noarch

%description    plugin-labwc
uwsm plugin for the labwc compositor.

%package        plugin-niri
Summary:        uwsm plugin for niri
Requires:       %{name} = %{version}-%{release}
Supplements:    (%{name} and niri)
BuildArch:      noarch

%description    plugin-niri
uwsm plugin for the niri compositor.

%package        plugin-sway
Summary:        uwsm plugin for Sway
Requires:       %{name} = %{version}-%{release}
Supplements:    (%{name} and sway)
BuildArch:      noarch

%description    plugin-sway
uwsm plugin for the Sway compositor.

%package        plugin-wayfire
Summary:        uwsm plugin for Wayfire
Requires:       %{name} = %{version}-%{release}
Supplements:    (%{name} and wayfire)
BuildArch:      noarch

%description    plugin-wayfire
uwsm plugin for the Wayfire compositor.

%prep
%autosetup -p1

%build
%meson -Duuctl=enabled -Dfumon=disabled -Dwait-tray=enabled -Duwsm-app=enabled
%meson_build

%install
%meson_install
%py_byte_compile %{python3} %{buildroot}%{_datadir}/%{name}/modules

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%files
%doc %{_docdir}/%{name}/
%license LICENSE
%{_bindir}/%{name}
%{_bindir}/%{name}-app
%{_bindir}/%{name}-terminal
%{_bindir}/%{name}-terminal-scope
%{_bindir}/%{name}-terminal-service
%{_bindir}/uuctl
%{_bindir}/wait-tray
%{_datadir}/applications/uuctl.desktop
%{_datadir}/%{name}/modules/
%{_libexecdir}/%{name}/prepare-env.sh
%{_libexecdir}/%{name}/signal-handler.sh
%{_mandir}/man1/uuctl.1.*
%{_mandir}/man1/%{name}.1.*
%{_mandir}/man1/%{name}-app.1.*
%{_mandir}/man3/%{name}-plugins.3.*
%{_userunitdir}/*-graphical.slice
%{_userunitdir}/wayland-*.service
%{_userunitdir}/wayland-*.target

%files plugin-hyprland
%{_datadir}/%{name}/plugins/hyprland.sh
%{_datadir}/%{name}/plugins/start_hyprland.sh

%files plugin-labwc
%{_datadir}/%{name}/plugins/labwc.sh

%files plugin-niri
%{_datadir}/%{name}/plugins/niri.sh
%{_datadir}/%{name}/plugins/niri_session.sh

%files plugin-sway
%{_datadir}/%{name}/plugins/sway.sh

%files plugin-wayfire
%{_datadir}/%{name}/plugins/wayfire.sh

%changelog
* Thu Jan 29 2026 Basil Crow <me@basilcrow.com> - 0.26.1-1
- Initial packaging
